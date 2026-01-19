# Methodology

This document describes the standard procedures and principles used for collecting, processing, and publishing all datasets in this project.

---

## 🎯 Guiding Principles

1. **Transparency** - every step of the process is documented
2. **Reproducibility** - pipeline is available and can be re-run
3. **Quality** - better small and clean than large and noisy
4. **Legality** - respecting copyright and terms of service
5. **Ethics** - responsible handling of sensitive content

---

## 📥 Data Collection

### Allowed Sources

✅ **Publicly available content**:
- News portals with open access
- Wikipedia and public encyclopedias
- Official institutional portals
- Public documents and announcements
- Open-source corpora

✅ **With respect**:
- robots.txt rules
- Rate limiting (max. 1 request/second)
- User-agent identification
- Terms of Service compliance

❌ **Forbidden**:
- Login-gated content
- Paywalled articles
- Private social media comments
- Content explicitly prohibiting scraping
- Personal data without consent

### Collection Process

1. **Source identification**
   - Legality verification
   - Source documentation
   - Access testing

2. **Scraper implementation**
   - Using trafilatura/BeautifulSoup
   - HTML boilerplate removal
   - Error handling and retry logic

3. **Metadata extraction**
   - URL
   - Date
   - Source
   - Language
   - Category (if available)

---

## 🧹 Data Processing

### Text Cleaning

```python
# Standard pipeline for clean text
1. HTML tag removal
2. Navigation and footer removal
3. Advertisement removal
4. Unicode normalization (NFC)
5. Whitespace normalization
6. Duplicate space removal
```

### Text Normalization

- **Unicode normalization**: NFC standard
- **Whitespace**: single space between words
- **Line breaks**: normalized to \n
- **Quotes**: unification (" vs ")
- **Dashes**: normalization (- vs – vs —)

### Deduplication

#### Exact Duplicates

```python
# Using hash functions
- SHA256 for exact match
- Removal of 100% identical documents
```

#### Near-Duplicates

```python
# Using MinHash/SimHash
- Threshold: 90% similarity
- Paragraph-level comparison for article-level deduplication
```

### Language Identification

**Primary strategy**: Source-based labeling
- `klix.ba` → `bs`
- `index.hr` → `hr`
- `blic.rs` → `sr`

**Secondary check**: FastText lid.176.bin
- Only for sanity check
- Removal of obviously incorrect labels

---

## 🏷️ Annotation (where applicable)

### Annotation Guidelines

For datasets requiring human annotation:

1. **Clear guidelines** - written instructions
2. **Training set** - examples with explanations
3. **Inter-annotator agreement** - minimum 80% (Cohen's kappa > 0.60)
4. **Quality checks** - random sampling and review
5. **Iteration** - guideline improvement based on feedback

### Annotation Tools

- Label Studio for NER and classification
- Custom scripts for simpler tasks
- Manual review where needed

---

## 📊 Dataset Splits

### Standard Split Strategy

```python
# Training/Validation/Test split
train: 80%
validation: 10%
test: 10%

# Stratified by:
- Language (sr/bs/hr)
- Source (balanced representation)
- Category (where applicable)
```

### Test Set Protection

⚠️ **Critical**:
- Test set is NOT published publicly
- Test set is kept separate
- Preventing data leakage

---

## 📤 Export and Format

### Standard Formats

**JSONL** (JSON Lines):
```jsonl
{"id": "uuid", "text": "...", "metadata": {...}}
{"id": "uuid", "text": "...", "metadata": {...}}
```

**Parquet**:
- Compressed columnar format
- Faster for large datasets
- Supported by Hugging Face

### Hugging Face Upload

```python
# Using datasets library
from datasets import Dataset, DatasetDict

# Creating dataset dict
dataset = DatasetDict({
    "train": train_dataset,
    "validation": val_dataset,
    "test": test_dataset  # Or keep private
})

# Push to hub
dataset.push_to_hub("balkan-nlp/dataset-name")
```

---

## 📝 Documentation

### Dataset Card Requirements

Every dataset MUST have:

1. **Dataset Description**
   - Purpose
   - Use cases
   - Languages

2. **Data Collection**
   - Sources
   - Collection method
   - Collection date

3. **Data Processing**
   - Cleaning steps
   - Deduplication strategy
   - Filtering criteria

4. **Dataset Statistics**
   - Size
   - Language distribution
   - Average text length

5. **Ethical Considerations**
   - Biases
   - Limitations
   - Intended use

6. **Licensing**
   - Data license
   - Usage restrictions
   - Attribution requirements

---

## 🔄 Versioning

### Semantic Versioning

```
v1.0.0 - Major.Minor.Patch
```

**Major** (1.x.x):
- Breaking changes in structure
- Change in data sources
- Significant quality change

**Minor** (x.1.x):
- Adding new data
- Cleaning improvements
- Backward-compatible changes

**Patch** (x.x.1):
- Bug fixes
- Documentation updates
- Metadata corrections

### Git Tags

```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

---

## ✅ Quality Assurance

### Pre-release Checklist

- [ ] Duplicate rate < 1%
- [ ] Language ID accuracy > 95%
- [ ] Metadata completeness 100%
- [ ] Manual review 1% random sample
- [ ] Dataset card completed
- [ ] License verified
- [ ] Test set validated
- [ ] Code review completed

---

## 🔗 Related Documents

- [Data Sources](DATA_SOURCES.md)
- [Phase 1](PHASE_1.md)
- [Phase 2](PHASE_2.md)
- [Phase 3](PHASE_3.md)
- [Phase 4](PHASE_4.md)

---

## 📌 Notes

This methodology is a **living document** and can be updated as the project progresses and new best practices emerge in the community.

All methodology changes should be:
- Documented in git history
- Explained in commit messages
- Reflected in updated dataset versions where applicable
