---
id: "tsukushi-a-round-ultra-bold-font"
title: "Tsukushi A Round Ultra Bold 5-Weight Typography Suite"
sidebarTitle: "Tsukushi Ultra Bold"
description: "Heavyweight Japanese Tsukushi A Round Gothic typography engine adapted with national standard GB simplified Chinese glyphs across 5 extra-bold optical weights."
category: "system-typography-fonts"
tier: 1
searchQueries:
  - "tsukushi round ultra bold font magisk"
  - "tsukushi heavy 5 weights magisk"
  - "thick rounded gothic font android root"
  - "lxgw tsukushi font module"
prerequisites:
  - "Android 9 through Android 15"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other global font replacement modules"
configPaths:
  - "/system/etc/fonts.xml"
  - "/system/fonts/Roboto-Bold.ttf"
  - "/system/fonts/Roboto-Black.ttf"
features:
  - "Engineered for high-density reading with substantial stroke weight and high contrast"
  - "Features 5 distinct bold typographic weights (Medium, Semi-Bold, Bold, Extra-Bold, Heavy)"
  - "Full national standard GB2312 and GB18030 simplified Chinese character harmonizations"
  - "Systemless font configuration preserving system partition integrity"
faq:
  - question: "How does this differ from the standard Tsukushi A Round Gothic module?"
    answer: "While the standard Tsukushi module focuses on lighter body text and 85% compact scale, this Ultra Bold edition provides heavy, high-contrast stroke weights specifically for users who prefer bold, prominent text across all apps."
  - question: "Will bold fonts clip in status bars or small buttons?"
    answer: "No. The baseline metrics and em-square heights have been normalized to match Android Roboto standards, preventing baseline clipping in status bars and text fields."
---

## Overview

**Tsukushi A Round Ultra Bold 5-Weight Typography Suite** (authored by beixin, based on upstream type engineering by lxgw) brings heavy, expressive rounded typography to rooted Android devices.

Standard mobile typefaces can appear thin and hard to distinguish outdoors or under direct sunlight. This module replaces standard system fonts with weighted variations of Tsukushi A Round Gothic, calibrated across 5 bold weight steps to ensure high-contrast readability, strong visual presence, and rounded, friendly terminal geometry.

---

## Technical Architecture & How It Works

The typography stack maps into `/system/etc/fonts.xml`:

### 1. Multi-Weight Font Aliasing

The module maps 5 distinct weights to the Android system typography hierarchy:

```xml
<family name="sans-serif">
    <font weight="400" style="normal">Tsukushi-Medium.ttf</font>
    <font weight="500" style="normal">Tsukushi-SemiBold.ttf</font>
    <font weight="700" style="normal">Tsukushi-Bold.ttf</font>
    <font weight="800" style="normal">Tsukushi-ExtraBold.ttf</font>
    <font weight="900" style="normal">Tsukushi-Heavy.ttf</font>
</family>
```

### 2. Glyph Harmonization

Japanese typefaces commonly include variant kanji forms (Shinjitai) that differ from mainland simplified Chinese (Hanzi). This suite incorporates font glyph substitutions from the open-source LXGW project, ensuring that CJK unified ideographs render with correct stroke counts and regional orthography.

---

## Troubleshooting & Verification

- **Refreshing Font Caches**: After flashing, perform a clean reboot. If specific third-party applications (like Chrome) retain old fonts, clear their application cache.
- **Uninstalling**: Simply toggle the module off in Magisk/KernelSU and reboot to return to system default fonts.
