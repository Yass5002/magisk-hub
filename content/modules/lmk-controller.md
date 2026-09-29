---
id: "lmk-controller"
title: "LMK Controller: Android Memory-Pressure Profiles"
sidebarTitle: "LMK Controller"
description: "Detect Android's LMK or LMKD path and apply selectable memory-pressure profiles through Magisk or KernelSU."
category: "performance-kernel"
tier: 1
searchQueries:
  - "LMK Controller Magisk"
  - "ferrdishx LMK Controller"
  - "Android LMKD tuning module"
  - "low memory killer KernelSU"
  - "Android PSI LMKD profiles"
prerequisites:
  - "Android 8.0 or later according to the upstream README"
  - "Magisk 20.4 or later, or KernelSU"
  - "A compatible module manager with WebUI support for the interactive interface"
  - "A recovery path and a backup before changing memory-management parameters"
conflicts:
  - "Other modules or vendor scripts that change LMK, LMKD, ZRAM, swappiness, or VM parameters"
  - "Kernel variants that expose none of the detection paths documented upstream"
configPaths:
  - "/data/adb/modules/lmk_controller_feerd/lmk_mode"
  - "/data/adb/lmk_controller/service.log"
  - "/data/adb/service.d/lmk_controller.sh"
features:
  - "Detects classic LMK, PSI LMKD, and legacy LMKD paths"
  - "Provides Gamer, Stable, and Normal profiles"
  - "Persists the selected profile and reapplies it at boot"
  - "Snapshots supported values and restores them during uninstall"
  - "Includes a WebUI dashboard for compatible module managers"
faq:
  - question: "Which root solutions does the release support?"
    answer: "The upstream README explicitly lists Magisk 20.4+ and KernelSU. It also notes compatibility issues under Kitsune Mask, so this guide does not list Kitsune as supported."
  - question: "What does the module change?"
    answer: "Depending on the detected kernel path and selected profile, it can change classic LMK minfree thresholds, ro.lmk.* properties, swappiness, VM settings, and ZRAM compression. The exact values are profile- and RAM-dependent."
  - question: "How can I tell which path was detected?"
    answer: "Check the boot or service log under /data/adb/lmk_controller/service.log and compare it with the documented detection nodes: /sys/module/lowmemorykiller/parameters/minfree and /proc/pressure/memory."
  - question: "What should I do if apps reload more often or the device becomes unstable?"
    answer: "Switch to the Normal profile or disable the module, then reboot. Remove competing memory-tuning modules and inspect the service log before testing another profile."
  - question: "Is the WebUI required?"
    answer: "The module can apply its saved profile through its boot scripts, but the upstream installation instructions recommend MMRL, KSU WebUI, or another compatible module manager for the interactive controls."
---

## Overview

LMK Controller tunes Android memory pressure without claiming that one profile is optimal for every device. The release identifies three paths:

- **Classic LMK** when `/sys/module/lowmemorykiller/parameters/minfree` exists.
- **PSI LMKD** when `/proc/pressure/memory` exists.
- **Legacy LMKD** when neither node is available.

The module then applies the selected Gamer, Stable, or Normal profile and records diagnostics. Its v1.4.1 release includes the detection and persistence logic, a WebUI, and snapshot/restore handling for supported values.

## Installation

1. Record the current device behavior and create a recovery plan.
2. Download `LMK_Controller-v1.4.1.zip` from the upstream release.
3. Flash it through Magisk, KernelSU, MMRL, or a compatible module manager.
4. Reboot.
5. Open the module WebUI, select a profile, and apply it.

The upstream README lists Android 8.0+, Magisk 20.4+, and KernelSU as requirements. A compatible WebUI-capable manager is needed for the interactive controls.

## Verification

Inspect the service log and saved mode:

```sh
su -c 'cat /data/adb/lmk_controller/service.log'
su -c 'cat /data/adb/modules/lmk_controller_feerd/lmk_mode'
```

The upstream README also documents these checks:

```sh
su -c 'getprop ro.lmk.low'
su -c 'getprop ro.lmk.medium'
su -c 'getprop ro.lmk.critical'
su -c 'getprop ro.lmk.psi_partial_stall_ms'
```

Do not compare the values with another device and assume that the same thresholds are safe. The module scales parts of its profiles based on detected RAM and kernel path.

## Compatibility and recovery

LMK and LMKD behavior is vendor- and kernel-dependent. Other memory, ZRAM, performance, or gaming modules may overwrite the same settings or make diagnosis difficult. Kitsune Mask compatibility is explicitly under investigation upstream and is not treated as supported here.

If the device becomes unstable, select Normal or disable the module from the root manager and reboot. If Android cannot boot, use the root manager's safe-mode mechanism or a compatible recovery environment. The upstream release includes uninstall logic intended to remove its service entry and restore its captured state, but recovery procedures still depend on the device and root solution.

## Sources

- [Upstream README](https://github.com/ferrdishx/LMK-Controller)
- [Upstream release](https://github.com/ferrdishx/LMK-Controller/releases/tag/v1.4.1)
- [Upstream source](https://github.com/ferrdishx/LMK-Controller)
