from __future__ import annotations

from typing import Dict, List

from datasets import Dataset, DatasetDict


def upload_dataset(splits: Dict[str, List[dict]], repo_name: str, private: bool, logger) -> None:
    dataset = DatasetDict({})
    for split_name, items in splits.items():
        dataset[split_name] = Dataset.from_list(items)

    logger.info("Uploading dataset to Hugging Face: %s", repo_name)
    dataset.push_to_hub(repo_name, private=private)
