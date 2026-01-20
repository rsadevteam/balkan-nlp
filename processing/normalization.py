from __future__ import annotations

import unicodedata
from typing import Dict

from utils.text_utils import normalize_text, normalize_whitespace


def normalize_document(text: str, config: Dict) -> str:
    normalization = config.get("unicode_normalization", "NFC")
    text = unicodedata.normalize(normalization, text)
    if config.get("normalize_quotes", True) or config.get("normalize_dashes", True):
        text = normalize_text(
            text,
            normalize_quotes_flag=config.get("normalize_quotes", True),
            normalize_dashes_flag=config.get("normalize_dashes", True),
        )
    if config.get("normalize_whitespace", True):
        text = normalize_whitespace(text)
    return text
