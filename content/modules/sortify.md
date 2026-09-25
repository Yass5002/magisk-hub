---
id: "sortify"
title: "Sortify: Automated Downloads Folder Organizer & File Sorter"
sidebarTitle: "Sortify Organizer"
description: "Automatically organizes messy Android Download folders into categorized subdirectories with configurable intervals and a native KernelSU WebUI."
category: "system-utilities"
tier: 1
searchQueries:
  - "sortify magisk"
  - "xcaptain09 sortify"
  - "auto sort android download folder"
  - "organize downloads directory root"
  - "kernelsu webui file organizer"
prerequisites:
  - "Root access via Magisk or KernelSU"
conflicts: []
configPaths:
  - "/data/adb/modules/sortify/"
features:
  - "Automated background organization: automatically sorts unfiled downloads into categorized folders (Images, Videos, Audio, Documents, APKs, Archives)"
  - "Configurable scan cadence: schedules automated sweeps (default: every 5 minutes) without draining background battery"
  - "Native KernelSU WebUI: adjust sorting behaviors, scan timers, and directory exceptions directly within the root manager interface"
  - "Manual action button support: trigger an instant one-tap cleanup using the Magisk/KernelSU Action button"
  - "Safe file collision handling: appends incremental version tags to duplicate filenames to guarantee zero data loss"
---

## Overview

Over months of daily smartphone use, the standard Android `/sdcard/Download/` directory inevitably degenerates into an unmanageable clutter of screenshots, installation APKs, PDF invoices, compressed ZIP archives, and video clips. Standard file managers require manual multi-selection and sorting.

Authored by xCaptaiN09, **Sortify** is a smart background file automation module for rooted Android devices. Running seamlessly in the background, Sortify inspects your `/sdcard/Download/` directory and automatically categorizes newly downloaded files into dedicated, orderly subfolders.

## Organization Structure

Sortify scans file MIME types and extensions, organizing files into intuitive categories:
- **APKs**: `.apk`, `.xapk`, `.apks`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.svg`
- **Videos**: `.mp4`, `.mkv`, `.mov`, `.webm`, `.avi`
- **Audio**: `.mp3`, `.flac`, `.wav`, `.aac`, `.m4a`
- **Documents**: `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.csv`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`

## Interactive Features & WebUI

- **Native WebUI**: For KernelSU users, Sortify embeds a full web dashboard. Configure scan frequencies, toggle specific category subfolders, and define ignore patterns without leaving the KernelSU app.
- **Action Button**: Trigger an immediate on-demand sorting pass anytime by tapping the Action button next to Sortify in Magisk or KernelSU Manager.
- **Safety First**: Never overwrites files. If an existing file with the same name exists in a target category folder, Sortify safely renames the new arrival.

## Installation

1. Download the latest `Sortify-v*.zip` archive from GitHub releases.
2. Install the package in **Magisk** or **KernelSU**.
3. Reboot your device.
4. Download files normally; Sortify will keep your Downloads directory pristine.
