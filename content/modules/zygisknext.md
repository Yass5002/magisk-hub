---
id: "zygisknext"
title: "Zygisk Next: Standalone Modern Zygisk Implementation"
sidebarTitle: "Zygisk Next"
description: "High-performance, standalone Zygisk injection implementation by Dr-TSNG / LSPosed Developers, delivering Zygisk API support across KernelSU, APatch, and Magisk."
category: "root-management"
tier: 1
searchQueries:
  - "zygisknext magisk module"
  - "dr-tsng zygisk next"
  - "standalone zygisk kernelsu apatch"
  - "zygisknext denylist policy"
  - "modern zygisk api loader"
prerequisites:
  - "KernelSU (kernel >= 10940, ksud >= 11575), APatch (>= 10700), or Magisk (>= 26402 with built-in Zygisk disabled)"
  - "Single root implementation only (do not mix Magisk and KernelSU)"
conflicts:
  - "Magisk's built-in Zygisk feature (must be toggled OFF in Magisk Settings to avoid dual loader collisions)"
  - "Other Zygisk loaders (ReZygisk, NeoZygisk) installed simultaneously"
configPaths:
  - "/data/adb/modules/zygisksu/"
  - "/data/adb/zygisksu/"
features:
  - "Independent Zygisk lifecycle: decouples module injection from Magisk's internal release cycle"
  - "Universal root support: brings full Zygisk module ecosystem support to KernelSU, APatch, and Magisk"
  - "Advanced namespace unmounting: clean DenyList and Umount policies that detach module mounts from target apps"
  - "WebUI & Action bugreport: includes a built-in WebUI dashboard and one-tap diagnostic archive generator (action.sh)"
  - "Extended native APIs: provides zygisk_next_api.h for init-oriented processes and HyperOS Rust Runtime callbacks"
faq:
  - question: "Why should I use Zygisk Next instead of Magisk's built-in Zygisk?"
    answer: "Magisk's built-in Zygisk has well-known memory signatures that modern anti-tamper suites check for. Zygisk Next (Dr-TSNG/ZygiskNext) provides a standalone, modernized Zygisk daemon with stronger isolation, WebUI controls, and full support for KernelSU and APatch."
  - question: "How do I configure module unmounting in Zygisk Next?"
    answer: "When using KernelSU or APatch, manage unmounting using the manager's native Umount modules toggles or Zygisk Next's WebUI. On Magisk, add target apps to 'Configure DenyList' while keeping 'Enforce DenyList' disabled."
  - question: "Why is the module folder named zygisksu?"
    answer: "Zygisk Next uses the internal module ID 'zygisksu', so its installed module directory is /data/adb/modules/zygisksu/ and its runtime state directory is /data/adb/zygisksu/."
---

## Overview

Maintained under **Dr-TSNG/ZygiskNext** by the **LSPosed Developers**, **Zygisk Next** (`v1.5.3`) is a standalone, closed-source (Proprietary license since `v4-0.9.2`) implementation of the Android **Zygisk** module injection API.

Historically, Zygisk was strictly tied to Magisk's internal release cycle. As kernel-level root solutions (KernelSU, APatch) emerged and anti-root detection evolved, Zygisk Next was built as an independent injection engine delivering higher stealth, WebUI management, and cross-manager portability across Magisk, KernelSU, and APatch.

---

## Technical Architecture & How It Works

### Zygote Specialization & Daemon Architecture

Zygisk Next hooks directly into Android's process spawning lifecycle via its `zygiskd` daemon:

1. **Pre-Zygote & Service Initialization**: During `post-fs-data.sh`, `zygiskd daemon` initializes runtime state under `/data/adb/zygisksu/` (rotating `znctx` and `modules_info`), and `service.sh` completes `zygiskd service-stage` and registers `/data/adb/service.d/.zn_cleanup.sh`.
2. **Zygote Fork Hooking**: Attaches to 32-bit and 64-bit Zygote processes, intercepting app specialization routines (`preAppSpecialize`, `postAppSpecialize`).
3. **API Dispatch**: Loads registered Zygisk modules from `/data/adb/modules/*/zygisk/` and also exposes native `zygisk_next_api.h` hooks and HyperOS Rust Runtime callbacks.
4. **Mount Isolation Enforcement**: Enforces clean namespace unmounting for sensitive apps before untrusted processes inspect `/proc/mounts`.

---

## Installation & Setup

1. Verify version prerequisites before flashing (recovery installation is blocked by `customize.sh`):
   - **KernelSU**: Kernel `>= 10940` and `ksud >= 11575` (ensure Magisk is not also installed).
   - **APatch**: Version code `>= 10700`.
   - **Magisk**: Version code `>= 26402`, with built-in **Zygisk** toggled **OFF** and **Enforce DenyList** toggled **OFF**.
2. Download the latest `Zygisk-Next-1.5.3-*.zip` release from `Dr-TSNG/ZygiskNext`.
3. Flash the module inside your root manager app and reboot your device.

---

## Configuration & Usage

- **WebUI Management**: Open the Zygisk Next WebUI directly from KernelSU, APatch, or a WebUI-capable Magisk manager to inspect status and configure policies.
- **Diagnostic Bugreports**: Tapping the **Action** button runs `action.sh`, collecting kernel info, `zygiskd status`, `znctx`, and logs into a compressed `ZygiskNext-bugreport-*.tar.gz` archive.

---

## Troubleshooting & Common Issues

- **Install Aborts in Magisk/KernelSU**: Confirm you are not running multiple root managers simultaneously (KernelSU aborts if a `magisk` binary is detected in `PATH`) and that your manager meets the minimum version codes.
- **Modules Fail to Load**: Ensure built-in Magisk Zygisk is disabled, reboot once after upgrading, and generate a bugreport via the **Action** button to inspect `zygiskd status`.
