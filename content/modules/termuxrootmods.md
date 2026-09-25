---
id: "termuxrootmods"
title: "Termux Root Modifications: Native Root Shell Integration"
sidebarTitle: "Termux Root Mods"
description: "Systemless Magisk module by rompelhd that integrates root access directly into Termux by patching `/system/etc/mkshrc` with a custom C++ launcher binary."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "termuxrootmods magisk"
  - "rompelhd termux root modifications"
  - "termux mkshrc root environment"
  - "termux root path fix magisk"
  - "seamless su shell termux"
prerequisites:
  - "Rooted Android device with Magisk v20.4 or higher"
  - "Termux application installed (F-Droid or GitHub release recommended)"
  - "ARM64, ARM (armhf), or x86_64 processor architecture"
conflicts: []
configPaths:
  - "/data/adb/modules/TermuxRootMods/"
  - "/system/etc/mkshrc"
features:
  - "Systemless `mkshrc` patching: intercepts Android's default MirBSD Korn Shell configuration file to run custom root initialization hooks"
  - "Environment harmonization: properly configures `PATH`, `LD_LIBRARY_PATH`, and terminal variables between Android's Toybox and Termux's GNU userland"
  - "High-performance C++ launcher: custom compiled binary launches shells with sub-millisecond overhead"
  - "Zero host system pollution: maintains root modifications purely within Magisk's overlay architecture without modifying physical `/system`"
---

## Overview

TermuxRootMods, developed by rompelhd, addresses a persistent friction point for developers using Termux on rooted Android devices: the disconnect between Termux's user environment and Android's native root shell.

When typing `su` within Termux, Android drops the user into an unconfigured, bare-bones MirBSD Korn Shell (`mksh`). Essential Termux binary directories (like `/data/data/com.termux/files/usr/bin`) are stripped from `PATH`, custom aliases and functions are unavailable, and terminal characteristics (`TERM`) frequently revert to raw defaults, breaking terminal utilities like `htop`, `tmux`, or `nano`. 

TermuxRootMods solves this systemlessly by patching Android's `/system/etc/mkshrc` to call a dedicated C++ binary, ensuring that executing `su` preserves an intelligent, fully configured Linux root shell.

## Prerequisites & Compatibility

- **Root Framework**: Magisk v20.4 or newer.
- **Application**: Termux (ensure you are using modern builds from F-Droid or GitHub; Google Play Store versions of Termux are deprecated).
- **Supported Architectures**: `arm64`, `armhf` (32-bit ARM), and `x86_64`.

There are no documented module conflicts.

## Technical Architecture

Under Android, interactive root shells execute `/system/etc/mkshrc` on startup:
1. TermuxRootMods injects a systemless overlay for `/system/etc/mkshrc`.
2. When a root shell initializes, the modified script calls a custom compiled native C++ binary bundled with the module.
3. The binary inspects the calling process context, verifies whether the session originated from Termux, and injects customized environment exports, history tracking, and shell prompt decorations.
4. If a custom shell (such as GNU Bash or Zsh) is configured, the binary facilitates smooth handover to that shell.

## Installation & Usage

1. Download the latest `TermuxRootMods-v*.zip` package from the repository releases.
2. Install via Magisk Manager and reboot your device.
3. Launch the **Termux** app.
4. Type `su` and press Enter.
5. Grant root permissions when prompted by Magisk.
6. The root shell will initialize immediately with enhanced environment variables and tool paths available.
7. Active module assets reside in:
   ```bash
   /data/adb/modules/TermuxRootMods/
   ```

## Troubleshooting & Verification

- **Standard Shell Still Appears After `su`**: Verify that the module is enabled in Magisk Manager and that the device was rebooted after installation. Check that `/system/etc/mkshrc` is being overlaid correctly:
  ```bash
  grep -i "TermuxRootMods" /system/etc/mkshrc
  ```
- **Terminal Display Artifacts**: If running screen-oriented programs under root produces garbled lines, ensure your `TERM` variable is exported appropriately:
  ```bash
  export TERM=xterm-256color
  ```
