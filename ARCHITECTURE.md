# Architecture

This document describes the system design, module organization, and data flow for the Balkan NLP dataset pipeline.

---

## 🎯 Design Principles

1. **Configuration-driven**: Business logic in code, parameters in YAML
2. **Separation of concerns**: Each module has one clear responsibility
3. **Reproducibility**: Same config → same output
4. **Transparency**: Every step is logged and auditable
5. **Modularity**: Components can be used independently

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         PIPELINE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Sources (Web/Files) → Scraping → Processing → Export       │
│                           ↓           ↓           ↓          │
│                        Cache      Intermediate  Output       │
│                                      Files      (JSONL)      │
│                                                   ↓          │
│                                            Hugging Face      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Module Organization

### 1. scraping/

**Purpose**: Fetch and extract raw content from web sources.

**Responsibilities**:

- HTTP requests with rate limiting
- HTML parsing and boilerplate removal
- Metadata extraction (date, source, URL)
- Error handling and retries
- Caching responses

**Does NOT**:

- Clean text
- Deduplicate
- Transform data

**Key Files**:

```
scraping/
├── __init__.py
├── fetch.py              # HTTP client with rate limiting
├── extract.py            # Content extraction (trafilatura wrapper)
└── sources/
    ├── common.py         # Shared utilities
    ├── klix.py           # Site-specific scraper
    ├── index.py          # Site-specific scraper
    └── blic.py           # Site-specific scraper
```

**Interface**:

```python
def scrape_source(url: str, config: dict) -> dict:
    """Scrape single URL.

    Returns:
        {
            'text': str,
            'title': str,
            'date': datetime,
            'url': str,
            'metadata': dict
        }
    """
```

---

### 2. processing/

**Purpose**: Transform raw scraped content into clean, structured data.

**Responsibilities**:

- Text cleaning (HTML, whitespace, unicode)
- Normalization (quotes, dashes, case)
- Deduplication (exact + near-duplicate)
- Language identification validation
- Quality filtering
- Dataset splitting (train/val/test)

**Does NOT**:

- Fetch data from web
- Write to disk
- Upload to Hugging Face

**Key Files**:

```
processing/
├── __init__.py
├── cleaning.py           # Text cleaning functions
├── normalization.py      # Unicode, whitespace normalization
├── deduplication.py      # MinHash, SHA256 dedup
├── language_check.py     # FastText validation
└── splitting.py          # Train/val/test splits
```

**Interface**:

```python
def clean_text(text: str, config: dict) -> str:
    """Clean and normalize text."""

def deduplicate(documents: list[dict], config: dict) -> list[dict]:
    """Remove duplicate and near-duplicate documents."""

def split_dataset(data: list[dict], config: dict) -> dict:
    """Split into train/val/test with stratification."""
```

---

### 3. export/

**Purpose**: Format and export processed data to various formats and destinations.

**Responsibilities**:

- Serialize to JSONL, Parquet
- Compress outputs
- Generate checksums
- Upload to Hugging Face
- Create dataset cards

**Does NOT**:

- Process or transform data
- Validate data quality

**Key Files**:

```
export/
├── __init__.py
├── to_jsonl.py           # JSONL export
├── to_parquet.py         # Parquet export
└── hf_upload.py          # Hugging Face integration
```

**Interface**:

```python
def to_jsonl(data: list[dict], output_path: str, compress: bool = True):
    """Export to JSONL format."""

def upload_to_hf(data: list[dict], repo_name: str, config: dict):
    """Upload to Hugging Face with dataset card."""
```

---

### 4. utils/

**Purpose**: Shared utilities used across modules.

**Responsibilities**:

- Logging setup
- Text utilities (counting, tokenization)
- Hashing functions
- Configuration loading
- File I/O helpers

**Key Files**:

```
utils/
├── __init__.py
├── logging.py            # Logging configuration
├── text_utils.py         # Text manipulation
├── hashing.py            # SHA256, MinHash
└── config.py             # YAML config loading
```

---

### 5. scripts/

**Purpose**: Entry points for running pipelines.

**Responsibilities**:

- CLI argument parsing
- Loading configurations
- Orchestrating pipeline steps
- Progress reporting

**Key Files**:

```
scripts/
├── run_clean_text.py     # Phase 1: Clean text corpus
├── run_language_id.py    # Phase 1: Language ID dataset
└── run_summarization.py  # Phase 1: Summarization dataset
```

**Example**:

```python
# scripts/run_clean_text.py
import argparse
from scraping import scrape_sources
from processing import clean_text, deduplicate
from export import to_jsonl, upload_to_hf

def main():
    args = parse_args()
    config = load_config(args.config)

    # Pipeline
    raw_data = scrape_sources(config['sources'])
    cleaned = clean_text(raw_data, config['cleaning'])
    deduped = deduplicate(cleaned, config['dedup'])

    # Export
    to_jsonl(deduped, config['output']['path'])
    upload_to_hf(deduped, config['output']['hf_repo'])

if __name__ == '__main__':
    main()
```

---

### 6. datasets/

**Purpose**: Configuration files for each dataset (NOT data storage).

**Structure**:

```
datasets/
├── clean_text/
│   ├── README.md         # Dataset documentation
│   ├── config.yaml       # Processing configuration
│   └── sources.yaml      # Source URLs
│
├── language_id/
│   ├── README.md
│   └── config.yaml
│
└── summarization/
    ├── README.md
    └── config.yaml
```

**CRITICAL**: This directory contains ONLY configuration and documentation, NEVER actual data files.

---

## 🔄 Data Flow

### Phase 1: Clean Text Corpus

```
┌──────────────┐
│  News Sites  │
│  Wikipedia   │
│  Gov Portals │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│  scraping/   │  ← sources.yaml
│  fetch.py    │  ← Rate limiting, robots.txt
│  extract.py  │  ← Trafilatura extraction
└──────┬───────┘
       │
       ↓ Raw HTML → Clean text + metadata
       │
┌──────────────┐
│ processing/  │
│ cleaning.py  │  ← Remove boilerplate, normalize
│ dedup.py     │  ← MinHash + SHA256
│ lang_check   │  ← FastText validation
└──────┬───────┘
       │
       ↓ Deduplicated documents
       │
┌──────────────┐
│   export/    │
│ to_jsonl.py  │  ← Format + compress
│ hf_upload.py │  ← Upload to HF
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Hugging Face │
│   Dataset    │
└──────────────┘
```

---

### Derived Datasets (Language ID, Summarization)

```
┌──────────────────┐
│  Clean Text      │  ← Base dataset
│  Corpus          │
└────────┬─────────┘
         │
         ├─────────────────┐
         │                 │
         ↓                 ↓
┌────────────────┐  ┌──────────────┐
│  Language ID   │  │ Summarization│
│  Extraction    │  │  Lead Extract│
└────────┬───────┘  └──────┬───────┘
         │                 │
         ↓                 ↓
    ┌────────┐        ┌────────┐
    │ HF LID │        │ HF Sum │
    └────────┘        └────────┘
```

---

## 🔧 Configuration System

### Hierarchy

```
1. defaults (in code)
2. config.yaml (dataset-specific)
3. config.local.yaml (gitignored, overrides)
4. environment variables (for secrets)
```

### Example: datasets/clean_text/config.yaml

```yaml
dataset:
    name: sr-bs-hr-clean-text
    version: 1.0.0

collection:
    user_agent: "BalkanNLP/1.0"
    timeout: 30
    max_retries: 3
    rate_limit: 1

cleaning:
    min_length: 200
    max_length: 50000
    unicode_normalization: NFC

deduplication:
    use_sha256: true
    use_minhash: true
    minhash_threshold: 0.90

output:
    formats: [jsonl, parquet]
    compression: gzip
    hf_repo: "balkan-nlp/sr-bs-hr-clean-text"
```

---

## 📦 Dependencies

### Core

- `requests` - HTTP client
- `trafilatura` - Web content extraction
- `beautifulsoup4` - HTML parsing fallback
- `pyyaml` - Configuration files

### Processing

- `datasets` - Hugging Face integration
- `pandas` - Data manipulation
- `datasketch` - MinHash deduplication
- `fasttext` - Language identification

### Export

- `pyarrow` - Parquet format
- `huggingface-hub` - HF uploads

---

## 🚦 Error Handling Strategy

### Levels

1. **Retry** - Network errors, timeouts (with backoff)
2. **Skip** - Invalid URLs, 404s (log and continue)
3. **Fail** - Configuration errors, missing dependencies (stop pipeline)

### Example

```python
# Retry with backoff
@retry(max_attempts=3, backoff=2.0)
def fetch_url(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text

# Skip invalid data
for url in urls:
    try:
        content = fetch_url(url)
    except RequestException as e:
        logger.warning(f"Skipping {url}: {e}")
        continue
```

---

## 💾 Storage & Caching

### Directory Structure

```
balkan-nlp/
├── cache/          # HTTP response cache (gitignored)
├── logs/           # Processing logs (gitignored)
├── models/         # Local ML models (gitignored)
├── output/         # Final datasets (gitignored)
│   ├── clean_text/
│   ├── language_id/
│   └── summarization/
└── stats/          # Dataset statistics (gitignored)
```

### Caching Strategy

- Cache HTTP responses during development
- Invalidate cache after 7 days
- Store cache with URL hash as key
- Compress cached responses

---

## 🔐 Security Boundaries

### Input Validation

- Validate URLs before fetching
- Sanitize filenames
- Validate YAML configs
- Check file sizes before processing

### Output Sanitization

- Remove PII (emails, phone numbers)
- Anonymize usernames
- Filter sensitive patterns
- Validate before HF upload

---

## 📊 Monitoring & Logging

### Logging Levels

- **DEBUG**: Detailed processing info
- **INFO**: Pipeline progress, statistics
- **WARNING**: Skipped items, validation issues
- **ERROR**: Failed operations, exceptions

### Metrics to Track

- Documents scraped per source
- Duplicate removal rate
- Processing time per step
- Output file sizes
- Error rates by type

### Example

```python
logger.info(f"Scraped {len(docs)} documents from {source}")
logger.info(f"Removed {dupes} duplicates ({dupes/len(docs)*100:.1f}%)")
logger.warning(f"Skipped {errors} URLs due to errors")
```

---

## 🧪 Testing Strategy

### Unit Tests

- Individual functions in isolation
- Mock external dependencies
- Test edge cases

### Integration Tests

- End-to-end pipeline on sample data
- Validate output format
- Check metadata completeness

### Manual Testing

- Sample 1% of output for human review
- Verify source attribution
- Check for quality issues

---

## 🚀 Deployment

### Local Development

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run pipeline
python scripts/run_clean_text.py --config datasets/clean_text/config.yaml
```

### Production (CI/CD)

```bash
# On server/GitHub Actions
pip install -e .
python scripts/run_clean_text.py --config config.yaml
```

---

## 📈 Scalability Considerations

### Current Design (Phase 1)

- Single-threaded processing
- Suitable for 50K-150K documents
- Processing time: hours to days

### Future Improvements (Phase 2+)

- Parallel scraping (multiprocessing)
- Distributed processing (Dask/Ray)
- Incremental updates
- Delta processing for new data

---

## 🔗 Related Documents

- [AGENTS.md](AGENTS.md) - AI agent instructions
- [METHODOLOGY.md](docs/METHODOLOGY.md) - Data processing methodology
- [SECURITY.md](SECURITY.md) - Security guidelines
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

---

**Last Updated**: 2026-01-19
