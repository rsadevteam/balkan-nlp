# Balkan NLP

## 🎯 Overview

This project aims to build a **high-quality, open, and reproducible dataset ecosystem** for **Serbian, Bosnian, and Croatian (sr/bs/hr)**.

The primary motivation is to address the lack of **clean, well-documented, and task-oriented datasets** for South Slavic languages, especially for modern **LLMs, NLP pipelines, and evaluation benchmarks**.

All datasets are published on **Hugging Face**, while this repository contains:

- the **project vision**
- the **dataset roadmap**
- the **methodology and phases**
- **configuration and pipeline code**

---

## 💡 Design Principles

- **Quality over quantity**
- **Transparency over size**
- **Reproducibility by default**
- **One dataset = one clear purpose**
- **Shared pipeline, separate Hugging Face datasets**
- **Iterative releases (v1.0, v1.1, …)**

---

## 📁 Project Structure

```
balkan-nlp/
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
│
├── models/             # Local language models (gitignored)
│
├── docs/
│   ├── PHASE_1.md
│   ├── PHASE_2.md
│   ├── PHASE_3.md
│   ├── PHASE_4.md
│   ├── METHODOLOGY.md
│   └── DATA_SOURCES.md
│
├── datasets/
│   ├── clean_text/
│   │   ├── sources.yaml
│   │   ├── config.yaml
│   │   └── README.md
│   │
│   ├── language_id/
│   │   ├── config.yaml
│   │   └── README.md
│   │
│   └── summarization/
│       ├── config.yaml
│       └── README.md
│
├── scraping/
│   ├── __init__.py
│   ├── fetch.py
│   ├── extract.py
│   └── sources/
│       ├── klix.py
│       ├── index.py
│       ├── blic.py
│       └── common.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── normalization.py
│   ├── deduplication.py
│   ├── language_check.py
│   └── splitting.py
│
├── export/
│   ├── __init__.py
│   ├── to_jsonl.py
│   ├── to_parquet.py
│   └── hf_upload.py
│
├── scripts/
│   ├── run_clean_text.py
│   ├── run_language_id.py
│   └── run_summarization.py
│
└── utils/
    ├── __init__.py
    ├── hashing.py
    ├── text_utils.py
    └── logging.py
```

---

## 🗺️ Dataset Roadmap

The project is organized into **four logical phases**.

### 📘 Phase 1 — Foundation (Required)

Core datasets that establish trust and usability.

- **Clean Text Corpus** (sr / bs / hr)
- **Language Identification** (sr vs bs vs hr)
- **News Summarization**

➡️ See details in: [`docs/PHASE_1.md`](docs/PHASE_1.md)

---

### 📗 Phase 2 — LLM Enablement (High Priority)

Datasets that make LLMs truly usable in sr/bs/hr.

- **Instruction / Q&A**
- **Paraphrase**
- **Toxic / Hate Speech**

➡️ See details in: [`docs/PHASE_2.md`](docs/PHASE_2.md)

---

### 📙 Phase 3 — Structured NLP & Evaluation (Advanced)

Research-grade datasets and benchmarks.

- **Named Entity Recognition (NER)**
- **Text Classification**
- **Translation** (sr↔hr↔bs, ↔EN)
- **LLM Evaluation / Benchmark**

➡️ See details in: [`docs/PHASE_3.md`](docs/PHASE_3.md)

---

### 📕 Phase 4 — Domain-Specific & Research-Grade (Optional)

Highly specialized, long-term value datasets.

- **Legal & Government Texts**
- **Public Institution QA**
- **ASR Post-processing**
- **Domain-specific instruction sets**

➡️ See details in: [`docs/PHASE_4.md`](docs/PHASE_4.md)

---

## 🚀 Hugging Face Publishing Strategy

- Each dataset is published as a **separate Hugging Face dataset**
- All datasets reference a **shared open-source pipeline**
- Dataset cards clearly document:
    - data sources
    - processing steps
    - limitations
    - licensing notes

---

## 📊 Status

| Phase   | Status                      |
| ------- | --------------------------- |
| Phase 1 | 🚧 Ready for implementation |
| Phase 2 | ⏳ Planned                  |
| Phase 3 | ⏳ Planned                  |
| Phase 4 | ⏳ Optional                 |

---

## 🤝 Contributing

This project is designed to be **open and extensible**.
Contributions, suggestions and dataset ideas are welcome.

---

## 📄 License

Code and documentation in this repository are released under an open-source license.
Individual datasets may have different usage constraints depending on the original source material.

---

## 📚 Additional Documentation

- [Methodology](docs/METHODOLOGY.md)
- [Data Sources](docs/DATA_SOURCES.md)
- [Phase 1 – Details](docs/PHASE_1.md)
- [Phase 2 – Details](docs/PHASE_2.md)
- [Phase 3 – Details](docs/PHASE_3.md)
- [Phase 4 – Details](docs/PHASE_4.md)
