---
id: "tsukushi-a-round-gothic-font"
title: "Tsukushi A Round Gothic Typography Suite: Balanced 85% Scale"
sidebarTitle: "Tsukushi Round"
description: "High-elegance rounded Japanese gothic typography engine ported systemlessly to Android, adapted with mainland simplified Chinese characters and calibrated 85% compact optical scaling."
category: "system-typography-fonts"
tier: 1
searchQueries:
  - "tsukushi round gothic magisk font"
  - "tsukushi a round mainland font magisk"
  - "japanese rounded gothic android font"
  - "tsukushi small font magisk"
prerequisites:
  - "Android 8 through Android 15"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other global font replacement modules"
configPaths:
  - "/system/etc/fonts.xml"
  - "/system/etc/fonts_base.xml"
  - "/system/fonts/Roboto-Regular.ttf"
features:
  - "Port of the iconic Tsukushi Round Gothic design with organic terminal curves"
  - "Incorporates mainland simplified Chinese glyph corrections to avoid Japanese variant misrenderings"
  - "Calibrated 85% optical scale creates a refined, high-information-density UI layout"
  - "Systemlessly replaces default system typography without touching the read-only system image"
faq:
  - question: "What does the 85% scaling mean for my device?"
    answer: "Standard Android fonts can look oversized on modern high-resolution displays. The 85% optical scale renders characters slightly smaller and more tightly spaced, increasing screen information density while maintaining legibility."
  - question: "Does this font cause missing character boxes (tofu) in messaging apps?"
    answer: "No. The module bundles comprehensive fallback font definitions, ensuring standard emoji, symbols, and less common Unicode characters fall back cleanly to system defaults."
---

## Overview

**Tsukushi A Round Gothic Typography Suite** (packaged by Xin Yu) is a systemless typography module bringing the aesthetic craftsmanship of Tsukushi Round Gothic to Android.

Renowned for its gentle, rounded stroke terminations and balanced counters, Tsukushi Round Gothic offers a warm yet sophisticated visual hierarchy. This edition specifically resolves common issues encountered when porting Japanese typefaces to Chinese Android environments by replacing conflicting kanji forms with standard mainland simplified glyphs, while applying an optical 85% scale for crisp UI balance.

---

## Technical Architecture & How It Works

Android renders UI typography through the FreeType engine configured by `/system/etc/fonts.xml`:

### 1. Typography Re-aliasing

The module maps Tsukushi Round Gothic font binaries into `/system/fonts/` and aliases standard system font weights:

- `Roboto-Regular.ttf` -> Tsukushi Round Regular
- `Roboto-Medium.ttf` -> Tsukushi Round Medium
- `Roboto-Bold.ttf` -> Tsukushi Round Bold

### 2. Optical Scaling Optimization

Rather than relying purely on user-level display density (DPI) adjustments, which can distort application layouts and web views, the font binaries themselves are engineered with calibrated em-square metrics at 85% baseline height. This preserves application layout geometry while presenting refined, compact typography.

---

## Troubleshooting & Verification

- **SystemUI Font Refresh**: A system reboot is mandatory after flashing for the Android zygote and font caches to rebuild.
- **Third-Party Keyboards**: Certain keyboards (e.g. Gboard) use their own embedded font rendering; if keyboard keys do not change immediately, restart the keyboard process.
