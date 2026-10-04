---
id: "miui-display-refresh-locker"
title: "MIUI Display Refresh Rate Locker: Disable Dynamic Downclocking"
sidebarTitle: "MIUI Refresh Locker"
description: "Kernel and SurfaceFlinger tuning module that locks high refresh rates (120Hz/144Hz) permanently on Xiaomi MIUI and HyperOS, preventing dynamic downclocking."
category: "performance-kernel"
tier: 1
searchQueries:
  - "miui global high refresh rate magisk"
  - "lock 120hz miui hyperos module"
  - "miui smartfps disable magisk"
  - "stop miui 60hz video downclock"
prerequisites:
  - "Xiaomi, Redmi, or POCO device with high refresh rate display running MIUI or HyperOS"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Conflicting vendor refresh rate overriding scripts"
configPaths:
  - "/system/etc/system.prop"
features:
  - "Disables MIUI proprietary SmartFPS and dynamic content refresh rate adaptation"
  - "Locks full panel refresh rates during video playback, browser scrolling, and text reading"
  - "Overrides vendor Joyose and SurfaceFlinger frequency downclocking policies"
  - "Maintains responsive, lag-free UI animations without touching system partitions"
faq:
  - question: "Why does MIUI drop my screen refresh rate from 120Hz to 60Hz?"
    answer: "Xiaomi MIUI and HyperOS include an aggressive battery saver algorithm (SmartFPS and Joyose) that detects static screen content, video streams, or certain app package names, automatically throttling the display controller down to 60Hz. This module disables that detection."
  - question: "Is this safe for the display panel?"
    answer: "Yes, it only forces the display to remain in the manufacturer's officially supported 120Hz/144Hz refresh modes without exceeding hardware design limits."
---

## Overview

**MIUI Display Refresh Rate Locker** (developed by key, based on research by kevmck, Liangmisanxing, and kakathic) is a targeted optimization module designed to fix the aggressive refresh rate drops prevalent on Xiaomi MIUI and HyperOS firmware.

While Xiaomi smartphones offer smooth 120Hz and 144Hz OLED displays, the stock system regularly throttles refresh rates to 60Hz when playing videos, reading ebooks, or opening third-party tools. This constant frequency fluctuation causes visible micro-stutter when scrolling or switching apps. This module completely stabilizes screen refresh rate.

---

## Technical Architecture & How It Works

The module neutralizes MIUI's frequency throttling across multiple system properties via `system.prop`:

### 1. SurfaceFlinger Property Overrides

```ini
# Disable dynamic smart fps adaptation
persist.sys.smartfps=0

# Disable vendor default fps downclocking switch
ro.vendor.fps.switch.default=false

# Disable content-aware refresh rate scaling in SurfaceFlinger
ro.surface_flinger.use_content_detection_for_refresh_rate=false
```

### 2. Framework Daemon Harmonization

By instructing the Android SurfaceFlinger compositor to ignore video playback frame-rate metadata, the display controller maintains the maximum scan rate regardless of whether the foreground media is 24 FPS, 30 FPS, or 60 FPS.

---

## Troubleshooting & Verification

- **Real-Time Frequency Display**: Navigate to **Settings > Additional settings > Developer options** and enable **Show refresh rate** to verify the persistent 120Hz/144Hz lock.
- **Battery Temperature**: Under extreme ambient temperatures, the device kernel may engage thermal safety throttles; this is a kernel-level hardware protection distinct from software SmartFPS.
