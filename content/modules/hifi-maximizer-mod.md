---
id: "hifi-maximizer-mod"
title: "Hi-Fi Maximizer: Low-Frequency Audio Jitter Reduction & Kernel Tuning"
sidebarTitle: "Hi-Fi Maximizer"
description: "Audiophile kernel and subsystem optimization module by zyhk that minimizes digital audio stream jitter on USB DACs, Bluetooth A2DP, and DLNA endpoints by tuning kernel governors and disabling background services."
category: "system-utilities"
tier: 1
searchQueries:
  - "hifi maximizer magisk module"
  - "yzyhk904 hifi-maximizer-mod"
  - "audio jitter reduction android"
  - "disable thermal engine audio jitter"
  - "audiophile kernel tweaks magisk"
prerequisites:
  - "Rooted Android device with Magisk"
  - "High-resolution audio playback hardware (USB DAC, Bluetooth LDAC/A2DP receiver, or audiophile DAP)"
conflicts:
  - "Competing performance governors or battery savers attempting to downclock the CPU during screen-off music playback"
configPaths:
  - "/data/adb/modules/hifi-maximizer-mod/"
features:
  - "Sub-50Hz jitter mitigation: specifically eliminates long-interval data rate fluctuations that disrupt DAC master clocks through Phase Locked Loops (PLL)"
  - "Performance governor locking: fixes CPU and GPU governors to performance profiles to prevent audio buffer underruns during frequency transitions"
  - "Thermal daemon suppression: terminates OEM thermal throttlers (`thermald`, `mi_thermald`, `thermal-engine`) that introduce scheduler jitter"
  - "Audio effect chain neutralization: cleanly bypasses `audio_effects.xml` to eliminate distortion-causing vendor equalizers and virtualizers"
  - "Dynamic Range Control (DRC) disablement: modifies audio policy XML files to remove hardware dynamic range compression"
---

## Overview

Hi-Fi Maximizer, engineered by audio researcher `zyhk`, is an uncompromising audiophile tuning module built for rooted Android smartphones and digital audio players (DAPs). While mobile audiophiles frequently attribute poor audio fidelity to analogue amplifier stages, research reveals that a significant culprit is low-frequency digital audio jitter (fluctuations under 50 Hz, or intervals longer than 20 milliseconds).

Higher-frequency jitter is readily filtered out by the Phase Locked Loop (PLL) hardware inside modern Digital-to-Analogue Converters (DACs). However, sub-10 Hz jitter—caused by aggressive CPU frequency scaling, Android Doze sleep cycles, Wi-Fi polling bursts, and thermal daemon interventions—modulates the DAC's master clock, generating subtle intermodulation distortion and foggy acoustic imaging. Hi-Fi Maximizer eliminates these jitter sources through kernel and service tuning.

## Prerequisites & Compatibility

- **Root Environment**: Magisk (stable or canary).
- **Target Audio Chains**: External USB DACs (both Synchronous, Adaptive, and Asynchronous modes), high-end Bluetooth LDAC/A2DP headphones, and high-fidelity 3.5mm DAC outputs.
- **Android Version**: Tested extensively across AOSP, LineageOS, crDroid, and various OEM ROMs.

### Conflict Considerations

Because Hi-Fi Maximizer locks CPU governors to high-performance states and disables Android Doze during audio playback, running it alongside aggressive battery-saver modules or conflicting CPU governor tweakers will create conflicts. Devices will prioritize audio clock stability over battery conservation.

## Key Technical Optimizations

### 1. Kernel Governor & Scheduler Lock
- Sets CPU and GPU scaling governors to `performance` mode.
- Changes the Linux I/O scheduler to `deadline` (or `cfq`), reducing storage access latency.
- Adjusts virtual memory swappiness to `0%` and enables laptop mode to minimize background disk thrashing.
- Disables MediaTek EAS+ scheduler routines (`/proc/cpufreq/cpufreq_sched_disable`).

### 2. Audio Pipeline & Effect Chain Neutralization
- Disables vendor effect chains by neutralizing `/vendor/etc/audio_effects.xml`, bypassing unneeded post-processing algorithms.
- Disables OEM Dynamic Range Control (DRC) in `audio_policy_configuration.xml` to restore natural dynamic range.
- Bypasses Android 13+ built-in spatial audio pipelines on Google Tensor and Qualcomm devices to avoid extraneous audio passes.

### 3. Service & Sensor Quenching
- Halts background thermal daemons (`thermal-engine`, `mi_thermald`, `thermald`).
- Halts `camera server`, `logd`, `traced`, and `traced_probes` services that frequently wake the CPU during playback.
- Disables Qualcomm MPDecision CPU hotplugging to avoid core switching spikes.

## Configuration & Usage

1. Flash the `magisk-hifi-maximizer-mod-*.zip` release via Magisk Manager.
2. Reboot your device.
3. Plug in your USB DAC or connect your Bluetooth headphones.
4. Active module assets reside in:
   ```bash
   /data/adb/modules/hifi-maximizer-mod/
   ```

## Troubleshooting & Important Notes

- **Increased Battery Usage**: Because CPU cores maintain steady frequency states and Doze is disabled, screen-off battery consumption during music playback will be noticeably higher. This is intentional to ensure jitter-free digital streams.
- **Device Heat**: With thermal throttling services suppressed, avoid running demanding 3D games or charging at high wattage while playing music.
