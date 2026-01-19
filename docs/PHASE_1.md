# Phase 1 — Foundation Datasets

## 🎯 Goal

Phase 1 establishes a clean, reproducible foundation of NLP datasets for Serbian, Bosnian, and Croatian languages. These datasets serve as the base layer for all subsequent phases and enable immediate use for language modeling, preprocessing, and summarization.

The primary objective is **quality over quantity**, improving upon existing noisy web corpora by providing curated, well-documented data.

---

## 📦 Datasets in Phase 1

1. **Clean Text Corpus** (sr / bs / hr)
2. **Language Identification Dataset** (sr vs bs vs hr)
3. **News Summarization Dataset**

Each dataset is published as a separate Hugging Face dataset repository but generated using a shared open-source pipeline.

---

## 📝 Dataset 1: Clean Text Corpus

### Purpose

A high-quality, deduplicated monolingual corpus for:
- LLM pretraining and continued pretraining
- Embeddings
- Tokenizer training
- Linguistic research

### Sources

- Public news portals (Bosnia, Croatia, Serbia)
- Wikipedia article pages (cleaned)
- Public institutional publications

### Processing

1. **HTML boilerplate removal** - removing navigation, ads
2. **Text normalization** - Unicode normalization, whitespace
3. **Deduplication** - exact + near-duplicate detection
4. **Language assignment** - based on source
5. **Quality filtering** - minimum length, removing empty documents

### Output Format

```jsonl
{
  "id": "uuid",
  "text": "Clean article text...",
  "language": "bs",
  "source": "klix.ba",
  "domain": "news"
}
```

### Target Size

- **50,000 - 150,000** documents for v1.0
- Balanced distribution across languages (sr/bs/hr)

---

## 🔍 Dataset 2: Language Identification

### Purpose

Reliably distinguish between Serbian, Bosnian, and Croatian, which are often misclassified by generic language ID systems.

### Construction

- **Short passages** (2-5 sentences)
- **Labels derived from known sources** (not automatic)
- **Balanced across languages**

### Output Format

```jsonl
{
  "text": "Short paragraph...",
  "label": "hr"
}
```

### Target Size

- **30,000 - 60,000** samples for v1.0

---

## 📰 Dataset 3: News Summarization

### Purpose

A real-world summarization dataset using human-written lead paragraphs as summaries.

### Construction

- **Article**: full cleaned text
- **Summary**: lead paragraph

This approach is:
- ✅ Human-written
- ✅ Non-synthetic
- ✅ Academically accepted

### Output Format

```jsonl
{
  "article": "Full article text...",
  "summary": "Lead paragraph summarizing the article..."
}
```

### Target Size

- **20,000 - 50,000** articles for v1.0

---

## ✅ Success Criteria

Phase 1 is considered successful if:

1. ✅ All three datasets are publicly available on Hugging Face
2. ✅ Each dataset has a clear dataset card with sources and methodology
3. ✅ Versioned releases (v1.0+)
4. ✅ Reusable open-source pipeline
5. ✅ Datasets are already usable for real ML tasks
6. ✅ Community can build Phase 2 datasets on this foundation

---

## ⏱️ Time Estimate

| Task | Duration |
|------|----------|
| Setup scraping pipeline | 3-5 days |
| Data collection | 5-7 days |
| Cleaning & deduplication | 4-6 days |
| Export and validation | 2-3 days |
| HF upload and documentation | 2-3 days |
| **TOTAL** | **2-4 weeks** |

---

## 🔗 Related Documents

- [Methodology](METHODOLOGY.md)
- [Data Sources](DATA_SOURCES.md)
- [Clean Text Dataset README](../datasets/clean_text/README.md)
- [Language ID Dataset README](../datasets/language_id/README.md)
- [Summarization Dataset README](../datasets/summarization/README.md)

---

## 📌 Guiding Principles

- **Quality over quantity**
- **Transparency over size**
- **Reproducibility by default**
- **Iterative releases** (v1.0 first, improvements later)
