---
id: "miui-stacked-recent-tasks"
title: "MIUI Stacked Recent Tasks Launcher: iOS Card Overview"
sidebarTitle: "MIUI Stacked Recents"
description: "Transforms the standard MIUI recent tasks overview into an iOS-style horizontal card-stacking deck with fluid physics and instant multitasking."
category: "customization-ui"
tier: 1
searchQueries:
  - "miui stacked recent tasks magisk"
  - "ios recents card deck miui"
  - "xposeded stacked desktop magisk"
  - "miui horizontal recents mod"
prerequisites:
  - "Xiaomi, Redmi, or POCO device running MIUI 12.5, 13, 14, or HyperOS"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other modules that patch launcher smali or recents providers"
configPaths:
  - "/system/priv-app/MiuiHome/MiuiHome.apk"
features:
  - "Enables horizontal overlapping card deck layout in recent tasks"
  - "Replicates fluid iOS spring animation physics when dismissing applications"
  - "Provides clear memory status bar and instant one-tap background clearing"
  - "Maintains full gesture navigation compatibility without gesture stutter"
faq:
  - question: "How does the stacked layout compare to MIUI's stock vertical grid?"
    answer: "MIUI default recents use a 2-column vertical grid. The stacked layout presents large, single-app previews that overlap horizontally, allowing easier one-handed browsing and clearer window previews."
  - question: "What should I do if the screen goes black upon reboot?"
    answer: "If you encounter an incompatible launcher conflict, enter custom recovery (TWRP/OrangeFox) or use Magisk safe mode to remove the module directory from /data/adb/modules/ppp."
---

## Overview

**MIUI Stacked Recent Tasks Launcher** (engineered by Xposeded and packaged for Magisk by Nanju Beizhi / 酷安:南橘北彘) is a specialized user interface modification that replaces Xiaomi's vertical 2-column task switcher with a horizontal, overlapping stacked card deck inspired by iOS multitasking.

For users accustomed to horizontal task switching or who find small dual-column previews difficult to read, this module reprograms the layout manager inside `MiuiHome.apk`, providing large, detailed app windows with smooth gesture inertia.

---

## Technical Architecture & How It Works

Task switching in MIUI is handled directly within the launcher package:

### 1. Layout Manager Replacement

The module overrides the default `RecentsView` implementation:

- Injects custom horizontal layout calculations that dynamically offset each background task card along the Z-axis.
- Applies scale factors (e.g. 0.9x to 0.7x) to background cards as they move away from the active center focus.

### 2. Gesture Transition Physics

Touch gesture curves are retuned to match the spring dynamics of stacked cards:

- Upward swipe flick: Dismisses the focused application with inertia.
- Downward swipe: Locks the application in memory to prevent automated cleanup.
- Horizontal scrub: Cycles rapidly across the deck without dropping frames.

---

## Troubleshooting & Verification

- **Changing Layout Options**: Open **Settings > Home screen > Arrange items in Recents** and verify that the layout switcher is set to **Horizontally**.
- **Lag or Frame Drops**: Ensure that your device has at least 3GB of free RAM; heavily cluttered background states can cause frame dips on older processors.
