---
id: "debugassistant"
title: "DebugAssistant: Automated Multi-Boot Logcat Capture & Crash Telemetry"
sidebarTitle: "DebugAssistant"
description: "Autonomous logcat capture utility that logs early boot sequences and retains diagnostic traces across three rolling reboot cycles for crash debugging."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "debugassistant magisk module"
  - "thepedroo debugassistant"
  - "capture early boot logcat android root"
  - "debug random reboot bootloop magisk"
  - "multi boot logcat rotation android"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "Android 8.0 or higher"
conflicts: []
configPaths:
  - "/data/adb/modules/debugassistant/"
features:
  - "Automatic boot logging: begins recording logcat streams during early service init without requiring a connected PC or USB ADB bridge"
  - "Three-cycle rolling retention: rotates logs across DebugAssistant.log, DebugAssistant-Boot1.log, and DebugAssistant-Boot2.log"
  - "Crash & bootloop diagnosis: preserves previous boot traces so logs from a crash or sudden panic survive the subsequent reboot"
  - "Automated redaction: filters out common user-sensitive tokens before writing traces to disk"
---

## Overview

Diagnosing intermittent system server panics, sudden kernel reboots, or early framework crashes on Android is difficult when using traditional desktop debugging tools. By the time a developer connects an ADB cable after a reboot, the active in-memory logcat ring buffer has been wiped clean, destroying all evidence of the fatal exception.

Developed by ThePedroo, **DebugAssistant** turns your rooted Android smartphone into a self-recording diagnostic system. Running silently during the earliest phases of Magisk/KernelSU initialization, DebugAssistant streams logcat output directly to persistent flash storage, maintaining a rolling archive across three consecutive boot cycles.

## 3-Boot Rolling Retention Architecture

To ensure diagnostic traces are never overwritten before you can inspect them, DebugAssistant maintains a cyclic log rotation:

- **`DebugAssistant-Boot2.log`**: Traces captured during the most recent (current) system startup.
- **`DebugAssistant-Boot1.log`**: Logs captured during the preceding boot cycle.
- **`DebugAssistant.log`**: The oldest preserved log file from two boots prior.

After the third consecutive boot, the oldest archive is pruned, ensuring that diagnostic records never consume excessive flash storage while guaranteeing that post-crash data is always safely preserved.

## Common Use Cases

- **Random Kernel Reboots**: Pinpoint which system service, vendor HAL, or background process triggered a hardware watchdog reboot.
- **Faulty Module Diagnostics**: Inspect what failed right before Zygote crashed when troubleshooting newly flashed customization packages.
- **Offline Field Testing**: Capture real-time application crashes and framework exceptions while mobile, without keeping a laptop connected.

## Installation & Log Retrieval

1. Download and flash the `DebugAssistant` `.zip` archive via **Magisk** or **KernelSU**.
2. Reboot your device. Logging begins automatically.
3. To view or retrieve captured logs, navigate to the module directory using a root file manager or terminal:
   ```bash
   su -c ls -l /data/adb/modules/debugassistant/
   ```
4. View the newest boot log directly:
   ```bash
   su -c cat /data/adb/modules/debugassistant/DebugAssistant-Boot2.log | grep -E "FATAL|AndroidRuntime"
   ```
