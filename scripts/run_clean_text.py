from __future__ import annotations

from datetime import datetime, timedelta, timezone
import gzip
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from uuid import uuid4
from urllib.parse import urlparse

import json
import typer
from dateutil import parser as date_parser

from export.hf_upload import upload_dataset
from export.to_jsonl import export_jsonl
from export.to_parquet import export_parquet
from processing.cleaning import clean_document, passes_quality_checks
from processing.deduplication import deduplicate_documents
from processing.language_check import validate_language
from processing.normalization import normalize_document
from processing.splitting import split_dataset
from scraping.extract import extract_article
from scraping.fetch import FetchConfig, Fetcher
from scraping.sources.common import collect_rss_entries, discover_urls, filter_sources, load_sources
from scraping.sources.wikipedia import WikipediaDumpConfig, download_dump, iter_wikipedia_articles
from utils.config import load_config
from utils.logging import setup_logging


app = typer.Typer(help="Run the Phase 1 clean-text pipeline.")


def _parse_since(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    value = value.strip()
    if value.endswith("d") and value[:-1].isdigit():
        days = int(value[:-1])
        return datetime.utcnow() - timedelta(days=days)
    if value.endswith("w") and value[:-1].isdigit():
        weeks = int(value[:-1])
        return datetime.utcnow() - timedelta(weeks=weeks)
    try:
        parsed = date_parser.parse(value)
        if parsed.tzinfo:
            return parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    except (ValueError, TypeError) as exc:
        raise typer.BadParameter("Invalid --since format") from exc


def _format_date(value: Optional[datetime]) -> Optional[str]:
    if not value:
        return None
    return value.date().isoformat()


def _build_fetcher(config: Dict, logger) -> Fetcher:
    collection = config.get("collection", {})
    fetch_config = FetchConfig(
        user_agent=collection.get("user_agent", "BalkanNLP/1.0"),
        timeout=collection.get("timeout", 30),
        max_retries=collection.get("max_retries", 3),
        respect_robots_txt=collection.get("respect_robots_txt", True),
        cache_enabled=collection.get("cache_enabled", True),
        cache_dir=Path(collection.get("cache_dir", "./cache")),
    )
    return Fetcher(fetch_config, logger)


def _collect_news_documents(
    source: Dict,
    fetcher: Fetcher,
    since: Optional[datetime],
    limit: Optional[int],
    default_rate_limit: float,
    logger,
) -> List[Dict]:
    if not source.get("url"):
        logger.warning("Missing URL for source %s", source.get("name"))
        return []
    documents: List[Dict] = []

    if source.get("rss_use_content"):
        entries = collect_rss_entries(source, fetcher, since)
        if limit:
            entries = entries[:limit]
        source_domain = urlparse(source.get("url", "")).netloc
        for entry in entries:
            documents.append(
                {
                    "text": entry["text"],
                    "title": entry.get("title"),
                    "date": _format_date(entry.get("date")),
                    "url": entry.get("url"),
                    "source": source_domain,
                    "language": source.get("language"),
                    "domain": source.get("type"),
                }
            )
        return documents

    urls = discover_urls(source, fetcher, since)
    if limit:
        urls = urls[:limit]
    logger.info("Discovered %s URLs for %s", len(urls), source.get("name"))

    source_domain = urlparse(source.get("url", "")).netloc
    for url in urls:
        html = fetcher.fetch(
            url,
            rate_limit=source.get("rate_limit", default_rate_limit),
            use_cloudscraper=source.get("use_cloudscraper", False),
        )
        if not html:
            continue
        extracted = extract_article(html, url)
        if not extracted or not extracted.get("text"):
            continue
        documents.append(
            {
                "text": extracted["text"],
                "title": extracted.get("title"),
                "date": _format_date(extracted.get("date")),
                "url": extracted.get("url"),
                "source": source_domain,
                "language": source.get("language"),
                "domain": source.get("type"),
            }
        )
    return documents


def _collect_wikipedia_documents(
    source: Dict,
    fetcher: Fetcher,
    limit: Optional[int],
    logger,
) -> List[Dict]:
    if not source.get("dump_url") or not source.get("dump_file"):
        logger.warning("Missing dump configuration for %s", source.get("name"))
        return []

    dump_config = WikipediaDumpConfig(
        url=str(source.get("url")),
        dump_url=str(source.get("dump_url")),
        dump_file=str(source.get("dump_file")),
        language=str(source.get("language")),
        source=str(source.get("url")),
    )
    cache_dir = Path(fetcher.config.cache_dir) / "wikipedia"
    dump_path = download_dump(dump_config, cache_dir, fetcher.config.user_agent, logger)
    documents: List[Dict] = []
    source_domain = urlparse(source.get("url", "")).netloc
    for idx, article in enumerate(iter_wikipedia_articles(dump_path)):
        if limit and idx >= limit:
            break
        url_title = article["title"].replace(" ", "_")
        documents.append(
            {
                "text": article["text"],
                "title": article.get("title"),
                "date": None,
                "url": f"{source.get('url')}/wiki/{url_title}",
                "source": source_domain,
                "language": source.get("language"),
                "domain": source.get("type"),
            }
        )
    return documents


def _apply_processing_pipeline(
    documents: Iterable[Dict],
    config: Dict,
    logger,
    assign_ids: bool = True,
) -> List[Dict]:
    cleaned_docs: List[Dict] = []
    cleaning_config = config.get("cleaning", {})
    quality_config = config.get("quality", {})
    language_config = config.get("language_assignment", {})

    for doc in documents:
        text = clean_document(doc["text"], cleaning_config)
        text = normalize_document(text, cleaning_config)
        if not passes_quality_checks(text, cleaning_config, quality_config):
            continue
        doc["text"] = text
        if not doc.get("language"):
            continue
        if not validate_language(doc, language_config, logger):
            continue
        if assign_ids:
            doc["id"] = str(uuid4())
        cleaned_docs.append(doc)

    return cleaned_docs


def _load_documents_from_path(path: Path, logger) -> List[Dict]:
    if not path.exists():
        raise typer.BadParameter(f"Missing input file: {path}")
    if path.suffix == ".parquet":
        import pandas as pd

        frame = pd.read_parquet(path)
        return frame.to_dict(orient="records")
    if path.suffix == ".gz":
        opener = gzip.open
    elif path.suffix == ".jsonl":
        opener = open
    else:
        raise typer.BadParameter(f"Unsupported input format: {path}")

    documents: List[Dict] = []
    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            documents.append(json.loads(line))
    logger.info("Loaded %s documents from %s", len(documents), path)
    return documents


def _load_merge_inputs(paths: List[Path], logger) -> List[Dict]:
    documents: List[Dict] = []
    for path in paths:
        documents.extend(_load_documents_from_path(path, logger))
    return documents


def _assign_ids(documents: Iterable[Dict]) -> List[Dict]:
    updated: List[Dict] = []
    for doc in documents:
        doc["id"] = str(uuid4())
        updated.append(doc)
    return updated


def _export_splits(splits: Dict[str, List[Dict]], config: Dict, logger) -> None:
    output_config = config.get("output", {})
    output_dir = Path(output_config.get("output_dir", "./output/clean_text"))
    formats = output_config.get("formats", ["jsonl"])
    compression = output_config.get("compression")

    for split_name, items in splits.items():
        if "jsonl" in formats:
            export_jsonl(items, str(output_dir / f"{split_name}.jsonl"), compression)
        if "parquet" in formats:
            export_parquet(items, str(output_dir / f"{split_name}.parquet"), compression)
        logger.info("Exported %s items for %s", len(items), split_name)


def _export_raw_documents(documents: List[Dict], config: Dict, suffix: str, logger) -> None:
    output_config = config.get("output", {})
    output_dir = Path(output_config.get("output_dir", "./output/clean_text")) / "raw"
    formats = output_config.get("formats", ["jsonl"])
    compression = output_config.get("compression")
    output_dir.mkdir(parents=True, exist_ok=True)
    if "jsonl" in formats:
        export_jsonl(documents, str(output_dir / f"{suffix}.jsonl"), compression)
    if "parquet" in formats:
        export_parquet(documents, str(output_dir / f"{suffix}.parquet"), compression)
    logger.info("Exported %s raw documents to %s", len(documents), output_dir)


def _save_stats(splits: Dict[str, List[Dict]], config: Dict) -> None:
    metadata = config.get("metadata", {})
    if not metadata.get("save_statistics", True):
        return
    stats_dir = Path(metadata.get("statistics_dir", "./stats/clean_text"))
    stats_dir.mkdir(parents=True, exist_ok=True)

    for split_name, items in splits.items():
        languages: Dict[str, int] = {}
        lengths = [len(item.get("text", "")) for item in items]
        for item in items:
            lang = item.get("language", "unknown")
            languages[lang] = languages.get(lang, 0) + 1
        average_length = sum(lengths) / len(lengths) if lengths else 0
        stats = {
            "count": len(items),
            "languages": languages,
            "average_length": average_length,
        }
        stats_path = stats_dir / f"{split_name}_stats.json"
        stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


@app.command()
def run(
    config_path: Path = typer.Option(
        Path("datasets/clean_text/config.yaml"),
        "--config",
        help="Path to dataset config.",
    ),
    sources_path: Path = typer.Option(
        Path("datasets/clean_text/sources.yaml"),
        "--sources",
        help="Path to source configuration.",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Discover URLs only."),
    limit: Optional[int] = typer.Option(None, "--limit", help="Limit URLs per source."),
    since: Optional[str] = typer.Option(None, "--since", help="ISO date or relative (7d)."),
    source: Optional[List[str]] = typer.Option(None, "--source", help="Source name filter."),
    no_upload: bool = typer.Option(False, "--no-upload", help="Skip Hugging Face upload."),
    no_split: bool = typer.Option(False, "--no-split", help="Export raw cleaned data only."),
    output_suffix: str = typer.Option("raw", "--output-suffix", help="Suffix for raw output."),
    merge_inputs: Optional[List[Path]] = typer.Option(
        None,
        "--merge-inputs",
        help="Input files to merge (repeatable).",
    ),
) -> None:
    config = load_config(config_path)
    logger = setup_logging(
        level=config.get("logging", {}).get("level", "INFO"),
        log_file=config.get("logging", {}).get("log_file"),
    )
    since_date = _parse_since(since)

    if merge_inputs and no_split:
        raise typer.BadParameter("--merge-inputs cannot be used with --no-split")
    if merge_inputs and dry_run:
        raise typer.BadParameter("--merge-inputs cannot be used with --dry-run")

    sources = load_sources(str(sources_path))
    sources = filter_sources(sources, source)

    if not sources and not merge_inputs:
        logger.warning("No sources enabled or matched the filter.")
        return

    fetcher = _build_fetcher(config, logger)

    if merge_inputs:
        documents = _load_merge_inputs(merge_inputs, logger)
        logger.info("Loaded %s documents from merge inputs", len(documents))
        deduped = deduplicate_documents(documents, config.get("deduplication", {}), logger)
        deduped = _assign_ids(deduped)
        splits = split_dataset(deduped, config.get("splits", {}))
        _export_splits(splits, config, logger)
        _save_stats(splits, config)

        output_config = config.get("output", {})
        hf_repo = output_config.get("hf_repo")
        if hf_repo and not no_upload:
            hf_splits = {
                "train": splits.get("train", []),
                "validation": splits.get("validation", []),
            }
            upload_dataset(hf_splits, hf_repo, output_config.get("hf_private", False), logger)
        elif hf_repo and no_upload:
            logger.info("Skipping Hugging Face upload (flagged).")
        return

    if dry_run:
        for src in sources:
            if src.get("type") == "wiki":
                logger.info("Wikipedia dump configured for %s", src.get("name"))
                continue
            if src.get("rss_use_content"):
                entries = collect_rss_entries(src, fetcher, since_date)
                logger.info("Dry run: %s RSS entries for %s", len(entries), src.get("name"))
            else:
                urls = discover_urls(src, fetcher, since_date)
                logger.info("Dry run: %s URLs for %s", len(urls), src.get("name"))
        return

    raw_documents: List[Dict] = []
    default_rate_limit = config.get("collection", {}).get("default_rate_limit", 1)

    for src in sources:
        if src.get("type") == "wiki":
            raw_documents.extend(_collect_wikipedia_documents(src, fetcher, limit, logger))
        else:
            raw_documents.extend(
                _collect_news_documents(
                    src,
                    fetcher,
                    since_date,
                    limit,
                    default_rate_limit,
                    logger,
                )
            )

    logger.info("Collected %s raw documents", len(raw_documents))

    processed = _apply_processing_pipeline(raw_documents, config, logger, assign_ids=not no_split)
    logger.info("Processed %s documents after cleaning", len(processed))

    if no_split:
        _export_raw_documents(processed, config, output_suffix, logger)
        return

    deduped = deduplicate_documents(processed, config.get("deduplication", {}), logger)
    logger.info("Deduplicated to %s documents", len(deduped))

    splits = split_dataset(deduped, config.get("splits", {}))
    _export_splits(splits, config, logger)
    _save_stats(splits, config)

    output_config = config.get("output", {})
    hf_repo = output_config.get("hf_repo")
    if hf_repo and not no_upload:
        hf_splits = {
            "train": splits.get("train", []),
            "validation": splits.get("validation", []),
        }
        upload_dataset(hf_splits, hf_repo, output_config.get("hf_private", False), logger)
    elif hf_repo and no_upload:
        logger.info("Skipping Hugging Face upload (flagged).")


if __name__ == "__main__":
    app()
