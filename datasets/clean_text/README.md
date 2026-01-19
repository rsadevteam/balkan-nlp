# Clean Text Corpus Dataset

## 📝 Description

High-quality, deduplicated monolingual text corpus for Serbian, Bosnian, and Croatian languages.

This dataset is designed as a foundation for:

- 🤖 LLM pretraining and continued pretraining
- 🔤 Tokenizer training
- 📊 Word embeddings and language models
- 🔬 Linguistic research

---

## 🎯 Purpose

Most existing sr/bs/hr corpora (OSCAR, CC100) suffer from:

- ❌ Noise (HTML fragments, navigation)
- ❌ Insufficient deduplication
- ❌ Mixed languages without clear boundaries
- ❌ Poor source documentation

**This dataset addresses these issues.**

---

## 📊 Statistics (Planned for v1.0)

| Metric          | Value            |
| --------------- | ---------------- |
| Total documents | 50,000 - 150,000 |
| Bosnian (bs)    | ~33%             |
| Croatian (hr)   | ~33%             |
| Serbian (sr)    | ~33%             |
| Average length  | 500-2000 words   |
| Dedup rate      | > 95%            |

---

## 🗂️ Format

```jsonl
{
	"id": "550e8400-e29b-41d4-a716-446655440000",
	"text": "Full cleaned article text...",
	"language": "bs",
	"source": "klix.ba",
	"domain": "news",
	"date": "2024-03-15",
	"url": "https://klix.ba/..."
}
```

### Fields

- **id**: Unique UUID for document
- **text**: Cleaned textual content
- **language**: sr/bs/hr
- **source**: Source domain
- **domain**: Content type (news, wiki, gov)
- **date**: Publication date (if available)
- **url**: Original URL (optional)

---

## 📥 Sources

### News Portals (80%)

**Bosnia and Herzegovina**:

- klix.ba
- avaz.ba
- faktor.ba
- n1info.ba

**Croatia**:

- index.hr
- jutarnji.hr
- vecernji.hr
- tportal.hr

**Serbia**:

- blic.rs
- politika.rs
- rts.rs
- n1info.rs

### Wikipedia (15%)

- bs.wikipedia.org
- hr.wikipedia.org
- sr.wikipedia.org

### Public Institutions (5%)

- Official announcements
- Public documents

---

## 🧹 Processing

### 1. Collection

- Web scraping with trafilatura
- Respect robots.txt
- Rate limiting (1 req/sec)

### 2. Cleaning

- HTML tag removal
- Boilerplate extraction
- Navigation/footer removal
- Unicode normalization (NFC)
- Whitespace normalization

### 3. Deduplication

- **Exact duplicates**: SHA256 hash
- **Near duplicates**: MinHash (90% threshold)
- Document-level + paragraph-level

### 4. Language Assignment

- Primary: Source-based labeling
- Secondary: FastText validation

### 5. Quality Filtering

- Minimum length: 200 characters
- Maximum length: 50,000 characters
- No empty documents
- Language confidence > 0.90

---

## 📂 Splits

```python
train: 80%      # For model training
validation: 10% # For validation during training
test: 10%       # For final evaluation (not published publicly)
```

**Stratification**:

- By language (sr/bs/hr)
- By source (balanced representation)

---

## 🔗 Derived Datasets

From this dataset we build:

- **Language Identification Dataset** (sr vs bs vs hr)
- **News Summarization Dataset** (article → summary)

---

## 📄 License

**Data**: Aggregated from public sources (see DATA_SOURCES.md)
**Usage**: Research and educational purposes
**Attribution**: Required

⚠️ **Disclaimer**: Users are responsible for verifying copyright laws in their jurisdiction.

---

## 🚀 Hugging Face

Dataset will be available at:

```
huggingface.co/datasets/balkan-nlp/sr-bs-hr-clean-text
```

---

## 📚 Citation

```bibtex
@dataset{balkan_nlp_clean_text_2026,
  title={SR/BS/HR Clean Text Corpus},
  author={Balkan NLP Project},
  year={2026},
  publisher={Hugging Face},
  url={https://huggingface.co/datasets/balkan-nlp/sr-bs-hr-clean-text}
}
```

---

## 🔄 Version History

- **v1.0.0** (TBD) - Initial release
    - 50K-150K documents
    - News + Wikipedia + Gov sources

---

## 🤝 Contributing

For suggestions, bug reports or contributing guidelines, see the main repo:
https://github.com/rsadevteam/balkan-nlp

---

## 📞 Contact

For questions about the dataset:

- GitHub Issues
- office@rsateam.com

---

**Status**: 🚧 In Development
