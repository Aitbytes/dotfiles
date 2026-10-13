---
name: source-quality
description: Source quality evaluation framework — tier hierarchy (1-5), CRAAP-style criteria, red flags, and cross-referencing techniques for rigorous research
---

## Source Quality Tier Hierarchy

Prioritize sources in this order when gathering evidence:

### Tier 1 — Highest Quality

- Peer-reviewed journals (Nature, Science, NEJM, JAMA)
- Systematic reviews & meta-analyses (Cochrane, Campbell)
- Government & regulatory bodies (WHO, CDC, FDA, SEC, central banks)
- Academic institutions (Harvard, MIT, Stanford, Oxford) research papers
- Court opinions & legal precedents

### Tier 2 — High Quality

- Established news with editorial standards (NYT, WSJ, Guardian, Economist, BBC)
- Industry standards bodies (IEEE, ISO, W3C, IETF)
- Professional associations (AMA, ABA, IEEE, ACM)
- Think tanks with methodological rigor (Brookings, RAND, NBER)

### Tier 3 — Moderate Quality

- Specialized news outlets (TechCrunch, STAT, FierceHealthcare, Law360)
- Expert blogs & Substacks with clear author credentials and citations
- Company documentation (official docs, white papers with methodology)
- Conference proceedings with peer review

### Tier 4 — Use with Caution

- General news sites (MSN, Yahoo, HuffPost — variable quality)
- Wikipedia (good for overviews; verify with primary sources)
- Reddit/Quora (anecdotal evidence; always verify)
- Social media (generally unreliable, even from experts)

### Tier 5 — Red Flags

- Anonymous sources without verification
- Sponsored content not clearly labeled
- Clickbait headlines or sensationalist language
- Sites with obvious bias and no counterpoint
- Sites selling products related to their claims

---

## Source Evaluation Criteria (CRAAP-style)

For every source, ask:

### 1. Authority & Expertise

- Who is the author? What are their credentials?
- What institution are they affiliated with?
- Do they have relevant expertise and a track record on this topic?

### 2. Purpose & Incentives

- Why was this created? Educational, commercial, political?
- Who funded this research? Does the author have conflicts of interest?
- Is this advertising in disguise?

### 3. Methodology & Evidence

- What evidence is presented? Is the methodology sound?
- Are there citations? Can you verify the claims elsewhere?
- Are limitations acknowledged?

### 4. Currency & Context

- When was this published? Has the information changed since?
- Are there more recent developments that supersede this?

### 5. Objectivity & Balance

- Is the language neutral or emotional?
- Are alternative viewpoints presented?
- Does it acknowledge uncertainty? Is there evidence of cherry-picking?

---

## Cross-Referencing Techniques

### Finding Contradictions

```
google-search_search: "[topic] criticism"
google-search_search: "[topic] limitations"
google-search_search: "[topic] controversy"
```

### Finding Supporting Evidence

```
google-search_search: "[topic] systematic review"
google-search_search: "[topic] meta-analysis"
google-search_search: "[topic] research study"
```

### Finding Expert Consensus

```
google-search_search: "[topic] expert consensus"
google-search_search: "[topic] clinical guidelines"
google-search_search: "[topic] position statement"
```

### Independent Confirmation Rule

For critical claims: require 3+ independent sources before treating a claim as High confidence.
Never upgrade a finding's confidence beyond what the sources support. If only Tier 3–4 sources confirm a claim, it stays at Medium confidence regardless of how many agree.

---

## Red Flags to Watch For

### In Sources

- Claims that seem too good to be true
- Absolute language ("always", "never", "proven")
- No citations or evidence provided
- Heavy emotional language / only one side presented
- Clear product promotion

### In Search Results

- All results from same domain
- Results that all cite each other (echo chamber)
- No independent verification
- Outdated information
- Results authored by non-experts

---

## Domain-Specific Source Targets

| Domain            | Primary Sources                                          | Search Operators                                               |
| ----------------- | -------------------------------------------------------- | -------------------------------------------------------------- |
| Health/Medical    | PubMed, Cochrane, CDC, WHO, FDA, JAMA, NEJM, BMJ         | `site:nih.gov OR site:who.int OR site:pubmed.ncbi.nlm.nih.gov` |
| Finance/Economics | SEC filings, Federal Reserve, IMF, World Bank, NBER      | `site:sec.gov OR site:federalreserve.gov OR site:imf.org`      |
| Scientific Papers | Google Scholar, arXiv, PubMed, IEEE Xplore, JSTOR        | `site:scholar.google.com OR site:arxiv.org`                    |
| Legal/Regulatory  | Court websites, government portals, official regulations | `site:courtlistener.com OR site:gov`                           |
| Technical         | Official docs, RFCs, IEEE, ACM                           | `site:docs OR site:ietf.org OR site:stackoverflow.com`         |

---

## Handling Disinformation

When you detect potentially false or misleading information:

1. Do not repeat the false claim as if it is fact
2. Present what credible sources say instead
3. Note the discrepancy clearly
4. Suggest verification with authoritative sources
5. Be direct: "This claim is not supported by credible evidence"

Example framing: "The claim that [X] causes [Y] is widely circulated, but I could not find any peer-reviewed research supporting this. In fact, [credible source] found [opposite finding]."
