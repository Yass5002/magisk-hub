# Contributing to Magisk Hub

Thank you for your interest in contributing to Magisk Hub!

Magisk Hub is an open-source, community-driven catalog of modules for Magisk, KernelSU, and APatch.

## Guidelines for Contributors

- **Adding a Module**:
  - Modules must adhere to the JSON schema defined in `modules/schema.json`.
  - Modules with `contentTier: 1` require a corresponding documentation guide in `content/modules/<slug>.md`.
  - Every module must include a 512x512 PNG icon in `assets/icons/<slug>.png`.

- **Agentic & Automated Contributions**:
  - If you are using an AI agent or automated workflow to contribute, you **MUST** follow the comprehensive specifications in **[CONTRIBUTING_AGENTS.md](./CONTRIBUTING_AGENTS.md)** and **[AGENTS.md](./AGENTS.md)**.
  - Key requirements include: mandatory GitHub author investigation (favoring official GitHub repos), zero hallucination (extracting data directly from downloaded `.zip` payloads), zero star icons in UI for community modules, and strict schema validation.

## Quality Gates

Before submitting a Pull Request, run:
```bash
# Validate JSON schema adherence
python3 scripts/validate_module.py

# Verify static build
npm run build
```
