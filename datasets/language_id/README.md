# Language Identification Dataset (sr vs bs vs hr)

## 📝 Description

Dataset for distinguishing between **Serbian**, **Bosnian**, and **Croatian** - three very similar South Slavic languages that are often misclassified.

---

## 🎯 Purpose

Existing language identification tools (FastText, langid) often struggle with:

- ❌ Coarse classification (treating them as one language)
- ❌ Low precision between sr/bs/hr
- ❌ Inconsistent performance across different text lengths

**This dataset enables**:

- ✅ Fine-grained language identification
- ✅ Preprocessing pipeline routing
- ✅ Evaluation of existing LID systems
- ✅ Training new models

---

## 📊 Statistics (Planned for v1.0)

| Metric                      | Value              |
| --------------------------- | ------------------ |
| Total samples               | 30,000 - 60,000    |
| Bosnian (bs)                | ~33%               |
| Croatian (hr)               | ~33%               |
| Serbian (sr)                | ~33%               |
| Average length              | 150-500 characters |
| Short text (<100 chars)     | 25%                |
| Medium text (100-300 chars) | 50%                |
| Long text (>300 chars)      | 25%                |

---

## 🗂️ Format

```jsonl
{
	"id": "550e8400-e29b-41d4-a716-446655440000",
	"text": "Kratak pasus teksta za identifikaciju...",
	"label": "bs",
	"source": "klix.ba",
	"length": 156
}
```

### Fields

- **id**: Unique UUID
- **text**: Text sample
- **label**: sr / bs / hr
- **source**: Source domain (for transparency)
- **length**: Length in characters

---

## 📥 Sources

Dataset is **derived from Clean Text Corpus** dataset.

### Labeling Strategy

**Source-based labeling** (NOT automatic detection):

| Source                             | Label |
| ---------------------------------- | ----- |
| klix.ba, avaz.ba, n1info.ba        | bs    |
| index.hr, jutarnji.hr, vecernji.hr | hr    |
| blic.rs, politika.rs, rts.rs       | sr    |
| bs.wikipedia.org                   | bs    |
| hr.wikipedia.org                   | hr    |
| sr.wikipedia.org                   | sr    |

**Why source-based?**

- ✅ Ground truth labels from authors
- ✅ No circular dependency (LID trained on LID output)
- ✅ Academically accepted practice

---

## 🚀 Hugging Face

Dataset will be available at:

```
huggingface.co/datasets/balkan-nlp/sr-bs-hr-language-id
```

---

## 📚 Citation

```bibtex
@dataset{balkan_nlp_language_id_2026,
  title={SR/BS/HR Language Identification Dataset},
  author={Balkan NLP Project},
  year={2026},
  publisher={Hugging Face},
  url={https://huggingface.co/datasets/balkan-nlp/sr-bs-hr-language-id}
}
```

---

**Status**: 🚧 In Development
