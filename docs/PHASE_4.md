# Phase 4 — Domain-Specific & Research-Grade

## 🎯 Goal

Phase 4 focuses on specialization and long-term value, enabling domain-specific and enterprise-grade NLP applications.

This phase enables:
- 🏛️ Public sector NLP
- ⚖️ Legal & compliance applications
- 🎤 Speech-to-text improvements
- 🏥 Healthcare and other domain applications

---

## 📦 Datasets in Phase 4

1. **Legal & Government Text Corpus**
2. **Public Institution QA Dataset**
3. **ASR Post-processing Dataset**
4. **Domain-specific Instruction Sets** (Health, Finance, Law)

---

## ⚖️ Dataset 1: Legal & Government Text Corpus

### Purpose

Support legal NLP, RAG systems, and compliance-focused applications with:
- Laws
- Regulations
- Official decisions
- Regulatory texts

### Format

```jsonl
{
  "id": "uuid",
  "text": "Text of law or decision...",
  "type": "law",
  "jurisdiction": "RS",
  "date": "2023-05-15",
  "source": "official_gazette"
}
```

### Sources

- Official gazettes (RS, FBiH, RS)
- Parliamentary documents
- EU regulations (translated)
- Municipal decisions

### Characteristics

- ✅ High level of formalization
- ✅ Precise terminology
- ✅ Clear document origin
- ⚠️ Licensing issues - verification needed

### Target Size

- **5,000 - 15,000** documents

---

## 🏛️ Dataset 2: Public Institution QA Dataset

### Purpose

Answer real citizen questions such as administrative procedures and public services.

### Format

```jsonl
{
  "question": "Kako izvaditi ličnu kartu u BiH?",
  "answer": "Za izdavanje lične karte potrebno je...",
  "category": "administrative",
  "institution": "MUP",
  "language": "bs"
}
```

### Sources

- FAQ sections of public institutions
- Official city/municipality information
- Call center transcripts (anonymized)
- Public e-government portals

### Use Cases

- Chatbots for citizens
- E-government assistants
- Information systems

### Target Size

- **3,000 - 8,000** Q&A pairs

---

## 🎤 Dataset 3: ASR Post-processing Dataset

### Purpose

Improve speech-to-text output normalization and punctuation for sr/bs/hr languages.

### Format

```jsonl
{
  "raw_asr": "danas je lijepo vrijeme trebalo bi izaci napolje",
  "corrected": "Danas je lijepo vrijeme. Trebalo bi izaći napolje.",
  "language": "bs"
}
```

### Characteristics

- Adding punctuation
- Capitalization
- Correcting diacritics
- Normalizing numbers and dates

### Sources

- Simulated ASR outputs
- Real ASR outputs (with permission)
- Manual correction workflow

### Target Size

- **10,000 - 25,000** sentences

---

## 🏥 Dataset 4: Domain-specific Instruction Sets

### 4a) Healthcare Instructions

#### Purpose

Medical information, symptom explanations, health advice.

#### Format

```jsonl
{
  "instruction": "Objasni simptome gripe",
  "response": "Simptomi gripe uključuju...",
  "domain": "healthcare",
  "verified": true
}
```

#### Ethical Considerations

⚠️ **Critically important**:
- Medical information must be accurate
- Disclaimer about seeking professional help
- Does not replace medical advice

---

### 4b) Finance Instructions

#### Purpose

Financial terminology, banking procedures, economic concepts.

#### Format

```jsonl
{
  "instruction": "Šta je hipoteka?",
  "response": "Hipoteka je kredit obezbijeđen nekretninom...",
  "domain": "finance"
}
```

---

### 4c) Legal Instructions

#### Purpose

Legal terminology, basic legal procedures, rights explanations.

#### Format

```jsonl
{
  "instruction": "Koja su osnovna prava potrošača?",
  "response": "Osnovna prava potrošača uključuju...",
  "domain": "legal"
}
```

---

## ✅ Success Criteria

Phase 4 is considered successful if:

1. ✅ Clearly defined domain scope
2. ✅ High information reliability
3. ✅ Enterprise usability
4. ✅ Expert validation for critical domains
5. ✅ Clear disclaimers for medical/legal datasets

---

## ⏱️ Time Estimate

| Dataset | Duration |
|---------|----------|
| Legal & Gov Corpus | 3-4 weeks |
| Public Institution QA | 2-3 weeks |
| ASR Post-processing | 2-3 weeks |
| Domain Instructions (all) | 4-6 weeks |
| **TOTAL** | **11-16 weeks** |

---

## ⚠️ Special Warnings

### Medical Content

- Must be verified by medical professionals
- Clear disclaimers
- Must not provide diagnoses or treatments

### Legal Content

- General information, not legal advice
- Disclaimer about consulting lawyers
- Information currency is critical

### Regulatory Content

- Check licenses for reproduction
- Source attribution
- Tracking law changes

---

## 🔗 Related Documents

- [Phase 3 - Structured NLP](PHASE_3.md)
- [Methodology](METHODOLOGY.md)
- [Data Sources](DATA_SOURCES.md)

---

## 📌 Notes

Phase 4 is **optional** but provides:
- 💼 Enterprise value
- 🎓 Research prestige
- 🌟 Unique datasets
- 📈 Long-term relevance

Start this phase only after successful completion of Phase 1-3.
