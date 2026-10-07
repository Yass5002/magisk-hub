---
id: "violetbox-root-toolbox"
title: "VioletBox Root Toolbox: Advanced All-in-One Root Administration Utility"
description: "Comprehensive all-in-one Android root utility by Smart-Paocai featuring SELinux mode management, raw partition reading/flashing, baseband font backup, module batch flashing, and device ID modification."
category: "system-utilities"
author: "Smart-Paocai"
version: "1.0.0"
updatedAt: "2026-10-04"
compatibility: ["Magisk", "KernelSU", "APatch"]
---

## Overview & System Architecture

**VioletBox**, authored by developer Smart-Paocai, is an advanced mobile root utility toolbox created for power users, ROM modders, and device maintainers. Built as the mobile standalone counterpart to the Violet PC Toolkit, VioletBox consolidates dozens of low-level Android administration operations into a unified graphical interface requiring no tethered computer.

## Key Built-in Capabilities

1. **SELinux Mode Controller**: Free switching between Enforcing and Permissive SELinux states with persistent boot-time automation.
2. **Partition Management**: Visual partition browser supporting raw direct read, write, dump, and erase operations on physical eMMC/UFS storage blocks.
3. **Baseband & Word Stock Backup**: Creates full binary dumps of modem, persist, and NVRAM/EFS partitions formatted for emergency recovery via Qualcomm EDL (9008) mode or bootloader flashing.
4. **Batch Root Module Manager**: Batch installs, updates, and manages modules across Magisk, KernelSU, and APatch environments.
5. **Application Management**: Privileged app freezer, uninstaller, APK extractor, and background process controller.
6. **Global Device & ID Spoofing**: Built-in device parameter masquerading and Android ID modification.
7. **Cloud OTA Extractor**: Fast cloud-based payload extraction from Android OTA zip packages.

## Installation & Setup

### Step 1: Install APK
Download and install `VioletBox_V1.0.0_release.apk`.

### Step 2: Grant Root Privileges
Launch VioletBox and grant permanent Superuser access when prompted by Magisk, KernelSU, or APatch.

### Step 3: SELinux Verification
Test SELinux switching in the UI, then verify via terminal:
```bash
getenforce
```

## Safety Notice

> [!CAUTION]
> The Partition Management and Raw Block Write utilities write directly to physical storage partitions (`/dev/block/bootdevice/by-name/`). Flashing invalid images to critical partitions (such as `boot`, `abl`, `xbl`, or `modem`) can cause hard bricking. Always verify partition names carefully before executing write operations.
