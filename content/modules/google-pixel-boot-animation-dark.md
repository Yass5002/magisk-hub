---
id: "google-pixel-boot-animation-dark"
title: "Google Pixel Boot Animation (Dark): Pure Black Startup Visuals"
sidebarTitle: "Pixel Boot Dark"
description: "Authentic Google Pixel boot animation systemless replacement with fluid 60 FPS four-color geometric particle dynamics and pure OLED black background."
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "google pixel boot animation magisk"
  - "pixel dark boot animation zip"
  - "pixel 60fps boot animation root"
  - "google startup animation magisk"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other modules modifying /system/media/bootanimation.zip or product media"
configPaths:
  - "/system/media/bootanimation.zip"
  - "/system/product/media/bootanimation.zip"
features:
  - "Replaces manufacturer OEM startup screens with clean Google Pixel typography and animations"
  - "Rendered in fluid 60 frames per second for smooth, stutter-free startup transitions"
  - "True #000000 black background optimized for OLED and AMOLED display panels"
  - "Multi-mount target support covering /system/media and /system/product/media across OEMs"
faq:
  - question: "Why does my boot animation not scale correctly to my screen resolution?"
    answer: "The animation contains standard 1080p and 1440p adaptive playback scaling in desc.txt. Modern Android bootanimation binaries automatically scale the frames to match device display resolution."
  - question: "Does this change the initial bootloader splash logo?"
    answer: "No. Boot animations handle the secondary stage of the boot sequence (when the Android kernel hands off to user-space init). The initial vendor splash logo is stored in the read-only bootloader/splash partition."
---

## Overview

**Google Pixel Boot Animation (Dark)** (packaged by Kuku de RCOL) is a refined visual customization module that brings Google's minimalist dark-mode Pixel startup sequence to any rooted Android device.

Stock OEM boot animations from manufacturers like Samsung, Xiaomi, and Oppo often feature high-contrast, bright white splash screens and prolonged visual branding. This module replaces those assets with the iconic Google 4-color morphing geometry on a pitch-black background, reducing visual fatigue during nighttime reboots while providing a stock Google experience.

---

## Technical Architecture & How It Works

Android handles boot visualization through the `/system/bin/bootanimation` daemon started by `init`:

### 1. File Overlay Target Resolution

Depending on OEM partition layout and Android version (Android 10 through 15), boot animations reside in different directories:

- `/system/media/bootanimation.zip`: Traditional AOSP and older OEM path.
- `/system/product/media/bootanimation.zip`: Modern Dynamic Partition target on Android 11+.

The module binds the high-framerate `bootanimation.zip` across both target mount points systemlessly, ensuring compatibility regardless of whether the ROM resolves assets from `/system` or `/product`.

### 2. Animation Architecture

The internal ZIP archive consists of:

- `desc.txt`: Defines viewport resolution (e.g., 1080 2400), target framerate (60 fps), and loop behavior.
- `part0/`: Opening sequence displaying Google particle convergence.
- `part1/`: Indefinite looping sequence that cycles until the framework signals `sys.boot_completed=1`.

---

## Troubleshooting & Verification

- **Previewing Without Rebooting**: You can test the animation directly via root shell:
  ```bash
  su -c "bootanimation"
  ```
  *(Press Ctrl+C or kill the process to stop the preview).*
- **Fast Boot Devices**: On devices with ultra-fast UFS 4.0 storage, boot completion may occur before the full sequence finishes. This is expected behavior as Android terminates the animation daemon immediately once the lockscreen is ready.
