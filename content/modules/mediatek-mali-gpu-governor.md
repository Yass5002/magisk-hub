---
id: "mediatek-mali-gpu-governor"
title: "Mediatek Mali GPU Governor (天玑GPU调速器)"
description: "Dynamic GPU governor module for MediaTek Dimensity processors featuring ARM Mali GPUs, optimizing frequency scaling, power consumption, and thermal stability under heavy gaming loads."
category: "performance-kernel"
author: "Seyud & Tools-cx-app"
version: "v2.12.3"
updatedAt: "2026-10-04"
compatibility: ["KernelSU", "APatch", "Magisk"]
---

## Overview & System Architecture

The **MediaTek Mali GPU Governor (天玑GPU调速器)**, developed by Seyud in collaboration with Tools-cx-app, is a low-level kernel governor optimization module designed specifically for MediaTek Dimensity SoCs utilizing ARM Mali graphics architectures (Valhall and 5th Gen Mali, such as Mali-G77, G78, G610, G710, G715, and Immortalis-G720).

Stock MediaTek GPU governors (such as `ged` and `simple_ondemand`) frequently suffer from either excessive thermal throttle step-downs or sluggish frequency ramp-up latency. This module interacts directly with MediaTek kernel sysfs nodes (`/sys/devices/platform/13000000.mali/` or `/sys/kernel/ged/hal/`) to implement fine-grained frequency tuning, power-aware rendering queues, and adaptive workload balancing.

## Key Performance Capabilities

1. **Adaptive Frequency Scaling**: Eliminates frame stutter by ramping Mali GPU clock frequencies proactively upon scene load spikes.
2. **Thermal-Aware Throttling Softening**: Replaces abrupt GPU frequency drops with smooth step-down curves, preventing jarring FPS fluctuations during extended gaming sessions.
3. **Energy Efficiency Tuning**: Adjusts DVFS (Dynamic Voltage and Frequency Scaling) tables to run at high-efficiency sweet-spot frequency bins.

## Installation & Verification

### Step 1: Flashing the Package
Flash the module zip via KernelSU, APatch, or Magisk Manager.

### Step 2: Verify Active Governor Sysfs
Reboot the device and check the GPU governor status:
```bash
cat /sys/kernel/ged/hal/gpu_boost_level
# or inspect active Mali governor
cat /sys/class/misc/mali0/device/devfreq/13000000.mali/governor
```

### Step 3: Monitor In-Game Frequencies
```bash
watch -n 1 "cat /sys/class/misc/mali0/device/devfreq/13000000.mali/cur_freq"
```

## Compatibility Notes

- **Supported Platforms**: MediaTek Dimensity series (Dimensity 1100/1200, 8100/8200/8300, 9000/9200/9300).
- **Incompatible Platforms**: Qualcomm Snapdragon (Adreno GPUs) and Samsung Exynos (Xclipse/AMD RDNA GPUs).
