---
id: "video-to-bootanimation"
title: "Video To Bootanimation: Convert MP4 Clips into Custom Android Boot Animations"
sidebarTitle: "Video To Bootanimation"
description: "Automated installer and CLI toolkit that converts user MP4 video files into high-framerate bootanimation.zip packages with auto-resolution and audio extraction."
category: "system-environment"
tier: 1
searchQueries:
  - "video to bootanimation magisk"
  - "rhythmcache video to bootanimation"
  - "convert mp4 to bootanimation android"
  - "bootvideo mp4 magisk module"
  - "custom bootanimation zip maker root"
prerequisites:
  - "Android device running an AOSP-derived or OEM ROM utilizing standard bootanimation.zip structures"
  - "Root access via Magisk or KernelSU"
  - "Source MP4 file placed at /sdcard/bootvideo.mp4 prior to installation"
conflicts:
  - "Samsung One UI devices (utilize proprietary Samsung .qmg compressed format rather than bootanimation.zip)"
configPaths:
  - "/sdcard/bootvideo.mp4"
  - "/sdcard/cfg.txt"
  - "/data/adb/modules/video-to-bootanimation/"
features:
  - "On-device video compilation: splits and compresses MP4 video frames into standard Android part folders during module flashing"
  - "Automatic media detection: queries video resolution, aspect ratio, and framerate without requiring manual image cropping"
  - "Optional startup audio: extracts and packages embedded soundtrack into audio.wav for supported ROMs"
  - "Target path flexibility: automatically selects or manually directs output to /system/media or /system/product/media"
  - "Bundled command-line tools: provides vid2boot and boot2vid binaries for post-install conversion in terminal"
---

## Overview

Replacing an Android boot animation traditionally involves extracting video frames, manually numbering hundreds of PNG files, drafting a precise `desc.txt` timing descriptor, and packaging everything with zero compression into a specific ZIP archive. If image resolutions or timing parameters deviate slightly from hardware constraints, the device displays a black screen during boot.

Developed by rhythmcache, **Video To Bootanimation** automates this entire pipeline directly on your handset. By dropping an ordinary MP4 video into your internal storage and flashing the module, the installer invokes embedded media utilities to parse the video, generate the appropriate descriptor, format the part directories, and overlay the output systemlessly.

## Prerequisites & Format Constraints

- **Source File**: You must place your video file at `/sdcard/bootvideo.mp4` (or `/storage/emulated/0/bootvideo.mp4`) **before** flashing the module ZIP.
- **ROM Architecture**: Works across standard AOSP, LineageOS, Pixel, Xiaomi, Motorola, and other ROMs that look for `bootanimation.zip` inside `/system/media/` or `/system/product/media/`.
- **Samsung One UI Incompatibility**: Samsung smartphones do not read `bootanimation.zip`. They rely on Samsung's proprietary `.qmg` format rendered by `bootchecker` binaries. This module will not alter boot animations on stock Samsung firmware.

## Configuration Options (`cfg.txt`)

While the module will automatically detect display dimensions and framerates if left unconfigured, you can customize the compilation by creating `/sdcard/cfg.txt` prior to flashing:

```ini
# video2boot configuration file
# Lines starting with # are ignored. Empty values = auto-detect.

# Custom path to source video
video=/sdcard/bootvideo.mp4

# Force custom resolution (leave blank to match source video)
width=1080
height=2400

# Target frame rate (e.g., 30 or 60)
fps=60

# Include audio track from video (on/off)
audio=off

# Target install location: auto, system/media, or system/product/media
output=auto
```

- **Audio Support**: Setting `audio=on` extracts the audio stream into `audio.wav`. Note that boot sound support depends on your ROM kernel and framework configurations; many modern AOSP builds have boot sound disabled by default.

## Installation Walkthrough

1. Locate the video clip you want to use and ensure it is formatted as an `.mp4`.
2. Rename the file to `bootvideo.mp4` and place it in the root directory of your internal storage (`/sdcard/bootvideo.mp4`).
3. *(Optional)* Create `/sdcard/cfg.txt` if you want to enforce specific resolutions, framerates, or audio inclusion.
4. Open Magisk or KernelSU and flash the **Video To Bootanimation** ZIP.
5. Watch the installer console as it parses the video, generates frames, and compresses `bootanimation.zip`.
6. Reboot to see your new custom startup animation.

## Terminal CLI Tools

The module also installs standalone command-line binaries accessible via root shell:

- **`vid2boot`**: Allows you to convert any custom video file to a bootanimation archive on the fly without re-flashing:
  ```bash
  su -c vid2boot /path/to/custom_video.mp4
  ```
- **`boot2vid`**: Reverses the process, converting an existing `bootanimation.zip` package back into an MP4 video file.
