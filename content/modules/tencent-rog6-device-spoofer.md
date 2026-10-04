---
id: "tencent-rog6-device-spoofer"
title: "Tencent ROG Phone 6 Dimensity Edition Device Spoofer: 165Hz/120Hz Mod"
sidebarTitle: "ROG Phone 6 Spoof"
description: "Systemless hardware identity spoofer configuring ASUS ROG Phone 6 Dimensity Supreme Edition properties (ASUS_AI2203_B) to bypass game graphics caps."
category: "system-environment"
tier: 1
searchQueries:
  - "rog phone 6 device spoofer magisk"
  - "asus_ai2203_b build prop root"
  - "unlock max graphics rog magisk"
  - "tencent rog phone model spoofer"
prerequisites:
  - "Magisk 17.0+, KernelSU, or APatch"
  - "Android smartphone with 120Hz or higher display"
conflicts:
  - "Other build.prop spoofing modules"
configPaths:
  - "/data/adb/modules/机型问题删我/system.prop"
features:
  - "Spoofs device properties to ASUS ROG Phone 6 Dimensity Supreme Edition (ASUS_AI2203_B)"
  - "Unlocks extreme graphics and frame rate presets in Tencent and NetEase mobile games"
  - "Simple system.prop injection with zero background process overhead"
  - "Universal compatibility across Magisk, KernelSU, and APatch"
faq:
  - question: "Will banking apps detect this model change?"
    answer: "The module modifies user-space product model properties. While banking apps primarily check root binary signatures (handled by Play Integrity/SafetyNet tools), game engines read these properties to enable high-refresh options."
---

## Overview

**Tencent ROG Phone 6 Dimensity Edition Device Spoofer** (authored by Shi Chang Liang Nian Ban De Kun / 酷安@时长两年半的坤) bypasses manufacturer graphics limits by impersonating ASUS's flagship gaming device.

---

## Technical Architecture & How It Works

The module injects properties via Magisk's `resetprop` framework:

```properties
ro.product.manufacturer=asus
ro.product.brand=asus
ro.product.marketname=腾讯ROG6天玑至尊版
ro.product.model=ASUS_AI2203_B
```
