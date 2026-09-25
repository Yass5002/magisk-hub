---
id: "swap-disabler"
title: "Swap Disabler: Eliminate Swap & Virtual RAM for High-RAM Devices"
sidebarTitle: "Swap Disabler"
description: "Disables Android swap space, virtual RAM expansion (RAM Plus, Dynamic RAM), and unnecessary paging at boot on devices with 8GB–16GB+ RAM."
category: "performance-kernel"
tier: 1
searchQueries:
  - "swap disabler magisk"
  - "rompelhd swap disabler"
  - "disable ram plus samsung root"
  - "disable swap on android magisk"
  - "turn off zram virtual ram root"
prerequisites:
  - "Root access via Magisk"
  - "Device with sufficient physical RAM (8 GB or higher recommended)"
conflicts:
  - "Swap management modules (such as magisk-swapspace or SwapBoost-Pro)"
configPaths:
  - "/data/adb/modules/Swap-Disabler/"
features:
  - "Automated boot swap termination: executes kernel swapoff across active swap devices and loopback partitions during early system boot"
  - "Flash storage lifespan protection: prevents continuous background write cycles to internal UFS/eMMC chips"
  - "Micro-stutter elimination: prevents application threads from blocking on disk I/O when reading paged memory blocks"
  - "Optimized for modern flagships: frees CPU compression overhead on handsets equipped with 8 GB, 12 GB, 16 GB, or 24 GB of physical RAM"
  - "Pure systemless execution: applies commands through boot service scripts without altering system partition integrity"
---

## Overview

Many smartphone manufacturers aggressively market "Virtual RAM," "RAM Plus," or "Dynamic RAM Expansion," which allocate several gigabytes of internal flash storage as a secondary swap partition. On older devices with 2GB–3GB of physical RAM, swap can prevent out-of-memory crashes. However, on modern smartphones equipped with 8GB, 12GB, 16GB, or more of high-speed LPDDR physical RAM, swap is not only redundant—it actively hinders performance.

Because flash storage operates orders of magnitude slower than physical RAM, paging memory back and forth induces I/O latency, micro-stutters during app switching, and accelerates wear on the device's internal flash storage chips.

Developed by rompelhd, **Swap-Disabler** is a systemless Magisk module that automatically executes `swapoff` commands during startup, permanently disabling active disk swap files and virtual RAM mechanisms.

## Advantages of Disabling Swap on High-RAM Devices

1. **Eliminates Storage Wear**: Prevents hundreds of gigabytes of unnecessary background write operations to internal UFS flash over months of daily use.
2. **Smoother App Switching**: Applications kept in fast physical RAM wake up instantly without waiting for compressed flash pages to swap in.
3. **Reduces CPU Workload**: Eliminates the CPU cycles the kernel spends calculating compression algorithms and managing swap tables.

## Installation & Verification

1. Verify that your device has at least 8 GB of physical RAM.
2. Download the latest `Swap-Disabler-v*.zip` archive from GitHub releases.
3. Flash the package in **Magisk Manager**.
4. Reboot your device.
5. In Termux or an ADB shell, verify that swap has been disabled:
   ```bash
   su -c free -m
   ```
   *(The Swap row should report `0` total and `0` used).*
