from __future__ import annotations

from typing import Dict, Iterable, List

from utils.hashing import compute_minhash, sha256_text
from utils.text_utils import tokenize_for_minhash

try:
    from datasketch import MinHashLSH
except ImportError:  # pragma: no cover - optional dependency
    MinHashLSH = None


def _dedup_sha256(documents: Iterable[Dict]) -> List[Dict]:
    seen = set()
    unique_docs: List[Dict] = []
    for doc in documents:
        digest = sha256_text(doc["text"])
        if digest in seen:
            continue
        seen.add(digest)
        unique_docs.append(doc)
    return unique_docs


def _dedup_minhash(documents: Iterable[Dict], threshold: float, num_perm: int) -> List[Dict]:
    if MinHashLSH is None:
        raise RuntimeError("datasketch is required for MinHash deduplication")

    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    unique_docs: List[Dict] = []

    for idx, doc in enumerate(documents):
        tokens = list(tokenize_for_minhash(doc["text"]))
        if not tokens:
            continue
        minhash = compute_minhash(tokens, num_perm=num_perm)
        if lsh.query(minhash):
            continue
        key = f"doc-{idx}"
        lsh.insert(key, minhash)
        unique_docs.append(doc)
    return unique_docs


def deduplicate_documents(documents: Iterable[Dict], config: Dict, logger) -> List[Dict]:
    deduped = list(documents)
    if config.get("use_sha256", True):
        deduped = _dedup_sha256(deduped)
    if config.get("use_minhash", False):
        try:
            deduped = _dedup_minhash(
                deduped,
                threshold=config.get("minhash_threshold", 0.9),
                num_perm=config.get("minhash_num_perm", 128),
            )
        except RuntimeError as exc:
            logger.warning("MinHash dedup skipped: %s", exc)
    return deduped
