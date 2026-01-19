# Data Sources

This document provides detailed information about all data sources used in the project, their status, access rules, and licensing information.

---

## 🎯 Source Selection Principles

1. **Public availability** - content must be publicly accessible
2. **Legality** - respecting copyright and ToS
3. **Quality** - reliable sources with good editorial standards
4. **Diversity** - balance of sources by region and type
5. **Currency** - preference for active sources

---

## 📰 News Portals

### Bosnia and Herzegovina

| Portal       | URL                     | Language | Status    | Notes                 |
| ------------ | ----------------------- | -------- | --------- | --------------------- |
| Klix.ba      | https://klix.ba         | BS       | ✅ Active | Largest portal in BiH |
| Avaz.ba      | https://avaz.ba         | BS       | ✅ Active | Daily news            |
| Faktor.ba    | https://faktor.ba       | BS       | ✅ Active | Analytics and news    |
| N1 Info BA   | https://n1info.ba       | BS       | ✅ Active | TV station and portal |
| Oslobodjenje | https://oslobodjenje.ba | BS       | ✅ Active | Traditional media     |

**Access**: robots.txt + rate limiting 1 req/sec

---

### Croatia

| Portal        | URL                 | Language | Status    | Notes                |
| ------------- | ------------------- | -------- | --------- | -------------------- |
| Index.hr      | https://index.hr    | HR       | ✅ Active | Largest portal in HR |
| Jutarnji list | https://jutarnji.hr | HR       | ✅ Active | Daily newspaper      |
| Večernji list | https://vecernji.hr | HR       | ✅ Active | Daily newspaper      |
| Tportal       | https://tportal.hr  | HR       | ✅ Active | News portal          |
| 24sata        | https://24sata.hr   | HR       | ✅ Active | Tabloid style        |

**Access**: robots.txt + rate limiting 1 req/sec

---

### Serbia

| Portal     | URL                 | Language | Status    | Notes                 |
| ---------- | ------------------- | -------- | --------- | --------------------- |
| Blic       | https://blic.rs     | SR       | ✅ Active | Largest portal in RS  |
| Politika   | https://politika.rs | SR       | ✅ Active | Traditional media     |
| RTS        | https://rts.rs      | SR       | ✅ Active | Public broadcaster    |
| N1 Info RS | https://n1info.rs   | SR       | ✅ Active | TV station and portal |
| B92        | https://b92.net     | SR       | ✅ Active | News portal           |

**Access**: robots.txt + rate limiting 1 req/sec

---

## 📚 Wikipedia

### Projects

| Project      | URL                      | Language | License      | Notes        |
| ------------ | ------------------------ | -------- | ------------ | ------------ |
| BS Wikipedia | https://bs.wikipedia.org | BS       | CC BY-SA 3.0 | Encyclopedia |
| HR Wikipedia | https://hr.wikipedia.org | HR       | CC BY-SA 3.0 | Encyclopedia |
| SR Wikipedia | https://sr.wikipedia.org | SR       | CC BY-SA 3.0 | Encyclopedia |

**Usage**:

- Articles only (article namespace)
- No talk pages
- No templates and infoboxes
- Text content only

**Export method**: Wikipedia dumps (XML export)

---

## 🏛️ Public Institutions

### Bosnia and Herzegovina

| Institution            | Type          | URL                          | Notes                  |
| ---------------------- | ------------- | ---------------------------- | ---------------------- |
| Official Gazette BiH   | Laws          | http://www.sluzbenilist.ba   | Legal acts             |
| Parliamentary Assembly | Documents     | http://www.parlament.ba      | Public documents       |
| FBiH Government        | Announcements | https://www.vladafbih.gov.ba | Official announcements |

---

### Croatia

| Institution           | Type          | URL                          | Notes                  |
| --------------------- | ------------- | ---------------------------- | ---------------------- |
| Narodne novine        | Laws          | https://narodne-novine.nn.hr | Official gazette       |
| Croatian Parliament   | Documents     | https://www.sabor.hr         | Public documents       |
| Government of Croatia | Announcements | https://vlada.gov.hr         | Official announcements |

---

### Serbia

| Institution          | Type          | URL                       | Notes                  |
| -------------------- | ------------- | ------------------------- | ---------------------- |
| Official Gazette RS  | Laws          | http://www.slglasnik.com  | Legal acts             |
| National Assembly    | Documents     | http://www.parlament.rs   | Public documents       |
| Government of Serbia | Announcements | https://www.srbija.gov.rs | Official announcements |

**Note**: Verification needed for each document individually - possible copyright.

---

## 🚫 Excluded Sources

### We do NOT use:

❌ **Social media**:

- Facebook comments
- Twitter/X posts
- Instagram content
- Reddit discussions

**Reason**: Privacy, unclear rights, noise

---

❌ **Paywalled content**:

- Subscription articles
- Premium content
- Registration-protected content

**Reason**: Violation of terms of service

---

❌ **User-generated content** (Phase 1):

- Forum posts
- Portal comments
- Blog comments

**Reason**: Privacy, quality
**Note**: May be considered for specific datasets in Phase 2/3 with clear guidelines

---

## 📋 Licensing Information

### News Portals

**Status**: Most news portals allow web scraping for research purposes but do not provide explicit licenses.

**Our approach**:

- Respect robots.txt
- Rate limiting
- Attribution in metadata
- Dataset license: research/educational use
- Not redistributing original HTML

⚠️ **Disclaimer**: Dataset users are responsible for complying with copyright laws in their jurisdiction.

---

### Wikipedia

**License**: CC BY-SA 3.0 / GFDL

**Requirements**:

- ✅ Attribution - citing Wikipedia as source
- ✅ ShareAlike - derived works under same license
- ✅ Free use and redistribution

---

### Public Documents

**Status**: Varies by country and document type

**Generally**:

- Laws and regulations - public domain
- Official announcements - reproduction allowed
- EU documents - open license

⚠️ **Verification needed** for each specific case.

---

## 🔄 Source Updates

### Adding New Sources

To add a new source:

1. ✅ Check robots.txt
2. ✅ Check Terms of Service
3. ✅ Test access
4. ✅ Document in this file
5. ✅ Implement scraper
6. ✅ Testing and validation

### Review Schedule

- **Quarterly**: Source availability check
- **Annually**: ToS changes verification
- **Ad-hoc**: When source becomes unavailable

---

## 📊 Source Statistics (Planned)

| Category     | Number of Sources | Percentage |
| ------------ | ----------------- | ---------- |
| News (BiH)   | 5                 | 25%        |
| News (HR)    | 5                 | 25%        |
| News (RS)    | 5                 | 25%        |
| Wikipedia    | 3                 | 15%        |
| Institutions | 6                 | 10%        |

**Total**: ~24 active sources for Phase 1

---

## 🔗 Related Documents

- [Methodology](METHODOLOGY.md)
- [Phase 1](PHASE_1.md)
- [README](../README.md)

---

## 📝 Version History

- **v1.0** (2026-01-19) - Initial documentation
- Future versions will be added as sources evolve

---

## ⚠️ Legal Disclaimer

This document provides information about data sources used in the project but **does not constitute legal advice**.

Dataset users are responsible for:

- Complying with local copyright laws
- Verifying licenses before commercial use
- Adhering to original source terms of service

For legal uncertainties, consult a lawyer.
