# AGENTS.md — Instructions for AI Code Agents

**Last Updated**: 2025-01-19  
**Project**: Balkan NLP - High-quality datasets for Serbian, Bosnian, and Croatian

---

## 🎯 Project Purpose

Build reproducible, high-quality NLP datasets for sr/bs/hr languages and publish them on Hugging Face.

**Core principle**: Quality over quantity, transparency over size.

---

## 📁 Repository Structure

```
balkan-nlp/
├── scraping/          # Web scraping modules
├── processing/        # Cleaning, dedup, normalization
├── export/            # JSONL, Parquet, HF upload
├── datasets/          # Dataset configs (NOT data files)
├── scripts/           # Entry points for pipelines
├── utils/             # Shared utilities
└── docs/              # Documentation
```

**CRITICAL**: Never commit data files (`.jsonl`, `.parquet`, `.csv`) to git.

---

## ✅ What You CAN Do

### Code

- Write Python 3.11+ code
- Use type hints where practical
- Add logging via `utils/logging.py`
- Create new scrapers in `scraping/sources/`
- Add processing modules in `processing/`
- Write dataset configs in YAML format

### Datasets

- Add new dataset configs in `datasets/{name}/`
- Each dataset needs: `README.md`, `config.yaml`
- Follow existing dataset structure (see `datasets/clean_text/`)

### Documentation

- Update relevant `.md` files when adding features
- Keep `CHANGELOG.md` updated

---

## ❌ What You MUST NOT Do

### Absolute Prohibitions

- ❌ **Never commit data files** (`.jsonl`, `.parquet`, `.csv`, `.txt`)
- ❌ **Never hardcode credentials** or API keys
- ❌ **Never scrape paywalled content**
- ❌ **Never ignore `robots.txt`**
- ❌ **Never exceed rate limits** (max 1 req/sec per source)
- ❌ **Never store PII** (names, emails, addresses) without anonymization
- ❌ **Never use copyrighted content** without proper attribution

### Code Prohibitions

- ❌ Don't use `print()` - use `logging` module
- ❌ Don't hardcode paths - use config files
- ❌ Don't write to repo root - use `./output/`, `./cache/`, `./logs/`
- ❌ Don't import from parent directories - keep modules independent

---

## 🏗️ Architecture Guidelines

### Data Flow

```
Sources → Scraping → Cleaning → Deduplication → Export → Hugging Face
```

### Module Boundaries

- **scraping/**: Only fetching and extraction, no cleaning
- **processing/**: Only transformation, no I/O
- **export/**: Only output formatting, no processing
- **utils/**: Pure functions, no side effects

### Configuration-Driven

- Use YAML configs in `datasets/{name}/config.yaml`
- No business logic in configs
- Configs should be declarative, not imperative

---

## 📝 Coding Standards

### Python Style

```python
# ✅ GOOD
def clean_text(text: str, remove_html: bool = True) -> str:
    """Remove HTML tags and normalize whitespace.

    Args:
        text: Input text to clean
        remove_html: Whether to strip HTML tags

    Returns:
        Cleaned text string
    """
    logger.info(f"Cleaning text of length {len(text)}")
    # ... implementation
    return cleaned_text

# ❌ BAD
def clean(t):
    print("cleaning")  # Use logging instead
    return t.strip()   # Too simplistic, no docstring
```

### Naming Conventions

- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Files: `snake_case.py`
- Configs: `lowercase.yaml`

### Error Handling

```python
# ✅ GOOD
try:
    response = fetch_url(url)
except RequestException as e:
    logger.error(f"Failed to fetch {url}: {e}")
    return None

# ❌ BAD
try:
    response = fetch_url(url)
except:
    pass  # Silent failure
```

---

## 🗂️ Adding New Datasets

### Checklist

1. Create `datasets/{name}/` directory
2. Add `README.md` (use existing as template)
3. Add `config.yaml` with all parameters
4. Add `sources.yaml` if needed
5. Document in `docs/DATASETS.md`
6. Update `docs/PHASE_X.md` if part of a phase

### Required Files

```
datasets/{name}/
├── README.md       # Dataset description, format, sources
├── config.yaml     # Processing configuration
└── sources.yaml    # Source URLs (if applicable)
```

### Dataset README Template

Must include:

- Description & purpose
- Output format (JSONL example)
- Sources
- Processing steps
- Target size
- License information
- Hugging Face link
- Citation

---

## 🔒 Security & Privacy

### Scraping Rules

- Always check `robots.txt`
- Respect rate limits (default: 1 req/sec)
- Use descriptive User-Agent: `BalkanNLP/1.0 (Research; +https://github.com/rsadevteam/balkan-nlp)`
- Handle errors gracefully (no hammering servers)

### Data Privacy

- No PII in datasets without explicit consent
- Anonymize usernames, emails, phone numbers
- No private comments or gated content
- Document data sources transparently

### Credentials

- Use environment variables or `config.local.yaml` (gitignored)
- Never commit API keys or passwords
- Use `python-dotenv` for local development

---

## 🧪 Testing & Validation

### Before Committing

- [ ] Code runs without errors
- [ ] No data files in commit
- [ ] Logging instead of print statements
- [ ] Type hints on public functions
- [ ] Docstrings on modules and functions
- [ ] Config files validated (YAML syntax)

### Dataset Validation

- [ ] Duplicate rate < 1%
- [ ] Language ID accuracy > 95%
- [ ] Metadata completeness 100%
- [ ] Sample 1% manual review
- [ ] Proper train/val/test splits

---

## 📤 Releasing Datasets

### Steps

1. Process data according to `docs/METHODOLOGY.md`
2. Run quality checks
3. Generate dataset statistics
4. Create Hugging Face dataset card
5. Upload to HF: `balkan-nlp/{dataset-name}`
6. Tag release: `git tag -a {dataset-name}-v1.0.0`
7. Update `CHANGELOG.md`

### Dataset Card Requirements

Must include:

- Dataset Description
- Data Collection methodology
- Processing steps
- Statistics
- Ethical Considerations
- Licensing
- Citation

---

## 🚫 Out of Scope

**Do NOT implement**:

- Model training code (only datasets)
- API servers or web interfaces
- Real-time scraping systems
- Commercial licensing support
- Non-Balkan languages

**If user requests these**: Politely explain project scope and suggest alternatives.

---

## 📚 Key Documents to Read

Before writing code, read:

1. `ARCHITECTURE.md` - System design
2. `docs/METHODOLOGY.md` - Data processing standards
3. `docs/DATA_SOURCES.md` - Allowed sources
4. `SECURITY.md` - Security rules
5. Relevant `docs/PHASE_X.md` for context

---

## 🎯 Definition of "Done"

### For Code

- [ ] Runs without errors
- [ ] Follows coding standards
- [ ] Has logging
- [ ] No data files committed
- [ ] Documentation updated

### For Datasets

- [ ] Config files complete
- [ ] README.md written
- [ ] Quality checks passed
- [ ] Published on Hugging Face
- [ ] Added to `DATASETS.md`

---

## 💡 Best Practices

### When Scraping

- Start with small tests (10 URLs)
- Cache responses during development
- Log everything (URLs, errors, stats)
- Be a good internet citizen

### When Processing

- Keep intermediate outputs for debugging
- Use meaningful filenames with timestamps
- Document processing parameters
- Save statistics at each step

### When Exporting

- Validate output format
- Compress large files (gzip)
- Generate checksums (SHA256)
- Test loading in HF datasets library

---

## 🔄 Workflow Example

```python
# Typical pipeline flow
from scraping import fetch_sources
from processing import clean_text, deduplicate
from export import to_jsonl, upload_to_hf

# 1. Scrape
raw_data = fetch_sources(config['sources'])

# 2. Process
cleaned = clean_text(raw_data, config['cleaning'])
deduped = deduplicate(cleaned, config['dedup'])

# 3. Export
to_jsonl(deduped, output_path)
upload_to_hf(deduped, config['hf_repo'])
```

---

## 🆘 Common Pitfalls

1. **Forgetting to check robots.txt** → Always respect it
2. **Committing data files** → Use `.gitignore`
3. **Hardcoding URLs** → Use config files
4. **Silent failures** → Log errors properly
5. **Ignoring rate limits** → Sleep between requests
6. **No deduplication** → Always deduplicate
7. **Missing metadata** → Document everything

---

## 📞 Questions?

- Check `ARCHITECTURE.md` for design questions
- Check `CONTRIBUTING.md` for process questions
- Check `docs/METHODOLOGY.md` for data questions
- Check `SECURITY.md` for safety questions

---

**Remember**: This is a research project prioritizing quality, transparency, and reproducibility. When in doubt, choose the cleaner, more documented, more ethical path.
