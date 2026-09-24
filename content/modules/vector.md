---
id: "vector"
title: "Vector: Next-Generation ART Hooking & Xposed Framework"
sidebarTitle: "Vector"
description: "The official modern successor to the LSPosed framework maintained by JingMatrix, bringing advanced ART hooking to Android 14 and 15."
category: "root-management"
tier: 1
searchQueries:
  - "vector xposed framework"
  - "lsposed alternative android 14 15"
  - "jingmatrix vector download"
  - "install vector zygisk module"
  - "modern xposed framework 2026"
prerequisites:
  - "Android 9.0 through Android 15"
  - "Magisk with Zygisk, KernelSU with Zygisk Next, or APatch"
conflicts:
  - "Original LSPosed (must be uninstalled before installing Vector)"
  - "EdXposed (deprecated)"
configPaths:
  - "/data/adb/lspd/"
  - "/data/adb/modules/vector/"
features:
  - "Seamless compatibility with all standard Xposed and LSPosed modules"
  - "Native support for modern Android 14 and Android 15 ART compiler changes and inline optimizations"
  - "Granular scope management: hook only selected target apps to eliminate battery drain and security vulnerabilities"
  - "Modern Material You companion manager application for enabling modules and managing scopes"
faq:
  - question: "Why should I use Vector instead of the original LSPosed?"
    answer: "Development on the upstream LSPosed repository halted in late 2023, causing crashes and module hook failures on modern Android 14 QPR updates and Android 15. Vector, maintained by active core contributors (JingMatrix), resolves ART inline deoptimization crashes and provides full compatibility with the latest Android releases."
  - question: "Do my existing Xposed modules work on Vector?"
    answer: "Yes, 100%. Vector implements the complete modern LSPosed and Xposed bridge APIs. Any module that worked under LSPosed will function identically on Vector without recompilation."
---

## Overview

Following the cessation of active development on the original LSPosed project, **Vector** (developed by **JingMatrix**) emerged as the official, active community continuation of the modern ART hooking runtime for Android.

The Xposed paradigm allows developers to modify the behavior of system components and third-party apps dynamically in memory without decompiling or modifying APK files on disk. Vector implements this capability via **Zygisk**, injecting into Android's Zygote process to hook Java methods at the native ART runtime level with minimal overhead and zero global system instability.

---

## Technical Architecture & How It Works

### ART Method Hooking with SandHook / Pine

1. **Zygisk Initialization**: When the Android OS initializes the 64-bit and 32-bit Zygote daemons, Vector's companion native library (`liblspd.so`) is injected into the process space.
2. **Scope Resolution**: Unlike legacy Xposed which hooked every single process on the device (causing heavy system stuttering), Vector queries its local SQLite database (`/data/adb/lspd/config.db`). Only applications explicitly added to a module's scope receive hook trampolines.
3. **ART Inline Hooking**: When target apps load, Vector intercepts class loading via ART runtime hooks. It patches the internal `ArtMethod` structure in memory, redirecting calls from the target method to the module's interceptor callbacks (`beforeHookedMethod` and `afterHookedMethod`).
4. **Isolated Manager Bridge**: The management interface communicates with the background daemon via native Unix domain sockets, preventing target apps from detecting the presence of the framework.

---

## Installation & Setup

### Step 1: Install the Module
1. Download the latest `Vector-vX.zip` (Zygisk release) from the repository.
2. Open **Magisk**, **KernelSU**, or **APatch**.
3. Flash the zip from the **Modules** screen and reboot your device.

### Step 2: Install the Vector Manager
1. After rebooting, a notification will appear prompting you to install the **Vector Manager** APK (or open the embedded web interface).
2. If the APK is not automatically placed in notifications, locate `manager.apk` inside `/data/adb/lspd/` and install it manually.

### Step 3: Activating Modules
1. Install any Xposed module APK (e.g., Hide My Applist, CustoMIUIzer, KnoxPatch).
2. Open **Vector Manager** $\rightarrow$ tap **Modules**.
3. Toggle the module **ON** and configure its target **Scope** (check the specific apps you want the module to modify).
4. Force stop or reboot the target apps to apply changes.
