---
id: "lsposed"
title: "LSPosed: Modern ART Runtime Hooking Framework for Android"
sidebarTitle: "LSPosed Framework"
description: "Modern successor to the Xposed Framework by LSPosed Developers, injecting into Android's Zygote to provide memory-only runtime method hooks with per-app scope isolation."
category: "root-management"
tier: 1
searchQueries:
  - "lsposed download"
  - "lsposed zygisk module"
  - "lsposed apk manager download"
  - "how to install lsposed on magisk"
  - "lsposed dialer code 5776733"
prerequisites:
  - "Android 8.1 (Oreo MR1) up to Android 14 (Android 15+ requires updated community forks like JingMatrix LSPosed)"
  - "Root access via Magisk (v24+ with Zygisk enabled), KernelSU (with Zygisk-Next), or APatch (with Zygisk-APatch)"
conflicts:
  - "Legacy EdXposed or Riru-based Xposed engines (must be fully uninstalled prior to flashing LSPosed Zygisk)"
  - "Global Zygote hooking modules operating without application scope filtering"
configPaths:
  - "/data/adb/modules/zygisk_lsposed/"
  - "/data/adb/lspd/"
  - "/data/system/users/0/lspd/"
features:
  - "Non-invasive ART method hooking: patches compiled ART dex methods dynamically in RAM without patching system partitions or modifying APK signatures"
  - "White-list scope management: modules only execute within user-designated target applications, preventing system-wide battery drain and app crashes"
  - "Parasitic SystemUI integration: delivers management controls through notifications or direct dialer intent without maintaining a persistent foreground service"
  - "Universal Xposed API support: provides 100% backward API compatibility with classic Xposed, EdXposed, and modern LSPlant engines"
faq:
  - question: "Why did the LSPosed manager app disappear from my home screen?"
    answer: "LSPosed installs by default as a 'parasitic manager' embedded inside the system framework. If SystemUI notifications are dismissed or restricted by OEM battery savers, open your phone dialer and call `*#*#5776733#*#*` (`*#*#LSPosed#*#*`) to launch it. Alternatively, download and install `manager.apk` from the official LSPosed release page."
  - question: "Why is my installed Xposed module not taking effect?"
    answer: "Unlike legacy Xposed where modules hooked all apps globally, LSPosed enforces a strict whitelist model. You must open LSPosed Manager, tap on the installed module, toggle it ON, and select the specific target application(s) from the Scope list. Then force stop the target app."
  - question: "How do I recover from a bootloop caused by an incompatible Xposed module?"
    answer: "LSPosed modules run inside user apps and system services. If a module causes a bootloop, reboot into Safe Mode (press and hold Volume Down during boot) to disable all third-party modules. Alternatively, via root shell or ADB, run: `touch /data/adb/modules/zygisk_lsposed/disable && reboot`."
---

## Overview

The **LSPosed Framework** is the modern, high-performance successor to the venerable Xposed Framework for Android. Developed by the LSPosed Developers team, it bridges the Android Runtime (ART) with dynamic instrumentation, enabling developers to hook Java and native methods in real time.

In traditional Android modification workflows, changing system behavior required recompiling system frameworks, patching APKs with tools like Apktool, or flashing monolithic custom ROMs. Xposed revolutionized this paradigm by injecting into the Zygote process and hooking class methods in memory.

However, earlier frameworks like the original Xposed and EdXposed suffered from serious limitations: they hooked every process globally, causing noticeable performance degradation, high battery consumption, and frequent app crashes. LSPosed solved this by redesigning the architecture around **Zygisk** and **per-application scope isolation**.

---

## Technical Architecture & Hooking Mechanics

LSPosed operates during early Android boot through Magisk or KernelSU's **Zygisk** (Zygote Injection) lifecycle:

- **init (PID 1)**: System initialization boots the OS and spawns core system daemons.
- **app_process / Zygote**: Loads `libart.so` and runtime classes; Zygisk dynamically loads the LSPosed core library (`zygisk_lsposed`).
- **Selective Process Forking**:
  - **Target App (In Scope)**: LSPosed hooks activated; module DEX loaded directly in RAM; method hooks executed via LSPlant.
  - **Normal App (Out of Scope)**: Zero hooks injected; zero overhead with native execution speed.

1. **Zygisk Injection**: When Android spawns the `zygote` (and `zygote64`) daemon, LSPosed injects its core hooking library (`liblspd.so`).
2. **Pre-Fork Evaluation**: Before Zygote forks a child process to run an application, LSPosed checks `/data/adb/lspd/` to see whether the target package name is present in the module's scope database.
3. **Selective ART Hooking**:
   - If the package is **not in scope**, Zygote forks cleanly without initializing the hooking engine. The application runs with 100% stock execution speed.
   - If the package is **in scope**, LSPosed initializes LSPlant, replaces target method entrypoints with dynamic trampoline hooks, and invokes the module's `IXposedHookLoadPackage` callbacks.

---

## Installation & Setup

### Prerequisites
1. A rooted device running **Android 8.1 to Android 14**.
2. A modern root manager:
   - **Magisk v24+**: Go to Settings -> Enable **Zygisk**, then reboot.
   - **KernelSU**: Flash **Zygisk-Next** module in KernelSU, then reboot.
   - **APatch**: Flash **Zygisk-APatch** module, then reboot.

### Step-by-Step Installation
1. Download `LSPosed-v1.9.2-7024-zygisk-release.zip`.
2. Open your root manager (Magisk / KernelSU / APatch) and navigate to the **Modules** tab.
3. Tap **Install from storage**, select the LSPosed ZIP archive, and wait for flashing to complete.
4. Reboot your device.
5. Upon boot, check your notification shade for the **LSPosed Manager** setup notification. Tap it to add the manager shortcut to your launcher.

---

## The Parasitic Manager & Dialer Secret Code

To maintain a minimal footprint and prevent third-party apps from detecting a standalone manager package on device storage, LSPosed utilizes a **parasitic manager** architecture:

- The manager UI is synthesized dynamically from system resources.
- If your notification was cleared or your launcher hid the shortcut, you can launch the LSPosed interface instantly by opening your stock Phone dialer and entering:
  ```
  *#*#5776733#*#*
  ```
  *(5776733 corresponds to L-S-P-O-S-E-D on a numeric telephone keypad).*

- Alternatively, if your OEM dialer does not parse secret codes, launch it directly via root terminal:
  ```bash
  su -c am start -n org.lsposed.manager/.ui.MainActivity
  ```

---

## Scope Configuration & Module Management

Every module in LSPosed requires explicit user permission and scope binding:

1. Install any compatible Xposed module APK (e.g., CorePatch, Bootloader Spoofer, HookVip).
2. Open **LSPosed Manager** -> navigate to the **Modules** tab (puzzle icon).
3. The newly installed module will appear greyed out with an "Unactivated" badge.
4. Tap the module, toggle the **Enable Module** switch at the top.
5. In the **Scope** section, check the target applications that the module is designed to modify (e.g. `com.android.systemui` for status bar tweaks, or specific target apps for bypasses).
6. Force stop and restart the selected applications to apply changes.

---

## Bootloop Recovery & Emergency Removal

If an aggressive or incompatible Xposed module causes a system freeze or bootloop during startup:

### Method 1: ADB Safe-Disable (Recommended)
Connect your device to a computer via USB:
```bash
# Disable LSPosed without uninstalling
adb wait-for-device shell touch /data/adb/modules/zygisk_lsposed/disable
adb reboot
```

### Method 2: Physical Key Safe Mode
During device startup, when the OEM boot animation appears, press and hold the **Volume Down** button continuously until the lockscreen displays "Safe Mode" in the lower corner. Safe Mode prevents all third-party modules from loading. Open Magisk/KernelSU and toggle off the problematic module.

### Method 3: Complete Removal
From custom recovery (TWRP/OrangeFox) terminal or root shell:
```bash
rm -rf /data/adb/modules/zygisk_lsposed
rm -rf /data/adb/lspd
```
