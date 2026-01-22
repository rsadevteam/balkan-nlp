from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional
import random

import pandas as pd
import typer

from export.hf_upload import upload_dataset
from export.to_jsonl import export_jsonl
from export.to_parquet import export_parquet
from processing.language_id import apply_balancing, extract_sample
from processing.splitting import split_dataset
from utils.config import load_config
from utils.logging import setup_logging


app = typer.Typer(help="Build the language identification dataset.")


def _load_documents(path: Path) -> List[Dict]:
    documents: List[Dict] = []
    if path.is_dir():
        jsonl_gz = sorted(path.glob("*.jsonl.gz"))
        jsonl = sorted(path.glob("*.jsonl"))
        parquet = sorted(path.glob("*.parquet"))
        if jsonl_gz:
            files = jsonl_gz
        elif jsonl:
            files = jsonl
        else:
            files = parquet
        for file_path in files:
            documents.extend(_load_documents(file_path))
        return documents

    if path.suffix == ".parquet":
        frame = pd.read_parquet(path)
        return frame.to_dict(orient="records")
    if path.suffix == ".gz":
        opener = gzip.open
    elif path.suffix == ".jsonl":
        opener = open
    else:
        raise typer.BadParameter(f"Unsupported input format: {path}")

    with opener(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            documents.append(json.loads(line))
    return documents


def _resolve_source_path(config: Dict, config_path: Path, override: Optional[Path]) -> Path:
    if override:
        return override
    source_path = config.get("source", {}).get("source_dataset_path")
    if not source_path:
        raise typer.BadParameter("source_dataset_path is required")
    path = Path(source_path)
    if not path.is_absolute():
        path = (config_path.parent / path).resolve()
    return path


def _export_outputs(splits: Dict[str, List[Dict]], config: Dict, logger) -> None:
    output = config.get("output", {})
    output_dir = Path(output.get("output_dir", "./output/language_id"))
    output_dir.mkdir(parents=True, exist_ok=True)
    compression = output.get("compression")
    formats = output.get("formats", ["jsonl"])

    for split_name, items in splits.items():
        if "jsonl" in formats:
            export_jsonl(items, str(output_dir / f"{split_name}.jsonl"), compression)
        if "parquet" in formats:
            export_parquet(items, str(output_dir / f"{split_name}.parquet"), compression)
        if "csv" in formats:
            frame = pd.DataFrame(items)
            frame.to_csv(output_dir / f"{split_name}.csv", index=False)
        logger.info("Exported %s items for %s", len(items), split_name)


@app.command()
def run(
    config_path: Path = typer.Option(
        Path("datasets/language_id/config.yaml"),
        "--config",
        help="Path to dataset config.",
    ),
    input_path: Optional[Path] = typer.Option(None, "--input-path", help="Override input path."),
    no_upload: bool = typer.Option(False, "--no-upload", help="Skip Hugging Face upload."),
    limit: Optional[int] = typer.Option(None, "--limit", help="Limit number of samples."),
) -> None:
    config = load_config(config_path)
    logger = setup_logging(
        level=config.get("logging", {}).get("level", "INFO"),
        log_file=config.get("logging", {}).get("log_file"),
    )

    source_path = _resolve_source_path(config, config_path, input_path)
    if not source_path.exists():
        raise typer.BadParameter(f"Input path not found: {source_path}")

    documents = _load_documents(source_path)
    if not documents:
        logger.warning("No documents found in %s", source_path)
        return
    logger.info("Loaded %s clean-text documents", len(documents))

    extraction_config = config.get("extraction", {})
    extraction_config["quality"] = config.get("quality", {})
    label_mapping = config.get("labeling", {}).get("source_mappings", {})
    rng = random.Random(config.get("splits", {}).get("random_seed", 42))

    samples: List[Dict] = []
    for doc in documents:
        sample = extract_sample(doc, extraction_config, label_mapping, rng)
        if sample:
            samples.append(sample)

    logger.info("Extracted %s candidate samples", len(samples))

    samples = apply_balancing(samples, config, rng)
    logger.info("Balanced to %s samples", len(samples))

    target = config.get("dataset", {}).get("target_size", {})
    max_samples = target.get("max_samples")
    min_samples = target.get("min_samples")
    if max_samples and len(samples) > max_samples:
        samples = samples[: max_samples]
    if min_samples and len(samples) < min_samples:
        logger.warning("Samples below minimum target (%s < %s)", len(samples), min_samples)
    if limit:
        samples = samples[:limit]

    splits = split_dataset(samples, config.get("splits", {}))
    _export_outputs(splits, config, logger)

    output = config.get("output", {})
    hf_repo = output.get("hf_repo")
    if hf_repo and not no_upload:
        upload_dataset(splits, hf_repo, output.get("hf_private", False), logger)
    elif hf_repo and no_upload:
        logger.info("Skipping Hugging Face upload (flagged).")


if __name__ == "__main__":
    app()
