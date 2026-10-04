---
id: "thunderbolt-lock-unlock-sounds"
title: "Thunderbolt Lock & Unlock Sound Effects: Electric Audio Cues for Android"
sidebarTitle: "Thunderbolt Sounds"
description: "Systemless audio customization module replacing stock Android lock and unlock acoustic sound effects with crisp, high-voltage electric cues."
category: "customization-ui"
tier: 2
searchQueries:
  - "thunderbolt lock sound magisk"
  - "change android unlock sound magisk"
  - "custom lockscreen sound root"
  - "android ui audio effect magisk"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other modules modifying /system/media/audio/ui/Lock.ogg or Unlock.ogg"
configPaths:
  - "/system/media/audio/ui/Lock.ogg"
  - "/system/media/audio/ui/Unlock.ogg"
features:
  - "Systemlessly overlays /system/media/audio/ui/ without touching system partition storage"
  - "Replaces default screen lock and unlock sounds with futuristic electric thunder acoustic cues"
  - "Pre-normalized audio mastering prevents audio clipping or sudden volume spikes"
  - "Zero background daemon overhead or battery drain"
faq:
  - question: "Why do I not hear the custom sounds after installing the module?"
    answer: "Ensure that 'Screen locking sound' is enabled in your Android system settings under Settings -> Sound & Vibration -> Additional Settings. Also verify that the phone is not set to silent or vibrate mode."
  - question: "Does this module require a reboot to take effect?"
    answer: "Yes, because system sound effects are loaded by the Android AudioService during initial framework startup, a device reboot is required after flashing."
---

## Overview

**Thunderbolt Lock & Unlock Sound Effects** (authored by ZHB) is a streamlined systemless audio module designed to enhance the tactile feel of device interaction by replacing generic Android screen lock and unlock sounds with crisp, electric audio cues.

Default Android lockscreen sounds are frequently subdued or inaudible in noisy environments. Thunderbolt provides high-clarity sound effects mastered specifically for smartphone speaker frequency responses, providing immediate auditory confirmation when securing or waking the device.

---

## Technical Architecture & How It Works

Android handles user interface sounds via the system framework AudioService, loading audio assets stored in `/system/media/audio/ui/`:

### 1. Overlay Mechanics

The module mounts pre-encoded OGG Vorbis audio tracks over the standard system paths:

- `/system/media/audio/ui/Lock.ogg`: Triggered when the display turns off and keyguard engages.
- `/system/media/audio/ui/Unlock.ogg`: Triggered when biometric authentication succeeds or keyguard is dismissed.

Because the module leverages Magisk/KernelSU systemless bind-mounting, the stock ROM partitions remain completely unmodified, preserving SafetyNet and Play Integrity evaluation states.

### 2. Audio Engineering

The audio files are encoded in high-bitrate OGG Vorbis format with peak limiting at -0.5 dBFS to prevent DAC clipping on low-cost smartphone amplifier stages while maintaining sharp transient response.

---

## Verification & Troubleshooting

- **Check System Settings**: Navigate to **Settings > Sound & vibration > Additional settings** and verify that **Screen locking sound** is toggled **ON**.
- **Inspect Mount Status**: Verify that the files are properly overlaid using a terminal:
  ```bash
  ls -l /system/media/audio/ui/Lock.ogg
  ```
- **Volume Levels**: Lock sounds are bound to the Android System notification/system volume channel. If volume is slider-limited, increase the system volume slider.
