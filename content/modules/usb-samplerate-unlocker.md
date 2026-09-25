---
id: "usb-samplerate-unlocker"
title: "USB Samplerate Unlocker: 192kHz, 384kHz & 768kHz Audio Output for Android USB DACs"
sidebarTitle: "USB Samplerate Unlocker"
description: "Binary-patches vendor ALSA utility shared libraries to unlock high-resolution audio streaming beyond Android's default 96kHz USB audio HAL cap."
category: "system-utilities"
tier: 1
searchQueries:
  - "usb samplerate unlocker magisk"
  - "zyhk usb samplerate unlocker"
  - "android 96khz usb dac limit bypass"
  - "libalsautils binary patch android"
  - "high resolution usb audio magisk"
prerequisites:
  - "Android 10 through Android 14"
  - "Root access via Magisk or KernelSU"
  - "External USB DAC capable of PCM playback at 192kHz, 384kHz, or 768kHz"
conflicts:
  - "audio-samplerate-changer (incorporates this module's patching routines natively)"
configPaths:
  - "/data/adb/modules/usb-samplerate-unlocker/post-fs-data.sh"
  - "/data/adb/modules/usb-samplerate-unlocker/system/vendor/"
features:
  - "Dynamic ALSA library patching: extracts and binary-modifies libalsautils.so and libalsautils_v2.so directly on device during boot"
  - "Sample rate tier unlocking: replaces the stock 96kHz hardware lookup table with 192kHz, 384kHz, or 768kHz profiles"
  - "Google Tensor optimization: patches vendor audio_platform_configuration.xml on Tensor SoCs to elevate USB offload limits from 96kHz to 192kHz"
  - "Configurable post-fs-data operation: toggle between default (192kHz), full (384kHz), and max (768kHz) profiles"
---

## Overview

Modern music streaming applications (such as Tidal, Apple Music, and Qobuz) provide lossless audio masters sampled at 192kHz and above. However, the standard Android Hardware Abstraction Layer (HAL) for USB audio (`libalsautils.so`) hardcodes a sample rate selection array capped at 96kHz (`std_sample_rates[]`). Even when an audiophile connects a high-end external Digital-to-Analog Converter (DAC) capable of 384kHz or 768kHz playback, Android forcibly downsamples audio streams exceeding 96,000 Hz.

Developed by zyhk, **USB Samplerate Unlocker** bypasses this constraint without requiring custom kernel compilation. During early boot, the module extracts your device's active vendor ALSA utility binaries, hexdumps the standard sample rate array, patches the table values in place, and overlays the modified library systemlessly.

## How the Binary Patching Mechanism Works

The module executes its logic during the `post-fs-data` boot stage:

1. **Extraction**: Inspects `/vendor/lib/` and `/vendor/lib64/` to identify present instances of `libalsautils.so` and `libalsautils_v2.so`.
2. **Disassembly & Search**: Dumps the binary contents into temporary memory buffers and scans for the stock byte signature:
   ```c
   std_sample_rates[] = {96000, 88200, 192000, 176400, 48000, 44100, 32000, 24000, 22050, 16000, 12000, 11025, 8000}
   ```
3. **Array Mutation**: Re-indexes the array based on the configured profile:
   - **`default` (192kHz)**: Prepends `{192000, 176400}` ahead of 96000.
   - **`full` (384kHz)**: Prepends `{384000, 352800, 192000, 176400}`.
   - **`max` (768kHz)**: Prepends `{768000, 705600, 384000, 352800, 192000, 176400}`.
4. **Tensor Platform Overrides**: On Google Tensor devices (Pixel 6 through Pixel 8 series), it additionally rewrites `/vendor/etc/audio_platform_configuration.xml` to raise the USB offload stream definition to 192kHz.
5. **Systemless Mount**: Reconstructs the modified `.so` binaries into `$MODDIR/system/vendor/{lib,lib64}/` to bind over stock vendor files.

## Operating Profiles & Configuration

By default, the module operates in **`full` (384kHz)** mode, which provides maximum resolution without audio jitter on most high-speed USB controllers.

If your specific DAC or USB controller experiences audio stuttering at 384kHz, you can throttle the ceiling to 192kHz:

1. Open `/data/adb/modules/usb-samplerate-unlocker/post-fs-data.sh` in a root file manager or terminal.
2. Locate the patch mode argument:
   - Change `full` to `default` (restricts to 192kHz).
   - Alternatively, change `full` to `max` (unlocks 768kHz for ultra-high-end DACs with verified buffer stability).
3. Save the file and reboot.

## Compatibility & Conflicts

- **Android Version**: Tested extensively across Android 10, 11, 12, 13, and 14 on Qualcomm, MediaTek, and Tensor SoCs.
- **Explicit Conflict**: Do not install alongside **Audio Samplerate Changer** (`audio-samplerate-changer`). That module incorporates USB Samplerate Unlocker routines alongside global system mixer overrides; stacking them creates race conditions in `post-fs-data.sh`.

## Verification

To verify that the higher sample rate is actively negotiated by the ALSA subsystem:

1. Connect your USB DAC and initiate high-res music playback.
2. In Termux or an ADB shell, check the stream state:
   ```bash
   su -c cat /proc/asound/card*/pcm*p/sub*/hw_params
   ```
3. Check the `rate:` parameter; it should reflect your track's native frequency (e.g., `rate: 192000 (192000/1)` or `rate: 384000 (384000/1)`) rather than being downsampled to 96000.
