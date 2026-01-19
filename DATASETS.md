# Datasets Catalog

This document provides an overview of all datasets in the Balkan NLP project, their relationships, and current status.

---

## 📊 Overview

| Dataset                 | Phase | Status      | Size (target)   | HF Repo                                  |
| ----------------------- | ----- | ----------- | --------------- | ---------------------------------------- |
| Clean Text Corpus       | 1     | 🚧 Planning | 50K-150K docs   | `balkan-nlp/sr-bs-hr-clean-text`         |
| Language Identification | 1     | 🚧 Planning | 30K-60K samples | `balkan-nlp/sr-bs-hr-language-id`        |
| News Summarization      | 1     | 🚧 Planning | 20K-50K pairs   | `balkan-nlp/sr-bs-hr-news-summarization` |
| Instruction / Q&A       | 2     | ⏳ Planned  | 10K-30K pairs   | `balkan-nlp/sr-bs-hr-instructions`       |
| Paraphrase              | 2     | ⏳ Planned  | 15K-40K pairs   | `balkan-nlp/sr-bs-hr-paraphrase`         |
| Toxic / Hate Speech     | 2     | ⏳ Planned  | 20K-50K samples | `balkan-nlp/sr-bs-hr-toxic-speech`       |

**Legend**:

- 🚧 Planning / In Development
- ⏳ Planned (not started)
- ✅ Released
- 🔄 Updating

---

## 🗺️ Dataset Relationships

```
┌──────────────────────┐
│  Clean Text Corpus   │  ← Foundation dataset
│   (Phase 1)          │
└──────────┬───────────┘
           │
           ├──────────────────────┬──────────────────────┐
           │                      │                      │
           ↓                      ↓                      ↓
  ┌────────────────┐    ┌──────────────────┐   ┌────────────────┐
  │  Language ID   │    │  Summarization   │   │  Instructions  │
  │   (Phase 1)    │    │    (Phase 1)     │   │   (Phase 2)    │
  └────────────────┘    └──────────────────┘   └────────────────┘
```

---

## 📦 Phase 1 Datasets

### 1. Clean Text Corpus

**Purpose**: Foundation monolingual corpus for sr/bs/hr languages.

**Sources**:

- News portals (Bosnia, Croatia, Serbia)
- Wikipedia (bs, hr, sr)
- Government announcements

**Output Format**:

```jsonl
{
	"id": "uuid",
	"text": "Full cleaned text...",
	"language": "bs",
	"source": "klix.ba",
	"domain": "news"
}
```

**Key Features**:

- Deduplicated (exact + near-duplicate)
- Source-based language labels
- Clean, normalized text
- Metadata preserved

**Use Cases**:

- LLM pretraining
- Embeddings training
- Tokenizer training
- Base for derived datasets

**Documentation**: [datasets/clean_text/README.md](datasets/clean_text/README.md)

---

### 2. Language Identification

**Purpose**: Distinguish between sr, bs, and hr languages.

**Derived From**: Clean Text Corpus

**Output Format**:

```jsonl
{
	"id": "uuid",
	"text": "Short text sample...",
	"label": "hr",
	"source": "index.hr",
	"length": 156
}
```

**Key Features**:

- Length-stratified (short/medium/long)
- Source-based ground truth labels
- Balanced across languages

**Use Cases**:

- Training LID models
- Evaluating existing LID systems
- Preprocessing pipeline routing

**Documentation**: [datasets/language_id/README.md](datasets/language_id/README.md)

---

### 3. News Summarization

**Purpose**: Article-to-summary dataset using human-written leads.

**Derived From**: Clean Text Corpus (news domain only)

**Output Format**:

```jsonl
{
	"id": "uuid",
	"article": "Full article text...",
	"summary": "Lead paragraph...",
	"language": "bs",
	"source": "klix.ba",
	"category": "politika"
}
```

**Key Features**:

- Human-written summaries (journalistic leads)
- Real-world compression ratios
- Categorized by topic

**Use Cases**:

- Training summarization models
- Fine-tuning LLMs
- Evaluating abstractive/extractive methods

**Documentation**: [datasets/summarization/README.md](datasets/summarization/README.md)

---

## 📦 Phase 2 Datasets (Planned)

### 4. Instruction / Q&A

**Purpose**: Enable instruction-following for LLMs.

**Sources**:

- Transformed news articles
- Educational materials
- FAQ sections
- Semi-automatic generation + validation

**Output Format**:

```jsonl
{
	"instruction": "Objasni šta je inflacija",
	"response": "Inflacija je...",
	"language": "bs"
}
```

**Target Size**: 10K-30K pairs

**Documentation**: [docs/PHASE_2.md](docs/PHASE_2.md)

---

### 5. Paraphrase

**Purpose**: Multiple ways to express same meaning.

**Sources**:

- Agency news on different portals
- Official announcements (multilingual)
- Administrative documents

**Output Format**:

```jsonl
{
	"text_a": "Odluka je donesena danas.",
	"text_b": "Danas je donijeta odluka.",
	"language": "bs",
	"similarity": "high"
}
```

**Target Size**: 15K-40K pairs

**Documentation**: [docs/PHASE_2.md](docs/PHASE_2.md)

---

### 6. Toxic / Hate Speech

**Purpose**: Support content moderation with region-specific toxic language.

**Sources**:

- Public comments (anonymized)
- Forums (with disclaimers)

**Output Format**:

```jsonl
{
	"text": "Comment text...",
	"label": "hate_speech",
	"language": "sr",
	"context": "political"
}
```

**Labels**:

- `toxic`, `hate_speech`, `offensive`, `non_toxic`

**Target Size**: 20K-50K samples

**Documentation**: [docs/PHASE_2.md](docs/PHASE_2.md)

---

## 📦 Phase 3 Datasets (Planned)

### 7. Named Entity Recognition (NER)

**Target Size**: 15K-30K sentences  
**Entities**: PERSON, LOCATION, ORGANIZATION, DATE

### 8. Text Classification

**Target Size**: 20K-50K documents  
**Categories**: Politics, Economy, Sports, Technology, etc.

### 9. Translation (sr↔hr↔bs)

**Target Size**: 10K-25K parallel sentences  
**Unique**: Rare resource for South Slavic variants

### 10. Translation (sr/bs/hr↔EN)

**Target Size**: 15K-40K parallel sentences

### 11. LLM Evaluation Benchmark

**Target Size**: 5K-10K questions  
**Types**: QA, reasoning, local knowledge

**Documentation**: [docs/PHASE_3.md](docs/PHASE_3.md)

---

## 📦 Phase 4 Datasets (Optional)

### 12. Legal & Government Texts

**Target Size**: 5K-15K documents  
**Types**: Laws, regulations, decisions

### 13. Public Institution QA

**Target Size**: 3K-8K Q&A pairs  
**Topics**: Administrative procedures, public services

### 14. ASR Post-processing

**Target Size**: 10K-25K sentences  
**Purpose**: Punctuation, capitalization, normalization

### 15. Domain Instructions (Health, Finance, Law)

**Target Size**: Varies by domain  
**Purpose**: Domain-specific instruction tuning

**Documentation**: [docs/PHASE_4.md](docs/PHASE_4.md)

---

## 🔗 Dataset Dependencies

### Independent Datasets

- Clean Text Corpus (no dependencies)

### Derived Datasets

**From Clean Text Corpus**:

- Language Identification
- News Summarization
- Instruction / Q&A (partially)

**From Multiple Sources**:

- Paraphrase (news + official docs)
- Toxic Speech (comments + forums)
- NER (news + wiki)

---

## 📏 Quality Standards

All datasets must meet:

- ✅ **Deduplication**: < 1% duplicates
- ✅ **Language accuracy**: > 95%
- ✅ **Metadata**: 100% complete
- ✅ **Manual review**: 1% sample
- ✅ **Documentation**: Complete dataset card
- ✅ **Licensing**: Clearly stated
- ✅ **Versioning**: Semantic versioning

---

## 📊 Statistics Summary (Planned)

| Metric    | Phase 1   | Phase 2  | Phase 3  | Phase 4 | Total     |
| --------- | --------- | -------- | -------- | ------- | --------- |
| Documents | 100K-220K | 45K-120K | 50K-115K | 18K-48K | 213K-503K |
| Size (GB) | 0.5-2.0   | 0.2-0.5  | 0.3-1.0  | 0.1-0.3 | 1.1-3.8   |
| Languages | 3         | 3        | 3+EN     | 3       | 3+EN      |

---

## 🚀 Release Schedule (Tentative)

**2025 Q1**: Phase 1 datasets  
**2025 Q2**: Phase 2 datasets  
**2025 Q3**: Phase 3 datasets  
**2025 Q4**: Phase 4 datasets (optional)

---

## 📋 Adding New Datasets

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

**Quick checklist**:

1. Create `datasets/{name}/` directory
2. Add `README.md` and `config.yaml`
3. Document sources in `docs/DATA_SOURCES.md`
4. Add entry to this file
5. Update relevant `docs/PHASE_X.md`

---

## 🔗 External Resources

- **Hugging Face Organization**: [balkan-nlp](https://huggingface.co/balkan-nlp)
- **GitHub Repository**: [rsadevteam/balkan-nlp](https://github.com/rsadevteam/balkan-nlp)

---

## 📞 Questions?

For dataset-specific questions:

- Check individual dataset README files
- Review [docs/METHODOLOGY.md](docs/METHODOLOGY.md)
- Open a GitHub Discussion

---

**Last Updated**: 2025-01-19
