from __future__ import annotations

import random
from collections import defaultdict
from typing import Dict, Iterable, List


def split_dataset(data: Iterable[Dict], config: Dict) -> Dict[str, List[Dict]]:
    data_list = list(data)
    stratify_fields = config.get("stratify_by", [])
    rng = random.Random(config.get("random_seed", 42))

    grouped: Dict[tuple, List[Dict]] = defaultdict(list)
    for item in data_list:
        key = tuple(item.get(field) for field in stratify_fields)
        grouped[key].append(item)

    splits = {"train": [], "validation": [], "test": []}
    train_ratio = config.get("train", 0.8)
    val_ratio = config.get("validation", 0.1)

    for items in grouped.values():
        rng.shuffle(items)
        total = len(items)
        train_count = int(total * train_ratio)
        val_count = int(total * val_ratio)
        splits["train"].extend(items[:train_count])
        splits["validation"].extend(items[train_count : train_count + val_count])
        splits["test"].extend(items[train_count + val_count :])

    return splits
