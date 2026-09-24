---
id: "magisk-frida"
title: "Magisk-Frida: Systemless Frida Server for Reverse Engineering"
sidebarTitle: "Magisk-Frida"
description: "Packs and runs the frida-server daemon systemlessly on rooted Android devices with auto-updating architecture and root companion scripts."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "magisk frida module download"
  - "frida server rooted android guide"
  - "virb3 magisk frida"
  - "run frida server on boot android"
  - "android app dynamic instrumentation"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "PC with Python and `frida-tools` installed (`pip install frida-tools`)"
conflicts:
  - "Manual background frida-server instances running on port 27042"
configPaths:
  - "/data/adb/modules/magisk-frida/"
  - "/data/local/tmp/frida-server"
features:
  - "Automatically runs the official native `frida-server` binary on device boot"
  - "Supports ARM, ARM64, x86, and x86_64 architectures with automatic CPU detection"
  - "Binds to localhost or all interfaces (`0.0.0.0`) for tethered USB and wireless debugging"
  - "Essential runtime instrumentation suite for dynamic security audits, hooking, and memory dumping"
faq:
  - question: "How do I connect to Frida from my computer?"
    answer: "Ensure your phone has USB debugging enabled, connect it via USB, and run `frida-ps -U` on your computer terminal. You will immediately see a list of running processes."
  - question: "Can banking apps detect frida-server running?"
    answer: "Yes, many anti-tamper SDKs scan for standard Frida TCP ports (27042) or look for frida-server named pipes in /proc/net/tcp. If you need stealth Frida for protected apps, consider ZygiskFrida or patching the frida-server binary string names."
---

## Overview

Maintained by **ViRb3**, **Magisk-Frida** is the premier module for security researchers, penetration testers, and reverse engineers who utilize the **Frida** dynamic instrumentation toolkit on Android.

Ordinarily, running `frida-server` on Android requires manually pushing the binary to `/data/local/tmp/`, setting execute permissions, and running it inside an interactive ADB shell that dies as soon as the terminal is closed. Magisk-Frida integrates `frida-server` into Android's systemless boot sequence, launching it as a supervised background daemon whenever your device powers on.

---

## Technical Architecture & How It Works

### Supervised Daemon Architecture

1. **Architecture Detection**: During module installation, Magisk-Frida probes `ro.product.cpu.abi` and selects the matching upstream `frida-server` binary for your hardware architecture.
2. **Boot Service Initialization**: During the `service.sh` late-boot phase, the module starts `frida-server` using a detached daemon process:
   ```bash
   /data/adb/modules/magisk-frida/frida-server -D
   ```
3. **SELinux Domain Assignment**: Sets appropriate SELinux context (`u:r:magisk:s0`) so frida-server can attach to target processes, inject companion `.so` libraries, and read memory mappings without triggering kernel security violations.

---

## Installation & Quickstart

### Step 1: Install the Module
1. Download `Magisk-Frida-vX.zip`.
2. Flash it in **Magisk**, **KernelSU**, or **APatch** and reboot.

### Step 2: Test from your Workstation
1. Install Frida tools on your computer:
   ```bash
   pip install frida-tools
   ```
2. Connect your phone via USB with ADB enabled.
3. Verify connection:
   ```bash
   frida-ps -U
   ```
4. Hook an app:
   ```bash
   frida -U -f com.example.targetapp -l hook.js
   ```
