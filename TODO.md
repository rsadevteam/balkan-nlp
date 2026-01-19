# TODO - Project Roadmap

This document tracks immediate tasks and long-term goals for Balkan NLP.

**Last Updated**: 2026-01-19

---

## 🎯 Current Focus: Phase 1 Implementation

**Goal**: Release first three datasets on Hugging Face

**Timeline**: 2-4 weeks

---

## ✅ Completed

- [x] Project structure
- [x] Documentation framework
- [x] Dataset specifications (Phase 1)
- [x] Methodology documentation
- [x] Security guidelines
- [x] Configuration files

---

## 🚧 In Progress

### Setup & Infrastructure

- [ ] **Python environment setup**
    - [ ] Test all dependencies install correctly
    - [ ] Verify Python 3.11+ compatibility
    - [ ] Set up virtual environment instructions

- [ ] **Development tools**
    - [ ] Configure Black formatter
    - [ ] Configure isort
    - [ ] Set up pre-commit hooks
    - [ ] Add pytest configuration

### Code Implementation

- [ ] **Utils module** (`utils/`)
    - [ ] `logging.py` - Logging configuration
    - [ ] `config.py` - YAML config loader
    - [ ] `text_utils.py` - Text manipulation
    - [ ] `hashing.py` - SHA256, MinHash

- [ ] **Scraping module** (`scraping/`)
    - [ ] `fetch.py` - HTTP client with rate limiting
    - [ ] `extract.py` - Trafilatura wrapper
    - [ ] `sources/common.py` - Shared utilities
    - [ ] Test scrapers on sample URLs

---

## 📋 Next Up (Priority Order)

### Week 1-2: Core Pipeline

1. **Implement basic scrapers**
    - [ ] News scraper template
    - [ ] robots.txt checker
    - [ ] Rate limiter class
    - [ ] Error handling

2. **Processing pipeline**
    - [ ] Text cleaning functions
    - [ ] Unicode normalization
    - [ ] Whitespace normalization

3. **Testing infrastructure**
    - [ ] Unit tests for utils
    - [ ] Integration tests for scraping
    - [ ] Sample data fixtures

### Week 3-4: Dataset Generation

4. **Clean Text Corpus**
    - [ ] Scrape 1000 articles (test)
    - [ ] Implement deduplication
    - [ ] Add language validation
    - [ ] Generate statistics
    - [ ] Manual review sample

5. **Export & Upload**
    - [ ] JSONL export
    - [ ] Parquet export
    - [ ] HF dataset card generation
    - [ ] Upload to Hugging Face

6. **Documentation**
    - [ ] Update CHANGELOG
    - [ ] Write dataset card
    - [ ] Document any issues found

---

## 📅 Phase 1 Milestones

### Milestone 1: Working Pipeline (Week 2)

- [ ] Can scrape 100 URLs successfully
- [ ] Clean and deduplicate data
- [ ] Export to JSONL
- [ ] All tests passing

### Milestone 2: Clean Text v0.1 (Week 3)

- [ ] 10K documents collected
- [ ] All three languages represented
- [ ] Quality checks passed
- [ ] Internal testing complete

### Milestone 3: Phase 1 Release (Week 4)

- [ ] Clean Text Corpus v1.0 on HF
- [ ] Language ID v1.0 on HF
- [ ] Summarization v1.0 on HF
- [ ] Documentation complete
- [ ] Announcement blog post

---

## 🔮 Future Phases

### Phase 2: LLM Enablement (Q2 2026)

- [ ] Instruction dataset generation
- [ ] Paraphrase extraction
- [ ] Toxic speech annotation
- [ ] Quality validation

### Phase 3: Structured NLP (Q3 2026)

- [ ] NER annotation
- [ ] Text classification
- [ ] Translation pairs
- [ ] LLM benchmark

### Phase 4: Domain-Specific (Q4 2026)

- [ ] Legal corpus
- [ ] Public QA
- [ ] ASR post-processing
- [ ] Domain instructions

---

## 🛠️ Technical Debt

### High Priority

- [ ] Add comprehensive error handling
- [ ] Implement proper logging throughout
- [ ] Add data validation at each step
- [ ] Create monitoring dashboard

### Medium Priority

- [ ] Optimize deduplication speed
- [ ] Add caching for HTTP requests
- [ ] Implement parallel scraping
- [ ] Add progress bars (tqdm)

### Low Priority

- [ ] Add dataset versioning system
- [ ] Create automated testing pipeline
- [ ] Build dataset statistics dashboard
- [ ] Add interactive documentation

---

## 📚 Documentation TODO

### High Priority

- [ ] Add code examples to ARCHITECTURE.md
- [ ] Create quickstart guide
- [ ] Add troubleshooting section
- [ ] Document common errors

### Medium Priority

- [ ] Create video tutorial
- [ ] Add API documentation
- [ ] Create developer guide
- [ ] Add dataset usage examples

### Low Priority

- [ ] Translate documentation to sr/bs/hr
- [ ] Create FAQ page
- [ ] Add case studies
- [ ] Create blog posts

---

## 🐛 Known Issues

_None yet - project is in initial development_

To report issues: https://github.com/rsadevteam/balkan-nlp/issues

---

## 💡 Ideas / Backlog

### Dataset Ideas

- [ ] Social media dataset (public tweets)
- [ ] Subtitle dataset (movie/TV subtitles)
- [ ] Academic papers dataset
- [ ] Code-switching dataset (sr/bs/hr + EN)

### Features

- [ ] Dataset viewer web app
- [ ] Quality metrics dashboard
- [ ] Automated dataset updates
- [ ] Community contributions system

### Integrations

- [ ] Weights & Biases integration
- [ ] MLflow tracking
- [ ] DVC for data versioning
- [ ] GitHub Actions CI/CD

---

## 🎯 Success Criteria

### Phase 1 Success

- ✅ 50K+ documents in Clean Text Corpus
- ✅ 30K+ samples in Language ID
- ✅ 20K+ pairs in Summarization
- ✅ < 1% duplicate rate
- ✅ > 95% language accuracy
- ✅ Published on Hugging Face
- ✅ 100+ downloads in first month

### Project Success (Long-term)

- ✅ All Phase 1-3 datasets released
- ✅ 1000+ downloads across datasets
- ✅ Cited in 10+ research papers
- ✅ Community contributions accepted
- ✅ Recognized as standard sr/bs/hr resource

---

## 📊 Tracking Progress

Update this file weekly with:

- Move completed items to ✅ Completed
- Add new items as discovered
- Update timeline estimates
- Note blockers or challenges

---

## 🤝 How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Quick ways to help:

1. Implement a scraper
2. Add tests
3. Improve documentation
4. Report bugs
5. Suggest new datasets

---

## 📞 Questions?

- **Technical**: Open a GitHub issue
- **General**: Start a discussion
- **Urgent**: Email office@rsateam.com

---

## 🔄 Review Schedule

This TODO should be reviewed:

- **Weekly**: Update progress, adjust priorities
- **Monthly**: Review milestones, update timeline
- **Quarterly**: Assess overall direction

---

**Next Review**: 2026-01-26

---

## 🎉 Quick Wins (Easy Tasks for New Contributors)

- [ ] Fix typos in documentation
- [ ] Add more examples to AGENTS.md
- [ ] Improve .gitignore
- [ ] Add code comments
- [ ] Create example scripts
- [ ] Write unit tests
- [ ] Update CHANGELOG

These are great first contributions! 🌟

---

**Remember**: Perfect is the enemy of good. Ship Phase 1, then iterate! 🚀
