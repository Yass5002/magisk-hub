---
id: "mesa-turnip-builder"
title: "Mesa Turnip Builder: Systemless Freedreno Turnip Vulkan Driver for Adreno"
sidebarTitle: "Mesa Turnip Builder"
description: "Flashable Magisk, KernelSU, and APatch module built with Android NDK r30 that replaces /system/vendor/lib64/hw/vulkan.adreno.so with Mesa Freedreno Turnip for Adreno 6xx–8xx GPUs on Android 14+."
category: "performance-kernel"
tier: 1
searchQueries:
  - "mesa turnip builder magisk module"
  - "turnip vulkan driver magisk ksu"
  - "vulkan.adreno.so android 14 15"
  - "adreno 6xx 7xx 8xx turnip module"
  - "v3kt0r-87 mesa turnip builder"
prerequisites:
  - "Qualcomm Snapdragon device with an Adreno 6xx, 7xx, or 8xx GPU"
  - "Android 14+ (`ro.build.version.sdk >= 34` required; Android 15 / SDK 35+ recommended for full Vulkan 1.4)"
  - "Magisk v25.2+, KernelSU, or APatch"
conflicts:
  - "Other GPU driver replacement modules targeting `/system/vendor/lib64/hw/vulkan.adreno.so`"
  - "Android 13 and older (`SDK < 34` — installer aborts intentionally)"
  - "Non-Qualcomm SoCs (MediaTek Mali/Immortalis, Exynos Xclipse, Pixel Tensor)"
configPaths:
  - "/data/adb/modules/turnip-mesa/"
  - "/system/vendor/lib64/hw/vulkan.adreno.so"
features:
  - "Replaces `/system/vendor/lib64/hw/vulkan.adreno.so` systemlessly with Mesa 26.3.1 Freedreno Turnip built against Android NDK r30"
  - "Applies strict SELinux `u:object_r:same_process_hal_file:s0` labeling so Android's SP-HAL linker namespace permits loading across all apps"
  - "Automatically purges stale `*shader*`, `*graphitecache*`, and `*gpucache*` directories across user and app data caches on install and uninstall"
  - "Enhances Vulkan extension completeness and rendering accuracy for emulators (Dolphin, PPSSPP, EggNS), ANGLE, and Vulkan titles"
faq:
  - question: "Why does `customize.sh` explicitly set the `same_process_hal_file` SELinux context on `vulkan.adreno.so`?"
    answer: "On Android 8.0+ (Treble), Vulkan ICD drivers are Same-Process HALs (SP-HALs) loaded directly inside unprivileged app processes. Without `u:object_r:same_process_hal_file:s0`, SELinux denies app processes from `mmap`/`execute` access to the mounted `.so`, causing Vulkan initialization crashes or immediate black screens."
  - question: "Why does the installer abort on Android 13 or older?"
    answer: "`customize.sh` checks `ro.build.version.sdk` (falling back to `ro.system.build.version.sdk`) and aborts if the value is below `34` (`Android 14 is now required!`). Additionally, Android 15 (`SDK 35`) is required for full Vulkan 1.4 support in recent Mesa Turnip builds."
  - question: "Do I need to manually clear game or emulator shader caches after flashing or removing Turnip?"
    answer: "No. Both `customize.sh` and `uninstall.sh` run a `find` sweep across `/data/user/*/*/*cache`, `/data/data/*/*cache`, and `/data/user_de/*/*/*cache` to delete `*shader*`, `*graphitecache*`, and `*gpucache*` directories so incompatible proprietary Adreno shaders cannot corrupt Turnip pipelines."
---

## Overview

Qualcomm's proprietary Adreno Vulkan drivers bundled in OEM firmware frequently freeze on older Vulkan point releases, omit modern extensions, or exhibit rendering glitches in console emulators and translation layers. **Mesa Turnip Builder** (`v3kt0r-87/Mesa-Turnip-Builder`, module ID `turnip-mesa`) packages upstream **Mesa Freedreno Turnip** builds compiled with **Android NDK r30** into a ready-to-flash systemless module (`Turnip-26.3.1-MAGISK-KSU.zip`).

---

## Technical Architecture & Payload Internals

Inspecting `Turnip-26.3.1-MAGISK-KSU.zip` shows a lean, Treble-compliant systemless driver replacement:

| File | Purpose |
| --- | --- |
| `system/vendor/lib64/hw/vulkan.adreno.so` | Compiled 64-bit Mesa Freedreno Turnip ICD driver overriding the stock Adreno Vulkan HAL |
| `customize.sh` | Verifies SDK >= 34, sets `0644` + `u:object_r:same_process_hal_file:s0` SELinux label, and purges GPU shader caches |
| `uninstall.sh` | Cleans shader/graphite/GPU caches upon module removal to prevent driver mismatch crashes |
| `module.prop` | Declares `id=turnip-mesa`, `version=v26.3.1`, and `updateJson` pointing to the `stable` release feed |

### Key Implementation Details

1. **SDK Enforcement**: `customize.sh` inspects `ro.build.version.sdk` and `ro.system.build.version.sdk`, aborting on any firmware older than Android 14 (`SDK 34`). Full Vulkan 1.4 feature exposure requires Android 15 (`SDK 35+`).
2. **SP-HAL SELinux Labeling**: After running `set_perm_recursive $MODPATH/system 0 0 0755 0644`, `customize.sh` executes:
   ```sh
   set_perm $MODPATH/system/vendor/lib64/hw/vulkan.adreno.so 0 0 0644 u:object_r:same_process_hal_file:s0
   ```
   This guarantees the systemless overlay passes Android's `sphal` linker namespace and SELinux policy checks for both system and third-party 64-bit applications.
3. **Automated Shader Cache Invalidations**: Proprietary Adreno shader caches are binary-incompatible with Mesa Turnip's NIR/IR3 compiler. Both installation and uninstallation automatically clean `*shader*`, `*graphitecache*`, and `*gpucache*` across `/data/data/`, `/data/user/`, and `/data/user_de/`.

---

## Installation & Configuration

1. Confirm your device uses a supported **Qualcomm Adreno 6xx, 7xx, or 8xx** GPU and runs **Android 14+** (SDK 34+).
2. Back up your boot/data or ensure you know how to enter root Safe Mode (since system-wide Vulkan replacement affects UI renderers if ANGLE/SkiaVk is active).
3. Flash `Turnip-26.3.1-MAGISK-KSU.zip` in **Magisk** (v25.2+), **KernelSU**, or **APatch**.
4. Wait for the GPU cache cleanup step to finish, then **reboot** your device.
5. Verify the active Vulkan driver version via **3DMark**, **GPU Caps Viewer / Vulkan Hardware Capability Viewer**, or emulator graphics logs (e.g., Dolphin, PPSSPP).

---

## Common Issues & Troubleshooting

- **SystemUI Glitches or Bootloop on Unsupported Adreno Variant**: Some newer or niche Adreno revisions (especially early 8xx or OEM-customized SkiaVk configurations) may encounter regressions with global Turnip replacement. Boot into Safe Mode (or remove `/data/adb/modules/turnip-mesa` via recovery/ADB) to revert cleanly—`uninstall.sh` will wipe incompatible Turnip shader caches automatically.
- **Game Crashes or Texture Corruption After Driver Update**: Force-stop the affected game/emulator and clear its app cache manually in case it stores compiled Vulkan pipeline caches outside standard `*shader*` directories.
- **32-bit Apps Still Using Stock Driver**: This build ships only 64-bit `lib64/hw/vulkan.adreno.so`. Modern 64-bit apps and emulators pick up Turnip, while legacy 32-bit `armeabi-v7a` binaries fall back to the vendor's 32-bit Vulkan ICD if present.
