---
id: "systemapp-nuker"
title: "System App Nuker (SAN): Modern Systemless Debloater with Overlay Whiteouts"
sidebarTitle: "System App Nuker"
description: "Advanced systemless debloater for Magisk, KernelSU, and APatch featuring a modern WebUI, OverlayFS directory whiteouts, and automated bootloop self-protection."
category: "system-utilities"
tier: 1
searchQueries:
  - "systemapp nuker magisk"
  - "system app nuker chisewaguri"
  - "android debloater webui kernelsu"
  - "overlayfs whiteout debloat root"
  - "bootloop guard debloater magisk"
prerequisites:
  - "Rooted Android device with Magisk, KernelSU, or APatch"
  - "Newer KernelSU setups require a working metamodule (e.g. Mountify) for overlay mounts"
  - "WebUI support (KernelSU / APatch built-in, or KSUWebUIStandalone / WebUI X on Magisk)"
conflicts: []
configPaths:
  - "/data/adb/modules/systemapp_nuker/"
  - "/sdcard/Download/"
features:
  - "OverlayFS whiteout mounting: creates character whiteout nodes to hide APK directories systemlessly without altering `/system` partitions"
  - "Comprehensive WebUI manager: search, inspect, and select system packages categorized by removal risk and dependency severity"
  - "Dual operational modes: choose between transparent OverlayFS filesystem whiteouts or standard `pm uninstall --user 0` commands"
  - "Automated bootloop safeguard: monitors early boot stages and automatically disables the module while preserving nuke lists if a bootloop is detected"
  - "Portable JSON lists: export and import debloat profiles to `/sdcard/Download/` across multiple ROMs and devices"
---

## Overview

System App Nuker (SAN), created by chisewaguri, is a modern systemless debloating module engineered for Magisk, KernelSU, and APatch. While legacy debloating scripts relied on cumbersome terminal prompts or destructive modifications to system partitions, SAN combines an intuitive WebUI with Linux OverlayFS whiteout technology.

Instead of actually deleting files from read-only `/system`, `/vendor`, or `/product` partitions, SAN creates filesystem whiteouts over the selected application directories. Android's VFS layer sees the target APK directories as completely nonexistent, cleanly removing the bloatware while ensuring that any change can be rolled back instantly without data loss.

## Prerequisites & Compatibility

- **Root Solution**: Magisk, KernelSU, or APatch.
- **KernelSU Mounting Notes**: Modern KernelSU environments without built-in overlay mounts require a working metamodule such as [Mountify](https://github.com/backslashxx/mountify) or the module's bundled Mountify helper script.
- **WebUI Interface**:
  - **KernelSU / APatch**: Directly integrated into the module list.
  - **Magisk**: Launch via the module action button, which opens [KSUWebUIStandalone](https://github.com/KOWX712/KsuWebUIStandalone) or WebUI X.

There are no documented module conflicts.

## Key Capabilities & Operating Modes

### 1. OverlayFS Whiteout Mode (Default)
In default mode, SAN records the exact filesystem paths of selected APKs and mounts overlay whiteout character devices over their parent directories during early boot. Android treats the directory as deleted. Crucially, SAN saves these paths prior to hiding them, ensuring that subsequent module updates or system refreshes can maintain whiteouts even when package manager queries (`pm path`) no longer see the packages.

### 2. Uninstall Only Mode
For users who prefer standard Android package management behavior, SAN can be switched to execute `pm uninstall --user 0`. In this mode, filesystem whiteouts are bypassed, and packages are hidden only within the primary user profile.

### 3. Integrated Bootloop Guard
Debloating carries inherent risks if essential system dependencies (like SystemUI or telephony providers) are mistakenly selected. SAN features an automated bootloop guard:
- The guard tracks whether the Android system successfully reaches the module's background service after boot.
- If two consecutive early boot attempts fail to reach the service, the module detects a bootloop, automatically disables itself, clears all active whiteouts, backs up the active nuke list, and restarts the device.
- Upon booting back into Android, the user can review and restore their saved configuration safely through the WebUI.

## Configuration & Usage

1. Install `SAN_v*.zip` through your root manager and reboot.
2. Launch the **System App Nuker** WebUI.
3. In the **Home** tab, browse installed system apps. Apps are organized into categorized safety tiers to help you assess removal risk.
4. Select the packages you wish to remove and press **Nuke**.
5. Reboot your device to apply the filesystem whiteouts.
6. To restore an app, navigate to the **Restore** tab, select the package, tap restore, and reboot.
7. To export your configuration, use **Export Config** to generate a reusable JSON file in `/sdcard/Download/`.
8. Active module runtime files reside in:
   ```bash
   /data/adb/modules/systemapp_nuker/
   ```

## Troubleshooting & Verification

- **Mount Error During Installation**: If the installer warns of missing mount capabilities on KernelSU, ensure that the Mountify metamodule is installed and enabled.
- **Apps Reappear After ROM Update**: If an OEM system update introduces new APK directory paths for bloatware, open the WebUI to re-scan and apply whiteouts to the new target paths.
