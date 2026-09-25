---
id: "clearbox"
title: "ClearBox: High-Speed System Cleaning, File Classification & Disk GC Suite"
sidebarTitle: "ClearBox"
description: "Comprehensive system cleaning and filesystem maintenance engine offering rule-based cache suppression, deep file categorization, disk GC, and terminal TUI control."
category: "system-utilities"
tier: 1
searchQueries:
  - "clearbox magisk module"
  - "flycom-e clearbox"
  - "android f2fs disk gc cleaner root"
  - "clearbox wipe cache configs"
  - "terminal tui android system cleaner"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
  - "Android 8.0 or higher"
  - "Terminal emulator (Termux) for TUI or companion Android application"
conflicts: []
configPaths:
  - "/data/adb/wipe_cache/"
  - "/data/adb/wipe_cache/CleanConfigs/"
  - "/data/adb/wipe_cache/FileConfigs/"
  - "/data/adb/modules/ClearBox/"
features:
  - "One-key system optimization: rapidly cleans temporary application junk, thumbnails, empty directories, and triggers kernel disk GC"
  - "Custom rule-based directory sweeping: allows users to define custom purge targets via simple text files in CleanConfigs"
  - "Deep file categorization & size filters: groups and purges specific file extensions based on min/max byte thresholds in FileConfigs"
  - "Ultra-low-overhead scheduler: automated maintenance managed by a lightweight Timed background process without daemon bloat"
  - "Full terminal TUI: launch an interactive, colorized management dashboard by typing ClearBox in any root terminal"
---

## Overview

Traditional mobile cleaning utilities frequently demand full-time foreground services, display intrusive advertisements, and merely purge superficial cache folders while leaving deep system residues and fragmented storage unaddressed.

Developed by FLYCOM-E, **ClearBox** is an open-source, high-throughput system maintenance suite for rooted Android devices. Built for speed and flexibility across Magisk, APatch, and KernelSU, ClearBox provides deep filesystem junk removal, empty folder elimination, customized path purging, and filesystem garbage collection (GC) through an interactive terminal interface (TUI) or an optional companion APK.

## Core Capabilities

### 1. High-Speed Cache & Junk Elimination
- **Third-Party App Cache Sweeping**: Purges accumulated WebView caches, network buffers, and thumbnail databases across installed applications without wiping persistent user data or login states.
- **Empty Directory Pruning**: Recursively sweeps internal and external storage to remove empty folder trees created by uninstalled applications.
- **Disk Garbage Collection (GC)**: Triggers filesystem-level garbage collection on modern F2FS partitions to consolidate data blocks and improve read/write latency.

### 2. Custom Directory Rules (`CleanConfigs`)
Users can declare specific folders or cache locations for automated purging by dropping text rule files into `/data/adb/wipe_cache/CleanConfigs/`:
- Supports initial root anchor definitions (`@/sdcard/Download/temporary`).
- Line-by-line relative and absolute file paths allow precise rule-based targeting.

### 3. Deep File Classification (`FileConfigs`)
Under `/data/adb/wipe_cache/FileConfigs/`, users can create `.conf` profiles to filter and purge files by extension and size boundaries:
```conf
# Target archive files between 10MB and 1GB
@MAX=1/G @MIN=10/M
zip 7z

# Remove specific temporary installation extensions regardless of size
@max=-1
apk tmp
```

## Management Interfaces

ClearBox does not require a persistent graphical app, offering two convenient modes:

1. **Interactive Terminal TUI**:
   Open Termux or an ADB shell, acquire root privileges, and invoke the tool:
   ```bash
   su -c ClearBox
   ```
   This launches an interactive, menu-driven console interface allowing you to run one-key cleaning, manage whitelists, and review storage statistics.
2. **Graphical Companion App**:
   An optional graphical management application is available during module setup for users who prefer Android UI navigation.

## Installation & Setup

1. Download the latest `ClearBox` release ZIP from GitHub.
2. Flash the module using **Magisk**, **APatch**, or **KernelSU**.
3. Reboot your device.
4. Launch Termux, run `su -c ClearBox`, and execute your first one-key system optimization pass.
