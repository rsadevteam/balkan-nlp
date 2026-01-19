# Phase 2 — LLM Enablement Datasets

## 🎯 Goal

Phase 2 focuses on making large language models useful and aligned for Serbian, Bosnian, and Croatian by providing task-oriented and instruction-following data.

This phase directly improves:

- 💬 Conversational quality
- 🧠 Reasoning capabilities
- 📝 Summarization
- 🛡️ Safety alignment

---

## 📦 Datasets in Phase 2

1. **Instruction / Q&A Dataset**
2. **Paraphrase Dataset**
3. **Toxic / Hate Speech Dataset**

All datasets are derived from Phase 1 data and curated public sources.

---

## 📝 Dataset 1: Instruction / Q&A Dataset

### Purpose

Enable instruction-following and chat-style behavior for LLMs in sr/bs/hr languages.

### Content

- Explanations
- How-to questions
- Summaries
- Reasoning prompts
- Educational content

### Format

```jsonl
{
	"instruction": "Objasni jednostavno šta je inflacija",
	"response": "Inflacija je porast cijena roba i usluga tokom vremena...",
	"language": "bs"
}
```

### Sources

- Transformation of news articles into Q&A format
- Public educational materials
- Institution FAQ sections
- Semi-automatic generation + human validation

### Target Size

- **10,000 - 30,000** instruction-response pairs

---

## 🔄 Dataset 2: Paraphrase Dataset

### Purpose

Improve robustness and semantic understanding by providing multiple valid ways of expressing the same meaning.

Special focus on variations between sr/bs/hr language variants.

### Format

```jsonl
{
	"text_a": "Odluka je donesena danas.",
	"text_b": "Danas je donijeta odluka.",
	"language": "bs",
	"similarity": "high"
}
```

### Sources

- Same news from different portals (agency news)
- Official announcements in different languages
- Parallel administrative documents

### Target Size

- **15,000 - 40,000** paraphrase pairs

---

## 🛡️ Dataset 3: Toxic / Hate Speech Dataset

### Purpose

Support moderation and safety systems with region-specific toxic language, including ethnic and political hate speech.

### Labels

- `toxic` - generally inappropriate
- `hate_speech` - hate speech
- `offensive` - offensive
- `non_toxic` - clean

### Format

```jsonl
{
	"text": "Comment text...",
	"label": "hate_speech",
	"language": "sr",
	"context": "political"
}
```

### Sources

- Public comments from news portals
- Forums (with clear disclaimers)
- Publicly available examples

### Ethical Considerations

⚠️ **Important**:

- Clear ethical documentation
- Anonymization
- Clear use-case guidelines
- Respecting dignity

### Target Size

- **20,000 - 50,000** labeled examples

---

## ✅ Success Criteria

Phase 2 is considered successful if:

1. ✅ Datasets usable for LLM fine-tuning
2. ✅ Clear annotation guidelines
3. ✅ Ethical and legal transparency
4. ✅ Demonstrated improvement in LLM performance
5. ✅ Community uses datasets for model training

---

## ⏱️ Time Estimate

| Dataset             | Duration      |
| ------------------- | ------------- |
| Instruction / Q&A   | 2-3 weeks     |
| Paraphrase          | 2-3 weeks     |
| Toxic / Hate Speech | 2-3 weeks     |
| **TOTAL**           | **6-9 weeks** |

---

## 🔗 Related Documents

- [Methodology](METHODOLOGY.md)
- [Phase 1 - Foundation](PHASE_1.md)
- [Phase 3 - Structured NLP](PHASE_3.md)

---

## 📌 Key Characteristics

- **Native content** - not translations
- **Regional context** - Balkan specificities
- **Quality validation** - human-in-the-loop
- **Ethical guidelines** - clear usage rules
