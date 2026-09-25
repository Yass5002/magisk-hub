---
id: "magnetar"
title: "MAGNETAR: Machine-Learning Adaptive Kernel & Device Performance Optimizer"
sidebarTitle: "MAGNETAR"
description: "All-in-one autonomous kernel optimization engine that uses lightweight machine learning to dynamically balance CPU, GPU, and memory states across Android 5.0 through modern releases."
category: "performance-kernel"
tier: 1
searchQueries:
  - "magnetar magisk module"
  - "kyliekyler magnetar"
  - "kernel optimizer machine learning android"
  - "magnetar ksu apatch"
  - "magnetar bugreport"
prerequisites:
  - "Android 5.0 (API 21) or higher"
  - "ARM or ARM64 processor architecture"
  - "Magisk 26404+, KernelSU 11422+, or APatch 10472+"
conflicts:
  - "Concurrent CPU governor tweakers, thermal throttling bypass modules, or background task scheduler tuners"
configPaths:
  - "/data/adb/modules/MAGNETAR/"
features:
  - "Autonomous workload scheduling: machine learning models classify foreground user demand to apply real-time governor parameter adjustments"
  - "Full hardware scope: synchronizes CPU cluster scaling, GPU render thresholds, memory compaction, and I/O scheduler queues"
  - "Zero configuration necessity: self-calibrating background daemon operates out of the box without requiring manual profile switching"
  - "Integrated diagnostic CLI: built-in command line tooling (`magnetar --bugreport`) captures system metrics and kernel node status for triage"
---

## Overview

MAGNETAR, authored by Kyliekyler, is an autonomous kernel tuning engine built for rooted Android platforms. While traditional performance scripts rely on static sysfs tweaks or rigid profile switches triggered by manual triggers, MAGNETAR uses lightweight machine learning heuristics to monitor user interaction patterns and dynamically shape kernel scheduler parameters in real time.

Operating transparently in the background, MAGNETAR aims to deliver low-latency touch response during active gaming and UI navigation, while ramping down aggressive frequency stepping and I/O polling during screen-off and sustained idle periods.

## Prerequisites & Compatibility

MAGNETAR is built to be broadly compatible across Android generations and root frameworks:

- **Operating System**: Android 5.0 (Lollipop, API 21) up to current Android releases.
- **CPU Architecture**: 32-bit ARM and 64-bit ARM (ARM64).
- **Root Solutions**:
  - Magisk v26.4 (build 26404) or later
  - KernelSU build 11422 or later
  - APatch build 10472 or later

### Conflict Considerations

Because MAGNETAR writes dynamic governors, energy-aware scheduling (EAS) parameters, and virtual memory tunings directly to `/sys` and `/proc`, running it concurrently with other aggressive performance managers (such as conflicting Uperf profiles, Scene governor scripts, or manual thermal mitigations) can lead to race conditions where scripts overwrite each other's tunings. Ensure any other general-purpose kernel tweakers are removed before flashing.

## Installation & Architecture

MAGNETAR is packaged as a standard flashable module zip:

1. Flash the release package via Magisk, KernelSU, or APatch manager.
2. Reboot the device to initialize the background daemon.
3. The module establishes its working directory and runtime hooks inside:
   ```bash
   /data/adb/modules/MAGNETAR/
   ```

Upon boot, MAGNETAR probes hardware capabilities—detecting CPU cluster layouts, available scaling governors, GPU sysfs interfaces, and RAM sizes—and launches its monitoring service to supervise workload states.

## Diagnostics & Commands

MAGNETAR includes native command-line tooling accessible via any root shell (`su`):

- **Capture Diagnostic State**:
  ```bash
  su -c magnetar --bugreport
  ```
  This command evaluates sysfs node bindings, confirms active daemon operations, and dumps a sanitized log file for submission when reporting issues to the project maintainers.

## Common Pitfalls & Recommendations

- **Thermal Throttling**: MAGNETAR optimizes scheduler response times and governor ramps, but it does not disable hardware thermal trip points. Devices with poor heat dissipation will still throttle according to vendor hardware limits.
- **Battery Drain on First Day**: Following installation, the heuristics daemon monitors baseline user interaction cycles. Allow 24–48 hours of normal usage before evaluating battery consumption changes.
