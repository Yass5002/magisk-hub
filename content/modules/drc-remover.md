---
id: "drc-remover"
title: "DRC Remover: Uncompressed Dynamic Range Audio for Qualcomm Snapdragon Android Devices"
sidebarTitle: "DRC Remover"
description: "Disables intrusive Dynamic Range Control (DRC) compression filters across speakers, 3.5mm jacks, Bluetooth, and USB DAC outputs by modifying vendor audio policy XMLs."
category: "system-utilities"
tier: 1
searchQueries:
  - "drc remover magisk module"
  - "zyhk drc remover"
  - "disable speaker_drc_enabled android"
  - "qualcomm audio dynamic range compression disable root"
  - "disable android audio compressor"
prerequisites:
  - "Android 10 through Android 14"
  - "Root access via Magisk or KernelSU"
  - "Device with active DRC enabled in stock firmware (primarily Qualcomm Snapdragon SDM and SM chipsets)"
conflicts:
  - "audio-samplerate-changer (already incorporates DRC removal logic)"
configPaths:
  - "/data/adb/modules/drc-remover/"
  - "/data/adb/modules/drc-remover/system/vendor/etc/"
features:
  - "Automated policy inspection: detects whether vendor audio configuration files have active DRC compression enabled"
  - "Precision XML patching: substitutes speaker_drc_enabled='true' declarations with 'false' across all hardware sinks"
  - "Wide output coverage: disables dynamic compression across internal speakers, wired 3.5mm analog outputs, Bluetooth A2DP, and USB DACs"
  - "Zero audio latency overhead: acts solely on vendor XML declarations without running persistent background daemons"
---

## Overview

Dynamic Range Control (DRC) is an audio DSP algorithm designed to compress acoustic dynamics by boosting quiet sounds and aggressively attenuating transient volume peaks. While beneficial for preventing distortion on tiny, low-power smartphone speakers, many smartphone manufacturers (particularly on Qualcomm Snapdragon platforms like SDM and SM series chipsets) force DRC onto **all** audio pipelines—including external USB DACs, high-fidelity Bluetooth codecs, and 3.5mm headphone jacks.

When DRC is active, musical passages lose punch, orchestral crescendos sound flat, and high-impedance headphones sound constrained. Because this compression is applied at the vendor audio HAL layer before audio leaves the Android mixing engine, software players cannot bypass it.

Developed by zyhk, **DRC Remover** locates your device's active vendor audio policy configuration, disables the hardware compression switch, and mounts the corrected configuration systemlessly.

## How DRC Remover Operates

During module initialization:

1. **Hardware Inspection**: Scans `/vendor/etc/` and `/vendor/etc/audio/` for active audio policy descriptors (e.g., `audio_policy_configuration.xml`, `audio_policy_configuration_a2dp_offload_disabled.xml`, etc.).
2. **Conditional Activation**: Determines whether `speaker_drc_enabled="true"` is declared. If the OEM firmware already leaves DRC disabled (common on MediaTek SoCs), the installer reports clean status and terminates without unnecessary modifications.
3. **XML Substitution**: Clones the active policy XML into `$MODDIR/system/vendor/...` and alters the boolean attribute:
   ```xml
   <!-- Stock Qualcomm Configuration -->
   <globalConfiguration speaker_drc_enabled="true"/>

   <!-- DRC Remover Patched Configuration -->
   <globalConfiguration speaker_drc_enabled="false"/>
   ```
4. **Systemless Mount**: Binds the patched XML directly over the vendor partition at boot.

## Important Operational Notes

- **A2DP Offload Changes**: If you change Developer Options settings that switch the active audio configuration file (such as enabling or disabling "A2DP Hardware Offload"), you must reflash or update DRC Remover so it targets the newly active XML configuration file.
- **Custom ROM Inversions**: A minority of third-party custom ROMs invert the programmatic meaning of `speaker_drc_enabled` inside custom HAL trees. If your ROM specifically requires inverted flags, test output dynamics carefully.
- **Explicit Conflict**: Do not install alongside **Audio Samplerate Changer** (`audio-samplerate-changer`), which already embeds this exact DRC removal logic into its installation sequence.

## Installation & Verification

1. Download and flash the `drc-remover` `.zip` in Magisk or KernelSU.
2. Examine the installer log output to verify that an active DRC policy file was discovered and patched.
3. Reboot the device.
4. Verify that the patched configuration is mounted:
   ```bash
   su -c grep "speaker_drc_enabled" /vendor/etc/audio_policy_configuration.xml
   ```
   The output should confirm `speaker_drc_enabled="false"`.
