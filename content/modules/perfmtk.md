---
id: "perfmtk"
title: "PerfMTK: MediaTek Kernel, Mali GPU, Touch Digitizer & Thermal Bypass Engine"
sidebarTitle: "PerfMTK"
description: "Hardware performance and thermal orchestration suite tailored for MediaTek Dimensity and Helio SoCs, featuring Mali GPU boost, digitizer overclocking, and charging thermal bypass."
category: "performance-kernel"
tier: 1
searchQueries:
  - "perfmtk magisk module"
  - "juaniman perfmtk"
  - "mediatek dimensity performance module root"
  - "mali gpu ged hal boost magisk"
  - "perfmtk charge bypass battery care"
prerequisites:
  - "MediaTek SoC with Mali GPU (Helio or Dimensity series)"
  - "Android 9.0 (Pie) through Android 15/16 with Linux kernel 4.14 to 6.1+"
  - "Root access via Magisk (v27+ recommended), KernelSU, or APatch"
  - "KernelSU & APatch require a magic mount helper module (Hybrid Mount or Mountify)"
conflicts: []
configPaths:
  - "/data/adb/modules/perfmtk/config/app_profiles.conf"
  - "/data/adb/modules/perfmtk/config/performance.conf"
  - "/data/adb/modules/perfmtk/config/balanced.conf"
  - "/data/adb/modules/perfmtk/config/powersave.conf"
features:
  - "4-tier app detection: tracks foreground application focus using LSPosed hooks, Netlink process connectors (cn_proc), or cgroup inotify"
  - "Hardware digitizer booster: unlocks touch sampling up to 480Hz/2160Hz via direct touchpanel ioctl calls and unpins touch IRQs from Little cores"
  - "Smart fast charge bypass: charges device at high speeds while routing thermal load away from battery cells to keep pack temperatures under 36°C"
  - "Predictive Thermal Guardian: monitors real-time temperature slopes (ΔT/Δt) to adjust frequencies smoothly and prevent sawtooth throttling"
  - "Exclusive MediaTek knobs: configures DRAM DVFSRC LPDDR5X bus clocks, Mali GED HAL frequency margins, and /sys/kernel/fpsgo drivers"
  - "Interactive terminal TUI & CLI: complete command-line suite for live telemetry streaming, profile selection, and thermal overrides"
---

## Overview

Unlike Qualcomm Snapdragon chipsets—which benefit from ubiquitous custom kernel development and standardized energy-aware scheduling—MediaTek Dimensity and Helio platforms rely on proprietary OEM drivers such as MediaTek Game Boost Engine (GBE), GED HAL, DVFSRC memory controllers, and the `fpsgo` frame prediction subsystem. Generic Android performance scripts frequently fail on MediaTek silicon because they attempt to tune non-existent Qualcomm sysfs nodes.

Developed by JUANIMAN, **PerfMTK** is an engineering-grade performance and energy orchestration daemon created specifically for MediaTek SoCs. PerfMTK taps directly into low-level MediaTek kernel drivers, unlocking digitizer polling rates, managing memory bus scaling up to 8533 MHz, and providing hardware charge bypass to protect battery longevity during competitive 120 FPS gaming.

## Core Hardware Subsystems & Capabilities

### 1. 4-Tier Foreground Detection
PerfMTK dynamically switches profiles between **Performance**, **Balanced**, **Powersave**, and **Powersave+** by monitoring the active foreground application. It implements a prioritized detection cascade:
1. **LSPosed Hook (`PerfMTK-Hook`)**: Instantaneous in-process window manager hook.
2. **Netlink Process Connector (`cn_proc`)**: Kernel-level socket listener tracking process fork and exec events.
3. **cgroup.procs inotify**: File-descriptor polling on kernel cgroup hierarchies.
4. **Adaptive Debounced Fallback**: Polling loop for non-standard environments.

### 2. Touch Digitizer & IRQ Isolation
- **Touch Sampling Unlock**: Directly interfaces with digitizer drivers (`/dev/xiaomi-touch`, `/proc/touchpanel`, `/sys/class/touch/touch_dev`, Samsung TSP) to engage maximum sampling rates (480Hz to 2160Hz).
- **IRQ Affinity Unpinning**: Prevents touch input interrupts from clustering onto efficiency cores, preventing thread preemption and micro-stutters during high-cadence touch gestures.

### 3. Thermal Bypass & Battery Care
- **Gaming Charge Bypass**: Permits full-speed charging during gaming sessions while intelligently managing current thresholds to hold battery temperatures between 31°C and 36°C.
- **Configurable Cutoff Guard**: Enforces an emergency hardware cutoff (default 52°C).
- **Battery Care**: Sets an upper charge ceiling (e.g., stopping charging automatically at 80%) to minimize battery degradation over time.

### 4. MediaTek Specific Hardware Knobs
- **DRAM DVFSRC**: Dynamically scales LPDDR5X RAM clock frequencies up to 8533 MHz during texture-heavy workloads.
- **Mali GPU & GED Tuning**: Adjusts `dvfs_margin_value` and `gpu_boost_level` on Linux 5.x and 6.x kernels.
- **FPSGO Optimization**: Adaptive configuration of `/sys/kernel/fpsgo` governor nodes on Android 14 through Android 16.

## Terminal CLI Usage (`perfmtk`)

Launch the interactive dashboard or execute profile changes via root terminal (`su -c perfmtk`):

```bash
# Apply operating profiles manually
su -c perfmtk performance
su -c perfmtk balanced
su -c perfmtk powersave

# Manage Smart Fast Charge Bypass
su -c perfmtk --charge-bypass on      # Force charging bypass during gaming
su -c perfmtk --charge-bypass off     # Revert to standard charging
su -c perfmtk --charge-bypass status  # Query current thermal bypass state

# Configure Battery Care charge limiter (e.g., cap at 80%)
su -c perfmtk --battery-care on 80
su -c perfmtk --battery-care off

# Manage Predictive Thermal Guardian
su -c perfmtk --tg on 75 2            # Target 75°C with max 2 clamp steps
su -c perfmtk --tg status             # Display real-time thermal slope

# Telemetry streaming
su -c perfmtk -s                      # Live formatted status snapshot
su -c perfmtk --stream 1000           # Stream telemetry as JSON every 1000ms
```

## Configuration & Profile Customization

Profiles are defined in plain-text configuration files stored under `/data/adb/modules/perfmtk/config/`:
- **`app_profiles.conf`**: Maps package identifiers to performance profiles and flags (e.g., `com.tencent.ig=performance;thermal=off;touch=game`).
- **`performance.conf` / `balanced.conf`**: Houses raw CPU governor definitions, frequency boundaries, and UCLAMP minimum/maximum scheduling weights.
