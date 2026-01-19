# Security Policy

This document outlines security, privacy, and ethical guidelines for the Balkan NLP project.

---

## 🔒 Security Principles

1. **No PII in datasets** - Personal information must be anonymized
2. **Respect source ToS** - Never violate terms of service
3. **Ethical scraping** - Be a good internet citizen
4. **No credentials in code** - Use environment variables
5. **Transparent sourcing** - Document all data sources

---

## 🚫 Absolute Prohibitions

### NEVER Do These Things

❌ **Scrape paywalled content**

- Violates copyright and ToS
- Legal liability

❌ **Store PII without anonymization**

- Names (unless public figures in news context)
- Email addresses
- Phone numbers
- Physical addresses
- IP addresses
- Social security numbers
- Credit card information

❌ **Ignore robots.txt**

- Always respect robots.txt
- Automated scraping must comply

❌ **Exceed rate limits**

- Default: 1 request/second
- Respect server capacity
- Implement exponential backoff

❌ **Commit credentials**

- API keys
- Passwords
- Access tokens
- Database URLs

❌ **Scrape private content**

- Login-gated pages
- Private social media profiles
- Members-only forums
- Internal company documents

---

## 🌐 Web Scraping Rules

### Before Scraping

1. **Check robots.txt**

```python
from urllib.robotparser import RobotFileParser

def can_scrape(url: str, user_agent: str) -> bool:
    """Check if URL can be scraped according to robots.txt."""
    rp = RobotFileParser()
    rp.set_url(f"{url}/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)
```

2. **Check Terms of Service**

- Read site's ToS
- Verify scraping is allowed
- Document in `docs/DATA_SOURCES.md`

3. **Verify license**

- Public domain?
- Creative Commons?
- Fair use applicable?

### During Scraping

**Rate Limiting**:

```python
import time
from datetime import datetime

class RateLimiter:
    def __init__(self, requests_per_second: float = 1.0):
        self.min_interval = 1.0 / requests_per_second
        self.last_request = None

    def wait(self):
        """Wait if necessary to respect rate limit."""
        if self.last_request:
            elapsed = (datetime.now() - self.last_request).total_seconds()
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
        self.last_request = datetime.now()
```

**User-Agent**:

```python
USER_AGENT = "BalkanNLP/1.0 (Research Project; +https://github.com/rsadevteam/balkan-nlp)"
```

**Error Handling**:

- Don't hammer servers on errors
- Implement exponential backoff
- Log all failures

### After Scraping

**Attribution**:

- Store source URL in metadata
- Credit original publishers
- Link to original content

---

## 🛡️ Data Privacy

### PII Handling

**Detection**:

```python
import re

# Email detection
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Phone number detection (Balkan formats)
PHONE_PATTERN = r'\b(\+381|0)[0-9]{8,9}\b'  # Serbian
# Add Bosnian and Croatian patterns

def contains_pii(text: str) -> bool:
    """Check if text contains PII."""
    if re.search(EMAIL_PATTERN, text):
        return True
    if re.search(PHONE_PATTERN, text):
        return True
    # Add more checks
    return False
```

**Anonymization**:

```python
def anonymize_text(text: str) -> str:
    """Remove PII from text."""
    # Replace emails
    text = re.sub(EMAIL_PATTERN, '[EMAIL]', text)

    # Replace phone numbers
    text = re.sub(PHONE_PATTERN, '[PHONE]', text)

    # Replace names (requires NER model)
    # text = replace_names(text)

    return text
```

### Sensitive Categories

**Extra caution required for**:

- Medical information
- Financial data
- Children's data
- Political opinions
- Religious beliefs
- Sexual orientation

**Action**: If dataset contains these → extra review + clear disclaimers

---

## 📜 Copyright & Licensing

### Allowed Sources

✅ **Public domain**

- Government documents
- Expired copyrights

✅ **Creative Commons**

- Wikipedia (CC BY-SA)
- Openly licensed content

✅ **Fair use** (with caution)

- News articles for research
- Factual data extraction
- Transformative use

### Prohibited Sources

❌ **Copyrighted without permission**

- Books, articles (paywalled)
- Song lyrics, poems
- Private communications

❌ **Unclear licensing**

- If in doubt, don't use

### Attribution Requirements

Always include:

```python
{
    "source": "klix.ba",
    "url": "https://klix.ba/article/...",
    "date": "2024-01-19",
    "license": "used_under_fair_use"  # or appropriate license
}
```

---

## 🔐 Credentials Management

### Environment Variables

```bash
# .env (gitignored)
HF_TOKEN=hf_xxxxxxxxxxxxx
DATABASE_URL=postgresql://user:pass@localhost/db
```

```python
# Usage in code
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not set")
```

### Config Files

```yaml
# config.local.yaml (gitignored)
huggingface:
    token: ${HF_TOKEN} # Reference environment variable

database:
    url: ${DATABASE_URL}
```

### Never Commit

- `.env` files
- `config.local.yaml`
- API keys in code
- Passwords
- Access tokens

---

## 🧪 Testing & Validation

### Before Dataset Release

**Security Checklist**:

- [ ] No PII in dataset
- [ ] All sources documented
- [ ] Licenses verified
- [ ] Attribution complete
- [ ] No credentials in metadata
- [ ] Sample manually reviewed

**PII Detection Script**:

```python
def validate_dataset(data: list[dict]):
    """Validate dataset for PII."""
    issues = []

    for i, item in enumerate(data):
        text = item.get('text', '')

        if contains_pii(text):
            issues.append(f"Item {i}: Contains PII")

        if not item.get('source'):
            issues.append(f"Item {i}: Missing source")

    return issues
```

---

## 🚨 Reporting Security Issues

### If You Find a Security Issue

**DO**:

1. Email office@rsateam.com
2. Include:
    - Description of issue
    - Steps to reproduce
    - Potential impact
    - Suggested fix (if any)

**DON'T**:

- Open public GitHub issue
- Disclose publicly before fix
- Share with third parties

### Response Timeline

- **24 hours**: Acknowledgment
- **7 days**: Assessment and plan
- **30 days**: Fix and disclosure (if applicable)

---

## 🔍 Audit Trail

### Logging Requirements

**Must log**:

- All scraping activities
- Source URLs accessed
- Errors and failures
- Processing steps
- Export operations

**Example**:

```python
logger.info(f"Scraping {url}")
logger.info(f"Retrieved {len(text)} characters")
logger.warning(f"Skipped {url}: Rate limit")
logger.error(f"Failed {url}: {error}")
```

### Metadata Preservation

Every dataset item must have:

```python
{
    "id": "uuid",
    "text": "...",
    "metadata": {
        "source": "klix.ba",
        "url": "https://...",
        "scraped_at": "2024-01-19T10:30:00Z",
        "pipeline_version": "1.0.0"
    }
}
```

---

## ⚖️ Legal Compliance

### GDPR (EU)

If dataset contains EU citizen data:

- Document legal basis (legitimate interest)
- Provide opt-out mechanism
- Honor data deletion requests
- Maintain processing records

### Copyright Law

- Respect copyright terms
- Use only fair use / public domain
- Attribute sources properly
- Honor DMCA takedown requests

### Terms of Service

- Read and comply with source ToS
- Don't circumvent access controls
- Respect rate limits
- Honor robots.txt

---

## 🛠️ Security Tools

### Recommended Tools

**Secret Scanning**:

```bash
# Install trufflehog
pip install truffleHog

# Scan for secrets
truffleHog --regex --entropy=False .
```

**Dependency Scanning**:

```bash
# Check for vulnerable dependencies
pip install safety
safety check
```

**PII Detection**:

```bash
# Use spaCy NER for name detection
python -m spacy download en_core_web_sm

# Or presidio for comprehensive PII detection
pip install presidio-analyzer presidio-anonymizer
```

---

## 📋 Pre-Release Security Checklist

Before releasing any dataset:

- [ ] No PII in dataset
- [ ] All sources legally obtained
- [ ] robots.txt respected
- [ ] Rate limits followed
- [ ] Attribution complete
- [ ] License documented
- [ ] No credentials in metadata
- [ ] Sample manually reviewed (1%)
- [ ] Security scan passed
- [ ] Documentation complete

---

## 🔗 Related Documents

- [METHODOLOGY.md](docs/METHODOLOGY.md) - Data collection methodology
- [DATA_SOURCES.md](docs/DATA_SOURCES.md) - Approved data sources
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

---

## 📞 Contact

**Security issues**: office@rsateam.com
**General questions**: Open a GitHub issue

---

**Remember**: When in doubt about legality or ethics, err on the side of caution. Skip questionable sources rather than risk violating privacy, copyright, or ToS.

---

**Last Updated**: 2025-01-19
