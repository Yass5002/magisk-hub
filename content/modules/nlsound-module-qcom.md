---
id: "nlsound-module-qcom"
title: "NLSound (Qualcomm): System-Level High-Resolution Audio & Microphone Engine"
sidebarTitle: "NLSound (Qualcomm)"
description: "Comprehensive systemless audio engine engineered for Qualcomm Snapdragon devices, offering DIRECT_PCM mode, tinymix hardware mixer tuning, ACDB calibration, and microphone gain optimization."
category: "system-utilities"
tier: 1
searchQueries:
  - "nlsound qualcomm magisk module"
  - "nlsound briclyaz github"
  - "direct_pcm android root"
  - "tinymix audio boost qualcomm"
  - "acdb audio patch magisk"
prerequisites:
  - "Qualcomm Snapdragon processor (Snapdragon 625 / MSM8953 or newer)"
  - "Android device with root access"
  - "Magisk, KernelSU, or APatch"
conflicts:
  - "Generic systemwide audio overhauls that indiscriminately overwrite Qualcomm audio HAL configurations or ALSA mixer paths"
configPaths:
  - "/data/adb/modules/NLSound/"
features:
  - "DIRECT_PCM audio pathing: enables bit-perfect PCM streams to eliminate unwanted software resampling and reduce playback latency"
  - "Sample rate & bit-depth locking: supports output configurations spanning standard 16-bit / 48 kHz up to 32-bit float / 384 kHz"
  - "Tinymix hardware mixer integration: fine-tunes internal DAC registers, hardware volume step intervals, and analog amplifier gain stages"
  - "Microphone recording fixes: increases recording sensitivity and disables distortion-inducing companders and aggressive limiters"
  - "ACDB (Audio Calibration Database) patching: parses and modifies proprietary vendor ACDB binaries to remove OEM loudness suppression"
---

## Overview

NLSound for Qualcomm, developed by Briclyaz and the NLSound Team, is an advanced audio enhancement module tailored specifically for devices running Qualcomm Snapdragon platforms. Unlike generic equalizer overlays that simply apply software EQ filters on top of the stock Android audio server, NLSound operates directly at the HAL (Hardware Abstraction Layer), ALSA driver, and DSP calibration level.

By interfacing with Qualcomm's proprietary ACDB (Audio Calibration Database) structures and the `tinymix` ALSA utility, NLSound addresses chronic smartphone audio shortcomings: muffled microphone capture in loud environments, aggressive dynamic range compression (companders), artificial volume step restrictions, and playback latency across wired and Bluetooth audio outputs.

## Prerequisites & Compatibility

To run NLSound Qualcomm, your device must satisfy the following technical prerequisites:

1. **System on Chip (SoC)**: A Qualcomm Snapdragon processor, minimum Snapdragon 625 (MSM8953) or newer. Devices powered by MediaTek, Samsung Exynos, Unisoc, or Google Tensor are not supported by this specific build.
2. **Root Manager**: Magisk, KernelSU, or APatch.
3. **Android Version**: Supports modern Android releases with standard Qualcomm audio HAL implementations.

### Incompatibility Notes

While NLSound handles interoperability with third-party audio systems gracefully (including intelligent patching for Dolby Atmos configurations and neutralizing unneeded sound effects like MusicFX or AudioFX), running multiple conflicting audio modules that aggressively patch identical ALSA mixer paths (`mixer_paths.xml`) can lead to device mute bugs or in-call audio failures. Test audio playback with a clean configuration before stacking other DSP modules.

## Architecture & Audio Capabilities

NLSound implements several low-level audio optimizations:

- **DIRECT_PCM Pipeline**: Bypasses the default Android AudioFlinger software mixer when compatible audio playback software is used, outputting bit-perfect streams directly to the Qualcomm hardware decoder.
- **Hardware Register Calibration**: Leverages `tinymix` to directly control analog gain nodes in Qualcomm audio codecs (such as WCD93xx series), preventing digital clipping while boosting maximum clean output volume.
- **Limiter & Compander Removal**: Strips hardcoded audio compression algorithms that crush dynamic range in music and cause volume fluctuation in video recording.
- **Fine-Grained Volume Steps**: Replaces rigid 15-step media sliders with fine-grained multi-step controls for precise low-volume listening on sensitive in-ear monitors (IEMs).

## Configuration & Usage

NLSound is deployed via your root manager's module installation interface:

1. Flash the release package (`NLSound.*.Qualcomm.Devices.zip`) through Magisk, KernelSU, or APatch.
2. The installation wizard guides you through audio parameter choices (such as volume boost levels, preferred sample rates, and microphone sensitivity).
3. If deploying headlessly, NLSound supports reading a pre-prepared configuration manifest placed before installation.
4. Active module assets and persistence files reside in:
   ```bash
   /data/adb/modules/NLSound/
   ```

## Troubleshooting & Verification

- **Microphone Mute or In-Call Distortion**: If the microphone fails to record or produces clipping during phone calls, reinstall the module and select a lower microphone boost multiplier during setup.
- **Audio Stutter in Bluetooth Headphones**: If high-resolution audio streams drop packets over Bluetooth, ensure your Bluetooth developer settings match the codec capabilities of your receiving headphones (e.g., LDAC / aptX HD 24-bit / 96 kHz).
- **Audio Fails After ROM Update**: Android system updates frequently regenerate vendor audio configuration files. If sound output reverts to stock behavior after an OTA, reflash NLSound to reapply ACDB and mixer patches.
