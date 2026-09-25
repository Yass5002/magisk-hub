---
id: "iunlockergl"
title: "iUnlocker GLTool: Advanced GPU, Display & Hardware Identity Spoofing for Mobile Gaming"
sidebarTitle: "iUnlocker GLTool"
description: "Spoofs OpenGL ES, Vulkan limits, display parameters, and CPU/RAM specifications to unlock extreme graphic presets, 90/120 FPS modes, and HDR rendering in games."
category: "performance-kernel"
tier: 1
searchQueries:
  - "iunlocker gltool magisk"
  - "i-taylo iunlockergl"
  - "spoof opengl vulkan android game fps"
  - "unlock 120 fps graphics settings pubg"
  - "iunlocker gltool apk zip"
prerequisites:
  - "Android 8.1 (API 27) or higher"
  - "Root access via Magisk v26.4+ (with Zygisk enabled) or KernelSU with Zygisk / ZygiskNext"
  - "64-bit ARM architecture (arm64-v8a tested)"
conflicts: []
configPaths:
  - "/data/adb/modules/Mjg2MjU1ODg0Mwo/"
features:
  - "OpenGL ES spoofing: alters GPU vendor strings, renderer models, OpenGL ES version identifiers, and supported GL extension tables"
  - "Vulkan API virtualization: modifies reported Vulkan device limits, video memory heaps, and driver version strings"
  - "Display pipeline overrides: fakes panel refresh rate ceilings, HDR10/Dolby Vision compliance, and wide color gamuts (DCI-P3)"
  - "Hardware profile masquerading: reports flagship device brands, SoC architecture capabilities, and simulated RAM pools"
  - "Bundled manager application: includes graphical companion APK inside the archive for profile selection and per-app injection"
---

## Overview

Major mobile gaming titles (including PUBG Mobile, Call of Duty: Mobile, Genshin Impact, and League of Legends: Wild Rift) inspect low-level hardware strings before unlocking maximum graphical quality presets or high framerate modes (90 FPS and 120 FPS). Devices with capable silicon are often locked out of flagship settings simply because game developers whitelist specific OEM model numbers or flagship GPU strings.

Developed by Taylo (i-Taylo), **iUnlocker GLTool** acts as a graphics and hardware identity spoofing bridge. Operating via the Zygisk runtime, it intercepts OpenGL ES and Vulkan API queries at the native Android framework layer, presenting spoofed hardware profiles to games without modifying system vendor partitions or flashing custom firmware.

## Spoofing Capabilities

iUnlocker GLTool hooks into graphical drivers and framework libraries to modify:

### 1. 3D Graphics API Headers
- **OpenGL ES**: Spoofs `GL_VENDOR`, `GL_RENDERER`, `GL_VERSION`, and enumerates artificial `GL_EXTENSIONS` required by proprietary game engines.
- **Vulkan**: Overrides `VkPhysicalDeviceProperties`, modifying driver version codes, memory heap allocations, and pipeline extension support.

### 2. Display & Visual Characteristics
- Overrides display refresh rate declarations to expose 90Hz, 120Hz, or 144Hz options.
- Simulates hardware HDR support (HDR10, HDR10+, Dolby Vision) and wide color gamut rendering (Display P3) in apps that restrict visual filters to verified displays.

### 3. Hardware Architecture & Memory
- Spoofs device manufacturer, model strings, and build fingerprint properties.
- Mask CPU architecture flags, core clusters, and available system RAM sizes to bypass arbitrary resource ceilings set by games.

## Compatibility Matrix

- **Android Versions**: Android API 27 (Android 8.1 Oreo) through modern Android releases.
- **Chipset Architecture**: Tested across Qualcomm Snapdragon, MediaTek Dimensity/Helio, and Samsung Exynos platforms on `arm64-v8a`.
- **Root Environment**:
  - **Magisk**: Version 26.4 or newer with **Zygisk** enabled in Magisk settings.
  - **KernelSU / APatch**: Requires an active Zygisk injection provider such as **ZygiskNext**.

## Installation & Configuration

1. Confirm that Zygisk is active in your root management environment.
2. Download the `iUnlockerGL` `.zip` archive from the official repository releases.
   - *Note*: The ZIP archive automatically extracts and installs the companion manager app during installation.
3. Flash the archive in Magisk or KernelSU and reboot the device.
4. Launch the newly installed **iUnlocker** application from your app drawer.
5. Grant root permissions when prompted.
6. Select your target game, pick an optimal device/GPU profile (e.g., flagship Adreno or Mali profiles), and save the configuration.
7. Launch the game to access newly unlocked graphics and framerate presets.

## Troubleshooting

- **Game Graphics Unchanged**: Ensure the target game is not added to the root manager's DenyList or Enforce DenyList without unmounting, which would block Zygisk from injecting the spoofing hook into the game process.
- **Companion App Missing on Boot**: If your ROM's package installer blocked the APK during module flash, manually extract `iUnlocker.apk` from the module ZIP and install it as a standard user application.
