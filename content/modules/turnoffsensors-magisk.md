---
id: "turnoffsensors-magisk"
title: "Turn Off Sensors: Automated Hardware Sensor Privacy at Boot"
sidebarTitle: "Turn Off Sensors"
description: "Automatically disables device hardware sensors (cameras, microphones, gyroscopes, accelerometers) on startup via Android's native sensor_privacy service."
category: "security-certificates"
tier: 1
searchQueries:
  - "turn off sensors magisk"
  - "adalynastatine turnoffsensors"
  - "disable sensors on startup android root"
  - "sensor_privacy android root"
  - "hardware privacy kill switch android"
prerequisites:
  - "Root access via Magisk"
  - "Android 10 or newer (tested across Android 10 through Android 17 builds)"
conflicts: []
configPaths:
  - "/data/adb/modules/turnoffsensors-magisk/"
features:
  - "Automated boot privacy: automatically activates Android's internal Sensors Off state immediately upon system startup"
  - "Comprehensive hardware muting: cuts off data streams from cameras, microphones, gyroscopes, accelerometers, and magnetometers"
  - "Framework-level integration: uses Android's official sensor_privacy service, preventing app crashes by supplying clean null/zero values"
  - "Defense against surveillance: stops untrusted applications from harvesting sensor data or microphone feeds during device boot"
  - "User-toggleable override: easily toggle sensors back on temporarily via Quick Settings developer tiles or shell commands"
---

## Overview

Starting in Android 10, Google added a developer feature called "Sensors Off," backed by the system `sensor_privacy` service. When engaged, it acts as a software kill-switch: cameras become unavailable to apps, microphones return silence, and inertial sensors (gyroscopes, accelerometers, proximity) return zero or static values. However, Android resets or does not automatically persist this toggle across system reboots, leaving a window of exposure whenever a device restarts.

Authored by AdalynAstatine, **TurnOffSensors-Magisk** is a lightweight security module that automatically invokes the Android `sensor_privacy` service during late boot, ensuring device sensors remain firmly disabled from the moment the operating system loads.

## Why Automated Sensor Privacy?

1. **Anti-Eavesdropping**: Malicious applications cannot silently engage the microphone or record ambient audio during early background boot sequences.
2. **Gyroscope & Accelerometer Tracking**: Modern advertising SDKs use micro-movements from inertial sensors to fingerprint users or infer typing patterns. Muting these sensors eliminates motion tracking vectors.
3. **App Stability**: Because the module interfaces directly with the Android platform's native `sensor_privacy` manager, applications gracefully handle the muted state without throwing unhandled exceptions or crashing.

## Usage & Controls

When sensors are turned off:
- The camera app will display a message that the camera is disabled.
- Microphones will not capture audio.
- The screen will not auto-rotate based on physical orientation.

To re-enable sensors temporarily:
- Add the **Sensors Off** quick settings tile via **Settings > System > Developer options > Quick settings developer tiles > Sensors Off**.
- Tapping the tile immediately restores full sensor functionality until the next reboot or until toggled off again.

## Installation

1. Verify your device runs Android 10 or newer.
2. Download the latest `TurnOffSensors-Magisk.zip` release from GitHub.
3. Install the module in **Magisk Manager**.
4. Reboot your phone. Hardware sensors will be immediately muted upon startup.
