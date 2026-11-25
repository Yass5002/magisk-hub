---
id: "fde-ai"
title: "FDE.AI (FeraDroid Engine): Adaptive Systemless Android Optimizer"
sidebarTitle: "FDE.AI"
description: "Standalone root optimizer APK (com.feravolt.fdeai) providing adaptive AI kernel, VM, CPU/GPU governor, thermal cooldown, and power management without modifying the system partition."
category: "performance-kernel"
tier: 1
searchQueries:
  - "fde ai apk download"
  - "feradroid engine magisk kernelsu"
  - "fde ai kernel vm optimizer"
  - "fde ai cooldownservice downscaleservice"
  - "fde ai charging bypass root"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch (Shizuku non-root mode is also supported with reduced kernel-level capabilities)"
  - "ARM64 (`arm64-v8a`) or ARMv7 (`armeabi-v7a`) Android device"
conflicts:
  - "Other active kernel/scheduler tuning apps or scripts (e.g., Franco Kernel Manager scripts, Konabess/scene daemon profiles)"
  - "Enabling Charging Bypass simultaneously with Battery Life Cycle Extender (mutually exclusive inside FDE.AI)"
configPaths:
  - "/data/data/com.android.system.optimizer/"
  - "/data/adb/fdeai/"
features:
  - "Real-time AI process detection classifying foreground applications as heavy or light to dynamically switch CPU/GPU governors, DDR/L3/UFS boosts, and read-ahead parameters"
  - "Dedicated background services including `CooldownService`, `DownscaleService`, `SoundService`, and `AutorunService` with Quick Settings tiles and floating performance overlays"
  - "Dynamic virtual memory (VM) tuner, Dynamic Read-Ahead (for 8GB+ RAM devices), ART/FS optimizer during screen-off charging, and built-in Universal Debloater lists"
  - "Configurable throttling temperature limits, Force Doze, background app killing, Battery Life Cycle Extender (6% resume hysteresis), and direct Charging Bypass"
faq:
  - question: "Does FDE.AI modify the `/system` partition or require flashing a ZIP?"
    answer: "No. FDE.AI is distributed as a standalone APK (`FDE.AI-v26.08.1.apk`, internal namespace `com.feravolt.fdeai`, packaged as `com.android.system.optimizer`). All kernel, sysfs, VM, and scheduler tweaks are applied dynamically at runtime in a systemless manner without touching `/system`."
  - question: "What is the difference between Root mode and Shizuku mode in FDE.AI?"
    answer: "In Root mode (via `libsu` with Magisk, KernelSU, or APatch), FDE.AI executes its bundled native binaries (`libfcore.so`, `libfdeinit.so`, `libfbusybox.so`, `libprofilehelper.so`) with superuser privileges to tune kernel nodes, CPU/GPU frequencies, DDR/L3/UFS buses, VM parameters, and charging hardware switches. Shizuku mode provides limited userland and `WRITE_SECURE_SETTINGS` optimizations where direct kernel sysfs writes are unavailable."
---

## Overview

**FDE.AI** (**FeraDroid Engine**), developed by **feravolt**, is a cross-platform, systemless Android optimization application designed to balance performance and battery efficiency based on real-time device telemetry and usage patterns. Unlike static `init.d` or `sysctl` scripts that hardcode identical parameters for every device, FDE.AI inspects hardware capabilities and software state at runtime so each device receives tailored tuning.

All active performance boosts automatically disengage when the display turns off, minimizing idle battery drain.

---

## Technical Architecture & Core Components

Inspection of `FDE.AI-v26.08.1.apk` confirms a multi-process Kotlin/Compose application backed by `libsu`, Shizuku (`rikka.shizuku.ShizukuProvider`), AndroidHiddenApiBypass, and native ELF libraries for both `arm64-v8a` and `armeabi-v7a`:

- **Native Execution Layer**:
  - `libfcore.so` and `libfdeinit.so`: Core native tuning engine and initialization routines.
  - `libfbusybox.so`: Bundled BusyBox binary (`Brutal_busybox`, GPLv2) used for deterministic shell and sysfs operations across varied Android environments.
  - `libprofilehelper.so`: Hardware/profile detection helper.
- **Dedicated Android Services & Processes**:
  - `:CooldownService` (`com.feravolt.fdeai.services.main.CooldownService`): Thermal relief and cooldown routine accessible via `TileServiceCooldown`.
  - `:DownscaleService` (`com.feravolt.fdeai.services.main.DownscaleService`): Display resolution/refresh-rate scaling (`60, 90, 120, 144 Hz` metadata support).
  - `:SoundService` (`com.feravolt.fdeai.services.main.SoundService`): Audio subsystem tuning and receiver (`SoundReceiver`).
  - `AutorunService` & `BootReceiver`: Restores configured AI profiles after `BOOT_COMPLETED` or `MY_PACKAGE_REPLACED`.
  - `OverlayServiceMainFloating` / `OverlayServiceTopFloating`: Real-time FPS and telemetry overlays.

### Adaptive AI & Kernel Tuning Functions

1. **Process Detection & Machine Learning**: Monitors the foreground application in real time to classify workloads as heavy (games/rendering) or light (messaging/browsing), adjusting system profiles automatically in AI Auto mode or according to user-defined per-app overrides.
2. **CPU Turbo, GPU Turbo & Bus Boosts**: Tunes CPU/GPU governors and minimum frequency floors under high load while respecting thermal thresholds. On supported SoCs, enables **DDR/L3/UFS boost** in performance mode.
3. **Throttling Control**: Optionally relaxes OS-level thermal throttling during sustained heavy workloads while enforcing user-configured temperature safety ceilings (automatically bypassed if the device overheats or is charging).
4. **Dynamic VM & Read-Ahead**: Continuously adjusts Linux virtual memory (`vm.*`) sysctl parameters based on live RAM utilization. On devices with **8 GB+ RAM**, dynamically increases block device `read_ahead_kb` during heavy app usage and restores defaults on exit.
5. **Screen-Off & Battery Lifecycle Management**:
   - **Force Doze / System Power Saver / System Data Saver / Background App Killer**: Aggressive idle power savings triggered when the screen turns off.
   - **ART & FS Optimizer**: Runs ART dexopt (`max` filter) manually or automatically, and schedules filesystem optimization (`fstrim`/FS checks) while the screen is off and charging.
   - **Battery Life Cycle Extender vs. Charging Bypass**: Caps maximum charge percentage (resuming when battery drops 6% below the set limit) or routes charger power directly to the system during gaming to reduce battery heat. These two modes are mutually exclusive.

---

## Installation & Setup

1. Download `FDE.AI-v26.08.1.apk` and install it normally on your Android device.
2. Grant **Superuser** permission in **Magisk**, **KernelSU**, or **APatch** when prompted on first launch (or authorize **Shizuku** for non-root mode).
3. Review and accept the EULA, select an initial preset (Balanced, Performance, or Power Saving), and grant notification/overlay permissions if you intend to use Quick Settings tiles (`TileServiceAiMode`, `TileServiceCooldown`, `TileServiceMainOverlay`) or FPS overlays.
4. Optionally configure temperature limits, per-app heavy/light classifications, and charging controls in the app settings.

---

## Verification & Operational Checks

Verify that FDE.AI services are running and inspect current kernel/VM values via an elevated ADB shell:

```bash
# Check active FDE.AI processes and services
su -c "ps -ef | grep -E 'fdeai|optimizer'"

# Inspect current VM and block read-ahead settings
su -c "cat /proc/sys/vm/swappiness; cat /sys/block/sda/queue/read_ahead_kb 2>/dev/null"

# Verify Doze state when screen-off Force Doze is enabled
dumpsys deviceidle get deep
```

> **Note**: FDE.AI is proprietary software. Do not combine it with other aggressive kernel or thermal-disabling modules that write conflicting values to `/sys/devices/system/cpu/` or `/proc/sys/vm/`.
