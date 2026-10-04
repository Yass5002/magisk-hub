# Agent Operating Instructions — Magisk Hub Repository

Welcome, Agent. You are operating in the **Magisk Hub** (`Yass5002/magisk-hub`) codebase — a modern, open-source catalog for Magisk, KernelSU, and APatch root modules built with Astro and Tailwind CSS.

Whenever you add, modify, or audit modules in this repository, you **MUST** strictly follow the guidelines detailed in [CONTRIBUTING_AGENTS.md](./CONTRIBUTING_AGENTS.md) and the standing rules below.

---

## 1. Mandatory Ingestion Rules (Quick Reference)

### 1.1 Pre-Ingestion Author GitHub Investigation
Before adding any module from an external distribution platform (e.g. `apk.magisk.vip`, Coolapk, Bilibili, developer forums):
- **Search GitHub**: Actively search for the author's official handle and module name.
- **Favor GitHub**: If the original author maintains an authentic official GitHub repository, set `sourceType: "github"`, link `sourceUrl`, and use GitHub release downloads.
- **Fallback to Community**: If no official GitHub repo exists, set `sourceType: "community"` and set `sourceUrl: null`. Never link third-party scrapers or mirror repositories.

### 1.2 Zero-Hallucination Ground Truth
- Do NOT guess or extrapolate module mechanics from model training knowledge.
- Download the real `.zip` payload to a scratch directory.
- Inspect `module.prop`, `customize.sh`, `service.sh`, `system/`, and APK manifests to extract real technical parameters, paths, and behaviors for `content/modules/<slug>.md`.

### 1.3 Bespoke Visual Assets
- Every module must have a bespoke 512x512 PNG icon in `assets/icons/<slug>.png` and `public/assets/icons/<slug>.png`.
- Zero generic placeholder icons are permitted.

### 1.4 Non-GitHub Community Modules: UI Rules
- Zero stars in UI (stars field is used purely for backend sorting).
- Community badge / pill rendered.
- When `sourceUrl` is `null`, source button is suppressed.

### 1.5 Quality Gates
Always verify before committing:
1. `python3 scripts/validate_module.py` (Must pass 100% of modules with 0 errors).
2. `npm run build` (Must compile all static routes and sitemaps with 0 errors).

---

## 2. Detailed Specification

For the complete technical specification, schema details, and authoring guidelines, consult:
👉 **[CONTRIBUTING_AGENTS.md](./CONTRIBUTING_AGENTS.md)**
