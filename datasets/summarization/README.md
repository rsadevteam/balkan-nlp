# News Summarization Dataset

## 📝 Description

Real-world summarization dataset for **Serbian**, **Bosnian**, and **Croatian** based on news articles and their lead paragraphs.

This dataset enables:
- 📝 Training summarization models
- 🧪 Evaluation of abstractive/extractive summarization
- 🤖 Fine-tuning LLMs for summarization

---

## 🎯 Purpose

Most summarization datasets for sr/bs/hr are:
- ❌ Synthetically generated (AI-written summaries)
- ❌ Translated from English
- ❌ Small and inconsistent

**This dataset is**:
- ✅ Human-written summaries (journalistic leads)
- ✅ Native content (not translations)
- ✅ High-quality and realistic
- ✅ Academically accepted approach

---

## 📊 Statistics (Planned for v1.0)

| Metric | Value |
|---------|-----------|
| Total articles | 20,000 - 50,000 |
| Bosnian (bs) | ~33% |
| Croatian (hr) | ~33% |
| Serbian (sr) | ~33% |
| Avg article length | 800-2000 words |
| Avg summary length | 50-150 words |
| Compression ratio | ~10:1 |

---

## 🗂️ Format

```jsonl
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "article": "Full news article text...",
  "summary": "Lead paragraph summarizing key information...",
  "language": "bs",
  "source": "klix.ba",
  "category": "politika",
  "date": "2024-03-15",
  "url": "https://klix.ba/..."
}
```

### Fields

- **id**: Unique UUID
- **article**: Full article text (without title and lead)
- **summary**: Lead paragraph (summary)
- **language**: sr / bs / hr
- **source**: Source portal
- **category**: News category (optional)
- **date**: Publication date
- **url**: Original URL

---

## 🚀 Hugging Face

Dataset will be available at:
```
huggingface.co/datasets/balkan-nlp/sr-bs-hr-news-summarization
```

---

## 📚 Citation

```bibtex
@dataset{balkan_nlp_summarization_2025,
  title={SR/BS/HR News Summarization Dataset},
  author={Balkan NLP Project},
  year={2025},
  publisher={Hugging Face},
  url={https://huggingface.co/datasets/balkan-nlp/sr-bs-hr-news-summarization}
}
```

---

**Status**: 🚧 In Development
