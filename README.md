# Magisk Hub

<div align="center">
  <h3>The Verified Directory of Active Magisk, KernelSU, and APatch Modules</h3>
  <p>Continuous 6-hour automated release audits • Zero dead projects • Real technical documentation</p>
  
  [![Validate Modules](https://github.com/Yass5002/magisk-hub/actions/workflows/validate-modules.yml/badge.svg)](https://github.com/Yass5002/magisk-hub/actions/workflows/validate-modules.yml)
  [![Sync Releases](https://github.com/Yass5002/magisk-hub/actions/workflows/sync-releases.yml/badge.svg)](https://github.com/Yass5002/magisk-hub/actions/workflows/sync-releases.yml)
  [![Schema](https://img.shields.io/badge/Schema-Draft--07-blue.svg)](modules/schema.json)
  [![License](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
</div>

---

## What is Magisk Hub?

**Magisk Hub** is an open-source, automated single source of truth for modern Android root modules. Unlike traditional module repositories that accumulate abandoned, broken, and unmaintained repositories from years past, Magisk Hub enforces a strict **active-development bar**:

- **Continuous Re-Audits**: A scheduled GitHub Action runs every 6 hours to query the GitHub GraphQL API for all listed repositories.
- **Strict Active Bar**: If a repository is archived, stale (>548 days without a push), deleted/404, or lacks downloadable `.zip`/`.apk` assets on its latest release, it is **hard-deleted** from the database.
- **Link-Rot Elimination**: All module icons are locally resolved and cached in `assets/icons/` to prevent broken image CDNs.
- **Grounded Content Tiers**: High-volume, foundational root modules feature hand-crafted in-depth technical guides covering architecture, configuration files (`/data/adb/...`), conflicts, and recovery steps.

---

## Content Tier Architecture

To maintain scale across hundreds of modules without algorithmic fluff or database bloat, Magisk Hub separates machine metadata from editorial documentation:

| Tier | Coverage | Storage | Description |
| :--- | :--- | :--- | :--- |
| **Tier 1** | ~25 Foundational Modules | `content/modules/<id>.md` | Full technical deep-dives: low-level mechanics (Zygisk, overlayfs, kernel hooks), prerequisites, conflicts, config paths, and FAQs. |
| **Tier 2** | Star Count $\ge 200$ | Grounded Assembly | Assembled dynamically from verified machine JSON data: direct release assets, category role, and installation guides. |
| **Tier 3** | Single-Purpose Utilities | Grounded Assembly | Clean data-only card and direct download link. Zero fake content. |

---

## Locked Ecosystem Categories

Every module is strictly categorized into one of 8 locked categories:

1. **`root-management`**: Core su daemons, Zygisk runtimes, root cloaking, and attestation bypass tools.
2. **`performance-kernel`**: CPU/GPU governor tuners, thermal throttle controls, and game performance modules.
3. **`system-environment`**: Systemless framework tweaks, OEM feature restoration, and OS-level modifications.
4. **`customization-ui`**: Status bar, gesture, navigation, launcher, and appearance customizations.
5. **`development-instrumentation`**: Dynamic hooking frameworks, Frida servers, debugging, and reverse engineering tools.
6. **`system-utilities`**: Audio DSP engines, call recorders, automated cleanup, and terminal power tools.
7. **`networking-proxies`**: Systemless adblockers, transparent TPROXY gateways, and privacy DNS redirectors.
8. **`security-certificates`**: CA certificate trust injectors, device identifier spoofing, and privacy guards.

---

## Local Development & Contribution

### Prerequisites
- Node.js 20+ and npm
- Python 3.10+
- `pip install -r scripts/requirements.txt`

### Commands

```bash
# Install dependencies
npm install
pip install -r scripts/requirements.txt

# Run module schema validation
npm run validate

# Start local Astro development server
npm run dev

# Build production static website (outputs to dist/)
npm run build

# Preview production build
npm run preview
```

---

## Submitting a New Module

Community contributions are welcome! To add an active module:

1. Create `modules/<your-module-slug>.json` conforming to `modules/schema.json`:
   ```json
   {
     "id": "your-module-slug",
     "name": "Your Module Name",
     "repo": "owner/repo",
     "category": "system-utilities",
     "description": "Clear 1-sentence explanation of what it does.",
     "compatibility": ["Magisk", "KernelSU"],
     "license": "GPL-3.0-only",
     "icon": null,
     "latestRelease": {
       "tag": "v1.0.0",
       "publishedAt": "2026-01-01T00:00:00Z",
       "url": "https://github.com/owner/repo/releases/tag/v1.0.0",
       "downloadUrl": "https://github.com/owner/repo/releases/download/v1.0.0/module.zip",
       "assetName": "module.zip"
     },
     "seo": {
       "title": "Your Module Name - Active Magisk Module",
       "description": "Clear meta description for search engines."
     }
   }
   ```
2. Run `npm run validate` to ensure your JSON conforms to Draft-07 schema and naming conventions.
3. Open a Pull Request. CI will automatically validate your module and build the preview site.

---

## License & Disclaimer

- Code and documentation are licensed under the [MIT License](LICENSE).
- **Disclaimer**: Magisk Hub is an independent community project. Android is a trademark of Google LLC. Magisk is developed by John Wu. This project is not affiliated with or endorsed by Google or device manufacturers.
