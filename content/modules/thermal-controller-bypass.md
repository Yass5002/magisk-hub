---
id: "thermal-controller-bypass"
title: "Thermal Controller Disabler (温控拜拜)"
description: "Systemless thermal management remover created by AiWanJi ToolBox to bypass thermal throttling, eliminate thermal limit configuration files, and prevent aggressive CPU/GPU downclocking."
category: "performance-kernel"
author: "Xiao Bai Yang / AiWanJi (小白杨(爱玩机))"
version: "183.72"
updatedAt: "2026-10-04"
compatibility: ["Magisk", "KernelSU", "APatch"]
---

## Overview & System Architecture

**Thermal Controller Disabler (温控拜拜)** is a performance optimization module developed by Xiao Bai Yang (小白杨), creator of the acclaimed AiWanJi ToolBox (爱玩机工具箱). Android OEMs implement restrictive thermal daemon policies that aggressively throttle CPU and GPU frequencies, dim screen brightness, and limit charging currents once battery temperature reaches 38°C–42°C.

This module uses systemless overlay mounting to neutralize vendor thermal policy files located in `/vendor/etc/`. By substituting active thermal control tables with clean dummy files, the operating system's thermal engine (`thermald` / `thermal-engine`) cannot trigger frequency capping policies, allowing devices to sustain peak performance during competitive gaming and intensive 3D rendering.

## Inspected Archive Components

Analysis of the flashable package reveals comprehensive neutralization of vendor thermal configuration tables:

- `/system/vendor/etc/thermal-phone.conf` (Standard mobile usage governor)
- `/system/vendor/etc/thermald-devices.conf` (Device thermal sensor mappings)
- `/system/vendor/etc/thermal-chg-only.conf` (Charging current thermal throttle)
- `/system/vendor/etc/thermal-4k.conf` (4K/8K video recording thermal caps)
- `/system/vendor/etc/thermal-camera.conf` & `thermal-per-camera.conf` (Camera thermal protection)
- `/system/vendor/etc/thermal-normal.conf` & `thermal-per-normal.conf` (General performance envelope)
- `/system/vendor/etc/thermal-video.conf` & `thermal-per-video.conf` (Video playback throttling)
- `/system/vendor/etc/thermal-map.conf` & `thermal-navigation.conf` (GPS navigation thermal restrictions)
- `/system/vendor/etc/thermal-class0.conf` & `thermal-per-class0.conf` (Low-power threshold policies)

## Key Performance Advantages

1. **Sustained Frame Rates**: Prevents sudden 120 FPS to 60 FPS drops during prolonged sessions in demanding games (*Genshin Impact*, *Honkai: Star Rail*, *PUBG Mobile*).
2. **Prevents Screen Dimming**: Disables automatic ambient brightness reduction triggered when the display panel reaches OEM thermal thresholds.
3. **Maintains Fast Charging Speeds**: Neutralizes `thermal-chg-only.conf`, ensuring fast charging rates remain active even when the screen is in use.

## Installation & Verification

### Step 1: Flashing the Module
Flash via Magisk, KernelSU, or APatch. The `install.sh` script automatically unzips all neutralized config files into `$MODPATH`.

### Step 2: Verify File Overlay
After rebooting, check that the `/vendor/etc/` thermal files have been mounted from the module:
```bash
ls -la /vendor/etc/thermal-normal.conf
# File size should reflect the module's neutralized configuration
```

### Step 3: Verify Governor Frequencies Under Load
Run a CPU burn-in or launch a heavy 3D benchmark while observing CPU frequencies:
```bash
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq
```

## Thermal Safety & Hardware Cautions

> [!WARNING]
> While this module disables software-level thermal throttling policies, modern SoCs have internal hardware-level thermal fuses (typically around 95°C–105°C) that prevent physical silicone damage. However, prolonged operation at extreme temperatures can accelerate lithium battery degradation. It is strongly recommended to use an external semiconductor cooling fan during extended gaming sessions.
