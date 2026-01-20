from __future__ import annotations

import hashlib
from typing import Iterable

try:
    from datasketch import MinHash
except ImportError:  # pragma: no cover - optional dependency
    MinHash = None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_minhash(tokens: Iterable[str], num_perm: int) -> "MinHash":
    if MinHash is None:
        raise RuntimeError("datasketch is required for MinHash deduplication")
    minhash = MinHash(num_perm=num_perm)
    for token in tokens:
        minhash.update(token.encode("utf-8"))
    return minhash
