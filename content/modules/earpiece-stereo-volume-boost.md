---
id: "earpiece-stereo-volume-boost"
title: "Earpiece Stereo & Volume Boost: Dual Speaker Emulation and ALSA Mixer Gain"
sidebarTitle: "Earpiece Stereo"
description: "ALSA mixer configuration module that repurposes the front telephony earpiece speaker as a secondary media transducer and increases hardware amplifier gain stages."
category: "audio-dsp-acoustics"
tier: 1
searchQueries:
  - "earpiece stereo mod magisk"
  - "dual speaker mod android"
  - "mixer paths volume boost"
  - "ear pa gain magisk module"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Qualcomm Snapdragon device utilizing ALSA mixer_paths.xml"
conflicts:
  - "Other modules replacing /vendor/etc/mixer_paths.xml directly"
configPaths:
  - "/system/vendor/etc/mixer_paths.xml"
  - "/system/vendor/etc/mixer_paths_overlay_static.xml"
features:
  - "Routes left audio channel playback to the front ear receiver speaker"
  - "Generates dual-speaker stereo spatial separation on devices with single bottom-firing speakers"
  - "Increases EAR PA Gain (Power Amplifier) register to positive decibel values (POS_1P5_DB)"
  - "Boosts digital volume registers (RX1 and RX2 Digital Volume) to overcome low call volume"
  - "Maintains distinct acoustic profiles between private voice calls and public media playback"
faq:
  - question: "Can driving audio through the earpiece damage the speaker hardware?"
    answer: "Telephony earpieces are designed primarily for voice frequencies (300Hz-3.4kHz) and feature smaller voice coils than dedicated bottom-firing loudspeakers. While this module safely boosts gain within manufacturer power tolerances, playing heavily distorted bass frequencies at maximum volume for prolonged periods is discouraged to preserve driver longevity."
  - question: "Will people nearby overhear my private phone calls?"
    answer: "No. The mixer paths explicitly distinguish between the 'earpiece' voice-call device path and the 'speaker-and-earpiece' media playback path. Voice calls continue to output at conversational, private acoustic levels."
---

## Overview

**Earpiece Stereo & Volume Boost** (authored by Stir-Fried Pufferfish, upstream repository: https://mi.fiime.cn/libcangku/2834.html) is an acoustic enhancement module engineered to convert single-speaker Android phones into dual stereo sound systems without physical hardware alterations.

Many mid-range and legacy flagship smartphones feature only one bottom-firing loudspeaker for music, videos, and games, while the front earpiece sits idle during media playback. By reconfiguring the device's Advanced Linux Sound Architecture (ALSA) mixer paths, this module commands the Qualcomm audio codec to route the left audio channel to the front earpiece transducer while directing the right channel to the bottom speaker.

Simultaneously, the module recalibrates analog power amplifier and digital gain registers to eliminate whisper-quiet call volume and provide substantial acoustic headroom.

---

## Technical Architecture & How It Works

Android audio drivers interface with hardware codecs (such as Qualcomm WCD93xx or PMIC audio codecs) through XML mixer definitions stored in `/vendor/etc/mixer_paths.xml`.

### 1. Dual Channel Routing

When media playback initiates, Android calls the `speaker` path. The module intercepts this path definition to activate both transducer circuits:

```xml
<!-- Modified Speaker Path with Simultaneous Earpiece Routing -->
<path name="speaker">
    <path name="earpiece" />
    <ctl name="SLIM RX0 MUX" value="AIF_MIX1_PB" />
    <ctl name="EAR PA Gain" value="POS_1P5_DB" />
    <ctl name="EAR PA Boost" value="ENABLE" />
</path>
```

### 2. Gain Stage Calibration

To ensure the smaller earpiece voice coil is audible alongside the high-output bottom speaker without distorting, the module adjusts both analog and digital gain stages:

- **Analog Power Amplifier (EAR PA)**: Shifted from default negative attenuation (e.g. `-1.5dB`) to positive gain (`+1.5dB`).
- **Digital DAC Volume (RX Digital Volume)**: Increased across `RX1` and `RX2` registers to optimize signal-to-noise ratios before digital-to-analog conversion.

---

## Compatibility & Reversion

Because this module utilizes standard ALSA control identifiers common across Qualcomm hardware platforms, it functions seamlessly on dozens of Snapdragon-powered devices.

To revert immediately back to factory audio routing and stock volume levels, disable the module in your root manager and restart your device.
