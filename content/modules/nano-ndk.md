---
id: "nano-ndk"
title: "Nano for Android NDK: Static Command-Line Text Editor"
sidebarTitle: "Nano for Android"
description: "Static ARM and ARM64 GNU nano text editor compiled with the Android NDK by osm0sis, providing complete terminfo definitions for on-device and TWRP terminal editing."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "nano ndk magisk module"
  - "nano terminal editor android osm0sis"
  - "static nano binary android"
  - "edit build.prop twrp nano"
  - "system etc terminfo android nano"
prerequisites:
  - "Android device with ARM (armv7a) or ARM64 (aarch64) CPU architecture"
  - "Magisk, KernelSU, SuperSU, or custom recovery environment (TWRP, OrangeFox)"
conflicts: []
configPaths:
  - "/data/adb/modules/nano-ndk/"
  - "/system/bin/nano"
  - "/system/etc/terminfo/"
features:
  - "Statically linked NDK binary: compiled without dynamic Bionic dependencies, guaranteeing reliable execution across Android versions"
  - "Complete terminfo database: deploys comprehensive terminfo profiles to `/system/etc/terminfo/` to ensure syntax highlighting and keybindings work across terminal emulators"
  - "Recovery mode emergency editing: when flashed in custom recovery, exposes `/sbin/nano` to allow editing boot scripts and `build.prop` during rescue sessions"
  - "Enhanced CLI wrapper: includes a custom launcher script supporting `--term` parameters to quickly test terminal display profiles"
---

## Overview

Nano for Android NDK, maintained by osm0sis on XDA-Developers, brings the popular GNU nano command-line text editor to rooted Android devices. While Android provides standard shell utilities via Toybox or BusyBox, neither typically provides a full-featured, screen-oriented text editor capable of handling syntax highlighting, smooth scrolling, and complex multi-key bindings.

Compiled statically using the official Android NDK, this build operates independently of target ROM Bionic libc quirks. It equips developers, sysadmins, and modders with an indispensable tool for editing configuration files, startup scripts, and property manifests directly from an on-device terminal or an active ADB shell.

## Prerequisites & Compatibility

- **Architecture**: 32-bit ARM (arm) and 64-bit ARM (arm64).
- **Root Environment**: Compatible with modern Magisk, KernelSU, APatch, and legacy SuperSU systemless installations.
- **Recovery Support**: Compatible with TWRP, OrangeFox, and PBRP for emergency in-recovery file editing.

There are no documented module conflicts.

## Key Capabilities & Dual Installation Modes

### 1. Booted Android Systemless Mode
When flashed through your root manager (e.g., Magisk):
- The static `nano` binary is systemlessly mounted to `/system/bin/nano` or `/system/xbin/nano`.
- A complete terminfo database tree is mounted at `/system/etc/terminfo/`.
- Users can launch `nano` from Termux, an on-device terminal emulator, or `adb shell` to edit scripts with full arrow key, keyboard shortcut, and search support.

### 2. Custom Recovery Rescue Mode
When flashed within TWRP or OrangeFox:
- The installer places a temporary wrapper executable directly into recovery's `/sbin/nano`.
- If a bad tweak, corrupted `build.prop`, or broken init script causes the device to bootloop, you can boot into TWRP, open TWRP's built-in terminal (or `adb shell`), and immediately open and correct the faulty file using `nano /data/adb/modules/...` without pulling files to a PC.

## Usage & Terminal Commands

To open and edit a file from a root shell:
```bash
su
nano /data/adb/modules/example_module/service.sh
```

### Profile Testing Wrapper

To override terminal emulator profile settings or resolve display rendering artifacts, use the bundled `--term` argument:
```bash
nano --term=xterm-256color /path/to/file.txt
```

Standard GNU nano shortcuts apply:
- **`Ctrl + O`**: Write Out (Save changes).
- **`Ctrl + X`**: Exit editor.
- **`Ctrl + W`**: Where Is (Search string).
- **`Ctrl + K`**: Cut text line.
- **`Ctrl + U`**: Uncut (paste) text line.

## Troubleshooting & Verification

- **Terminal Display Garbled**: If keys produce strange escape codes (e.g. `^[[A` instead of moving the cursor up), verify that the `TERM` environment variable is defined in your shell:
  ```bash
  export TERM=xterm-256color
  ```
- **Permission Denied in Recovery**: Ensure the `/system` or `/data` partition containing the target file is checked as mounted under the recovery **Mount** menu before invoking `nano`.
