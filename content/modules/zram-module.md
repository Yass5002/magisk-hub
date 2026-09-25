---
id: "zram-module"
title: "ZRAM Module: Custom Kernel Compression Algorithms & Sizing Manager"
sidebarTitle: "ZRAM Module"
description: "Configures custom ZRAM sizing and dynamically loads kernel compression algorithm modules (lz4kd, zstdn) at boot without modifying system partitions."
category: "performance-kernel"
tier: 1
searchQueries:
  - "zram module magisk"
  - "furlc zram-module"
  - "android load custom zram algorithm"
  - "lz4kd zstdn zram kernel"
  - "kernelsu custom zram size module"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "Android kernel compiled with ZRAM support and loadable module support (CONFIG_MODULES=y)"
conflicts: []
configPaths:
  - "/data/adb/modules/ZRAM-Module/"
features:
  - "Dynamic kernel module loading: automatically detects and inserts custom out-of-tree compression driver modules (.ko) such as lz4kd and zstdn at boot"
  - "Custom ZRAM capacity allocation: easily customize the total in-memory compressed swap disk size"
  - "Reduced decompression overhead: leverages advanced compression algorithms to achieve faster memory page retrieval times"
  - "Zero partition modification: executes all modprobe routines and sysfs parameter binding systemlessly"
  - "Dual root compatibility: operates natively under both Magisk and KernelSU environments"
---

## Overview

ZRAM is an essential Linux kernel feature that creates a virtual compressed block device inside physical RAM. By compressing inactive memory pages rather than writing them to slow flash storage, ZRAM effectively expands usable RAM and keeps applications alive in the background.

However, stock Android kernels are typically locked to standard `lz4` or `lzo-rle` compression algorithms, and fixed ZRAM sizes cannot easily be altered without recompiling the entire boot image. Furthermore, custom kernel developers who compile optimized out-of-tree compression drivers (such as `lz4kd` or `zstdn`) face challenges distributing these drivers cleanly.

Developed by FurLC, **ZRAM-Module** is a specialized performance utility for Magisk and KernelSU. It automates the loading of custom compression kernel modules (`.ko`) during early startup and configures custom ZRAM block sizes systemlessly.

## Key Capabilities

1. **Automated `.ko` Driver Insertion**: The module searches its internal directory during early boot and executes `insmod` / `modprobe` on bundled compression algorithm drivers (such as `lz4kd.ko` or `zstdn.ko`).
2. **Dynamic Algorithm Binding**: Once the driver is registered in the kernel crypto API, the module binds it directly to `/sys/block/zram0/comp_algorithm`.
3. **Flexible Sizing**: Allows users to specify an exact ZRAM block size (e.g., 4GB, 6GB, 8GB) before initializing `swapon`.
4. **Ideal for Custom Kernels**: Perfect for users running custom kernels designed for performance and low-latency gaming.

## Installation & Configuration

1. Download the latest `ZRAM-Module-v*.zip` archive from GitHub releases.
2. Install the package in **Magisk** or **KernelSU**.
3. Reboot your device.
4. Verify the active compression algorithm and ZRAM allocation in Termux:
   ```bash
   su -c cat /sys/block/zram0/comp_algorithm
   su -c free -m
   ```
