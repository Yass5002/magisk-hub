---
id: "infamick-script"
title: "Infamick Script: Advanced Multi-Tool Shell Utility for Rooted Android"
sidebarTitle: "Infamick Script"
description: "Interactive root shell utility providing Samsung CSC editing, Knox package disabling, battery cycle diagnostics, hardware button remapping, and partition backups."
category: "system-environment"
tier: 1
searchQueries:
  - "infamick script magisk"
  - "infamousmick infamick script"
  - "android root shell utility script"
  - "deknoxer csc changer magisk"
  - "battery cycle count android root"
prerequisites:
  - "Root access via Magisk"
  - "Terminal emulator (such as Termux) installed"
conflicts: []
configPaths:
  - "/data/adb/modules/infamick-script/"
features:
  - "Battery health & charging manager: inspects actual battery health, cycle counts, estimated Screen-On Time (SOT), and controls charging status"
  - "Samsung enhancements: includes a CSC region code switcher and an automated Knox debloater tool (Deknoxer)"
  - "Hardware key remapper: easily remap Bixby, Power, Volume Up, and Volume Down key bindings"
  - "Low-level partition backup: dump and backup any physical partition directly using raw dd imaging"
  - "System maintenance & optimization: multiple cache-trim passes, boot counter resets, SELinux mode toggling, and display DPI scaling"
---

## Overview

Created by InfamousMick, **Infamick-script** is a comprehensive, interactive command-line maintenance and optimization utility for rooted Android smartphones. Designed to condense dozens of complex terminal commands and secret codes into a unified terminal interface, Infamick provides immediate control over hardware settings, battery charging thresholds, partition backups, and OEM-specific features—especially on Samsung Galaxy devices.

## Core Feature Set

### 1. Battery & Power Management
- **Hardware Telemetry**: Query battery cycle counts, temperature sensors, and design capacity directly from kernel power-supply nodes.
- **Charging Control**: Systematically disable or enable battery charging on demand, ideal for stationary or plugged-in devices.
- **Drain Optimization**: Disables misbehaving background wake services to resolve idle battery drain.

### 2. Samsung System Customization
- **CSC Region Changer**: Switch active Samsung Country Specific Code (CSC) configurations systemlessly.
- **Deknoxer**: Selectively freeze or disable Knox security services and enterprise telemetry without tripping system errors.
- **Bixby Remapping**: Rebind the dedicated Bixby hardware button to launch custom apps, shortcuts, or flashlight controls.

### 3. Deep Maintenance & Backups
- **Partition Imaging**: Execute automated `dd` dumps of critical partition blocks (boot, recovery, EFS, persist) directly to `/sdcard/`.
- **Display Resolution & DPI**: Query and modify active display scaling parameters without needing an external PC or ADB connection.
- **SELinux Management**: Check active SELinux enforcement status and switch between Permissive and Enforcing modes when debugging root modules.

## How to Run Infamick

1. Install the module via **Magisk Manager** and reboot.
2. Launch **Termux** or your preferred Android terminal emulator.
3. Request root permissions and launch the menu:
   ```bash
   su
   infamick
   ```
4. Follow the interactive numbered menus to execute maintenance tasks, adjust display parameters, or trigger hardware tests.
