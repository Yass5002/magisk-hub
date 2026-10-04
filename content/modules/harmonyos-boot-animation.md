---
id: "harmonyos-boot-animation"
title: "HarmonyOS Boot Animation & Chime: Installation & Technical Guide"
sidebarTitle: "HarmonyOS Boot"
description: "Systemless replacement module delivering Huawei's official HarmonyOS boot sequence visuals and high-fidelity startup sound across Magisk, KernelSU, and APatch."
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "harmonyos boot animation magisk"
  - "huawei startup animation android root"
  - "bootaudio mp3 magisk module"
  - "harmonyos boot sound zip"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Device with unencrypted data or compatible systemless media mount"
conflicts:
  - "Any module mounting to /system/media/bootanimation.zip"
configPaths:
  - "/system/media/bootanimation.zip"
  - "/system/media/bootaudio.mp3"
features:
  - "Official HarmonyOS concentric ring dynamic particle boot animation"
  - "Integrated bootaudio.mp3 delivering authentic startup acoustic chime"
  - "Zero-compression PNG frame archive preserving visual sharpness"
  - "Dynamic aspect ratio adaptation for 1080p, 2K, and 1440p displays"
faq:
  - question: "Why does the startup audio not play on my ROM?"
    answer: "Startup sound playback requires ROM-level support for bootaudio or boot_audio service in the device init.rc scripts. While the visual animation works universally, audio depends on whether your OEM firmware enables early audio playback."
  - question: "Will this overwrite my stock boot animation permanently?"
    answer: "No. Magisk, KernelSU, and APatch use overlayfs or bind-mounts. Removing the module instantly restores your original vendor boot animation."
---

## Overview

**HarmonyOS Boot Animation & Chime** (packaged by Yu Kong / 余空) provides a clean, elegant visual and acoustic modernization for Android devices by implementing Huawei's signature HarmonyOS startup experience.

The module packages both the graphic animation archive (`bootanimation.zip`) and the accompanying high-fidelity stereo startup audio (`bootaudio.mp3`), mounting them systemlessly over the standard Android media directory.

---

## Technical Architecture & How It Works

Android handles early user-space visual output via `/system/bin/bootanimation`, an unprivileged binary executed by the `surfaceflinger` process during Android initialization:

### 1. Animation Archive Structure

Within `/system/media/bootanimation.zip`, the archive conforms to standard Android boot container specifications:

```text
bootanimation.zip
├── desc.txt          # Playback timing, resolution, and loop parts
├── part0/            # First-stage intro: luminous energy ring formation
└── part1/            # Continuous loop: orbital rotation until Android Zygote init
```

The header descriptor (`desc.txt`) defines the framerate and rendering mode:

```text
1080 2400 60
p 1 0 part0
p 0 0 part1
```

- **Width & Height**: Rendered at native 1080x2400, automatically scaled by SurfaceFlinger to fit ultra-wide panels.
- **Framerate**: 60 frames per second for stutter-free fluid dynamics.
- **Loop Parameters**: `part0` plays once to completion; `part1` loops indefinitely until `sys.boot_completed=1` triggers animation exit.

### 2. Startup Acoustic Chime

The module provides `/system/media/bootaudio.mp3`. When the device's `init.rc` contains a `service bootanim` that supports the `-audio` flag or invokes `audiocontrol`, the sound stream is automatically passed to the hardware Audio HAL during display handoff.

---

## Installation & Verification

1. Flash `harmonyos-boot-animation-v1.0.zip` via Magisk Manager, KernelSU Manager, or APatch WebUI.
2. Reboot the device.
3. Observe the concentric HarmonyOS ring visual and audio sequence during system startup.
