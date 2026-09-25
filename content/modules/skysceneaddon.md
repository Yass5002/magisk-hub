---
id: "skysceneaddon"
title: "SkyScene Add-on: Advanced Android Kernel Memory & ZRAM Optimization"
sidebarTitle: "SkyScene Add-on"
description: "Optimizes kernel memory management, ZRAM swapping algorithms, LRU/MGLRU page reclaim, and cgroup process queues for legacy and modern ARM devices."
category: "performance-kernel"
tier: 1
searchQueries:
  - "skyscene addon magisk"
  - "weirdmidas skysceneaddon"
  - "mglru zram optimization android"
  - "android memory thrashing fix root"
  - "kernelsu ram management module"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "ARM or ARM64 Android device running Linux kernel 4.x, 5.x, or 6.x"
conflicts: []
configPaths:
  - "/data/adb/modules/SkySceneAddon/"
features:
  - "Multi-generation memory support: contains optimized heuristics for modern MGLRU (cgroups v2) and legacy page reclaim (LRU / cgroups v1)"
  - "Memory thrashing elimination: regulates dirty page writeouts and kswapd wakeup cycles to prevent catastrophic UI stutter under heavy multitasking"
  - "ZRAM & swap stream tuning: optimizes compressed in-memory swap streams to balance decompression latency and memory density"
  - "LMK queue harmony: coordinates kernel memory pressure notifications with Android userspace Low Memory Killer (LMK) queues"
  - "Universal systemless tuning: applies dynamic sysctl and sysfs memory tunables at late service boot without modifying system partitions"
---

## Overview

One of the primary causes of severe frame drops, UI freezes, and sudden app terminations on Android is **memory thrashing**—a pathological condition where the Linux kernel spends more CPU cycles frantically compressing pages into ZRAM and evicting file-backed caches than actually running user applications. Stock Android OEM memory management configurations often suffer from poorly calibrated reclaim thresholds that aggravate this issue.

Developed by WeirdMidas, **SkySceneAddon** (SkyScene Add-on) is a specialized memory management optimization module. Designed to bridge the gap between legacy and modern Android kernel generations, it implements proven formulas to streamline swapping, page cache reclaim, and ZRAM compression.

## Architecture & Optimizations

### 1. Modern vs. Legacy Kernel Tuning
- **Modern Hardware (MGLRU & cgroup v2)**: Fine-tunes Multi-Gen LRU generation scan intervals and cost-benefit ratios, allowing Linux 5.10+ kernels to accurately identify inactive memory pages.
- **Legacy Platforms (Active/Inactive LRU & cgroup v1)**: Calibrates classic twin-list page scanner parameters to minimize CPU spinlocks on older 32-bit and 64-bit devices.

### 2. ZRAM Data Compression & Paging
- Adjusts anonymous memory swap thresholds (`vm.swappiness`) and cache pressure (`vm.vfs_cache_pressure`).
- Ensures that read-heavy application code pages are preserved in RAM while infrequently accessed background heaps are efficiently compressed into ZRAM.

### 3. Thrashing Prevention & LMK Harmony
- Synchronizes kernel memory event reporting with userspace Low Memory Killer (`lmkd`) daemons.
- Avoids premature process termination while guaranteeing that foreground gaming and camera workloads always have immediate access to unfragmented memory pages.

## Installation & Support

- **Supported Root Solutions**: Fully compatible with **Magisk** and **KernelSU**.
- **Installation**:
  1. Download `SkyScene.Add-on.zip` from GitHub releases.
  2. Flash the module in your root manager and reboot.
  3. The service script automatically detects your active kernel capabilities (LRU vs MGLRU) and applies the matching optimization profile.
