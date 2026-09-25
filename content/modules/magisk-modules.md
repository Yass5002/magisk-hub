---
id: "magisk-modules"
title: "NewFuture Magisk Modules Suite: Automated Networking, ADB & Battery Emulation"
sidebarTitle: "NewFuture Utilities"
description: "Suite of automated system utilities providing LAN-to-Wi-Fi auto switching, battery status simulation for SBCs, and boot-time automated ADB startup."
category: "networking-proxies"
tier: 1
searchQueries:
  - "newfuture magisk modules"
  - "magisk lan auto switch"
  - "magisk fake battery bypass"
  - "magisk auto adb root"
  - "ethernet wifi auto toggle android root"
prerequisites:
  - "Root access via Magisk"
conflicts: []
configPaths:
  - "/data/adb/modules/magisk-modules/"
features:
  - "Magisk LAN Auto Switch: detects eth0 link state to automatically disable Wi-Fi when connected to Ethernet and re-enable Wi-Fi when unplugged"
  - "Magisk Fake Battery: mocks 100% battery level, constant AC power, and standard temperatures for devices running without a physical battery"
  - "Magisk Auto ADB: automatically starts the Android Debug Bridge (ADB) daemon listening on designated ports upon device startup"
  - "Autonomous operation: clean, lightweight shell daemons executing during system boot without requiring third-party companion apps"
  - "Open source MIT license: auditable POSIX-compliant scripting designed for embedded Android systems and media boxes"
---

## Overview

Maintained by NewFuture, **magisk-modules** is a curated suite of specialized automation tools designed for Android power users, single-board computer (SBC) tinkerers, TV box owners, and server deployments. Rather than broad interface themes, these utilities target concrete hardware and networking automation tasks that stock Android handles poorly.

## Component Utilities

### 1. Magisk LAN Auto Switch
Android often maintains active Wi-Fi connections even when an Ethernet adapter (`eth0` or USB LAN) is plugged in, leading to routing confusion and unnecessary RF power consumption.
- **Link State Monitoring**: Listens for network carrier events on `eth0`.
- **Automatic Toggle**: Immediately disables Wi-Fi when Ethernet connects, and restores Wi-Fi instantly when the LAN cable is disconnected.

### 2. Magisk Fake Battery
When converting old Android phones or specialized dev boards into dedicated home servers, dashcams, or 3D printer controllers, removing swollen lithium-ion batteries is a crucial fire-safety precaution.
- **Hardware Power Emulation**: Intercepts kernel battery telemetry and reports 100% state-of-charge, optimal temperature, and AC wall power.
- **Bypasses Shutdown Traps**: Prevents Android from triggering emergency battery shutdown routines or refusing to boot due to missing battery thermistors.

### 3. Magisk Auto ADB
- **Automated Debugging**: Automatically enables USB debugging and TCP/IP wireless debugging on port 5555 as soon as network interfaces come online at boot.

## Installation

1. Select and download the relevant component package (e.g., `magisk-auto-adb-*.zip` or `magisk-lan-auto-switch-*.zip`) from the project releases.
2. Install the archive in **Magisk Manager**.
3. Reboot your device to enable the background service.
