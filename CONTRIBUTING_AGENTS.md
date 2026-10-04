# Magisk Hub — Autonomous Agent Ingestion & Contribution Specification

> **Target Audience**: AI Agents (AGY, Copilot, Cursor, Windsurf, Claude Code) and Autonomous Contributors adding or maintaining modules in Magisk Hub.
> **Scope**: Standard Operating Procedures (SOP) for module ingestion, author verification, ground-truth research, visual design, and schema compliance.

---

## 1. Core Principles & Philosophy

1. **Equal Technical Value**: Every single module receives identical, rigorous technical scrutiny regardless of category, star count, or source origin.
2. **Zero-Hallucination & Ground-Truth Anchoring**: Never generate documentation, configuration paths, or technical claims based on model training assumptions or speculative guesses. Everything must be physically verified against the module's downloaded archive payload.
3. **Authenticity Over Vanity**: Never link random third-party scrapers, re-upload mirrors, or unrelated forks as "source code". If an authentic, original repository does not exist, the source URL must be strictly `null`.
4. **Active Author GitHub Investigation**: Before adding any module discovered on an external distribution platform (Coolapk, Bilibili, forums, `apk.magisk.vip`), always investigate if the original author maintains an official GitHub repository for that module, favoring GitHub as the primary upstream source.

---

## 2. Pre-Ingestion Workflow: Author & Source Investigation

When ingesting candidates from external platforms or candidate lists:

### 2.1 The Author GitHub Investigation Protocol (Mandatory)
Before authoring any metadata JSON or markdown documentation, the agent **MUST** perform an active investigation to determine if the module author maintains an official GitHub repository:

1. **Query Strategy**:
   - Search GitHub for the original author's handle, developer alias, and the module identifier/name.
   - Inspect internal module files (`module.prop`, `README.md`, `update.json`, `updateJson`, and script headers) for repository links or developer contact URLs.
2. **Authenticity Verification**:
   - Confirm that the discovered GitHub repository is genuinely owned and maintained by the original author (verify matching commit history, author username parity, PGP/GPG signatures, release tags, or cross-links from their forum profile).
   - **STRICT PROHIBITION**: Reject third-party mirror scrapers, automated archive re-upload bots, and unrelated personal forks.
3. **Source Priority Resolution**:
   - **Case A: Official GitHub Repository Verified (FAVOR GITHUB)**:
     - Set `sourceType: "github"`.
     - Set `sourceUrl: "https://github.com/<owner>/<repo>"`.
     - Anchor `latestRelease` to the official GitHub release tag and asset download URL.
     - Use the upstream Git repository commit history and documentation as the primary technical ground truth.
   - **Case B: No Official GitHub Repository Found (STRICT COMMUNITY FALLBACK)**:
     - Set `sourceType: "community"`.
     - Set `sourceUrl: null` and `latestRelease.url: null`.
     - Set `latestRelease.downloadUrl` to the verified platform direct download endpoint (e.g. `https://apk.magisk.vip/download.php?id=<id>`).
     - The UI automatically suppresses the source button when `sourceUrl` is `null`.

---

## 3. Ground-Truth Research & Payload Analysis

Every module documentation guide (`content/modules/<slug>.md`) must be backed 100% by physical code inspection of the module payload:

### 3.1 Download & Extraction
- Download the archive directly to a designated scratch directory.
- Extract the complete zip structure and inspect:
  - `module.prop`: Ground-truth `id`, `name`, `version`, `versionCode`, `author`, `description`.
  - Shell scripts: `customize.sh`, `service.sh`, `post-fs-data.sh`, `system.prop`, `uninstall.sh`.
  - Payload directories: `system/`, `vendor/`, `common/`, `META-INF/`.
  - Android APKs: Identify overlays (`vendor/overlay/*.apk`), system apps (`system/app/`), privileged apps (`system/priv-app/`).

### 3.2 Technical Documentation Standards (`content/modules/<slug>.md`)
- **Frontmatter**:
  - `id`: Exact slug matching filename.
  - `title`: Clear English title with functional descriptor.
  - `sidebarTitle`: Concise sidebar title (2–3 words).
  - `description`: Technical single-sentence summary.
  - `category`: Must match an allowed enum value in `modules/schema.json`.
  - `tier`: Set to `1`.
  - `searchQueries`: 4–6 relevant search keywords in English.
  - `prerequisites`: Exact root solutions (Magisk, KernelSU, APatch) and Android version requirements.
  - `conflicts`: Realistic conflicting module classes or system components.
  - `configPaths`: Exact physical paths modified or created by the module on `/system` or `/data/adb/modules/<id>/`.
  - `features`: 4 bullet points derived directly from actual code features.
  - `faq`: 2 technical Q&As addressing operational edge cases, battery impact, or safety mechanics.
- **Body Content**:
  - **Overview**: Author attribution, operational context, and core purpose.
  - **Technical Architecture & How It Works**: Detail the exact files, sysfs nodes, shell commands, and Android subsystems (SurfaceFlinger, Audio HAL, RRO, cgroups, SELinux, PackageManager).
  - **Verification & Operational Commands**: Real bash/ADB commands for checking status on a live device.

---

## 4. Visual Asset Standards (Icons)

Never leave any module with a generic placeholder icon:
- **Location**: Every module must have a bespoke icon saved at:
  - `assets/icons/<slug>.png`
  - `public/assets/icons/<slug>.png`
- **Specifications**:
  - Resolution: Exactly `512x512` pixels.
  - Format: PNG with RGBA transparency.
  - Geometry: Modern squircle base (rounded rectangle with radius ~110px).
  - Design: Aesthetic color gradient with distinct, high-contrast vector/glyph iconography representing the module's core function.

---

## 5. Non-GitHub Community Modules: UI & Standing Rules

To maintain high visual quality and catalog integrity for community modules:
1. **Zero Star Icons in UI**: Never display star ratings (`★ 0` or star counts) in the UI for non-GitHub community modules.
2. **Backend Sorting Standing**: Store platform download metrics (e.g. from `apk.magisk.vip`) in the `stars` field solely to enable search and catalog sorting by popularity.
3. **Visual Distinction**: Community modules display a minimal, refined accent color (indigo badge/border) and an explicit `community` pill.
4. **Source Link Suppression**: When `sourceUrl` is `null`, the UI hides the source code button, showing only the direct download link and technical documentation.

---

## 6. Schema Adherence (`modules/<slug>.json`)

Module definitions must strictly adhere to `modules/schema.json` (Draft-07):
- `id`: String matching filename slug without `.json`.
- `name`: English title.
- `repo`: String (GitHub `owner/repo`) or `null`.
- `author`: String identifying the developer.
- `sourceType`: `"github"` or `"community"`.
- `sourceUrl`: Verified GitHub URL or `null`.
- `category`: Must be one of:
  - `root-management`
  - `performance-kernel`
  - `system-environment`
  - `customization-ui`
  - `development-instrumentation`
  - `system-utilities`
  - `networking-proxies`
  - `security-certificates`
  - `xposed-runtime-hooks`
  - `audio-dsp-acoustics`
  - `system-typography-fonts`
  - `battery-power-charging`
  - `boot-animations-ui`
- `softwareType`: `"flashable-module"`, `"zygisk-module"`, etc.
- `compatibility`: Array of `["Magisk", "KernelSU", "APatch"]`.
- `license`: Valid SPDX license identifier (e.g. `"GPL-3.0-only"`, `"Apache-2.0"`, `"MIT"`, `"Proprietary"`).
- `icon`: `"assets/icons/<slug>.png"`.
- `stars`: Integer (GitHub star count or platform download volume for community modules).
- `contentTier`: `1` (demands corresponding `content/modules/<slug>.md`).
- `latestRelease`:
  - `tag`: Version string (e.g. `"v1.0.0"`).
  - `publishedAt`: ISO 8601 timestamp.
  - `url`: Release page URL or `null`.
  - `downloadUrl`: Direct downloadable `.zip` URL.
  - `assetName`: Standardized archive filename.
- `seo`:
  - `title`: SEO-optimized page title.
  - `description`: 150–160 character meta description.

---

## 7. Verification & Quality Gates

Before committing any batch or changes, execute both quality gates:

1. **Schema Validation**:
   ```bash
   python3 scripts/validate_module.py
   ```
   *Requirement: 100% of modules pass with zero errors.*

2. **Static Compilation**:
   ```bash
   npm run build
   ```
   *Requirement: All static routes, sitemaps, and pages compile with zero errors.*

---

## 8. Execution & Delivery Discipline

- **No Detached / Background Jobs**: Execute all commands synchronously under direct supervision.
- **Commit Format**: Follow Conventional Commits:
  - `feat(community): ingest batch N community modules (#X-#Y)`
- **Delivery Protocol**: Always push changes to `origin/master` and deliver an ingestion report via `SEND_FILE:` accompanied by a concise 1-line-per-item summary in chat.
