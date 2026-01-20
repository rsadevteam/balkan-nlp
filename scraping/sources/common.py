from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse
import xml.etree.ElementTree as ElementTree

import importlib

from bs4 import BeautifulSoup
from dateutil import parser as date_parser
import yaml


def load_sources(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    sources: List[Dict[str, Any]] = []
    for group, entries in data.items():
        for entry in entries:
            entry = dict(entry)
            entry["group"] = group
            sources.append(entry)
    return sources


def filter_sources(sources: Iterable[Dict[str, Any]], names: Optional[List[str]]) -> List[Dict[str, Any]]:
    enabled = [source for source in sources if source.get("enabled", False)]
    if not names:
        return enabled
    names_set = {name.strip() for name in names}
    return [source for source in enabled if source.get("name") in names_set]


def _default_sitemap_urls(base_url: str) -> List[str]:
    base = base_url.rstrip("/")
    return [f"{base}/sitemap.xml", f"{base}/sitemap_index.xml"]


def _default_rss_urls(base_url: str) -> List[str]:
    base = base_url.rstrip("/")
    return [f"{base}/rss", f"{base}/feed"]


def _parse_iso_date(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        parsed = date_parser.parse(value)
        if parsed.tzinfo:
            return parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    except (ValueError, TypeError):
        return None


def _is_allowed_domain(url: str, source: Dict[str, Any]) -> bool:
    parsed = urlparse(url)
    source_domain = urlparse(source.get("url", "")).netloc
    allowed_domains = source.get("allowed_domains") or [source_domain]
    return any(parsed.netloc.endswith(domain) for domain in allowed_domains if domain)


def _strip_html(value: str) -> str:
    if not value:
        return ""
    soup = BeautifulSoup(value, "html.parser")
    return soup.get_text(" ", strip=True)


def _load_feedparser():
    try:
        return importlib.import_module("feedparser")
    except ImportError:
        return None


def _collect_sitemap_urls(
    sitemap_url: str,
    fetcher,
    since: Optional[datetime],
    depth: int = 0,
) -> List[str]:
    if depth > 2:
        return []
    sitemap_text = fetcher.fetch(sitemap_url)
    if not sitemap_text:
        return []

    try:
        root = ElementTree.fromstring(sitemap_text)
    except ElementTree.ParseError:
        return []
    urls: List[str] = []

    if root.tag.endswith("sitemapindex"):
        for sitemap in root.iter():
            if not sitemap.tag.endswith("sitemap"):
                continue
            loc = sitemap.find("{*}loc")
            if loc is None or not loc.text:
                continue
            urls.extend(
                _collect_sitemap_urls(loc.text, fetcher, since, depth + 1)
            )
        return urls

    for url_elem in root.iter():
        if not url_elem.tag.endswith("url"):
            continue
        loc = url_elem.find("{*}loc")
        if loc is None or not loc.text:
            continue
        lastmod = url_elem.find("{*}lastmod")
        if since and lastmod is not None:
            lastmod_date = _parse_iso_date(lastmod.text)
            if lastmod_date and lastmod_date < since:
                continue
        urls.append(loc.text)
    return urls


def _collect_rss_urls(
    rss_url: str,
    fetcher,
    since: Optional[datetime],
) -> List[str]:
    rss_text = fetcher.fetch(rss_url)
    if not rss_text:
        return []

    try:
        root = ElementTree.fromstring(rss_text)
    except ElementTree.ParseError:
        return []
    urls: List[str] = []
    for item in root.iter():
        if not item.tag.endswith("item"):
            continue
        link = item.find("{*}link")
        pub_date = item.find("{*}pubDate")
        if since and pub_date is not None:
            parsed = _parse_iso_date(pub_date.text or "")
            if parsed and parsed < since:
                continue
        if link is not None and link.text:
            urls.append(link.text.strip())
    return urls


def discover_urls(source: Dict[str, Any], fetcher, since: Optional[datetime]) -> List[str]:
    urls: List[str] = []
    sitemaps = source.get("sitemaps") or _default_sitemap_urls(source["url"])
    rss_feeds = source.get("rss") or _default_rss_urls(source["url"])

    for sitemap_url in sitemaps:
        urls.extend(_collect_sitemap_urls(sitemap_url, fetcher, since))

    for rss_url in rss_feeds:
        urls.extend(_collect_rss_urls(rss_url, fetcher, since))

    if not urls:
        urls = [source["url"]]

    filtered = [url for url in urls if _is_allowed_domain(url, source)]
    return list(dict.fromkeys(filtered))


def collect_rss_entries(source: Dict[str, Any], fetcher, since: Optional[datetime]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    rss_feeds = source.get("rss") or _default_rss_urls(source["url"])

    for rss_url in rss_feeds:
        rss_text = fetcher.fetch(rss_url)
        if not rss_text:
            continue
        feedparser = _load_feedparser()
        if feedparser is None:
            raise RuntimeError("feedparser is required for RSS content extraction")
        feed = feedparser.parse(rss_text)
        for item in feed.entries:
            link = item.get("link") or item.get("id")
            if not link or not _is_allowed_domain(link, source):
                continue
            published = item.get("published") or item.get("updated") or item.get("pubDate")
            published_dt = _parse_iso_date(published)
            if since and published_dt and published_dt < since:
                continue
            content_value = ""
            if item.get("content"):
                content_value = item.content[0].get("value", "")
            if not content_value:
                content_value = item.get("summary") or item.get("description") or ""
            text = _strip_html(content_value)
            if not text:
                continue
            entries.append(
                {
                    "text": text,
                    "title": item.get("title"),
                    "url": link,
                    "date": published_dt,
                }
            )

    return entries
