from __future__ import annotations

import bz2
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

import mwxml
import mwparserfromhell
import requests


@dataclass
class WikipediaDumpConfig:
    url: str
    dump_url: str
    dump_file: str
    language: str
    source: str


def download_dump(config: WikipediaDumpConfig, cache_dir: Path, user_agent: str, logger) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    dump_path = cache_dir / config.dump_file
    if dump_path.exists():
        logger.info("Using cached Wikipedia dump: %s", dump_path)
        return dump_path

    dump_url = f"{config.dump_url}{config.dump_file}"
    logger.info("Downloading Wikipedia dump: %s", dump_url)
    with requests.get(dump_url, stream=True, headers={"User-Agent": user_agent}, timeout=120) as response:
        response.raise_for_status()
        with dump_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    return dump_path


def _extract_latest_revision(page) -> Optional[str]:
    latest = None
    for revision in page:
        latest = revision
    if latest is None:
        return None
    return latest.text


def iter_wikipedia_articles(dump_path: Path) -> Iterable[Dict[str, str]]:
    with dump_path.open("rb") as handle:
        with bz2.open(handle, "rb") as decompressed:
            dump = mwxml.Dump.from_file(decompressed)
            for page in dump:
                if page.namespace != 0:
                    continue
                text = _extract_latest_revision(page)
                if not text:
                    continue
                wikicode = mwparserfromhell.parse(text)
                cleaned = wikicode.strip_code()
                yield {
                    "title": page.title,
                    "text": cleaned,
                }
