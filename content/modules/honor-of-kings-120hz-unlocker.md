---
id: "honor-of-kings-120hz-unlocker"
title: "Honor of Kings 120Hz Ultra High Frame Rate Unlocker: iQOO 8 Pro Mod"
sidebarTitle: "Honor of Kings 120Hz"
description: "Systemless iQOO 8 Pro device profile spoofing that unlocks native 120 FPS ultra-high frame rate graphics in Tencent Honor of Kings and Arena of Valor."
category: "performance-kernel"
tier: 1
searchQueries:
  - "honor of kings 120fps magisk"
  - "unlock 120hz arena of valor root"
  - "iqoo 8 pro device spoofing magisk"
  - "v2141a system prop unlock"
prerequisites:
  - "Magisk 17.0+, KernelSU, or APatch"
  - "Device with 120Hz physical display panel"
conflicts:
  - "Other device profile spoofers"
configPaths:
  - "/data/adb/modules/46793794/system.prop"
features:
  - "Injects vivo iQOO 8 Pro flagship device signature (model V2141A)"
  - "Unlocks native 'Extreme' 120 FPS frame rate toggle inside game settings"
  - "Eliminates frustrating 60 FPS software caps in Honor of Kings / Arena of Valor"
  - "Minimalist 2.5 KB footprint with zero background service battery drain"
faq:
  - question: "Does this guarantee steady 120 FPS?"
    answer: "The module unlocks the 120 FPS software toggle in the game settings menu. Actual in-game framerate stability depends on your device's GPU and thermal performance."
---

## Overview

**Honor of Kings 120Hz Ultra High Frame Rate Unlocker** (authored by YouLinw de ROM Ri Chang / @YouLinw的ROM日常) unlocks the native 120 FPS display option in Tencent's flagship MOBA title.

---

## Technical Architecture & How It Works

The module injects the official partner device properties:

```properties
ro.product.manufacturer=vivo
ro.product.brand=vivo
ro.product.model=V2141A
```

During initialization, the game engine queries `Build.MODEL`. Detecting the iQOO 8 Pro (`V2141A`), it unlocks the 120 FPS setting.
