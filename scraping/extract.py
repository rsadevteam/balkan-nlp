from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup
import trafilatura
from trafilatura.metadata import extract_metadata


def extract_article(html: str, url: str) -> Optional[Dict[str, Any]]:
    if not html:
        return None

    extracted = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        include_images=False,
        include_links=False,
    )

    if extracted is None:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        title = soup.title.string.strip() if soup.title and soup.title.string else None
        return {"text": text, "title": title, "date": None, "url": url}

    metadata = extract_metadata(html)
    date_value: Optional[datetime] = None
    if metadata and metadata.date:
        date_value = metadata.date

    return {
        "text": extracted,
        "title": metadata.title if metadata else None,
        "date": date_value,
        "url": url,
    }
