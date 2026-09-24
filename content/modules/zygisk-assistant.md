---
id: "zygisk-assistant"
title: "Zygisk Assistant: Anti-Detection & Sandbox Root Masking"
sidebarTitle: "Zygisk Assistant"
description: "Open-source Zygisk module dedicated to cloaking root binaries, debugging flags, and mount points from aggressive banking security frameworks."
category: "root-management"
tier: 1
searchQueries:
  - "zygisk assistant download"
  - "zygisk assistant vs shamiko"
  - "how to hide root from banking apps"
  - "open source root hide module"
  - "zygisk assistant config guide"
prerequisites:
  - "Magisk 26.0+ (Zygisk enabled), KernelSU, or APatch with Zygisk Next"
conflicts:
  - "Other modules attempting to hook the exact same libc unmount trampolines simultaneously without coordination"
configPaths:
  - "/data/adb/zygisk_assistant/config.json"
  - "/data/adb/modules/zygisk-assistant/"
features:
  - "100% open-source alternative to proprietary root-hiding modules"
  - "Conceals `/system/bin/su`, `/system/xbin/su`, and `/data/adb` from filesystem scanning"
  - "Masks abnormal process environment variables and ptrace debug properties"
  - "Integrates cleanly with Magisk DenyList without requiring complex whitelist files"
faq:
  - question: "How does Zygisk Assistant differ from Shamiko?"
    answer: "Shamiko is closed-source and proprietary, developed exclusively by the LSPosed team with heavily obfuscated binaries. Zygisk Assistant is 100% fully open-source, allowing security researchers and privacy enthusiasts to audit the exact code executing with elevated privileges."
  - question: "Do I need to enable Enforce DenyList in Magisk?"
    answer: "Follow the specific instructions for the release: Zygisk Assistant reads the packages selected in your DenyList, but typically functions best when Enforce DenyList is turned OFF in Magisk so that Zygisk hooks remain active to perform dynamic unmounting."
---

## Overview

Developed by **snake-4**, **Zygisk Assistant** was created to provide a modern, fully open-source, auditable root-hiding companion for rooted Android devices.

As enterprise and banking security suites (like Promon SHIELD, AppSealing, and ThreatMetrix) began scanning for known closed-source hiding tools, community demand grew for a transparent, auditable Zygisk module. Zygisk Assistant intercepts filesystem, mount, and environment queries, providing robust root cloaking without opaque proprietary blobs.

---

## Technical Architecture & How It Works

### Userspace Syscall & C Library Interception

1. **Zygote Fork Hook**: When a sandboxed application is forked from the Zygote process, Zygisk Assistant checks whether the target package is configured for hiding.
2. **Mount Table Scrubbing**: The module intercepts calls to `read` and `fopen` when accessing `/proc/mounts`, `/proc/self/mountinfo`, and `/proc/self/mountstats`. It dynamically filters out all loop mount records, Magisk mirror directories, and overlayfs tokens.
3. **Property Masking**: It intercepts Android properties related to development and debugging:
   - `ro.debuggable`: Forced to `0`
   - `ro.secure`: Forced to `1`
   - `ro.build.type`: Forced to `user`
   - `persist.sys.usb.config`: Strips `adb`
4. **Binary Cloaking**: Filesystem calls querying `/system/bin/su`, `/data/adb/`, or root manager packages are routed to return standard "Not Found" error codes (`ENOENT`).

---

## Installation & Setup

1. Open your root manager (**Magisk**, **KernelSU**, or **APatch**).
2. Download and flash the latest `Zygisk-Assistant-vX.zip`.
3. In Magisk, go to **Settings** $\rightarrow$ **Configure DenyList** $\rightarrow$ select the applications you want to hide root from.
4. Ensure **Enforce DenyList** is toggled **OFF** (so Zygisk Assistant can inject its companion library into the process).
5. Reboot your device.
