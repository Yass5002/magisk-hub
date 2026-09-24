# Action Plan: magisk.yssn.tech SEO Roadmap

Prioritized recommendations for `https://magisk.yssn.tech` categorized by urgency and impact.

---

## Priority Legend
- **Critical**: Blocks indexing, causes social/rendering failures, or invalidates search specifications.
- **High**: Directly impacts search ranking eligibility, rich snippet features, or mobile performance.
- **Medium**: Optimization opportunities for crawl efficiency, security posture, and editorial authority.
- **Low**: Polish, hygiene, and incremental enhancements.

---

## Phase 1: Completed & Verified Fixes (Ready for Production Deployment)

The following fixes have been fully coded in the working tree, tested, and verified across all 209 built HTML documents in `dist/`:

| Item | Priority | File(s) | Status | Verification Result |
|------|----------|---------|--------|---------------------|
| **1. Twitter Card Syntax** | Critical | `src/layouts/BaseLayout.astro` | ✅ Complete | Verified 0 occurrences of `property="twitter:"`. All Twitter tags use `name="twitter:*"`. |
| **2. Dynamic FAQPage Schema** | High | `src/pages/modules/[slug].astro` | ✅ Complete | Verified all 25 flagship module guides in `dist/` contain valid `FAQPage` JSON-LD schema. |
| **3. Trailing Slash Normalization** | High | `src/pages/modules/[slug].astro`, `src/pages/index.astro`, `src/components/Breadcrumbs.astro` | ✅ Complete | Verified 0 internal non-trailing slash links across all 209 pages. All Schema.org URLs match canonical paths. |
| **4. AI Endpoints (`llms.txt`)** | High | `public/llms.txt`, `public/llms-full.txt` | ✅ Complete | Both files generated and built into `dist/`. Configured with `Content-Type: text/plain` in `vercel.json`. |
| **5. HTTP Security Headers** | High | `vercel.json` | ✅ Complete | Defined `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and `Referrer-Policy`. |
| **6. Icon Asset Optimization** | High | `assets/icons/`, `scripts/optimize_icons.py` | ✅ Complete | Rescaled icons to max 128px bounding box. Directory shrunk by 91.2% (4.88 MB -> 428 KB). |
| **7. Security & Safety Policy** | Medium | `src/pages/security.astro` | ✅ Complete | Published at `/security/` with WebPage schema and comprehensive verification disclosures. |
| **8. Image Alt Attribute Hygiene** | Medium | `src/pages/modules/[slug].astro` | ✅ Complete | Sitewide audit verified 0 image tags missing `alt` attributes across all 209 output pages. |

---

## Phase 2: Immediate Production Deployment (Next Step)

To promote the staged optimizations from local build to the live domain:

1. **Review Git Status & Commit**:
   ```bash
   git add -A
   git commit -m "feat(seo): deploy twitter meta fixes, dynamic FAQ schema, security policy, and asset optimizations"
   git push origin master
   ```
2. **Post-Deployment Smoke Test**:
   - `curl -I https://magisk.yssn.tech/llms.txt` (verify HTTP 200)
   - `curl -I https://magisk.yssn.tech/security/` (verify HTTP 200)
   - Inspect live headers to confirm `X-Content-Type-Options: nosniff` is delivered by Vercel edge.

---

## Phase 3: Future Architectural & Content Enhancements (Month 2)

| Initiative | Priority | Description | Expected Impact |
|------------|----------|-------------|-----------------|
| **Homepage DOM Windowing** | Medium | Currently, all 196 module cards are rendered into a single 758 KB HTML document. Pre-render the top 24-36 cards in initial HTML and hydrate remaining cards progressively. | Reduces initial HTML weight by ~70%, speeding up First Contentful Paint on mobile. |
| **Self-Hosted Web Fonts** | Medium | Bundle `@fontsource/inter` and `@fontsource/jetbrains-mono` at build time instead of requesting `fonts.googleapis.com`. | Eliminates external render-blocking network requests and speeds up LCP. |
| **Tier 1 Guide Expansion** | Medium | Handcraft technical documentation for the next 25 most popular modules in `content/modules/`. | Elevates thin stubs into high-information-gain pages with unique FAQs and rich snippets. |
| **Sitemap `<lastmod>` Attributes** | Low | Inject upstream release timestamps (`publishedAt`) as `<lastmod>` in `sitemap-0.xml`. | Optimizes Googlebot crawl frequency for recently updated packages. |

---

## Phase 4: Ongoing Monitoring & Iteration

- **Search Console Rich Results**: Monitor Search Console impressions for `SoftwareApplication` and `FAQPage` rich results once Google recrawls the updated sitemap.
- **Drift Monitoring**: Run periodic drift checks via `claude-seo run drift_history.py https://magisk.yssn.tech/` to catch regressions after automated release synchronizations.
- **AI Citation Auditing**: Query Perplexity and ChatGPT Search on core Android root queries to monitor Magisk Hub citations.
