from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import gzip
import json

import pandas as pd
import typer

from export.hf_upload import upload_dataset
from utils.config import load_config
from utils.logging import setup_logging


app = typer.Typer(help="Upload existing dataset splits to Hugging Face.")


def _load_documents(path: Path) -> List[Dict]:
    if path.suffix == ".parquet":
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
    return documents


def _resolve_split_file(input_dir: Path, split_name: str) -> Optional[Path]:
    candidates = [
        input_dir / f"{split_name}.jsonl.gz",
        input_dir / f"{split_name}.jsonl",
        input_dir / f"{split_name}.parquet",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _load_splits(input_dir: Path, overrides: Dict[str, Optional[Path]], logger) -> Dict[str, List[Dict]]:
    splits: Dict[str, List[Dict]] = {}
    for split_name in ("train", "validation", "test"):
        path = overrides.get(split_name)
        if not path and input_dir:
            path = _resolve_split_file(input_dir, split_name)
        if path:
            splits[split_name] = _load_documents(path)
            logger.info("Loaded %s items for %s from %s", len(splits[split_name]), split_name, path)
    if not splits:
        raise typer.BadParameter("No split files found. Provide --input-dir or --train/--validation/--test.")
    return splits


@app.command()
def run(
    config_path: Path = typer.Option(
        ..., "--config", help="Path to dataset config (for hf_repo/logging defaults)."
    ),
    input_dir: Optional[Path] = typer.Option(
        None, "--input-dir", help="Directory with train/validation/test files."
    ),
    train_path: Optional[Path] = typer.Option(None, "--train", help="Train split file path."),
    validation_path: Optional[Path] = typer.Option(
        None, "--validation", help="Validation split file path."
    ),
    test_path: Optional[Path] = typer.Option(None, "--test", help="Test split file path."),
    hf_repo: Optional[str] = typer.Option(None, "--hf-repo", help="Override HF repo id."),
    private: Optional[bool] = typer.Option(
        None, "--private/--public", help="Override HF visibility."
    ),
) -> None:
    config = load_config(config_path)
    logger = setup_logging(
        level=config.get("logging", {}).get("level", "INFO"),
        log_file=config.get("logging", {}).get("log_file"),
    )

    output_config = config.get("output", {})
    repo_name = hf_repo or output_config.get("hf_repo")
    if not repo_name:
        raise typer.BadParameter("hf_repo is required (set in config or pass --hf-repo).")
    repo_private = private if private is not None else output_config.get("hf_private", False)

    resolved_input_dir = input_dir
    if not resolved_input_dir and not any([train_path, validation_path, test_path]):
        output_dir = output_config.get("output_dir")
        if output_dir:
            resolved_input_dir = (config_path.parent / output_dir).resolve()

    splits = _load_splits(
        resolved_input_dir if resolved_input_dir else Path("."),
        {"train": train_path, "validation": validation_path, "test": test_path},
        logger,
    )
    upload_dataset(splits, repo_name, repo_private, logger)


if __name__ == "__main__":
    app()
