from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


def export_parquet(data: Iterable[dict], output_path: str, compression: str | None = None) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(list(data))
    compression_arg = compression if compression else None
    frame.to_parquet(path, index=False, compression=compression_arg)
    return path
