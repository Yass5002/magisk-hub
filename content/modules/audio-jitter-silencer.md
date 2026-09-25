---
id: "audio-jitter-silencer"
title: "Audio Jitter Silencer: Low-Frequency Jitter Suppression & Doze Optimization"
sidebarTitle: "Audio Jitter Silencer"
description: "Specialized audio optimization module by zyhk that suppresses sub-50Hz digital stream rate jitter on Bluetooth earphones and USB DACs by disabling adaptive battery and network throttling."
category: "system-utilities"
tier: 1
searchQueries:
  - "audio jitter silencer magisk"
  - "zyhk audio jitter silencer"
  - "reduce bluetooth audio jitter android"
  - "usb dac jitter fix root"
  - "deviceidle.xml audio whitelist"
prerequisites:
  - "Android 11 through Android 14"
  - "Qualcomm or MediaTek SoC architecture (ARM32 or ARM64)"
  - "Magisk root environment"
conflicts: []
configPaths:
  - "/data/system/deviceidle.xml"
  - "/data/adb/modules/audio-jitter-silencer/"
features:
  - "Sub-50Hz stream rate stabilization: targets low-frequency (<50Hz) audio data rate variations that perturb DAC master clocks through Phase Locked Loops (PLL)"
  - "Adaptive battery suppression: disables adaptive battery drain monitoring and adaptive connectivity governors that cause transient CPU and radio downclocking"
  - "Wi-Fi suspend prevention: disables Wi-Fi suspend optimizations in the network manager to ensure steady data streaming to network DACs"
  - "Automated Doze whitelist integration: merges audio players, audio servers, and DAC HALs into Android's power exemption list (`deviceidle.xml`)"
  - "Safe state restoration: maintains clean backups of `/data/system/deviceidle.xml` and restores them automatically upon uninstallation"
---

## Overview

Audio Jitter Silencer, created by audio engineer `zyhk`, is a targeted systemless utility designed to eliminate subtle acoustic distortion on digital audio outputs—particularly on Bluetooth earphones (LDAC, aptX HD, AAC), USB DACs, and network streaming endpoints.

Digital audio jitter consists of two distinct phenomena: phase variations in the DAC's master clock, and frequency variations in the incoming digital audio data rate. In mobile devices, Android's power-saving features—such as adaptive battery tracking, Wi-Fi suspend timeouts, and aggressive Doze throttling—cause micro-pauses and bursty data delivery. In DACs using Phase Locked Loops (PLL) to synchronize with incoming audio streams, sub-50 Hz rate variations modulate the master clock, generating short artificial reverberations and a foggy acoustic soundstage. Audio Jitter Silencer eliminates these generators systemlessly.

## Prerequisites & Compatibility

- **Android Versions**: Tested extensively on Android 11, 12, 13, and 14 (LineageOS, crDroid, phh AOSP GSIs).
- **SoC Compatibility**: Qualcomm Snapdragon and MediaTek processor families in both 32-bit and 64-bit ARM configurations.
- **Root Framework**: Magisk.

There are no documented module conflicts.

## Operational Architecture

The module systematically deactivates the four largest sources of stream rate jitter:

1. **Adaptive Battery Drain Monitor**: Disables background drain monitoring heuristics within the Android battery manager service.
2. **Adaptive Connectivity**: Disables network manager routines that switch radio power states during background media playback.
3. **Wi-Fi Suspend Optimizations**: Disables Wi-Fi radio suspend timers, guaranteeing continuous, low-latency packet delivery for streaming audio.
4. **Doze Whitelist Merger**: Directly parses Android's persistent power management configuration (`/data/system/deviceidle.xml`), merges an audio-specific whitelist covering core media servers, and creates a backup to ensure clean restoration upon removal.

## Installation & The Double Reboot Rule

Follow this specific installation sequence to ensure Android's Device Idle Controller parses the modified XML properly:

1. Flash `audio-jitter-silencer-*.zip` in Magisk Manager.
2. **First Reboot**: Reboot the device. During this boot, the module merges the audio whitelist into `/data/system/deviceidle.xml`.
3. **Second Reboot (Crucial)**: Once the device reaches the home screen, **reboot the device one more time immediately**. This second reboot ensures that Android's Device Idle Controller daemon loads the updated XML from disk rather than using its cached in-memory configuration.
4. Module assets and runtime state persist in:
   ```bash
   /data/adb/modules/audio-jitter-silencer/
   ```

## Troubleshooting & Audio Tips

- **Manual Digital Wellbeing Recommendation**: The developer notes that if "Digital Wellbeing" exists as a system app, its activity tracking generates severe background CPU spikes. It is strongly recommended to either uninstall Digital Wellbeing or change its Battery Usage in Android Settings from "Optimized" to "Restricted".
- **Modifying Battery Optimizations Later**: If you manually alter battery optimization settings for other apps after installing this module, Android may filter out the merged entries. To refresh, simply uninstall the module (reboot twice) and reinstall (reboot twice).
