---
id: "ios-san-francisco-fonts"
title: "iOS San Francisco Font Suite: Systemless Apple Typography for Android"
sidebarTitle: "iOS SF Fonts"
description: "Systemless font package that integrates Apple's San Francisco Pro and SF Compact typography across Android UI, lockscreens, and applications with calibrated weights and baseline metrics."
category: "system-typography-fonts"
tier: 1
searchQueries:
  - "ios fonts magisk"
  - "san francisco font android"
  - "apple font magisk module"
  - "sf pro font module android 14"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Android 8.0 (Oreo) through Android 14"
conflicts:
  - "Other systemless font replacement modules (Fontloader, Fontcraft, EvilFont)"
configPaths:
  - "/system/fonts/Roboto-Regular.ttf"
  - "/system/etc/fonts.xml"
features:
  - "Systemlessly replaces default Roboto typography with Apple San Francisco Pro (SF Pro)"
  - "Provides full weight coverage from Ultralight (100) to Black (900) and matching italics"
  - "Calibrated font ascent, descent, and line-gap metrics to prevent text truncation in OEM status bars"
  - "Preserves CJK and regional font fallback chains in fonts.xml for multilingual compatibility"
  - "Optimized OpenType/TrueType glyph tables ensuring crisp rendering on high-DPI displays"
faq:
  - question: "Will this font module break lockscreen clocks or OEM custom widgets?"
    answer: "No. The module adheres to Android's standardized font metric specifications, ensuring that status bar clocks, lockscreen digital clocks, and widget headers maintain consistent vertical centering without baseline clipping."
  - question: "Does this module alter system emojis?"
    answer: "No. The iOS San Francisco Font Suite exclusively replaces Latin, numeric, and standard punctuation glyphs. The underlying emoji font (such as NotoColorEmoji or OEM emoji sets) remains completely untouched."
---

## Overview

**iOS San Francisco Font Suite** (packaged and maintained by Chestnut EBQO) delivers Apple's proprietary San Francisco (SF Pro) typography to rooted Android devices through systemless overlay mounting.

In stock Android configurations, Google uses Roboto as the default system font across applications and UI chrome. While functional, many users prefer the geometry, optical sizing, and legibility of Apple's San Francisco typeface. Replacing system fonts via traditional recovery flashing risks bricking font services or corrupting `fonts.xml`. This module implements a safe, modular override that mounts verified SF Pro TrueType assets over `/system/fonts/`.

---

## Technical Architecture & How It Works

Android resolves typographic styles via XML configuration located in `/system/etc/fonts.xml`. The OS defines named families (such as `sans-serif`) mapped to weight ranges:

| Android Font Weight | Mapped File Name | SF Pro Variant |
|---|---|---|
| 100 (Thin) | `Roboto-Thin.ttf` | SF Pro Display Thin |
| 300 (Light) | `Roboto-Light.ttf` | SF Pro Display Light |
| 400 (Regular) | `Roboto-Regular.ttf` | SF Pro Text Regular |
| 500 (Medium) | `Roboto-Medium.ttf` | SF Pro Text Medium |
| 700 (Bold) | `Roboto-Bold.ttf` | SF Pro Text Bold |
| 900 (Black) | `Roboto-Black.ttf` | SF Pro Display Heavy |

### 1. Systemless Magic Mount

During the `post-fs-data` stage, Magisk/KernelSU intercepts directory lookup requests to `/system/fonts/`. Files packaged in the module's `system/fonts/` directory are bound dynamically on top of the physical system partition in memory, leaving the underlying block device completely read-only.

### 2. Metric Normalization

A common failure in generic font ports is mismatched font bounding boxes (`OS/2` table metrics in TrueType files), which leads to vertical text clipping in status bars, truncated descenders (e.g. `g`, `y`, `p`), or misaligned app titles. The font files in this suite have been tuned to match standard Android Roboto line spacing metrics.

---

## Installation & Removal

1. Open your root manager (Magisk Manager, KernelSU Manager, or APatch WebUI).
2. Navigate to Modules and flash the downloaded `.zip` file.
3. Reboot your device to allow the Android font cache daemon (`system_server`) to reload glyph tables.
4. To revert to stock fonts at any time, toggle off or remove the module in your root manager and reboot.
