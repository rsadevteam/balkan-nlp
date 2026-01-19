# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Phase 1 - Foundation Datasets (In Progress)

#### Clean Text Corpus

- 🚧 Planning data collection pipeline
- 🚧 Implementing scrapers for news sources
- 🚧 Designing deduplication strategy

#### Language Identification

- 🚧 Planning extraction from Clean Text Corpus
- 🚧 Designing labeling strategy

#### News Summarization

- 🚧 Planning lead extraction methodology
- 🚧 Designing quality filters

---

## [0.1.0] - 2025-01-19

### Added

#### Project Structure

- Initial project setup
- Repository structure created
- Documentation framework established

#### Core Documentation

- `README.md` - Project overview
- `AGENTS.md` - AI agent instructions
- `ARCHITECTURE.md` - System design
- `CONTRIBUTING.md` - Contribution guidelines
- `SECURITY.md` - Security and privacy guidelines
- `DATASETS.md` - Dataset catalog
- `LICENSE` - MIT license

#### Phase Documentation

- `docs/PHASE_1.md` - Foundation datasets specification
- `docs/PHASE_2.md` - LLM enablement datasets specification
- `docs/PHASE_3.md` - Structured NLP datasets specification
- `docs/PHASE_4.md` - Domain-specific datasets specification

#### Methodology

- `docs/METHODOLOGY.md` - Data collection and processing standards
- `docs/DATA_SOURCES.md` - Approved data sources documentation

#### Dataset Configurations

- `datasets/clean_text/` - Clean text corpus configuration
    - README.md with dataset specification
    - config.yaml with processing parameters
    - sources.yaml with source URLs
- `datasets/language_id/` - Language ID configuration
    - README.md with dataset specification
    - config.yaml with extraction parameters
- `datasets/summarization/` - Summarization configuration
    - README.md with dataset specification
    - config.yaml with processing parameters

#### Development Setup

- `pyproject.toml` - Python package configuration
- `.gitignore` - Git ignore rules
- Folder structure for modules:
    - `scraping/` - Web scraping modules
    - `processing/` - Data processing modules
    - `export/` - Export and upload modules
    - `scripts/` - Pipeline entry points
    - `utils/` - Shared utilities

---

## Release Notes

### [0.1.0] - Initial Release

**Project Launch** 🚀

This is the initial release of Balkan NLP, establishing the project structure and documentation framework for building high-quality NLP datasets for Serbian, Bosnian, and Croatian languages.

**Key Highlights**:

- ✅ Complete project structure
- ✅ Comprehensive documentation for AI agents and contributors
- ✅ Phase 1 dataset specifications ready
- ✅ Clear methodology and security guidelines
- ✅ Ready for implementation

**Next Steps**:

- Implement Phase 1 scrapers
- Begin Clean Text Corpus collection
- Set up processing pipeline
- Establish quality validation

---

## Future Releases (Planned)

### [0.2.0] - Phase 1 Alpha (TBD)

**Planned Features**:

- Working scrapers for news sources
- Basic cleaning pipeline
- Initial dataset samples

### [1.0.0] - Phase 1 Release (TBD)

**Planned Features**:

- Clean Text Corpus v1.0
- Language Identification v1.0
- News Summarization v1.0
- Complete documentation
- Published on Hugging Face

### [1.1.0] - Phase 2 Start (TBD)

**Planned Features**:

- Instruction / Q&A dataset
- Paraphrase dataset
- Toxic speech dataset

---

## Version Naming Convention

### Major Versions

- `1.x.x` - Phase 1 datasets
- `2.x.x` - Phase 2 datasets
- `3.x.x` - Phase 3 datasets
- `4.x.x` - Phase 4 datasets

### Minor Versions

- `x.1.x` - New dataset in current phase
- `x.2.x` - Major improvements to existing datasets

### Patch Versions

- `x.x.1` - Bug fixes, documentation updates
- `x.x.2` - Minor improvements, metadata corrections

---

## Dataset Versioning

Each dataset follows its own versioning:

```
balkan-nlp/sr-bs-hr-clean-text
├── v1.0.0 - Initial release
├── v1.1.0 - Additional sources
└── v2.0.0 - Major reprocessing
```

See individual dataset READMEs for specific version histories.

---

## Contributing to Changelog

When adding changes:

1. Add entry under `[Unreleased]` section
2. Use appropriate category:
    - `Added` - New features
    - `Changed` - Changes to existing functionality
    - `Deprecated` - Soon-to-be removed features
    - `Removed` - Removed features
    - `Fixed` - Bug fixes
    - `Security` - Security improvements

3. Link to relevant pull requests or issues
4. Update version numbers when releasing

**Example**:

```markdown
### Added

- Scraper for klix.ba (#42)
- Deduplication module using MinHash (#45)

### Fixed

- Rate limiting in fetch.py (#48)
```

---

## Links

- [Repository](https://github.com/rsadevteam/balkan-nlp)
- [Hugging Face](https://huggingface.co/balkan-nlp)
- [Issues](https://github.com/rsadevteam/balkan-nlp/issues)
- [Discussions](https://github.com/rsadevteam/balkan-nlp/discussions)

---

**Last Updated**: 2025-01-19
