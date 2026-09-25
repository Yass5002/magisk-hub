---
id: "hydro-br-leur"
title: "Hydro-Brûleur: Custom Kernel & Display Booster for MediaTek / Snapdragon Xiaomi Devices"
sidebarTitle: "Hydro-Brûleur"
description: "Hardware-specific performance optimization module engineered for Xiaomi and Redmi devices running custom kernels (Yuni, AngelBeats, Pandora) with MediaTek fpsgo and Iris display processor tuning."
category: "performance-kernel"
tier: 1
searchQueries:
  - "hydro brûleur magisk module"
  - "hydro-br-leur aestasbritannia"
  - "redmi k60 ultra corot kernel module"
  - "iris_configs.xml magisk"
  - "yuni angelbeats pandora kernel optimization"
prerequisites:
  - "Supported Xiaomi, Redmi (e.g. Corot / K60 Ultra), or select OnePlus/Realme Snapdragon devices"
  - "Custom kernel environment (Yuni Kernel, AngelBeats Kernel, Pandora Kernel) or compatible stock kernel"
  - "Magisk 26300+ or KernelSU"
conflicts:
  - "Unsupported OEM devices outside specified MediaTek Dimensity and Snapdragon hardware branches"
  - "Third-party FPS booster modules overwriting MediaTek fpsgo or Iris display chip configurations"
configPaths:
  - "/data/adb/modules/scene_systemless/settings.txt"
  - "/data/adb/modules/scene_systemless/"
features:
  - "Intelligent kernel detection: inspects uname strings during installation to tailor system props and power tables for Yuni, AngelBeats, or Pandora kernels"
  - "MediaTek fpsgo & perfmgr tuning: remaps DDR frequency tables and targets 48, 60, 90, and 120 FPS targets for consistent frame pacing"
  - "Pixelworks Iris display chip calibration: injects tuned `iris_configs.xml` and helper routines to optimize MEMC and display engine pipelines"
  - "Dynamic cloud mode routing: switches booster configuration JSON files based on detected kernel build timestamps and revision flags"
---

## Overview

Hydro-Brûleur, developed by AestasBritannia alongside community kernel contributors (Shadow3, Mly, M7recRAB, Ski, and Hamjin), is a specialized hardware-level optimization module for Xiaomi, Redmi, and select BBK devices. Rather than applying generic Linux VM sysctl parameters across disparate phones, Hydro-Brûleur focuses specifically on devices such as the Redmi K60 Ultra ("corot") and paired Xiaomi platforms.

The module inspects the active Linux kernel build string during flashing, reconfiguring its payload to interface with custom kernels—specifically Yuni Kernel, AngelBeats Kernel, and Pandora Kernel—and targeting low-level subsystems like MediaTek `mtk_fpsgo` frame scheduling and Pixelworks Iris display coprocessors.

## Prerequisites & Compatibility

Hydro-Brûleur is strictly scoped to compatible hardware and kernel environments:

1. **Hardware**: Xiaomi / Redmi devices featuring supported SoCs (notably MediaTek Dimensity platforms like Dimensity 9200+ on the K60 Ultra, alongside select OnePlus and Realme targets).
2. **Kernel**:
   - Stock kernel with MediaTek `fpsgo` and `perfmgr` interfaces.
   - Or custom kernels: **Yuni Kernel**, **AngelBeats Kernel**, or **Pandora Kernel** (both Open and Beta variants).
3. **Root Framework**: Magisk v26.3 (26300) or higher, or KernelSU.

### Documented Incompatibilities

Flashing Hydro-Brûleur on unrelated OEM devices (such as Samsung, Google Pixel, or Motorola) or generic AOSP GSIs is explicitly unsupported. Its installer scripts make direct modifications to vendor power profiles (`powercontable.xml`) and vendor display configs that will not execute correctly on non-target platforms.

## Internal Architecture & Functionality

During deployment (`customize.sh`), the module performs deep hardware introspection:

- **Kernel Probing**: Reads `uname -r` to identify custom kernel signatures (`Yuni`, `AngelBeats`, or `Pandora`). If a custom kernel is detected, it patches active service scripts in `/data/adb/modules/<kernel_id>/service.sh`, unsets conflicting touch idle timers, and aligns frequency bound nodes.
- **Iris Display Chip Management**: Deploys `iris_helper.sh` and custom `iris_configs.xml` trees to leverage hardware display coprocessors for display interpolation and refresh rate stabilization.
- **MediaTek Frame Scheduling**: Converts generic `perfmgr_mtk` sysfs references to modern `mtk_fpsgo` targets, dynamically adjusting DDR bus remapping tables for 48, 60, 90, and 120 FPS render pipelines.

## Configuration & Paths

Hydro-Brûleur maintains its configuration files and working state inside:
```bash
/data/adb/modules/scene_systemless/
```
Module runtime flags and historical user settings are parsed from:
```bash
/data/adb/modules/scene_systemless/settings.txt
```

## Troubleshooting & Verification

- **Kernel Signature Mismatches**: If you change or update your custom kernel after installing Hydro-Brûleur, reinstall the module from your root manager. The installer generates configuration paths specifically tied to the kernel string present at install time.
- **Display Desync or Stutter**: Ensure no competing display rate forcing apps or third-party frame rate limiters are active, as these interfere with Iris display helper routines and MediaTek DDR frequency remapping.
