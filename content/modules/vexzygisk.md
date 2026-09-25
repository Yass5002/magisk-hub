---
id: "vexzygisk"
title: "VexZygisk: Pure C Standalone Zygisk Runtime with Custom Linker"
sidebarTitle: "VexZygisk"
description: "Pure C standalone Zygisk runtime for KernelSU and APatch featuring the custom csoloader linker to defeat anti-cheat and root detections."
category: "root-management"
tier: 1
searchQueries:
  - "vexzygisk kernelsu"
  - "lxiaoyao077 vexzygisk"
  - "rezygisk c rewrite"
  - "csoloader zygisk bypass detection"
  - "standalone zygisk apatch"
prerequisites:
  - "Root access via KernelSU or APatch"
conflicts:
  - "Other standalone Zygisk implementations (such as Zygisk Next or ReZygisk)"
configPaths:
  - "/data/adb/modules/vexzygisk/"
features:
  - "Pure C engine: rewritten from scratch in clean, modern C, eliminating C++ standard library overhead and reducing binary size"
  - "Custom csoloader dynamic linker: maps standard Zygisk module libraries into app address spaces without touching the system linker"
  - "Anti-detection stealth: defeats linker symbol scraping and library inspection hooks employed by modern mobile anti-cheat engines"
  - "Dual module loader path: routes standard Zygisk modules through csoloader while preserving system linker paths for Zygisk Next modules"
  - "Zero fork latency: delivers near-instantaneous Zygote process fork times with negligible memory and CPU overhead"
---

## Overview

In the KernelSU and APatch ecosystems, bringing Zygisk module support into the Android application lifecycle requires a standalone Zygisk injection daemon. However, many conventional Zygisk implementations load third-party `.so` module libraries directly through Android's standard system dynamic linker (`/linker` or `/linker64`). Because security scanners and anti-cheat systems inspect the dynamic linker's internal namespaces and `/proc/self/maps` memory regions, system-linked modules are easily exposed.

Developed by Lxiaoyao077 (derived from ReZygisk), **VexZygisk** is an advanced, standalone Zygisk implementation rewritten completely in pure **C**. It introduces a proprietary custom dynamic loader (**csoloader**) designed specifically to neutralize linker-based root detection.

## Key Architectural Innovations

### 1. Pure C Codebase
By eliminating the C++ standard template library (`libc++_shared.so`) and runtime dependencies, VexZygisk produces significantly smaller binaries that execute with lower memory overhead and tighter CPU cache locality during Zygote process forks.

### 2. The `csoloader` Custom Linker
When an application process forks from Android's Zygote daemon:
- **Standard Zygisk Modules**: Instead of calling `dlopen()` through the Android Bionic linker, VexZygisk maps and relocates ELF binaries manually via `csoloader`. This bypasses linker hooks and hides loaded module libraries from conventional linker inspection APIs.
- **Zygisk Next Modules**: Loads modules requiring official system linker ABI contracts through the standard path, ensuring 100% module ecosystem compatibility.

### 3. Dedicated Per-Root Compilation
Rather than shipping bloated hybrid scripts, VexZygisk compiles distinct, optimized builds tailored specifically for KernelSU or APatch.

## Installation & Conflict Warnings

- **Important Conflict**: You must **not** run VexZygisk concurrently with other Zygisk providers (such as Zygisk Next or ReZygisk). Disable any existing Zygisk modules before flashing.
- **Installation**:
  1. Download the latest `VexZygisk-*.zip` release from GitHub.
  2. Install via **KernelSU** or **APatch**.
  3. Reboot your device.
  4. Your favorite Zygisk modules (LSPosed, PlayIntegrityFix, Shamiko) will now load seamlessly.
