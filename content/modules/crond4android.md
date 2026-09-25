---
id: "crond4android"
title: "crond4Android: Native Cron Daemon & Scheduled Task Automation for Android Root"
sidebarTitle: "crond4Android"
description: "Deploys a lightweight busybox-backed crond scheduler onto KernelSU, APatch, and Magisk, featuring crontab CLI commands, task persistence, and a WebUI."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "crond4android magisk module"
  - "poweran2020 crond4android"
  - "cron daemon android root"
  - "crontab command kernelsu apatch"
  - "schedule background tasks android"
prerequisites:
  - "Root access via KernelSU, APatch, or Magisk"
  - "Busybox environment (provided by root solution or built-in helper)"
conflicts: []
configPaths:
  - "/data/adb/crond/logs/run.log"
  - "/data/adb/crond/spool/"
  - "/data/adb/crond/conf/"
  - "/system/bin/crontab"
features:
  - "Native busybox crond engine: executes standard UNIX cron syntax schedules silently in the background"
  - "WebUI management: view and edit cron schedules directly in KernelSU, APatch, and MMRL interfaces"
  - "Anti-detection installation toggle: allows users to omit the global /system/bin/crontab binary to evade root scanners"
  - "Data persistence safeguards: supports KEEP_ON_UNINSTALL flag to protect custom task configurations across module updates"
  - "Granular boot control: disable automated boot execution at will by creating a simple MANUAL flag file"
---

## Overview

Automating background tasks on Android—such as scheduled database backups, night-time cache maintenance, network toggles, or dynamic configuration scripts—often requires bulky automation applications like Tasker or Termux:Boot running full-time in the background. In contrast, standard Linux servers rely on the lightweight, battle-tested `cron` daemon.

Developed by powerAn2020, **crond4Android** ports the native `crond` daemon to Android through **KernelSU**, **APatch**, and **Magisk**. Utilizing busybox's efficient cron engine, the module provides a standard UNIX `crontab` environment, complete execution logging, and an integrated WebUI for effortless task scheduling without battery drain.

## File Hierarchy & Storage Layout

All daemon configurations, scheduled spools, and execution traces are neatly isolated under `/data/adb/crond/`:

- **Cron Spool Directory**: `/data/adb/crond/spool/`  
  Stores per-user cron tables. Root tasks reside in `/data/adb/crond/spool/root`.
- **Execution Log**: `/data/adb/crond/logs/run.log`  
  Captures execution timestamps, triggered task outputs, and error reports.
- **Configuration Directory**: `/data/adb/crond/conf/`  
  Houses behavior modifier flags.

## Operational Flags & Customization

The module supports several operational flags placed in `/data/adb/crond/conf/`:

- **Preserve Tasks Across Uninstalls**: Create an empty file at `/data/adb/crond/conf/KEEP_ON_UNINSTALL` to ensure your cron scripts and spools are not purged if the module is removed or updated.
- **Disable Boot Autostart**: Create `/data/adb/crond/conf/MANUAL` to prevent `crond` from starting automatically at boot.
- **Stealth / Anti-Detection Setup**: Since version 1.0.3, creating `/sdcard/crond4android.setup` with the content `1` before installation installs the `/system/bin/crontab` binary symlink. Leaving this unset avoids creating exposed global binaries that banking root detectors might inspect.

## Managing Cron Tasks via CLI

You can manage your scheduled jobs using standard UNIX cron syntax:

```bash
# Add a nightly log cleanup task running at 04:30 AM
echo '30 4 * * * echo "" > /data/adb/crond/logs/run.log' >> /data/adb/crond/spool/root

# List currently scheduled cron jobs
su -c crontab -l

# Open interactive crontab editor
su -c crontab -e
```

## Installation & WebUI

1. Download the latest `crond4Android` release ZIP.
2. Flash the module in **KernelSU**, **APatch**, or **Magisk**.
3. Reboot your device.
4. Access the module's WebUI directly inside KernelSU Manager or MMRL to configure jobs graphically, or use standard terminal commands.
