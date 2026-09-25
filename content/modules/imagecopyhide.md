---
id: "imagecopyhide"
title: "ImageCopyHide: Automated Photo Duplication and Concealment Daemon"
sidebarTitle: "ImageCopyHide"
description: "Automatically monitors the camera directory and creates concealed backup copies of photos in a dedicated hidden storage folder."
category: "security-certificates"
tier: 1
searchQueries:
  - "imagecopyhide magisk"
  - "auto backup dcim camera folder root"
  - "cookieof imagecopyhide"
  - "magisk copy hide photos daemon"
  - "android automatic photo copier"
prerequisites:
  - "Root access via Magisk"
  - "Active internal storage with standard /sdcard/DCIM/Camera directory"
conflicts: []
configPaths:
  - "/data/adb/modules/imagecopyhide/"
  - "/sdcard/wot/cptp_config"
features:
  - "Automated DCIM monitoring: periodically inspects /sdcard/DCIM/Camera for newly captured images and media"
  - "Dedicated concealment vault: copies captured media into /sdcard/wot/cptp for secondary preservation"
  - "Configurable scan cadence: adjust polling intervals directly through a plain-text configuration file (default: 45 seconds)"
  - "Toggleable execution: enable or disable the copying routine at runtime without uninstalling the module"
  - "Zero-overhead shell service: runs as a background service initiated at late system boot"
---

## Overview

Whether you are securing evidentiary photos against accidental deletion, maintaining immediate offline redundant backups, or archiving media captured on rooted Android devices, having an automated background file copier is a reliable safeguard.

Created by cookieof, **ImageCopyHide** is a systemless Magisk service that monitors the default Android camera storage directory (`/sdcard/DCIM/Camera`) and copies new files into a dedicated target destination (`/sdcard/wot/cptp`).

## Configuration: `cptp_config`

ImageCopyHide is managed via a simple configuration file placed in internal storage at `/sdcard/wot/cptp_config`:

```ini
# /sdcard/wot/cptp_config
ENABLED=1
INTERVAL=45
```

- **`ENABLED`**: Set to `1` to activate the automated copying loop; set to `0` to pause all background operations.
- **`INTERVAL`**: Specifies the polling cycle frequency in seconds (default is `45` seconds). Lower intervals provide faster replication at the expense of slight storage polling, while higher values conserve battery during idle periods.

## Installation

1. Download the latest `ImageCopyHide-v*.zip` from GitHub releases.
2. Flash the module in **Magisk Manager**.
3. Reboot your Android device.
4. The service will automatically create the `/sdcard/wot/` directory structure and default configuration on first boot.
