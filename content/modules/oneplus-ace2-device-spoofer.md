---
id: "oneplus-ace2-device-spoofer"
title: "OnePlus Ace 2 Device Identity Spoofer: Gaming Frame Rate Unlocker"
sidebarTitle: "OnePlus Ace 2 Spoof"
description: "Systemless build property injection module that spoofs device identity to OnePlus Ace 2 (PHK110) to unlock 90FPS and 120FPS options in competitive mobile games."
category: "system-environment"
tier: 1
searchQueries:
  - "oneplus ace 2 device spoofer magisk"
  - "unlock 120 fps peace elite root"
  - "spoof phk110 build prop"
  - "oneplus 120hz game unlock magisk"
prerequisites:
  - "Magisk 16.0+, KernelSU, or APatch"
  - "Android 8.0 through Android 14"
conflicts:
  - "Other monolithic device model spoofing modules"
configPaths:
  - "/data/adb/modules/ONEPLUSACE2/common/system.prop"
features:
  - "Injects authentic OnePlus manufacturer and brand property definitions"
  - "Spoofs hardware model string to PHK110 (OnePlus Ace 2)"
  - "Unlocks 90 FPS and 120 FPS high frame rate tiers in Peace Elite, PUBG, and Genshin Impact"
  - "Pure systemless build property injection without APK tampering"
faq:
  - question: "Does this module change my system language or UI?"
    answer: "No. The module only modifies device identification strings checked by game servers to determine supported graphics tiers. Your operating system UI and language remain unaffected."
---

## Overview

**OnePlus Ace 2 Device Identity Spoofer** (authored by You Xi Li Jie 6) allows mobile gamers to access ultra-high frame rate modes (90 FPS / 120 FPS) that game publishers restrict to specific promotional partner hardware.

---

## Technical Architecture & How It Works

The module supplies `/common/system.prop` containing key identification overrides:

```properties
ro.product.manufacturer=ONEPLUA
ro.product.brand=ONEPLUS
ro.product.model=PHK110
```

When games query `android.os.Build.MODEL` and `Build.BRAND`, the runtime returns the OnePlus Ace 2 hardware profile.
