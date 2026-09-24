---
id: "rezygisk"
title: "ReZygisk: Standalone Open-Source Zygisk Engine for Modern Root"
sidebarTitle: "ReZygisk"
description: "High-performance, standalone implementation of the Zygisk API designed specifically for KernelSU, APatch, and custom root solutions."
category: "root-management"
tier: 1
searchQueries:
  - "rezygisk download"
  - "rezygisk vs zygisk next"
  - "standalone zygisk kernelsu"
  - "performanc rezygisk guide"
  - "how to enable zygisk on kernelsu"
prerequisites:
  - "KernelSU or APatch installed (or Magisk with built-in Zygisk disabled)"
  - "Android 8.0 through Android 15"
conflicts:
  - "Zygisk Next (do not run two standalone Zygisk engines simultaneously)"
  - "Built-in Magisk Zygisk toggle enabled simultaneously"
configPaths:
  - "/data/adb/rezygisk/"
  - "/data/adb/modules/rezygisk/"
features:
  - "100% open-source, auditable implementation of the Zygisk C/C++ module API"
  - "Engineered for kernel-assisted root solutions (KernelSU / APatch) without requiring Magisk framework"
  - "Optimized hook trampolines with lower memory consumption and faster app fork times"
  - "Zero telemetry, zero tracking, strictly focused on module execution stability"
faq:
  - question: "Why do I need ReZygisk if I already use KernelSU?"
    answer: "KernelSU operates purely at the Linux kernel level and does not natively inject code into Android's userspace Zygote process. Many of the most popular root modules (such as Shamiko, PlayIntegrityFork, and Vector) require Zygisk to intercept app processes. ReZygisk provides that Zygote bridge."
  - question: "Can I use ReZygisk on Magisk?"
    answer: "You can, but you must first turn OFF Magisk's built-in Zygisk toggle in Magisk settings to prevent symbol collisions and process crashing."
---

## Overview

Developed by **PerformanC**, **ReZygisk** is a clean, open-source, standalone implementation of the **Zygisk API** specification.

While Magisk incorporates its own proprietary Zygisk implementation directly into `magiskd`, modern alternatives like KernelSU and APatch adhere to a minimalist kernel-space design philosophy. To run the vast ecosystem of modules that depend on Zygisk hooks (such as Vector/Xposed, PlayIntegrityFork, and audio enhancers), KernelSU requires an external Zygote injection engine. ReZygisk fulfills this requirement with a clean, performant architecture.

---

## Technical Architecture & How It Works

### Zygote Ptrace & Loader Injection

1. **Daemon Initialization**: At boot time, ReZygisk starts a background monitoring daemon that watches for the initialization of Android's 32-bit and 64-bit Zygote processes (`app_process32` and `app_process64`).
2. **Ptrace Hijack**: During the early initialization of the Zygote process (before the first application is forked), ReZygisk uses ptrace to inject its native loader library (`librezygisk.so`).
3. **API Implementation**: ReZygisk registers the full official Zygisk API functions:
   - `preAppSpecialize`: Executed before app privileges are dropped to standard sandbox UID.
   - `postAppSpecialize`: Executed after sandbox privileges are active.
   - Companion process IPC channels.
4. **Module Dispatch**: Whenever any app process is spawned, ReZygisk checks `/data/adb/modules/` for active Zygisk modules and loads their native `.so` payloads directly into the target process.

---

## Installation & Setup

1. Open **KernelSU** or **APatch**.
2. Download the latest `ReZygisk-vX.zip` from releases.
3. Flash the package via the **Modules** tab.
4. Reboot your phone.
5. In your module list, ReZygisk will show as active. You can now flash any standard Zygisk module (like PlayIntegrityFork or Vector) and they will function seamlessly.
