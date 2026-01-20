from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Iterable


def export_jsonl(data: Iterable[dict], output_path: str, compression: str | None = None) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if compression == "gzip":
        output_file = path.with_suffix(path.suffix + ".gz")
        with gzip.open(output_file, "wt", encoding="utf-8") as handle:
            for item in data:
                handle.write(json.dumps(item, ensure_ascii=False) + "\n")
        return output_file

    with path.open("w", encoding="utf-8") as handle:
        for item in data:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    return path
