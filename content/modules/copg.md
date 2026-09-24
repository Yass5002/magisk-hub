---
id: "copg"
title: "COPG: Per-App Device & GPU Spoofer with WebUI"
sidebarTitle: "COPG"
description: "Advanced per-app device, CPU, and GPU spoofer enabling high-framerate 90/120fps modes and hardware profile masking via an on-device WebUI."
category: "performance-kernel"
tier: 1
searchQueries:
  - "copg magisk module download"
  - "unlock 90fps 120fps games magisk"
  - "alirezaparsi copg guide"
  - "per app device spoofer zygisk"
  - "gpu model spoofer android"
prerequisites:
  - "Magisk (with Zygisk), KernelSU, or APatch"
  - "Android 9.0 through Android 15"
conflicts:
  - "Global device spoofers modifying ro.product build props universally"
configPaths:
  - "/data/adb/copg/"
  - "/data/adb/modules/copg/"
features:
  - "Per-app spoofing: spoof a Xiaomi 14 Ultra or ROG Phone 8 exclusively for games while your phone remains stock everywhere else"
  - "Interactive on-device WebUI accessible through root managers to select device templates"
  - "Unlocks restricted graphic settings: 90Hz, 120Hz, and Extreme HDR in PUBG, CoD Mobile, Genshin, and Wild Rift"
  - "OpenGL and Vulkan GPU renderer string spoofing (e.g. spoofing Adreno 750 / Mali-G720)"
faq:
  - question: "Why do games lock high frame rates on capable phones?"
    answer: "Many mobile game developers partner with specific smartphone brands (like ASUS ROG, Black Shark, or OnePlus) to grant exclusive 90fps or 120fps modes, artificially locking unlisted devices to 60fps even if their hardware is more powerful. COPG tricks games into believing you are running on an approved flagship model."
  - question: "Will COPG break Google Wallet or banking apps?"
    answer: "No. Unlike legacy build.prop editors that altered your device model globally, COPG operates strictly per-app via Zygisk. Your banking apps and Google Play Services continue to see your certified stock fingerprint."
---

## Overview

Developed by **AlirezaParsi**, **COPG** (Custom OEM Profile Generator) is a modern Zygisk-based per-app hardware profile spoofer equipped with a full on-device WebUI.

In the mobile gaming ecosystem, popular competitive titles (such as PUBG Mobile, Call of Duty: Warzone, Genshin Impact, and Brawl Stars) restrict graphical settings, particle density, and 90Hz/120Hz refresh rate options based on a device's reported OEM model and GPU renderer strings. COPG lets you assign custom flagship hardware profiles on a granular, per-application basis without affecting system stability.

---

## Technical Architecture & How It Works

### Targeted Zygisk Property & OpenGL Interception

1. **Process-Level Targeting**: When an application process is launched, COPG checks `/data/adb/copg/profiles.json` to see if a custom profile is assigned to that package.
2. **Build Prop Emulation**: Hooks `__system_property_get` within the target process, returning spoofed strings for `ro.product.model`, `ro.product.brand`, and `ro.product.manufacturer`.
3. **OpenGL / Vulkan Query Hooking**: Hooks `glGetString(GL_RENDERER)` and `glGetString(GL_VENDOR)`, tricking the 3D rendering engine into believing a top-tier GPU (like Snapdragon 8 Gen 3 Adreno 750) is active.
4. **Isolated Scope**: Apps not configured in COPG experience zero interference and read standard system properties directly from the OS.

---

## Installation & Setup

1. Open **Magisk**, **KernelSU**, or **APatch**.
2. Download and flash the latest `COPG-vX.zip`.
3. Reboot your device.
4. Open the **COPG WebUI** directly from your root manager's module interface (or browse to `http://127.0.0.1:8080` if configured).
5. Search for your game in the app list, choose a target preset (e.g. *ASUS ROG Phone 8 Pro*), and tap **Apply**.
6. Launch the game, open graphics settings, and enable high-framerate modes.
