# Magisk Hub

<div align="center">
  <h3>An active-source directory for Magisk, KernelSU, and APatch modules</h3>
  <p>Release metadata refreshed every 6 hours, with source-backed documentation for selected modules</p>

  [![Validate Modules](https://github.com/Yass5002/magisk-hub/actions/workflows/validate-modules.yml/badge.svg)](https://github.com/Yass5002/magisk-hub/actions/workflows/validate-modules.yml)
  [![Sync Releases](https://github.com/Yass5002/magisk-hub/actions/workflows/sync-releases.yml/badge.svg)](https://github.com/Yass5002/magisk-hub/actions/workflows/sync-releases.yml)
  [![Schema](https://img.shields.io/badge/Schema-Draft--07-blue.svg)](modules/schema.json)
  [![License](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
</div>

Magisk Hub is a static directory of Android root modules. It indexes module metadata from upstream GitHub repositories and links directly to their release pages and downloadable assets.

Live site: https://magisk.yssn.tech

## What the automation checks

The scheduled release sync runs every 6 hours. For each configured upstream repository, it checks:

- The repository can be reached and is not archived.
- Recent push activity meets the configured freshness window.
- A latest GitHub release is available.
- The release contains a downloadable ZIP asset, or an APK where the module record explicitly supports it.
- The release asset URL is reachable.
- Repository metadata and the module record can be normalized into the local schema.

These checks describe repository and release availability. They do not prove that a module is safe, bug-free, compatible with every device, or independently security-audited. Every module remains a third-party project, and root modules can cause boot loops, data loss, instability, or other device problems. Read the upstream documentation, keep a recovery path, and make a backup before installation.

Modules can be removed automatically when they no longer satisfy the configured freshness, repository, release, or asset checks. A removal is a directory maintenance decision, not a safety verdict.

## Documentation tiers

The directory separates machine-readable metadata from editorial documentation:

| Tier | Coverage | Storage | Description |
| :--- | :--- | :--- | :--- |
| **Tier 1** | Selected foundational modules | `content/modules/<id>.md` | Source-backed guides with prerequisites, configuration, limitations, recovery notes, and FAQs. |
| **Tier 2** | Higher-interest modules | Module JSON plus generated page sections | Build-time page content derived from available module metadata and release information. |
| **Tier 3** | Single-purpose utilities | Module JSON | A concise data card with upstream links and a direct release asset. |

Tier 2 content is assembled at build time for the static site. It is not fetched dynamically by visitors.

## Categories

Every module uses one of these eight categories:

1. **`root-management`**: Root managers, Zygisk runtimes, and root-related tools.
2. **`performance-kernel`**: CPU, GPU, thermal, governor, and gaming performance tools.
3. **`system-environment`**: Systemless framework tweaks and operating-system changes.
4. **`customization-ui`**: Status bar, gestures, launchers, navigation, and appearance.
5. **`development-instrumentation`**: Hooking, Frida, debugging, and reverse-engineering tools.
6. **`system-utilities`**: Audio, cleanup, call recording, backup, and terminal utilities.
7. **`networking-proxies`**: Ad blockers, proxy gateways, DNS tools, and network clients.
8. **`security-certificates`**: Certificate, device-identity, and privacy-related tools.

## Repository layout

- `modules/`: normalized module records and the JSON schema.
- `content/modules/`: optional Tier 1 Markdown guides.
- `assets/icons/`: cached local module icons.
- `public/assets/`: generated static copies of asset files. Do not edit directly.
- `scripts/`: validation and release synchronization tooling.
- `src/`: Astro pages and components.
- `dist/`: generated production output. It is ignored by Git.

## Local development

### Requirements

- Node.js `>=22.12.0`
- npm `>=9.6.5`
- Python 3.10+

Install Python dependencies with:

```bash
pip install -r scripts/requirements.txt
```

Install Node dependencies and run the checks:

```bash
npm install
npm run validate
npm run build
```

Start a local development server:

```bash
npm run dev
```

Preview the production output:

```bash
npm run preview
```

## Contributing a module

Magisk Hub uses upstream repositories as its source of release metadata. Alt Repo and other catalogs may help discover candidates, but a contribution must be verified against the original upstream repository.

1. Add `modules/<module-id>.json` using the format in `modules/schema.json`.
2. Use a unique lowercase kebab-case `id` that matches the filename.
3. Link the original upstream repository and a direct release asset.
4. Use only a category from the locked list above.
5. Use `icon: null` when no local icon is available.
6. Add `content/modules/<module-id>.md` only when the guide is grounded in upstream documentation or directly inspected source.
7. Run `npm run validate` and `npm run build`.
8. Open a pull request with the upstream repository, release tag, asset name, and verification notes.

The scheduled sync may update release metadata or prune a module after it is merged. The workflow commits those generated changes to `master`. A pull request that overlaps generated records may need to be rebased after the workflow runs.

If a module is pruned, re-add it by updating the original module record with current upstream evidence and submitting a new pull request. Do not restore a stale generated record without checking the upstream repository and release again.

## License and scope

The code and documentation in this repository are licensed under the [MIT License](LICENSE).

Magisk Hub is an independent community directory. It is not affiliated with Google, Magisk, KernelSU, APatch, device manufacturers, or the developers of the listed modules. Product names and trademarks belong to their respective owners.
