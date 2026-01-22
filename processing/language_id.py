from __future__ import annotations

import random
import re
import string
from typing import Dict, Iterable, List, Optional
from uuid import uuid4

from utils.text_utils import digit_ratio, word_count


SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> List[str]:
    sentences = [sentence.strip() for sentence in SENTENCE_SPLIT_RE.split(text) if sentence.strip()]
    return sentences


def split_paragraphs(text: str) -> List[str]:
    paragraphs = [para.strip() for para in text.split("\n\n") if para.strip()]
    return paragraphs


def assign_length_bucket(text: str, buckets: Dict[str, Dict[str, int]]) -> Optional[str]:
    length = len(text)
    for name, bucket in buckets.items():
        min_chars = bucket.get("min_chars", 0)
        max_chars = bucket.get("max_chars", 10**9)
        if min_chars <= length <= max_chars:
            return name
    return None


def punctuation_ratio(text: str) -> float:
    if not text:
        return 0.0
    punctuation = sum(char in string.punctuation for char in text)
    return punctuation / len(text)


def passes_quality_filters(text: str, config: Dict) -> bool:
    min_words = config.get("min_words", 0)
    max_words = config.get("max_words", 10**9)
    count = word_count(text)
    if count < min_words or count > max_words:
        return False

    reject_patterns = config.get("reject_if_contains", [])
    for pattern in reject_patterns:
        if pattern in text:
            return False

    max_digit_ratio = config.get("max_digit_ratio")
    if max_digit_ratio is not None and digit_ratio(text) > max_digit_ratio:
        return False

    max_punctuation_ratio = config.get("max_punctuation_ratio")
    if max_punctuation_ratio is not None and punctuation_ratio(text) > max_punctuation_ratio:
        return False

    return True


def extract_sample(
    document: Dict,
    config: Dict,
    label_mapping: Dict[str, str],
    rng: random.Random,
) -> Optional[Dict]:
    text = document.get("text", "")
    if not text:
        return None

    method = config.get("method", "random_sentences")
    min_sentences = config.get("min_sentences", 2)
    max_sentences = config.get("max_sentences", 5)

    if method == "random_paragraphs":
        units = split_paragraphs(text)
    else:
        units = split_sentences(text)

    if len(units) < min_sentences:
        return None

    count = rng.randint(min_sentences, max_sentences)
    count = min(count, len(units))
    start = rng.randint(0, len(units) - count)
    sample_text = " ".join(units[start : start + count])

    if not passes_quality_filters(sample_text, config.get("quality", {})):
        return None

    length_buckets = config.get("length_buckets", {})
    bucket = assign_length_bucket(sample_text, length_buckets) if length_buckets else None
    if length_buckets and bucket is None:
        return None

    source = document.get("source", "unknown")
    label = label_mapping.get(source, document.get("language"))
    if not label:
        return None

    return {
        "id": str(uuid4()),
        "text": sample_text,
        "label": label,
        "source": source,
        "length": len(sample_text),
        "length_bucket": bucket,
        "source_doc_id": document.get("id"),
    }


def balance_languages(samples: List[Dict]) -> List[Dict]:
    by_language: Dict[str, List[Dict]] = {}
    for sample in samples:
        by_language.setdefault(sample["label"], []).append(sample)
    if not by_language:
        return samples
    min_count = min(len(items) for items in by_language.values())
    balanced: List[Dict] = []
    for items in by_language.values():
        balanced.extend(items[:min_count])
    return balanced


def balance_sources(samples: List[Dict]) -> List[Dict]:
    by_language: Dict[str, Dict[str, List[Dict]]] = {}
    for sample in samples:
        by_language.setdefault(sample["label"], {}).setdefault(sample["source"], []).append(sample)

    balanced: List[Dict] = []
    for sources in by_language.values():
        min_count = min(len(items) for items in sources.values())
        for items in sources.values():
            balanced.extend(items[:min_count])
    return balanced


def balance_lengths(samples: List[Dict], buckets: Dict[str, Dict[str, float]]) -> List[Dict]:
    by_language: Dict[str, Dict[str, List[Dict]]] = {}
    for sample in samples:
        bucket = sample.get("length_bucket")
        if bucket is None:
            continue
        by_language.setdefault(sample["label"], {}).setdefault(bucket, []).append(sample)

    balanced: List[Dict] = []
    for language, bucket_map in by_language.items():
        total = sum(len(items) for items in bucket_map.values())
        for bucket_name, bucket_config in buckets.items():
            target_ratio = bucket_config.get("percentage", 0)
            target_count = int(total * target_ratio)
            items = bucket_map.get(bucket_name, [])
            balanced.extend(items[:target_count])
    return balanced


def apply_balancing(samples: List[Dict], config: Dict, rng: random.Random) -> List[Dict]:
    rng.shuffle(samples)
    balancing = config.get("balancing", {})
    if balancing.get("balance_languages"):
        samples = balance_languages(samples)
    if balancing.get("balance_sources"):
        samples = balance_sources(samples)
    if balancing.get("balance_lengths"):
        length_buckets = config.get("extraction", {}).get("length_buckets", {})
        samples = balance_lengths(samples, length_buckets)
    rng.shuffle(samples)
    return samples
