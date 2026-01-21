from __future__ import annotations

import gzip
import importlib
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests


@dataclass
class FetchConfig:
    user_agent: str
    timeout: int
    max_retries: int
    respect_robots_txt: bool
    cache_enabled: bool
    cache_dir: Path


class RateLimiter:
    def __init__(self, requests_per_second: float = 1.0) -> None:
        self.min_interval = 1.0 / requests_per_second
        self.last_request: Optional[float] = None

    def wait(self) -> None:
        if self.last_request is None:
            self.last_request = time.time()
            return
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()


class Fetcher:
    def __init__(self, config: FetchConfig, logger) -> None:
        self.config = config
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": config.user_agent})
        self._cloudscraper_session = self._create_cloudscraper_session()
        self._warned_cloudscraper = False
        self._robots: Dict[str, RobotFileParser] = {}
        self._limiters: Dict[str, RateLimiter] = {}
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, url: str) -> Path:
        digest = sha256(url.encode("utf-8")).hexdigest()
        return self.config.cache_dir / f"{digest}.gz"

    def _get_robot_parser(self, base_url: str) -> RobotFileParser:
        if base_url not in self._robots:
            parser = RobotFileParser()
            parser.set_url(urljoin(base_url, "/robots.txt"))
            try:
                parser.read()
            except Exception as exc:
                self.logger.warning("Failed to read robots.txt for %s: %s", base_url, exc)
            self._robots[base_url] = parser
        return self._robots[base_url]

    def _get_rate_limiter(self, domain: str, rate_limit: float) -> RateLimiter:
        if domain not in self._limiters:
            self._limiters[domain] = RateLimiter(rate_limit)
        return self._limiters[domain]

    def _create_cloudscraper_session(self) -> Optional[requests.Session]:
        try:
            module = importlib.import_module("cloudscraper")
        except ImportError:
            return None
        session = module.create_scraper()
        session.headers.update({"User-Agent": self.config.user_agent})
        return session

    def _allowed_by_robots(self, url: str) -> bool:
        if not self.config.respect_robots_txt:
            return True
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        parser = self._get_robot_parser(base_url)
        return parser.can_fetch(self.config.user_agent, url)

    def fetch(self, url: str, rate_limit: float = 1.0, use_cloudscraper: bool = False) -> Optional[str]:
        if not self._allowed_by_robots(url):
            self.logger.info("Blocked by robots.txt: %s", url)
            return None

        parsed = urlparse(url)
        limiter = self._get_rate_limiter(parsed.netloc, rate_limit)
        limiter.wait()

        if self.config.cache_enabled:
            cache_path = self._cache_path(url)
            if cache_path.exists():
                try:
                    with gzip.open(cache_path, "rt", encoding="utf-8") as handle:
                        return handle.read()
                except OSError as exc:
                    self.logger.warning("Failed to read cache for %s: %s", url, exc)

        session = self.session
        if use_cloudscraper:
            if self._cloudscraper_session is None:
                if not self._warned_cloudscraper:
                    self.logger.warning("cloudscraper not available; using requests")
                    self._warned_cloudscraper = True
            else:
                session = self._cloudscraper_session

        for attempt in range(1, self.config.max_retries + 1):
            try:
                response = session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
                text = response.text
                if self.config.cache_enabled:
                    cache_path = self._cache_path(url)
                    with gzip.open(cache_path, "wt", encoding="utf-8") as handle:
                        handle.write(text)
                return text
            except requests.RequestException as exc:
                self.logger.warning("Fetch failed (%s/%s) for %s: %s", attempt, self.config.max_retries, url, exc)
                time.sleep(min(2**attempt, 10))

        return None
