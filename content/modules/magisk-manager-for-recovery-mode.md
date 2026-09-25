---
id: "magisk-manager-for-recovery-mode"
title: "Magisk Manager for Recovery Mode (mm): Terminal Rescue & Bootloop Prevention"
sidebarTitle: "Magisk Manager (Recovery)"
description: "Interactive terminal-based rescue utility for TWRP and OrangeFox, enabling users to toggle, disable, or delete problematic Magisk modules during bootloops without wiping user data."
category: "root-management"
tier: 1
searchQueries:
  - "magisk manager for recovery mode"
  - "mm recovery magisk rikj000"
  - "fix magisk bootloop twrp terminal"
  - "disable magisk module from recovery"
  - "sh sdcard mm"
prerequisites:
  - "Magisk v19.0 through v30.X"
  - "Custom recovery environment (TWRP, OrangeFox, PBRP) with a built-in terminal or ADB shell access"
conflicts: []
configPaths:
  - "/sdcard/mm"
  - "/data/adb/modules/"
features:
  - "Bootloop recovery engine: lists all installed Magisk modules and lets users selectively disable or remove culprits without data loss"
  - "Filesystem integrity repairs: automatically checks and repairs `magisk.img` filesystems via `e2fsck -fy`"
  - "Global mode toggles: instantly switch Core-Only Mode or Magic Mount settings on or off directly from recovery"
  - "Interactive CLI wizard: straightforward numeric menus navigable in TWRP's built-in touchscreen terminal or via `adb shell`"
  - "Universal Magisk support: continuously maintained for compatibility across Magisk versions from v19.0 to modern v30.X builds"
---

## Overview

Magisk Manager for Recovery Mode (`mm`), originally conceived by VR25 and comprehensively modernized and maintained by Rikj000, is a critical rescue tool for Android power users and module developers. When an incompatible module causes a bootloop, Android cannot reach the graphical Magisk Manager application to allow disabling the offending package.

`mm` solves this dilemma by providing a complete, interactive module management environment directly inside custom recoveries like TWRP, OrangeFox, and PitchBlack Recovery Project (PBRP). Through a simple terminal command, users can enumerate installed modules, toggle disable flags, or completely remove faulty files without needing to perform a factory reset.

## Prerequisites & Compatibility

- **Magisk Version**: Broad compatibility covering Magisk v19.0 through v30.X.
- **Recovery Environment**: Any custom recovery featuring an interactive terminal console or accessible via `adb shell` from a computer.
- **Storage Requirement**: Installation packages should be stored on internal device storage rather than external SD cards for consistent recovery mounting.

There are no documented module conflicts; `mm` operates strictly as a maintenance and diagnostic utility.

## Installation & Deployment

`mm` can be acquired and flashed through several channels:

1. **Magisk Manager / MRepo / MMRL**: Download and install `Magisk Manager for Recovery Mode (mm)` via the Magisk app or community managers like MMRL.
2. **Custom Recovery Flashing**: Alternatively, flash the `MagiskManagerForRecovery_v*.zip` file directly from TWRP recovery.
3. The installation automatically establishes the terminal runner script at `/sdcard/mm`.

## Usage & Terminal Commands

When experiencing a bootloop or needing to manage modules outside Android:

1. Boot your device into your custom recovery (e.g., TWRP).
2. Ensure the `/data` partition is mounted and decrypted.
3. Open the **Advanced > Terminal** menu in your recovery interface (or launch `adb shell` from a connected PC).
4. Run either of the following commands:
   ```bash
   */mm
   # or
   sh /sdcard/mm
   ```
5. An interactive menu will appear on screen:
   - **List installed modules**: Displays all active modules in `/data/adb/modules/` along with their enabled/disabled status.
   - **Toggle Module State**: Enter the number corresponding to a module to disable or re-enable it.
   - **Remove Module**: Delete the module folder entirely from `/data/adb/modules/`.
   - **Toggle Core-Only Mode**: Force Magisk to load only core binaries and skip all modules on the subsequent boot.

## Troubleshooting & Tips

- **Terminal Reports File Not Found**: If executing `sh /sdcard/mm` returns an error, verify that the `/data` and internal storage partitions are properly mounted and decrypted within your recovery's Mount menu.
- **Module Disabled But Still Loops**: Some modules modify persistent vendor properties or system settings. If disabling individual modules does not resolve the bootloop, use `mm` to enable **Core-Only Mode**, reboot into Android, and cleanly uninstall residual companion apps.
