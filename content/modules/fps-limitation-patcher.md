---
id: "fps-limitation-patcher"
title: "FPS Limitation Patcher: Systemless PowerKeeper Thermal & Refresh Rate Unlocker for HyperOS / MIUI"
sidebarTitle: "FPS Limitation Patcher"
description: "Decompiles and patches Xiaomi's PowerKeeper app on the fly to eliminate aggressive thermal frame rate throttling and unlock true 90Hz/120Hz gaming."
category: "performance-kernel"
tier: 1
searchQueries:
  - "fps limitation patcher magisk"
  - "mods-center fps limitation patcher"
  - "remove xiaomi 60 fps limit powerkeeper"
  - "hyperos miui 120hz game unlock root"
  - "patch powerkeeper thermal throttle"
prerequisites:
  - "Xiaomi, Redmi, or POCO smartphone running stock or custom MIUI / HyperOS"
  - "Root access via Magisk or KernelSU"
  - "Presence of com.miui.powerkeeper in system framework partitions"
conflicts:
  - "Non-Xiaomi devices and pure AOSP ROMs (do not use MIUI PowerKeeper)"
configPaths:
  - "/data/adb/modules/fps-limitation-patcher/"
features:
  - "Automated on-device patching: pulls, disassembles, and modifies the device's native PowerKeeper APK during installation"
  - "Thermal throttling bypass: removes hardcoded 60 FPS downclocking ceilings enforced during battery saver or elevated temperatures"
  - "System-wide high refresh rate: forces 90Hz, 120Hz, and 144Hz panel refresh rates across games and third-party apps"
  - "Zero partition modification: overlays the patched PowerKeeper binary systemlessly over /system/app/ or /product/app/"
---

## Overview

On Xiaomi, Redmi, and POCO smartphones running MIUI or HyperOS, the proprietary **PowerKeeper** package (`com.miui.powerkeeper`) strictly governs battery profiling and thermal throttling. Even if a smartphone features a 120Hz or 144Hz display panel and flagship silicon, PowerKeeper forcibly downclocks gaming titles (like Genshin Impact, PUBG, or Call of Duty) to 60 FPS or 45 FPS as soon as battery temperatures exceed 38°C.

Developed by Mods-Center, **FPS Limitation Patcher** is an automated on-device patcher. During installation, the module extracts your smartphone's installed version of PowerKeeper, decompiles its bytecode to strip out thermal downclocking tables and framerate limiters, and overlays the modified APK systemlessly.

## How On-Device Patching Works

Unlike pre-compiled APK replacements that often cause signature mismatches or bootloops across different MIUI/HyperOS regional firmware releases, this module patches your device's exact stock package:

1. **Extraction**: The installer locates the active `PowerKeeper.apk` from `/system/app/`, `/system_ext/app/`, or `/product/app/`.
2. **Bytecode Modification**: Using embedded DEX utilities, it alters the conditional branches inside PowerKeeper's thermal profile classes that enforce `fps_limit` policies.
3. **Systemless Mount**: The newly patched APK is bound directly over the stock location, ensuring full cryptographic and framework compatibility.
4. **Unconstrained Framerates**: Games and applications can render at the maximum refresh rate supported by your display panel without being throttled by battery service daemons.

## Installation & Setup

1. Verify that your device is a Xiaomi, Redmi, or POCO phone running MIUI or HyperOS.
2. Download the `FPS-Limitation-Patcher` `.zip` from GitHub releases.
3. Open Magisk or KernelSU and flash the archive.
   - *Note*: Installation takes longer than standard modules because it decompiles, patches, and rebuilds the APK directly on the device.
4. Reboot your device.
5. Launch your target game; verify via developer options ("Show refresh rate") that the panel maintains 90Hz/120Hz rendering.
