# Schema & Structured Data Findings: magisk.yssn.tech

## Overview
Inspection and validation of Schema.org JSON-LD structured data implementations across homepage, category hubs, platform filters, and module detail pages.

---

## 1. Implemented Schema Types & Verification

### Homepage (`/`)
1. **WebSite**:
   - Includes `potentialAction` (`SearchAction`) targeting `https://magisk.yssn.tech/?q={search_term_string}`.
   - Verified valid syntax.
2. **FAQPage**:
   - 4 general FAQs covering Magisk module functionality, KernelSU/APatch compatibility, downloads, and installation procedures.
   - Verified valid syntax.
3. **ItemList**:
   - Renders top 10 featured modules with verified trailing-slash URLs (`https://magisk.yssn.tech/modules/magisk/`).

### Module Detail Pages (`/modules/[slug]/`)
1. **SoftwareApplication**:
   - Configured across all 195 module detail pages.
   - Properties: `operatingSystem: "Android"`, `applicationCategory: "UtilitiesApplication"`, `softwareVersion`, `downloadUrl`, `license`, `offers: {price: "0", priceCurrency: "USD"}`, `author`.
   - Verified: All URLs now match canonical trailing slash format.
2. **HowTo**:
   - Provides step-by-step flashing instructions (Download ZIP -> Open Root Manager -> Flash & Reboot).
3. **FAQPage (Dynamic Injection)**:
   - **Resolved Locally**: `src/pages/modules/[slug].astro` now parses `frontmatter.faq` and injects dynamic `FAQPage` JSON-LD schema on all 25 Tier 1 flagship guides.
   - Verified: Exactly 25 module HTML pages in `dist/` contain active `FAQPage` schema.
4. **BreadcrumbList**:
   - Hierarchy: Home (`/`) -> Category (`/categories/[category]/`) -> Module Name (`/modules/[slug]/`).
   - Verified: All breadcrumb items use normalized trailing-slash URLs.

### Category & Compatibility Pages (`/categories/*`, `/compatibility/*`)
1. **CollectionPage**:
   - Declares name, description, category URL, and item count.
2. **BreadcrumbList**:
   - Normalizes category navigation paths.

### Security Policy Page (`/security/`)
1. **WebPage**:
   - Outlines verification process, malware screening, bootloop protection, and safety guidelines.
