---
id: "hyperoptimize"
title: "HyperOptimize: System & Kernel Parameter Optimization for HyperOS"
sidebarTitle: "HyperOptimize"
description: "Tunes HyperOS kernel parameters, SurfaceFlinger rendering, wakelocks, and I/O scheduling to minimize background power consumption."
category: "performance-kernel"
tier: 1
searchQueries:
  - "hyperoptimize magisk"
  - "hyperos battery optimization module"
  - "tatshsiow hyperoptimize"
  - "hyperos kernel tweaks power saving"
  - "xiaomi hyperos battery saver magisk"
prerequisites:
  - "Root access via Magisk 20.4+ or KernelSU 0.6.6+"
  - "Xiaomi, Redmi, or POCO device running Xiaomi HyperOS"
  - "Anti-bootloop module installed as a recommended safety precaution"
conflicts:
  - "Nakixii Pandora Kernel"
  - "Other kernel or power optimization modules with duplicate sysctl tweaks"
configPaths:
  - "/data/adb/modules/HyperOptimize/"
features:
  - "Targeted power reduction: reconfigures system and kernel tunables to curb excessive battery drain rather than pushing artificial benchmarks"
  - "SurfaceFlinger & rendering adjustments: tunes graphics queue parameters to reduce GPU active cycles during idle screen states"
  - "Logging and wakelock suppression: lowers redundant debugging logcat overhead and mitigates aggressive background wakeups"
  - "I/O and CPU governor scheduling: adjusts Linux scheduler energy profiles to favor energy-efficient CPU cluster residency"
  - "Pure systemless execution: applies configuration scripts at late service boot without modifying the physical system or vendor partitions"
---

## Overview

Xiaomi's HyperOS incorporates deep system services, background telemetry, and aggressive animation engines that can generate substantial idle power drain, particularly on devices running early or unoptimized vendor firmware.

Created by TatshSiow, **HyperOptimize** is a systemless tuning module engineered to optimize kernel and operating system parameters with a single objective: reducing power consumption and extending battery longevity. Rather than aiming for peak gaming performance, HyperOptimize reins in unnecessary background activity, verbose logging, and aggressive wakeups across Xiaomi, Redmi, and POCO smartphones running HyperOS.

## Core Tuning Mechanisms

The module executes during late boot (`service.sh`) to apply targeted adjustments:

1. **Kernel & Scheduler Efficiency**: Reconfigures CPU governor downscaling rates and scheduler frequencies to keep background tasks on efficiency cores whenever demanding foreground workloads subside.
2. **SurfaceFlinger & GPU Rendering**: Optimizes frame dispatch queues and display composition parameters to prevent GPU pipeline thrashing during static UI display.
3. **Wakelock & Telemetry Throttling**: Restricts non-critical system broadcast wakeups and reduces continuous debug logging in user builds.
4. **I/O Storage Scheduling**: Adjusts block device read-ahead queues and writeback timers to minimize repetitive flash storage wake cycles.

## Installation & Safeguards

HyperOptimize alters low-level kernel parameters. An anti-bootloop safeguard module is strongly advised before flashing.

1. Download `HyperOptimize_v*.zip` from the project's official releases.
2. Open **Magisk Manager** or **KernelSU Manager**.
3. Install the module archive from internal storage.
4. Reboot your device.

## Known Conflicts

- **Nakixii Pandora Kernel**: HyperOptimize has documented conflicts with Nakixii Pandora custom kernels due to competing governor parameters.
- **Overlapping Performance Modules**: Do not run HyperOptimize concurrently with other all-in-one optimizer modules that write conflicting `sysctl` or `/sys/devices/system/cpu/` nodes.

## Recovery

If your device fails to boot or encounters instability after installation:
1. Boot into custom recovery (TWRP/OrangeFox) or run `adb reboot recovery`.
2. Open the recovery file manager or terminal.
3. Remove the module directory at `/data/adb/modules/HyperOptimize`.
4. Reboot the device.
