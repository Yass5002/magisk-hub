---
id: "bcr"
title: "BCR: Basic Call Recorder (Lossless On-Device System Call Recording)"
sidebarTitle: "BCR"
description: "Zero-dependency, open-source native call recorder capturing uncompressed two-way phone calls directly from the Android audio HAL."
category: "system-utilities"
tier: 1
searchQueries:
  - "bcr basic call recorder magisk"
  - "best call recorder rooted android 14"
  - "chenxiaolong bcr download"
  - "lossless two way call recording android"
  - "bcr call recording setup guide"
prerequisites:
  - "Android 10.0 through Android 15"
  - "Magisk, KernelSU, or APatch (can also install as an APK if granted direct system permissions)"
conflicts:
  - "Third-party accessibility-based call recording apps (cause audio focus conflicts)"
configPaths:
  - "/data/media/0/CallRecordings/"
  - "/data/adb/modules/bcr/"
features:
  - "Direct two-way voice stream capture (both caller and recipient recorded at pristine hardware quality)"
  - "Multiple output formats: FLAC (lossless), Opus, AAC, and WAV"
  - "Automated file organization with customizable filename templates (contact name, number, date, duration)"
  - "100% offline, privacy-respecting: zero internet permissions, zero analytics, zero cloud transmission"
faq:
  - question: "Why do non-root call recording apps only record my voice and not the other person?"
    answer: "Google completely restricted access to audio streams from the voice call uplink and downlink in Android 10+ for standard apps. Third-party apps attempt to record the earpiece using the microphone, resulting in muffled, quiet audio. BCR uses systemless root privilege to capture the raw audio stream directly from the telephony audio HAL before it reaches speakers."
  - question: "Where are recorded calls saved?"
    answer: "By default, BCR stores recordings in your internal storage under the CallRecordings/ directory, which you can browse using any standard Android file manager."
---

## Overview

Developed by **chenxiaolong**, **BCR** (Basic Call Recorder) is widely regarded as the most reliable, clean, and battery-efficient call recording solution available for Android.

Due to privacy regulations and Google API restrictions introduced in recent Android versions, unrooted devices cannot record internal audio streams during phone calls. BCR solves this by operating as a privileged system component. It registers with the underlying Android telephony framework, capturing the uncompressed digital audio streams for both sides of the call directly from the hardware mixer.

---

## Technical Architecture & How It Works

### Native Telephony Framework Capture

1. **Privileged Installation**: When installed as a Magisk / KernelSU module, BCR places its helper package into `/system/priv-app/` and injects permissions into `/system/etc/permissions/privapp-permissions-bcr.xml`.
2. **Audio Record Source**: BCR accesses privileged audio source constants:
   - `MediaRecorder.AudioSource.VOICE_CALL`
   - `MediaRecorder.AudioSource.VOICE_UPLINK` (your microphone)
   - `MediaRecorder.AudioSource.VOICE_DOWNLINK` (incoming caller audio)
3. **Hardware Encoder Streaming**: Audio buffers are passed directly to Android's native `MediaCodec` or software encoders, encoding into lightweight Opus or uncompressed FLAC in real-time.
4. **Zero Battery Overhead**: The recording service only runs when an active telephony state transition occurs (`EXTRA_STATE_OFFHOOK`). When the call terminates (`EXTRA_STATE_IDLE`), the file is closed and the process returns to sleep.

---

## Installation & Setup

### Method 1: Root Module (Recommended)
1. Download `BCR-vX.zip` from releases.
2. In Magisk or KernelSU, flash the module and reboot your device.
3. Once booted, open the **BCR** app icon from your app launcher.
4. Grant the requested storage and notification permissions.

### Method 2: Systemless Integration
For devices using custom ROMs or AOSP-based builds, BCR seamlessly integrates into the stock dialer and status bar without requiring background overlays.

---

## Configuration & Practical Usage

Inside the BCR application:
- **Audio Output Format**: Choose **Opus** (recommended: 32kbps or 64kbps for crisp voice clarity with tiny file sizes ~500KB per 10min call) or **FLAC** for archival lossless quality.
- **Output Directory**: Configure a local folder on your storage, or designate a folder synced to Nextcloud / Syncthing.
- **Filename Pattern**: Customize variables:
  `%contact%_%number%_%year%-%month%-%day%_%hour%-%minute%`
- **Auto-Delete Rules**: Set retention policies to automatically prune recordings older than 30, 60, or 90 days.
