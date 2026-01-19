# Phase 3 — Structured NLP & Evaluation

## 🎯 Goal

Phase 3 introduces structured NLP tasks and evaluation benchmarks, positioning the project as a regional reference for serious NLP and research.

This phase enables:
- 🔍 Enterprise NLP applications (RAG, search)
- 🌍 Translation and multilingual models
- 📊 Standardized LLM evaluation
- 🎓 Academic research

---

## 📦 Datasets in Phase 3

1. **Named Entity Recognition (NER)**
2. **Text Classification (Topics)**
3. **Translation** (sr↔hr↔bs, ↔EN)
4. **LLM Evaluation / Benchmark Dataset**

---

## 🏷️ Dataset 1: Named Entity Recognition (NER)

### Purpose

Support RAG systems, search applications, and enterprise NLP with locally-relevant named entities.

### Entities

- `PERSON` - people
- `LOCATION` - locations (cities, countries, regions)
- `ORGANIZATION` - organizations, companies, institutions
- `DATE` - dates and temporal markers
- `EVENT` - events (optional)

### Format

```jsonl
{
  "text": "Predsjednik BiH Denis Bećirović posjetio je Sarajevo.",
  "entities": [
    {"text": "Denis Bećirović", "label": "PERSON", "start": 17, "end": 32},
    {"text": "Sarajevo", "label": "LOCATION", "start": 47, "end": 55}
  ],
  "language": "bs"
}
```

### Construction

- **Automatic annotation** - using existing NER tools (spaCy, Stanza)
- **Human correction** - at least 20% of samples
- **Silver + Gold subsets** - clear quality marking

### Target Size

- **15,000 - 30,000** annotated sentences

---

## 📂 Dataset 2: Text Classification (Topics)

### Purpose

Topic classification for news and web content, useful for filtering, routing, and recommendations.

### Categories

- Politics (Politika)
- Economy (Ekonomija)
- Sports (Sport)
- Technology (Tehnologija)
- Health (Zdravlje)
- Culture (Kultura)
- Crime (Kriminal)
- Lifestyle (Životni stil)

### Format

```jsonl
{
  "text": "Article text...",
  "category": "ekonomija",
  "language": "sr"
}
```

### Sources

- Already categorized news articles
- Automatic extraction + validation

### Target Size

- **20,000 - 50,000** classified documents

---

## 🌍 Dataset 3: Translation Datasets

### 3a) SR ↔ HR ↔ BOS Parallel Dataset

#### Purpose

Parallel sentences between South Slavic variants, which is a **rare and very valuable** resource.

#### Format

```jsonl
{
  "bs": "Odluka je donesena danas.",
  "hr": "Odluka je donesena danas.",
  "sr": "Odluka je doneta danas.",
  "source": "official_communication"
}
```

#### Sources

- Agency news in multiple languages
- Official documents (EU, laws)
- Institutional announcements

#### Target Size

- **10,000 - 25,000** parallel sentences

---

### 3b) SR/BOS/HR ↔ EN Translation Dataset

#### Purpose

Enable fine-tuning of translation models between sr/bs/hr and English.

#### Format

```jsonl
{
  "sr": "Predsjednik je danas održao govor.",
  "en": "The president delivered a speech today.",
  "direction": "sr-en"
}
```

#### Sources

- Parallel news articles
- EU and international documents
- Subtitles (optional, with license)

#### Target Size

- **15,000 - 40,000** parallel sentences

---

## 📊 Dataset 4: LLM Evaluation / Benchmark

### Purpose

Provide standardized evaluation benchmark for sr/bs/hr language models, including:

- ❓ Question Answering
- 🧠 Reasoning
- 📚 Reading comprehension
- 🌍 Local cultural knowledge
- 🧮 Math reasoning

### Format

```jsonl
{
  "question": "Ko je bio prvi predsjednik Bosne i Hercegovine?",
  "answer": "Alija Izetbegović",
  "category": "history",
  "difficulty": "easy",
  "language": "bs"
}
```

### Construction

- Mix of manual and adapted questions
- Focus on local context (geography, history, culture)
- Multiple-choice + open-ended questions

### Target Size

- **5,000 - 10,000** evaluation questions

---

## ✅ Success Criteria

Phase 3 is considered successful if:

1. ✅ Research-grade annotation quality
2. ✅ Clear evaluation splits (train/dev/test)
3. ✅ Citability in academic papers
4. ✅ Usage in industry and research projects
5. ✅ Reproducible evaluation protocols

---

## ⏱️ Time Estimate

| Dataset | Duration |
|---------|----------|
| NER | 3-5 weeks |
| Text Classification | 1-2 weeks |
| Translation (sr↔hr↔bs) | 4-6 weeks |
| Translation (↔EN) | 2-3 weeks |
| LLM Benchmark | 2-3 weeks |
| **TOTAL** | **12-19 weeks** |

---

## 🔗 Related Documents

- [Phase 2 - LLM Enablement](PHASE_2.md)
- [Phase 4 - Domain Specific](PHASE_4.md)
- [Methodology](METHODOLOGY.md)

---

## 📌 Notes

- **Annotation quality** is critical - better small but accurate dataset
- **Inter-annotator agreement** should be > 0.8
- **Test sets** must not be publicly available (leakage prevention)
- **Benchmark results** should be reproducible
