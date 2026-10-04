---
id: "xiaomi-13pro-device-spoofer"
title: "Xiaomi 13 Pro Device Identity Spoofer"
description: "Systemless device identity spoofer masquerading device properties as Xiaomi 13 Pro (2210132C) to unlock 120 FPS high refresh rates and flagship gaming profiles."
category: "system-environment"
author: "Da Feng Mei Le Yun Bu Fei (大风没了云不飞)"
version: "v1.0"
updatedAt: "2026-10-04"
compatibility: ["Magisk", "KernelSU", "APatch"]
---

## Overview & System Architecture

The **Xiaomi 13 Pro Device Identity Spoofer** is a lightweight, systemless property injection module developed by Da Feng Mei Le Yun Bu Fei (大风没了云不飞). It modifies Android product identification properties to match the Chinese domestic flagship **Xiaomi 13 Pro** (`2210132C`, Snapdragon 8 Gen 2).

Modern mobile titles—including *Honor of Kings* (王者荣耀), *Peace Elite / PUBG Mobile* (和平精英), and *Genshin Impact* (原神)—maintain server-side hardware whitelists. Devices not explicitly identified as top-tier flagships are locked to 60 FPS or low graphic presets. By spoofing the device identity at boot via `system.prop`, this module enables extreme frame rate modes (90 FPS, 120 FPS) and ultra-high graphical fidelity.

## Injected System Properties

Physical inspection of `common/system.prop` reveals exact flagship spoofing strings:

```properties
ro.product.manufacturer=Xiaomi
ro.product.brand=Xiaomi
ro.product.model=Xiaomi 13Pro
ro.product.name=2210132C
ro.product.device=2210132C
```

## Key Benefits

1. **High Refresh Rate Unlocking**: Unlocks 90Hz and 120Hz graphic options across Tencent and NetEase games.
2. **Flagship Feature Whitelist**: Unlocks Xiaomi Cloud Computer, Gallery HDR enhancements, and high-performance gaming modes in Game Turbo.
3. **Clean Systemless Execution**: Modifies properties at runtime without modifying system partition read-only blocks, ensuring seamless OTA and SafetyNet/Play Integrity coexistence.

## Installation & Verification

### Step 1: Flashing the Module
Install through Magisk Manager, KernelSU app, or APatch Manager.

### Step 2: Verify Injected Properties
After rebooting, run the following verification commands via ADB shell or local terminal:
```bash
getprop ro.product.model
# Output: Xiaomi 13Pro

getprop ro.product.name
# Output: 2210132C

getprop ro.product.device
# Output: 2210132C
```

### Step 3: Game Clear Cache
To ensure game servers register the updated model name, clear cache on the target game application:
```bash
pm clear-cache <package.name>
```

## Compatibility & Safety Notes

- **Universal Compatibility**: Works across all Magisk (v20.4+), KernelSU, and APatch installations regardless of device brand (Xiaomi, OnePlus, Realme, Samsung, Google Pixel).
- **Play Integrity / SafetyNet**: Does not alter security patch levels or bootloader lock status. If used alongside Play Integrity Fix, ensure Play Integrity Fix loads device fingerprints as required.
