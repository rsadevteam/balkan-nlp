from __future__ import annotations

from typing import Dict, List

from utils.text_utils import (
    anonymize_text,
    contains_pii,
    digit_ratio,
    special_char_ratio,
    word_count,
)


def _remove_patterns(text: str, patterns: List[str]) -> str:
    for pattern in patterns:
        text = text.replace(pattern, "")
    return text


def clean_document(text: str, config: Dict) -> str:
    patterns = config.get("exclude_patterns", [])
    if patterns:
        text = _remove_patterns(text, patterns)
    if contains_pii(text):
        text = anonymize_text(text)
    return text.strip()


def passes_quality_checks(text: str, cleaning_config: Dict, quality_config: Dict) -> bool:
    if not text:
        return False
    min_length = cleaning_config.get("min_length", 0)
    max_length = cleaning_config.get("max_length", 10**9)
    if len(text) < min_length or len(text) > max_length:
        return False

    min_words = quality_config.get("min_words_per_document", 0)
    max_words = quality_config.get("max_words_per_document", 10**9)
    count = word_count(text)
    if count < min_words or count > max_words:
        return False

    max_digit_ratio = quality_config.get("max_digit_ratio")
    if max_digit_ratio is not None and digit_ratio(text) > max_digit_ratio:
        return False

    max_special_ratio = quality_config.get("max_special_char_ratio")
    if max_special_ratio is not None and special_char_ratio(text) > max_special_ratio:
        return False
    return True
