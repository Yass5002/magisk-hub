---
id: "yetanotherbootloopprotector"
title: "Yet Another Bootloop Protector (YABP): Multi-Stage Boot Failure Safeguard"
sidebarTitle: "Yet Another Bootloop Protector"
description: "Comprehensive bootloop and SystemUI failure prevention engine for Magisk, KernelSU, and APatch by rhythmcache, featuring marker-based crash recovery and recovery flashing triggers."
category: "root-management"
tier: 1
searchQueries:
  - "yetanotherbootloopprotector magisk"
  - "yabp bootloop protector rhythmcache"
  - "systemui failure protector magisk"
  - "disable all modules twrp yabp"
  - "magisk boot timeout recovery"
prerequisites:
  - "Android device rooted with Magisk, KernelSU, or APatch"
  - "Accessible `/data` partition for state marker tracking"
conflicts: []
configPaths:
  - "/data/adb/YABP/allowed-modules.txt"
  - "/data/adb/YABP/allowed-scripts.txt"
  - "/data/adb/systemui.monitor.disable"
  - "/data/local/tmp/service.log"
features:
  - "Marker-based bootloop tracking: creates progressive marker files across incomplete boots, automatically disabling modules upon the third failed attempt"
  - "Boot timeout watchdog: initiates automated disarming and reboot if the device fails to report boot completion within 120 seconds"
  - "Optional SystemUI monitor: actively monitors SystemUI process health, triggering recovery if the UI crashes repeatedly or freezes for >25 seconds"
  - "Comprehensive script disarming: resets file permissions on `service.d`, `post-fs-data.d`, `post-mount.d`, and `boot-completed.d` scripts to non-executable `644`"
  - "Recovery emergency trigger: flashing the module zip inside TWRP or OrangeFox instantly disables all modules and scripts for immediate manual rescue"
---

## Overview

Yet Another Bootloop Protector (YABP), developed by rhythmcache (`triple_fault`), is an automated watchdog module designed to protect rooted Android devices against bootloops, boot animation freezes, and SystemUI crashes caused by problematic Magisk, KernelSU, or APatch modules.

When modifying Android system components, incompatible SELinux rules, framework overlays, or vendor props can cause the operating system to stall during boot or crash in a loop. YABP acts as an automated safety net: it tracks boot completion state machines, enforces a maximum allowable boot duration, and automatically neutralizes rogue modules and scripts if the system cannot reach a stable interactive desktop.

## Prerequisites & Compatibility

- **Root Environments**: Magisk, KernelSU, and APatch.
- **Custom Recoveries**: Compatible with TWRP, OrangeFox, and PBRP for emergency rescue flashing.
- **Device Support**: Universal architecture compatibility across ARM, ARM64, and x86 devices.

There are no documented module conflicts.

## How YABP Works

### 1. Progressive Marker Mechanics
- At each boot startup, YABP checks for existing marker files in its working directory.
- If the previous boot did not reach the `boot_completed` stage, a marker file is recorded.
- If three markers accumulate (`marker1`, `marker2`, `marker3`), YABP declares a confirmed bootloop:
  - It creates a `disable` flag in every installed module directory in `/data/adb/modules/`.
  - It strips executable permissions from all custom scripts in `/data/adb/service.d/`, `/data/adb/post-fs-data.d/`, `/data/adb/post-mount.d/`, and `/data/adb/boot-completed.d/` (`chmod 644`).
  - It triggers a clean reboot so the device can boot into Android without third-party interference.

### 2. Boot Completion Timeout
YABP checks system status every 5 seconds. If Android does not broadcast `sys.boot_completed=1` within 2 minutes (120 seconds), YABP assumes the device is hung on the boot animation, executes the disarm routine, and reboots.

### 3. Optional SystemUI Crash Monitor
During module installation, users can enable the SystemUI Monitor. This watchdog checks the status of `com.android.systemui` every 5 seconds. If SystemUI remains crashed or inactive for more than 25 seconds, YABP neutralizes active modules to recover the display.
- To disable the monitor:
  ```bash
  su -c touch /data/adb/systemui.monitor.disable
  ```
- To re-enable the monitor:
  ```bash
  su -c rm -f /data/adb/systemui.monitor.disable
  ```

### 4. Recovery Rescue Flashing
If a device is stuck in recovery and you cannot access a shell, simply flashing `YetAnotherBootloopProtector-*.zip` in TWRP immediately disarms all modules and restores standard script permissions without requiring terminal commands.

## Configuration & Whitelists

To prevent mission-critical security or diagnostic modules from being disabled during automated recovery, add their IDs to:
- **Allowed Modules**: `/data/adb/YABP/allowed-modules.txt`
- **Allowed Scripts**: `/data/adb/YABP/allowed-scripts.txt`

Runtime execution logs are written to:
```bash
/data/local/tmp/service.log
```

## Troubleshooting & Limitations

- **Kernel-Level Hangs**: If a custom kernel panics before the filesystem is mounted or during early `init`, YABP cannot run. Such kernel panics require fastboot kernel reflashing.
- **Direct System Partition Modifications**: YABP guards against systemless modules; it cannot repair destructive modifications made directly to physical `/system` or `/vendor` partitions.
