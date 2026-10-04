---
id: "apatch"
title: "APatch: KernelPatch-Based Root Solution for Android Kernels & Boot Images"
sidebarTitle: "APatch"
description: "Revolutionary kernel-level root solution by bmax121 utilizing KernelPatch to patch stock boot images directly, featuring SuperKey security, KPM inline-hooking, and Magisk-compatible APM modules."
category: "root-management"
softwareType: "standalone-app"
tier: 1
searchQueries:
  - "apatch download apk"
  - "apatch root android"
  - "kernelpatch apatch guide"
  - "apatch superkey forgotten"
  - "apatch vs kernelsu vs magisk"
prerequisites:
  - "ARM64 architecture device"
  - "Linux kernel version 3.18 through 6.12"
  - "Kernel compiled with CONFIG_KALLSYMS=y"
  - "Unlocked bootloader and access to stock boot.img or init_boot.img"
conflicts:
  - "Concurrent root solutions (Magisk or KernelSU installed simultaneously on the same boot image)"
  - "Stock Samsung Knox security protections without custom vault bypass"
configPaths:
  - "/data/adb/ap/"
  - "/data/adb/modules/"
  - "/data/adb/ap/superkey"
features:
  - "Stock boot image patching: patches the kernel binary directly inside boot.img without requiring kernel source recompilation"
  - "SuperKey authentication: kernel-enforced cryptographic passphrase preventing unauthorized privilege escalation even if apps execute raw su commands"
  - "KPM (Kernel Patch Modules): injects dynamic C code into kernel memory with inline-hook and syscall-table-hook capabilities"
  - "APM (APatch Modules): full compatibility with standard systemless overlay filesystem modules"
  - "SELinux bypass in kernel space: avoids userspace SELinux policy tampering that triggers enterprise detection daemons"
faq:
  - question: "How does APatch differ from Magisk and KernelSU?"
    answer: "Magisk operates entirely in userspace by modifying the init binary in the ramdisk. KernelSU operates inside the kernel but historically requires building a custom kernel or using a GKI (Generic Kernel Image) device. APatch provides the best of both worlds: it operates directly inside the kernel like KernelSU, but achieves this by patching your stock boot.img using KernelPatch, requiring no custom kernel compilation."
  - question: "What is the APatch SuperKey and why is it mandatory?"
    answer: "The SuperKey is a private passphrase set during boot image patching. In APatch, the su binary communicates with the kernel driver via a privileged ioctl/syscall. If the requesting process cannot verify against the kernel-stored SuperKey hash, the kernel silently denies root access. This prevents malware from abusing su even in permissive environments."
  - question: "What should I do if my phone bootloops after installing an APM module?"
    answer: "APatch includes built-in Safe Mode recovery. Reboot your device and repeatedly press the Volume Down key as soon as the boot splash appears. APatch detects the key press and unmounts all active modules (`/data/adb/modules/`). Alternatively, flashing your stock, unpatched `boot.img` via fastboot instantly removes APatch without affecting your user data."
---

## Overview

**APatch**, developed by bmax121 and the open-source AndroidPatch team, is a next-generation Android root implementation that bridges the gap between Magisk's ease of installation and KernelSU's deep kernel-level stealth.

Traditional root solutions such as Magisk operate in userspace by intercepting `/init` in the boot ramdisk and dynamically modifying SELinux rules. Modern banking applications and Play Integrity hardware attestations continuously monitor userspace process trees and SELinux modifications.

KernelSU moved root privileges into kernel space (`task_struct->cred`), but required users to either compile a custom kernel from vendor source code or own a device running Google's standardized GKI (Generic Kernel Image, Linux 5.10+).

APatch resolves this dilemma through **KernelPatch**: a tool that analyzes and patches the kernel binary directly inside your stock `boot.img` or `init_boot.img`. It brings kernel-space root, inline kernel hooking, and systemless overlay capabilities to virtually any ARM64 device running Linux kernel 3.18 through 6.12.

---

## Architectural Comparison: Magisk vs. KernelSU vs. APatch

```
┌────────────────────────────────────────────────────────────────────────┐
│                                Userspace                               │
├───────────────────────┬────────────────────────┬───────────────────────┤
│        Magisk         │        KernelSU        │        APatch         │
│  - Patches /init      │  - KernelSU App (UI)   │  - APatch App (UI)    │
│  - magiskd daemon     │  - Minimal su stub     │  - Authenticated su   │
│  - Alters SELinux     │                        │  - Enforces SuperKey  │
├───────────────────────┴────────────────────────┴───────────────────────┤
│                               Kernel Space                             │
├───────────────────────┬────────────────────────┬───────────────────────┤
│        Magisk         │        KernelSU        │        APatch         │
│  - Stock untouched    │  - Compiled in-tree    │  - KernelPatch hook   │
│    kernel             │  - Hooks sys_read/exec │  - Inline hooks       │
│                       │  - GKI / source build  │  - KPM module support │
└───────────────────────┴────────────────────────┴───────────────────────┘
```

---

## Core Technologies

### 1. KernelPatch Binary Modification
KernelPatch statically disassembles the kernel binary embedded within your device's stock `boot.img`. By scanning for kernel symbol tables (`kallsyms`), it identifies crucial memory management, process credentials, and syscall dispatch vectors. It patches entry routines to divert control flow into KernelPatch's micro-hook engine without modifying kernel headers or recompiling.

### 2. SuperKey Cryptographic Isolation
In standard root environments, any process executing `su` prompts a root manager dialog or interacts with a local socket. APatch implements kernel-level privilege gating using a secret **SuperKey**:
- During initial patching in the APatch app, you specify a private passphrase (SuperKey).
- The hash of this key is embedded into the patched boot image.
- When an application requests root access, the APatch Manager authenticates against the kernel driver using this key.
- Without the correct SuperKey, the kernel's hook engine treats the process as completely unprivileged, rendering standard root detection heuristics ineffective.

### 3. Dual Module Architecture: KPM & APM
APatch introduces a two-tier modular architecture:
- **APM (APatch Modules)**: Traditional systemless filesystem modules built on OverlayFS. These share identical architecture with Magisk and KernelSU modules, allowing you to mount files over `/system` and `/vendor` without modifying storage blocks.
- **KPM (Kernel Patch Modules)**: Low-level C modules compiled to execute directly inside kernel space. KPM allows developers to inline-hook internal kernel functions, modify syscall behavior, or alter network socket buffers in real time.

---

## Step-by-Step Installation Guide

### Step 1: Extract Stock Boot Image
1. Download the official stock firmware package matching your device's exact build number.
2. Extract the boot image:
   - For devices launched with Android 13 or newer: locate `init_boot.img`.
   - For devices launched with Android 12 or older: locate `boot.img`.

### Step 2: Patch via APatch Manager
1. Download and install the latest official `APatch` APK release.
2. Open APatch and tap **Patch Boot Image**.
3. Select your extracted `boot.img` or `init_boot.img`.
4. Define your **SuperKey**. Ensure this passphrase is memorable; it is required to unlock root management inside the application.
5. Tap **Start**. The app runs KernelPatch to patch kernel offsets and outputs `apatch_patched_*.img` to your `Download/` folder.

### Step 3: Flash Patched Image
Connect your device to your workstation and reboot into bootloader (Fastboot) mode:

```bash
# If patching init_boot:
fastboot flash init_boot apatch_patched_*.img

# If patching boot:
fastboot flash boot apatch_patched_*.img

# Reboot device
fastboot reboot
```

6. Upon booting into Android, open the APatch app, enter your SuperKey, and grant Superuser permissions as needed.

---

## Safe Mode & Emergency Recovery

If a malformed APM module causes a bootloop:
1. Hard-reset your device by holding **Power + Volume Down**.
2. As soon as the manufacturer splash appears, repeatedly press and release **Volume Down**.
3. APatch detects the Safe Mode hardware key interrupt and disables all APM modules during early boot.
4. If a severe kernel panic occurs due to an experimental KPM module, flash your original, unpatched stock `boot.img` via fastboot:
   ```bash
   fastboot flash boot stock_boot.img
   fastboot reboot
   ```
   This immediately restores stock kernel operation without altering your apps, photos, or device settings.
