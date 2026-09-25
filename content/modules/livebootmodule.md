---
id: "livebootmodule"
title: "LiveBoot: Standalone Bootlog & Kernel DMESG Boot Animation"
sidebarTitle: "LiveBoot"
description: "Replaces traditional boot animations with live, color-coded Linux kernel dmesg and Android logcat streams during device bootup."
category: "system-environment"
tier: 1
searchQueries:
  - "liveboot magisk module"
  - "liveboot chainfire magisk"
  - "dmesg logcat boot animation android"
  - "livebootmodule symbuzzer"
  - "verbose boot animation android"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "Tested on Android 12, 13, 14, 15, and 16 ROMs"
conflicts:
  - "Custom OEM boot screens that strictly enforce non-standard SurfaceFlinger framebuffer formats"
configPaths:
  - "/data/adb/modules/livebootmagisk/config"
  - "/data/adb/modules/livebootmagisk/loader.sh"
features:
  - "Live boot streaming: renders real-time dmesg kernel messages and logcat output directly to the screen"
  - "Standalone implementation: operates completely autonomously without requiring Chainfire's legacy companion APK"
  - "Customizable visual modes: configure dark, transparent, or default backgrounds with custom line counts and word wrap"
  - "Log saving capabilities: optionally archives the complete boot stream to /data/cache for debugging bootloops"
  - "Configurable exit delay: adjust suicide delay timing to cover black screen gaps before the launcher appears"
faq:
  - question: "Do I need Chainfire's LiveBoot app installed from the Play Store?"
    answer: "No. This module is a modern, standalone port of Chainfire's original LiveBoot technology. It embeds the rendering binaries and configuration parsers directly into the module without needing any third-party APK."
  - question: "How do I configure LiveBoot settings like text colors or log levels?"
    answer: "Edit the plain text configuration file located at /data/adb/modules/livebootmagisk/config. Do not add comments or extra formatting lines, as the minimal shell parser expects strict key-value tokens."
---

## Overview

Maintained by **symbuzzer** (based on the pioneering work of **Chainfire**), **LiveBoot** replaces standard Android splash animations with a live, Unix-style scrolling console output of `logcat` and kernel `dmesg` buffers during device startup.

For kernel developers, ROM builders, and power users, standard OEM boot animations mask critical initialization events. LiveBoot renders hardware initialization, mount operations, daemon startups, and SELinux denials in real time directly to the physical display, making it an invaluable diagnostic tool.

---

## Technical Architecture & How It Works

### SurfaceFlinger Native Buffer Rendering

LiveBoot operates before the Android zygote fully initializes:

1. **Early Boot Loader**: Triggered via `loader.sh` during `post-fs-data`. It launches a low-level native daemon compiled to talk directly to Android's `surfaceflinger` compositor.
2. **Buffer Multiplexing**: Captures raw output streams from `/dev/kmsg` (or `dmesg`) and the Android logging sockets (`/dev/socket/logd`).
3. **Hardware Display Output**: Formats and color-codes log lines according to their severity level (Verbose, Debug, Info, Warning, Error, Fatal) and blits them to the framebuffer until `sys.boot_completed` triggers the exit sequence.

---

## Installation & Setup

1. Download the latest `LiveBoot-v*.zip` release.
2. Flash the module in Magisk, KernelSU, or APatch.
3. Reboot your device to immediately see the live boot console stream.

---

## Configuration & Usage

Customize display behavior by editing:
```bash
/data/adb/modules/livebootmagisk/config
```

### Configurable Options
- **Backgrounds**: `transparent`, `dark`, or default.
- **Logcat Buffers**: Select active buffers (`M` for Main, `S` for System, `R` for Radio, `C` for Crash).
- **Log Saving**: Set `save` to preserve the boot log under `/data/cache/liveboot.log`.
- **Exit Timing**: Set a custom suicide delay in milliseconds to ensure smooth transitions into the desktop launcher.

---

## Troubleshooting & Common Issues

- **Black Screen During Boot**: Some custom OEM ROMs implement strict DRM surface constraints that prevent external tools from drawing onto the primary display. If the screen remains dark until the launcher loads, verify ROM compatibility.
