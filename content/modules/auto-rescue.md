---
id: "auto-rescue"
title: "Auto Rescue: Automated Bootloop Watchdog and Module Recovery"
sidebarTitle: "Auto Rescue"
description: "Kernel and init startup watchdog that tracks boot cycles, detects system crashes, and automatically disables unstable Magisk/KernelSU modules to prevent soft bricks."
category: "system-utilities"
tier: 1
searchQueries:
  - "auto rescue magisk"
  - "magisk bootloop saver"
  - "automatic brick rescue magisk"
  - "recover from bootloop kernelsu"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other aggressive bootloop-saving modules executing simultaneous killall commands"
configPaths:
  - "/data/adb/modules/Automatic_brick_rescue/Number_of_starts.log"
  - "/data/adb/modules/Automatic_brick_rescue/whitelist.conf"
  - "/data/adb/modules/Automatic_brick_rescue/Automatic_brick_rescue.sh"
features:
  - "Monitors early-stage Android init execution through post-fs-data and late-service stages"
  - "Tracks boot attempts via persistent filesystem counter in Number_of_starts.log"
  - "Places .disable trigger files in third-party module directories upon detecting crash thresholds"
  - "Configurable whitelist allows mission-critical root daemons to stay enabled during recovery"
  - "Built-in 30-minute grace delay after OTA system updates prevents false-positive disables"
faq:
  - question: "How does Auto Rescue determine that the device is in a bootloop?"
    answer: "During early boot (post-fs-data), the module increments a persistent boot attempt counter. If the operating system fails to reach the sys.boot_completed=1 state and reboots repeatedly, the counter exceeds the allowable threshold, triggering an emergency disable routine across all non-whitelisted modules."
  - question: "How can I prevent a critical module from being disabled?"
    answer: "Add the directory name of your essential module (as found in /data/adb/modules/) to /data/adb/modules/Automatic_brick_rescue/whitelist.conf. Any module ID specified in the whitelist is skipped during rescue execution."
---

## Overview

**Auto Rescue** (originally authored by Han and Qingfeideyic, maintained by Fendou Youth on 52pojie: https://www.52pojie.cn/thread-1600094-1-1.html) is an automated systemless watchdog designed to recover Android devices from soft bricks and bootloops caused by incompatible Magisk, KernelSU, or APatch modules.

When modifying low-level Android framework libraries, audio effects, or system properties, a malfunctioning script can cause the Zygote process to crash or the SystemUI daemon to hang indefinitely. Without custom recovery (TWRP/OrangeFox) or USB debugging enabled, users often face full data wipes to restore booting. Auto Rescue eliminates this risk by executing autonomous health checks during the bootloader handoff and init sequence.

---

## Technical Architecture & How It Works

Auto Rescue divides its supervisory responsibilities across two stages of the Android boot sequence:

### 1. Early Boot Stage (post-fs-data.sh)

When the root manager executes `post-fs-data.sh`, the root filesystem is mounted read-write in `/data`. Auto Rescue inspects its persistent state directory:

1. **Attempt Logging**: It reads `/data/adb/modules/Automatic_brick_rescue/Number_of_starts.log`. If the previous boot never signaled completion, the counter increments.
2. **Crash Threshold Evaluation**: If the counter reaches the threshold (typically 2 consecutive interrupted boots), Auto Rescue initiates the fail-safe recovery procedure before late services or Zygote hooks can run.
3. **Selective Disablement**: Auto Rescue scans `/data/adb/modules/` and creates an empty `.disable` file in each active module directory. Modules explicitly listed in `whitelist.conf` (such as core root managers or display drivers) are spared.

### 2. Late Boot Stage (service.sh)

Once the Android framework initializes, `service.sh` runs asynchronously in the background:

1. **Completion Polling**: The daemon periodically checks system properties using `getprop sys.boot_completed`.
2. **Counter Reset**: Once `sys.boot_completed` returns `1`, Auto Rescue confirms that the user space and graphical interface are healthy. It resets `Number_of_starts.log` back to `0`.
3. **OTA Upgrade Protection**: When an Android OS upgrade occurs, the initial startup process can take substantially longer due to ART dexopt compilation and package migration. Auto Rescue detects system updates and injects a 30-minute delay threshold to avoid disabling modules prematurely.

---

## Configuration & Whitelist Management

Auto Rescue provides a local configuration file to protect essential modules:

```bash
# Whitelist configuration path
/data/adb/modules/Automatic_brick_rescue/whitelist.conf
```

### Adding Modules to the Whitelist

To ensure specific modules remain operational during a rescue event, append their folder slugs to the file:

```text
# Example whitelist entries:
Automatic_brick_rescue
playintegrityfix
shamiko
```

---

## Troubleshooting & Diagnostics

- **Inspect Boot Logs**: Review `/data/adb/modules/Automatic_brick_rescue/Number_of_starts.log` via root shell or termux to inspect recorded startup iterations.
- **Re-enabling Modules**: If a module was disabled during a false alarm, remove the `.disable` file from `/data/adb/modules/<module-slug>/.disable` and reboot the device.
