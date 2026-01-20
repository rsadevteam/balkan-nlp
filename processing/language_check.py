from __future__ import annotations

from functools import lru_cache
from typing import Dict, Optional

try:
    import fasttext
except ImportError:  # pragma: no cover - optional dependency
    fasttext = None


@lru_cache(maxsize=1)
def _load_fasttext(model_path: str):
    if fasttext is None:
        raise RuntimeError("fasttext is required for language validation")
    return fasttext.load_model(model_path)


def validate_language(document: Dict, config: Dict, logger) -> bool:
    if not config.get("use_fasttext_validation", False):
        return True

    model_path = config.get("fasttext_model_path")
    if not model_path:
        logger.warning("FastText model path not set; skipping validation")
        return True

    try:
        model = _load_fasttext(model_path)
    except RuntimeError as exc:
        logger.warning("FastText validation skipped: %s", exc)
        return True

    text = document.get("text", "")
    if not text:
        return False
    labels, probabilities = model.predict(text.replace("\n", " "), k=1)
    if not labels:
        return False
    predicted = labels[0].replace("__label__", "")
    confidence = probabilities[0] if probabilities else 0.0
    expected = document.get("language")
    min_confidence = config.get("min_confidence_for_override", 0.95)
    if predicted != expected and confidence >= min_confidence:
        return False
    return True
