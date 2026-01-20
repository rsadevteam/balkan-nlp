from __future__ import annotations

import re
from typing import Iterable


EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(\+\d{3}|0)\d{8,10}\b")
WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_whitespace(text: str) -> str:
    text = WHITESPACE_PATTERN.sub(" ", text)
    return text.strip()


def normalize_quotes(text: str) -> str:
    return text.replace("“", '"').replace("”", '"').replace("„", '"')


def normalize_dashes(text: str) -> str:
    return text.replace("–", "-").replace("—", "-")


def normalize_text(text: str, normalize_quotes_flag: bool = True, normalize_dashes_flag: bool = True) -> str:
    if normalize_quotes_flag:
        text = normalize_quotes(text)
    if normalize_dashes_flag:
        text = normalize_dashes(text)
    return text


def word_count(text: str) -> int:
    return len(text.split())


def digit_ratio(text: str) -> float:
    if not text:
        return 0.0
    digits = sum(char.isdigit() for char in text)
    return digits / len(text)


def special_char_ratio(text: str) -> float:
    if not text:
        return 0.0
    specials = sum(not char.isalnum() and not char.isspace() for char in text)
    return specials / len(text)


def contains_pii(text: str) -> bool:
    return bool(EMAIL_PATTERN.search(text) or PHONE_PATTERN.search(text))


def anonymize_text(text: str) -> str:
    text = EMAIL_PATTERN.sub("[EMAIL]", text)
    text = PHONE_PATTERN.sub("[PHONE]", text)
    return text


def tokenize_for_minhash(text: str) -> Iterable[str]:
    return re.findall(r"\w+", text.lower())
