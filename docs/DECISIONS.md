# Decision Record

This file tracks key implementation decisions for the Balkan NLP pipeline.

## 2026-01-20 — Phase 1 (Clean Text) Decisions

- Government sources remain disabled in Phase 1. They will be considered in v1.1
  after the clean-text pipeline is stable.
- Wikipedia ingestion uses dump parsing with `mwxml` + `mwparserfromhell` for
  higher-quality wikitext stripping.
- Test split is exported locally only. Hugging Face uploads include train and
  validation splits during Phase 1.
- Source discovery prioritizes sitemaps and RSS feeds. Homepage crawling is a
  fallback only when sitemap/RSS is unavailable.
- CLI uses Typer with `--dry-run`, `--limit`, `--since` (ISO date with optional
  relative shorthand), and `--source` filters.
