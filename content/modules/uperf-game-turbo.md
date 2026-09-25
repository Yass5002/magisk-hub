---
id: "uperf-game-turbo"
title: "Uperf Game Turbo: Userspace Performance & Scheduler Controller"
sidebarTitle: "Uperf Game Turbo"
description: "Dynamic userspace performance daemon reading raw Linux touch events and SurfaceFlinger hooks to adjust CPU/GPU frequencies and cpuset thread affinity."
category: "performance-kernel"
tier: 1
searchQueries:
  - "uperf game turbo magisk"
  - "uperf governor tuning android"
  - "uperf powercfg sh balance"
  - "yinwanxi uperf game turbo"
  - "android userspace performance controller"
prerequisites:
  - "Android 6.0 or newer"
  - "64-bit architecture (arm64-v8a)"
  - "Magisk 20.4+ or direct root shell access for manual deployment"
  - "Supported SoC hardware platform (pre-tuned configurations available for popular Qualcomm, MediaTek, Exynos, and Tensor chipsets)"
conflicts:
  - "Automated touch simulation or screen tap macro apps (can cause touch report dropout in the input reader)"
  - "MIUI 12 launcher unresponsiveness when sfanalysis is enabled (workaround: delete /data/adb/modules/uperf/enable_sfanalysis)"
  - "Conflicting third-party kernel frequency boost modules (should be disabled to prevent conflicting governors)"
configPaths:
  - "/sdcard/Android/yc/uperf/cur_powermode.txt"
  - "/sdcard/Android/yc/uperf/uperf_log.txt"
  - "/data/powercfg.sh"
  - "/data/adb/modules/uperf/"
  - "/data/adb/modules/uperf/enable_sfanalysis"
features:
  - "Direct Linux input polling: reads raw hardware touch signals from the kernel input subsystem to detect taps and swipes instantly"
  - "SurfaceFlinger frame hook: tracks rendering start, lag, and completion via sfanalysis hooks to preempt frame drops"
  - "Dynamic thread migration: binds active UI-rendering threads to big/prime CPU cores during scrolling"
  - "Granular power modes: switches between auto, balance, powersave, performance, and fast states"
  - "Scene toolbox integration: full compatibility with Scene per-application performance profiles"
faq:
  - question: "Does Uperf increase battery consumption during device standby?"
    answer: "No. Uperf is designed with low standby overhead. In sleep states, its profiles reduce the number of active CPU cores woken by background alarms and use conservative frequency ramp-up curves, slightly improving standby battery life."
  - question: "What should I do if my touch screen becomes unresponsive on MIUI 12?"
    answer: "This is a documented compatibility issue between MIUI 12's proprietary launcher and the SurfaceFlinger hook. To resolve it, delete /data/adb/modules/uperf/enable_sfanalysis and reboot your device."
---

## Overview

Forked and modernized by **yinwanxi** (based on the original project by **Matt Yang**), **Uperf Game Turbo** is a userspace governor and performance controller for Android.

Stock Linux kernel governors often react too slowly to sudden user interaction, leading to micro-stutters during app launches or intensive gaming. Uperf replaces reactive kernel boost routines with intelligent userspace scene detection. By listening directly to raw touch input events, SurfaceFlinger frame pacing, and cpuset transitions, it boosts frequencies and binds threads precisely when workload spikes occur.

---

## Technical Architecture & How It Works

### Userspace Telemetry & Sysfs Node Management

Uperf bypasses Android's high-level framework to monitor hardware load with minimal latency:

1. **Direct Touch Polling**: Reads event packets directly from `/dev/input/event*`. When a touch contact or fling gesture is detected, Uperf immediately commands the CPU governor to ramp up clocks before Android's UI rendering pipeline even requests a new frame.
2. **SurfaceFlinger Analysis (`sfanalysis`)**: Hooks into the Android `surfaceflinger` compositor process. It tracks frame production deadlines, immediately detecting rendering latency or buffer stalls and boosting GPU and CPU frequency targets to avoid dropped frames.
3. **Cpuset & Thread Affinity Optimization**: Automatically binds the active application's UI thread and render thread to high-efficiency or performance core clusters (big/prime cores) while isolating background tasks onto little cores.
4. **Sysfs Node Abstraction**: Employs chipset-specific JSON configurations tailored to individual SoC architectures (Snapdragon, Dimensity, Google Tensor, Exynos) to modulate frequency tables, energy-aware scheduling (EAS) parameters, and thermal margins.

---

## Installation & Setup

### Method 1: Magisk / KernelSU / APatch
1. Download the latest `Uperf-Game-Turbo-*.zip` release.
2. Flash the module via your root manager and reboot.
3. After reboot, check `/sdcard/Android/yc/uperf/uperf_log.txt` to confirm that the daemon has initialized and recognized your SoC platform.

### Method 2: Standalone Shell Execution
Uperf does not require Magisk and can be installed on custom embedded environments or rooted stock ROMs:
1. Extract the package to `/data/uperf`.
2. Set execute permissions (`chmod 755 *.sh`).
3. Run `sh /data/uperf/setup_uperf.sh` followed by `sh /data/uperf/run_uperf.sh`.

---

## Configuration & Practical Usage

### Power Mode Switching

Uperf provides five operational power profiles:
- `auto`: Dynamically scales performance based on active foreground application demand.
- `balance`: Slightly smoother than stock OEM scheduling while conserving power.
- `powersave`: Minimizes energy draw while preserving essential UI fluidity.
- `performance`: Aggressive frequency scaling prioritized for competitive gaming.
- `fast`: Highly responsive profile optimized for touch response.

#### Changing the Default Power Mode
Edit the text file located at:
```bash
/sdcard/Android/yc/uperf/cur_powermode.txt
```
Replace the content with your preferred mode (e.g. `balance` or `auto`) and reboot.

#### Live Mode Switching
Switch modes dynamically from a root terminal without rebooting:
```bash
sh /data/powercfg.sh balance
```
*(Also fully compatible with Scene / Omarea VTools for per-app automated mode switching).*

---

## Troubleshooting & Common Issues

- **MIUI 12 Touchscreen Lockup**: If the home screen stops responding to touch on MIUI 12 devices, delete `/data/adb/modules/uperf/enable_sfanalysis` and reboot to disable the SurfaceFlinger hook while keeping userspace governor controls active.
- **Unsupported Hardware**: If installation halts with an `unsupported` platform warning, your device's SoC lacks a pre-compiled JSON profile under `/data/uperf/config/`.
