# Generative Engine Optimization (GEO) Findings: magisk.yssn.tech

## Overview
Analysis of citation readiness, passage structure, entity clarity, and brand presence in AI answer surfaces (Perplexity, ChatGPT Search, Claude, Google AI Overviews).

---

## 1. Entity & Topic Authority
- **Entity Clarity**:
  - The site clearly positions itself around well-defined technical entities: `Magisk`, `KernelSU`, `APatch`, `Zygisk`, `Systemless Root`, `Play Integrity API`, `Hardware-backed Key Attestation`.
  - Brand name "Magisk Hub" is consistently associated with root module discovery.
- **Answer-First Formatting (Flagship Guides)**:
  - The 25 flagship guides (`content/modules/*.md`) utilize answer-first paragraphs immediately explaining:
    1. Exactly what the module does.
    2. Which root solutions are verified compatible.
    3. How the technical mechanism hooks into Android zygote/kernel space.
  - This structure aligns with AI search citation engines that extract standalone factual snippets.

---

## 2. Citability Scores & Information Gain
- **High Citability**:
  - High citation likelihood for technical queries such as *"How does Zygisk-Assistant bypass root detection?"* or *"What is the difference between PlayIntegrityFix and PlayIntegrityFork?"*.
  - Presence of verbatim terminal commands (`sqlite3`, `curl`, `magisk --install-module`) increases answer-engine citation value.
- **Low Citability (Tier 3 modules)**:
  - 120+ pages contain generic content that generative search engines can summarize directly from GitHub metadata without needing to cite the directory.

---

## 3. Recommended Actions
- Add a centralized `/faq/` or `/knowledge-base/` aggregating all 25 guide FAQs into a searchable technical troubleshooting knowledge base.
- Implement structured author bio schemas (e.g. `Organization` or technical curator profiles) to establish publisher entity authority.
