---
id: "sunshine-global-high-refresh-rate"
title: "Sunshine Global High Refresh Rate Enabler: Force 120Hz/144Hz"
sidebarTitle: "Global High Refresh"
description: "Universal display frequency tuning module that forces 120Hz or 144Hz refresh rate across all user applications, system overlays, and video players without throttling."
category: "performance-kernel"
tier: 1
searchQueries:
  - "sunshine rate magisk"
  - "force 120hz global magisk module"
  - "unlock 120hz all apps root"
  - "disable 60hz refresh rate lock android"
prerequisites:
  - "Android smartphone with 90Hz, 120Hz, or 144Hz physical display panel"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other aggressive display refresh rate locking scripts"
configPaths:
  - "/system/bin/sunshine_rate"
  - "/data/adb/modules/Sunshine_Rate/service.sh"
features:
  - "Forces maximum display panel refresh rate universally across all installed apps"
  - "Eliminates frustrating 60Hz throttling inside video playback apps and camera viewfinders"
  - "Automated background watchdog maintains refresh rate locks across thermal limits"
  - "Lightweight shell script daemon with zero measurable CPU overhead"
faq:
  - question: "Does forcing 120Hz everywhere increase battery consumption?"
    answer: "Yes, running the display at maximum refresh rate continuously increases power draw by approximately 5% to 10% during active screen-on time compared to dynamic variable refresh rate (VRR)."
  - question: "Can this module damage my display hardware?"
    answer: "No. The module only activates refresh rate modes that are natively supported and advertised by your device's display controller and kernel drivers."
---

## Overview

**Sunshine Global High Refresh Rate Enabler** (authored by Everything by the sun) is an operating system tuning module engineered to eliminate vendor-imposed refresh rate throttling.

Modern smartphones advertise 120Hz or 144Hz display panels, yet manufacturer software frequently limits refresh rates to 60Hz in critical applications—such as web browsers, video streaming apps (YouTube, Netflix), maps, and camera viewfinders. Sunshine Rate bypasses these software policies, delivering uncompromising smoothness across the entire operating system.

---

## Technical Architecture & How It Works

The module operates by interacting directly with the Android SurfaceFlinger and display HAL:

### 1. Display Mode Discovery

During boot initialization, the background service queries the display driver for available hardware mode IDs:

```bash
# Query hardware display configurations
dumpsys display | grep -E "mSupportedModes|mDefaultModeId"
```

### 2. Global Policy Override

The daemon issues commands to the Android window manager and settings database, locking peak and minimum refresh rates to the panel's maximum capacity:

```bash
settings put system min_refresh_rate 120.0
settings put system peak_refresh_rate 120.0
settings put global user_refresh_rate 120
```

By continuously evaluating the state of `sys.boot_completed` and device thermal events, it ensures that aggressive OEM power-saving daemons cannot reset the display back to 60Hz.

---

## Troubleshooting & Verification

- **Real-Time FPS Verification**: Enable **Show refresh rate** under **Developer options** to monitor your screen's actual refresh rate in real time.
- **Game Compatibility**: Some games enforce hardcoded 60 FPS caps within their game engine; for these titles, pair with a frame rate unlocker or vendor performance module.
