# Performance & Core Web Vitals (CWV) Findings: magisk.yssn.tech

## Overview
Analysis of page loading performance, Core Web Vitals risks (LCP, INP, CLS), asset optimization, document payload weight, and network bottlenecks across the live site and local build.

---

## 1. Document Payload Weight (Homepage HTML)
- **Measured Transfer Weight**:
  - Raw HTML Document: **758 KB (775,990 bytes)**.
  - Gzip transfer: ~120 KB.
- **Root Cause**:
  - The homepage renders all 196 module cards directly into static HTML markup to support client-side instant search and filtering without external network fetches.
  - Generates 205 headings, 227 links, 198 image elements, and several thousand DOM nodes.
- **CWV Impact**:
  - **LCP & FCP**: Increases HTML parsing duration and main-thread DOM tree construction on low-end mobile devices.
  - **Memory & INP**: High DOM node count can introduce micro-stutter during live search keystroke events on constrained hardware.
- **Ongoing Optimization Recommendation**:
  - In a future phase, evaluate progressive client-side windowing or rendering the top 24-36 featured modules in initial static HTML while hydrating the remaining catalog on idle.

---

## 2. Image Optimization & Asset Footprint
- **Local Resolution**:
  - Ran `scripts/optimize_icons.py` with Pillow using Lanczos resampling.
  - Downscaled all raster icons exceeding 128x128px to a maximum 128px bounding box.
  - **Results**:
    - Entire `assets/icons/` directory shrunk from **4.88 MB to 428 KB (91.2% total reduction)**.
    - `assets/icons/czero.png`: Shrunk from 1.61 MB to 11.1 KB (99.3% reduction).
    - `assets/icons/device-faker.png`: Shrunk from 1.41 MB to 16.2 KB (98.9% reduction).
    - `assets/icons/playintegrityfix.png`: Shrunk from 2477px / 406 KB to 128px / 40.6 KB.
  - **Alt Text Hygiene**:
    - Audit verified 0 image tags missing `alt` attributes across all 209 output HTML documents.

---

## 3. Font Loading & External Resources
- **Font Delivery**:
  - Fonts loaded from `fonts.googleapis.com` with `preconnect` hints for `fonts.googleapis.com` and `fonts.gstatic.com`.
  - While preconnect mitigates handshake latency, external CSS remains an external render-blocking dependency.
  - Recommendation: Self-host fonts locally via `@fontsource/inter` and `@fontsource/jetbrains-mono` in a subsequent enhancement.

---

## 4. Cumulative Layout Shift (CLS)
- **Status**: Pass
- Image elements explicitly include width and height attributes (`width="64" height="64"`, `width="44" height="44"`, `width="24" height="24"`).
- Zero layout shift observed during initial viewport render.
