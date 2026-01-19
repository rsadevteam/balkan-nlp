# Contributing to Balkan NLP

Thank you for your interest in contributing to Balkan NLP! This document provides guidelines for contributing code, datasets, and documentation.

---

## 🎯 Project Scope

**In Scope**:

- High-quality datasets for sr/bs/hr languages
- Data collection and processing pipelines
- Documentation and methodology
- Quality assurance and validation tools

**Out of Scope**:

- Model training or inference code
- API servers or web applications
- Real-time data processing
- Languages other than sr/bs/hr

---

## 🚀 Getting Started

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/rsadevteam/balkan-nlp.git
cd balkan-nlp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional but recommended)
pre-commit install
```

### 2. Understand the Architecture

Read these documents before contributing:

1. [README.md](README.md) - Project overview
2. [AGENTS.md](AGENTS.md) - Coding guidelines
3. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
4. [docs/METHODOLOGY.md](docs/METHODOLOGY.md) - Data processing standards

---

## 📝 Types of Contributions

### 1. Adding a New Dataset

**Before you start**:

- Check if the dataset fits project scope (sr/bs/hr languages)
- Verify data sources are legal and ethical
- Discuss in GitHub Issues first for major datasets

**Steps**:

1. **Create dataset directory**:

```bash
mkdir -p datasets/{dataset_name}
```

2. **Add configuration files**:

```yaml
# datasets/{dataset_name}/config.yaml
dataset:
    name: { dataset_name }
    version: 1.0.0
    description: "Brief description"

# Add processing parameters here
```

3. **Write README.md**:
   Use `datasets/clean_text/README.md` as template. Must include:

- Description & purpose
- Output format with example
- Data sources
- Processing steps
- Statistics
- License information

4. **Add to documentation**:

- Add entry to `docs/DATASETS.md`
- Update relevant `docs/PHASE_X.md`

5. **Test the pipeline**:

```bash
python scripts/run_{dataset_name}.py --config datasets/{dataset_name}/config.yaml
```

**Checklist**:

- [ ] Config files complete and valid YAML
- [ ] README follows template
- [ ] Sources documented in `docs/DATA_SOURCES.md`
- [ ] Tested on sample data
- [ ] No data files committed
- [ ] Documentation updated

---

### 2. Adding a New Scraper

**Location**: `scraping/sources/{source_name}.py`

**Template**:

```python
"""Scraper for {source_name}."""

import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def scrape_{source_name}(url: str, config: dict) -> Optional[dict]:
    """Scrape article from {source_name}.

    Args:
        url: Article URL
        config: Scraping configuration

    Returns:
        Dictionary with keys: text, title, date, url, metadata
        None if scraping fails
    """
    try:
        # Implementation here
        return {
            'text': article_text,
            'title': title,
            'date': publication_date,
            'url': url,
            'metadata': {
                'source': '{source_name}',
                'category': category,
            }
        }
    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")
        return None
```

**Requirements**:

- [ ] Respects `robots.txt`
- [ ] Implements rate limiting
- [ ] Handles errors gracefully
- [ ] Logs all actions
- [ ] Returns None on failure
- [ ] Has docstring with examples

---

### 3. Improving Processing Modules

**Location**: `processing/{module_name}.py`

**Guidelines**:

- Keep functions pure (no side effects)
- Add type hints
- Write comprehensive docstrings
- Add unit tests in `tests/`
- Log important operations

**Example**:

```python
def deduplicate_texts(
    texts: list[str],
    threshold: float = 0.9
) -> list[str]:
    """Remove near-duplicate texts using MinHash.

    Args:
        texts: List of text strings
        threshold: Similarity threshold (0.0-1.0)

    Returns:
        List of unique texts

    Example:
        >>> texts = ["Hello world", "Hello world!", "Different text"]
        >>> deduplicate_texts(texts, threshold=0.9)
        ["Hello world", "Different text"]
    """
    # Implementation
```

---

### 4. Documentation Improvements

**Types**:

- Fix typos or unclear explanations
- Add examples or tutorials
- Improve API documentation
- Translate documentation (if maintaining translations)

**Process**:

1. Edit the relevant `.md` file
2. Ensure Markdown is valid
3. Check all links work
4. Submit PR

---

## 🔍 Code Review Process

### Before Submitting PR

Run these checks:

```bash
# Code formatting
black .
isort .

# Linting
flake8 .

# Type checking
mypy .

# Tests
pytest
```

### PR Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No data files committed

## Related Issues

Closes #XXX
```

---

## 📋 Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) formatter (line length: 100)
- Use [isort](https://pycqa.github.io/isort/) for import sorting

### Naming

- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names (no single letters except in loops)

### Documentation

- Docstrings for all public functions and classes
- Google style docstrings
- Type hints on function signatures
- Comments for complex logic only

### Logging

```python
import logging

logger = logging.getLogger(__name__)

# ✅ GOOD
logger.info(f"Processing {len(docs)} documents")
logger.warning(f"Skipped {n} invalid entries")
logger.error(f"Failed to process {url}: {error}")

# ❌ BAD
print("Processing documents")  # Use logging
logger.debug("Some detail")    # INFO for important events
```

---

## 🧪 Testing Guidelines

### Unit Tests

```python
# tests/test_processing.py
import pytest
from processing.cleaning import clean_text


def test_clean_text_removes_html():
    input_text = "<p>Hello <b>world</b></p>"
    expected = "Hello world"
    assert clean_text(input_text) == expected


def test_clean_text_normalizes_whitespace():
    input_text = "Hello    world\n\n"
    expected = "Hello world"
    assert clean_text(input_text) == expected
```

### Integration Tests

```python
# tests/test_pipeline.py
def test_full_pipeline_on_sample():
    """Test complete pipeline on small sample."""
    sample_urls = ["https://example.com/article1"]

    # Run pipeline
    result = run_pipeline(sample_urls, config)

    # Validate output
    assert len(result) > 0
    assert 'text' in result[0]
    assert 'metadata' in result[0]
```

---

## 🔒 Security Guidelines

### Scraping

- Always check `robots.txt`
- Implement rate limiting (default: 1 req/sec)
- Use descriptive User-Agent
- Handle errors gracefully

### Data Privacy

- Never commit PII
- Anonymize sensitive data
- Document data sources
- Respect copyright and ToS

### Credentials

- Use environment variables
- Never hardcode API keys
- Add sensitive files to `.gitignore`

---

## 📤 Commit Guidelines

### Commit Messages

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:

```
feat(scraping): add klix.ba scraper

Implements scraper for klix.ba news portal with rate limiting
and error handling.

Closes #42

---

docs(methodology): clarify deduplication strategy

Adds examples and pseudocode for MinHash implementation.

---

fix(processing): handle empty documents

Previously crashed on empty strings. Now logs warning and skips.
```

---

## 🚫 Common Mistakes

### ❌ Don't Do This

```python
# Committing data files
git add output/dataset.jsonl  # NO!

# Hardcoding paths
output_file = "/home/user/data/output.json"  # NO!

# Silent failures
try:
    process()
except:
    pass  # NO!

# Using print instead of logging
print("Processing...")  # NO!

# No type hints
def process(data):  # NO!
    return data
```

### ✅ Do This Instead

```python
# Use .gitignore for data files
# (already configured)

# Use config files for paths
output_file = config['output']['path']  # YES!

# Log errors properly
try:
    process()
except ProcessError as e:
    logger.error(f"Processing failed: {e}")  # YES!
    return None

# Use logging module
logger.info("Processing documents")  # YES!

# Add type hints
def process(data: list[dict]) -> list[dict]:  # YES!
    return data
```

---

## 📞 Getting Help

- **Questions**: Open a [GitHub Discussion](https://github.com/rsadevteam/balkan-nlp/discussions)
- **Bugs**: Open a [GitHub Issue](https://github.com/rsadevteam/balkan-nlp/issues)
- **Security**: Email office@rsateam.com

---

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Unprofessional conduct

---

## 🏆 Recognition

Contributors will be:

- Listed in `CONTRIBUTORS.md`
- Acknowledged in dataset citations
- Credited in release notes

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🔄 Review Process

1. **Submit PR** with clear description
2. **Automated checks** run (formatting, tests)
3. **Code review** by maintainer
4. **Address feedback** if needed
5. **Merge** when approved

Typical review time: 2-7 days

---

Thank you for contributing to Balkan NLP! 🎉

---

**Questions?** Read [AGENTS.md](AGENTS.md) for detailed coding guidelines or open an issue.
