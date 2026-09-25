---
id: "partition-backup"
title: "Partition Backup: Comprehensive Block-Level Partition Dumper for Android"
sidebarTitle: "Partition Backup"
description: "Versatile root utility to inspect, list, and create raw block-level image backups of critical Android partitions with both CLI and WebUI interfaces."
category: "system-utilities"
tier: 1
searchQueries:
  - "partition backup magisk module"
  - "rhythmcache partition backup"
  - "backup android partitions root"
  - "dump boot vendor system raw img android"
  - "kernelsu partition backup webui"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
  - "Sufficient free storage (internal storage or USB OTG drive) to hold partition image files"
conflicts: []
configPaths:
  - "/data/adb/modules/partition-backup/"
features:
  - "Dual interface support: manage backups through an interactive WebUI dashboard (KernelSU/APatch) or via terminal command-line interface (CLI)"
  - "Selective partition imaging: specify exact partition names (such as boot, init_boot, vendor_boot, persist) to generate raw .img dumps"
  - "Partition table listing: query all physical block devices and active partitions using partition -l"
  - "Custom destination paths: store output images anywhere on internal storage or external USB-C flash drives"
  - "Universal root manager compatibility: functions identically under Magisk, KernelSU, and APatch environments"
---

## Overview

Before flashing experimental kernels, custom ROMs, GSI images, or low-level root modifications, creating raw block-level backups of critical partitions (such as `boot`, `init_boot`, `vendor_boot`, `persist`, and modem `efs`) is the single most effective insurance policy against bricking an Android device.

Developed by rhythmcache, **partition-backup** is a comprehensive system utility that simplifies the extraction and archival of raw partition images. Providing both a standalone command-line executable (`partition`) and an integrated **WebUI** dashboard for modern root managers, it allows users to safely dump and restore partition blocks without requiring a PC or tethered ADB connection.

## Command-Line Interface (`partition`)

Run the `partition` command with root privileges inside Termux:

```bash
Usage: partition [OPTIONS]

Options:
  -b, --backup PARTITIONS     Backup partitions (comma-separated list, e.g. boot,vendor)
  -d, --directory DIR         Target backup directory (default: current working directory)
  -l, --list                  List all available block partitions on the device
  -h, --help                  Show help information
```

### Common Usage Examples

1. **List available partitions**:
   ```bash
   su -c partition -l
   ```
2. **Back up critical boot and vendor partitions to internal storage**:
   ```bash
   su -c partition -b boot,vendor_boot,init_boot -d /sdcard/PartitionBackups
   ```
3. **Back up all standard partitions before flashing a custom ROM**:
   ```bash
   su -c partition -b boot,vendor,system,persist -d /sdcard/Download
   ```

## WebUI Management

For users running **KernelSU** or **APatch**, the module includes an intuitive WebUI. Simply open your root manager app, navigate to the module card for Partition Backup, and tap the WebUI button to view all partitions with one-tap backup toggles.

## Installation

1. Download the latest `partition-backup-*.zip` release.
2. Flash the module in **Magisk**, **KernelSU**, or **APatch**.
3. Reboot your device to enable the CLI binary and WebUI assets.
