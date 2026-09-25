---
id: "rclone-fuse3-magisk"
title: "Rclone FUSE3 Magisk Module: Systemless Cloud Storage Mount & Automation"
sidebarTitle: "Rclone FUSE3 Mount"
description: "Integrates Rclone with FUSE 3.17.x into Android to mount remote cloud storage (Google Drive, OneDrive, WebDAV, S3) directly as local directories."
category: "system-utilities"
tier: 1
searchQueries:
  - "rclone fuse3 magisk"
  - "newfuture rclone magisk"
  - "mount google drive on android root"
  - "rclone fuse mount android storage"
  - "cloud storage local folder android"
prerequisites:
  - "Root access via Magisk"
  - "Android device kernel with FUSE filesystem support (/dev/fuse enabled)"
conflicts: []
configPaths:
  - "/data/adb/modules/rclone-fuse3-magisk/"
features:
  - "FUSE 3.17.x integration: incorporates modern libfuse3 binaries to expose remote cloud remotes as local filesystem mount points"
  - "Automated boot mounts: automatically initializes mount points for designated cloud providers during system boot"
  - "Embedded Web GUI: start and manage remote credentials, sync tasks, and directories through the Rclone Web UI"
  - "Broad cloud ecosystem: supports dozens of storage backends including Google Drive, Microsoft OneDrive, Dropbox, S3, WebDAV, and SFTP"
  - "Seamless app compatibility: enables media players, emulators, and local file managers to read remote files directly"
---

## Overview

Rclone is universally acclaimed as the "Swiss Army knife of cloud storage," allowing users to synchronize, copy, and mount dozens of different cloud storage providers across POSIX operating systems. On Android, however, mounting cloud remotes directly into the local filesystem hierarchy requires root privileges and a functioning FUSE (Filesystem in Userspace) library.

Maintained by NewFuture, **rclone-fuse3-magisk** is a systemless Magisk module that packages a fully compiled Rclone binary alongside **libfuse 3.17.x**. It allows rooted Android devices to mount remote cloud buckets directly into accessible directories (such as `/mnt/cloud/` or `/sdcard/Cloud/`), making cloud storage transparently accessible to any local Android app.

## Key Features

1. **Native FUSE Mount Engine**: Employs an optimized libfuse3 userspace driver tailored for Android's kernel FUSE interface (`/dev/fuse`).
2. **Automated Boot Scripting**: Configure your remotes once; the module automatically mounts them upon system startup.
3. **Web-Based Dashboard**: Built-in support for launching the official Rclone Web GUI, allowing you to configure remotes and transfer rules directly inside your smartphone's browser.
4. **Transparent File Access**: Stream video files directly from OneDrive or Google Drive inside VLC or MX Player without downloading the entire media file locally first.

## Quick Start & Usage

1. Download the latest `magisk-rclone_arm64-v8a.zip` release from GitHub.
2. Install the module in **Magisk Manager** and reboot.
3. Generate your Rclone remote configuration:
   ```bash
   su -c rclone config
   ```
4. Follow the interactive configuration prompts to link your preferred cloud service (e.g., Google Drive, OneDrive, or WebDAV).
5. Configure automated mounting in the module's service script or trigger mounts manually via `rclone mount <remote>: <mountpoint> --daemon`.
