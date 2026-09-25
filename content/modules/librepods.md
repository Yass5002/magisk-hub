---
id: "librepods"
title: "LibrePods: AirPods Feature Integration for Rooted Android"
sidebarTitle: "LibrePods"
description: "Open-source background service and system integration bringing Apple-exclusive AirPods features like listening mode switching, ear detection, and battery reporting to Android."
category: "system-utilities"
tier: 1
searchQueries:
  - "librepods magisk module"
  - "airpods features on android root"
  - "librepods xposed bluetooth hook"
  - "airpods battery status android"
  - "librepods noise cancellation android"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "Xposed framework (LSPosed or Vector) with scope set to Bluetooth (com.android.bluetooth) on Android versions prior to Android 17"
conflicts:
  - "Root-hiding modules configured to hide root from the system Bluetooth process (prevents LSPosed hooks from attaching)"
  - "Google Play Store release of LibrePods installed concurrently with the root module (causes signature mismatch issues)"
configPaths:
  - "/system/priv-app/LibrePods/LibrePods.apk"
  - "/system/etc/permissions/privapp-permissions-librepods.xml"
  - "/data/adb/modules/librepods/"
features:
  - "Native listening mode toggling: Active Noise Cancellation, Transparency, and Off modes directly from Quick Settings or app interface"
  - "Optical in-ear detection with automatic audio routing: pauses playback and routes sound back to device speaker when earbuds are removed"
  - "Real-time battery monitoring for left bud, right bud, and charging case integrated into system notifications and widgets"
  - "VendorID protocol emulation: unlocks Apple-exclusive proprietary Bluetooth commands without requiring macOS or iOS devices"
  - "System-level privilege injection: grants BLUETOOTH_PRIVILEGED and MODIFY_PHONE_STATE permissions systemlessly"
faq:
  - question: "Why does LibrePods require an Xposed framework on Android?"
    answer: "Due to Apple's non-standard Bluetooth implementation and a documented bug in Android's Fluoride Bluetooth stack, standard third-party apps cannot establish the custom RFCOMM channel required for AirPods control packets. An Xposed module hook into com.android.bluetooth is necessary to patch the Bluetooth stack at runtime until the upstream fix lands in Android 17."
  - question: "Can I use the Google Play Store build alongside this root module?"
    answer: "No. The Play Store release and GitHub root module are signed with different cryptographic keys. Installing both creates package signature conflicts. Use the root module package directly if you require privileged Bluetooth permissions and status bar battery integration."
---

## Overview

Developed by **kavishdevar**, **LibrePods** is a reverse-engineered implementation of Apple's proprietary accessory protocol for AirPods on Android. 

While AirPods operate as standard Bluetooth A2DP audio sinks on any device, advanced hardware capabilities—such as switching between Active Noise Cancellation (ANC) and Transparency modes, optical ear-detection pausing, spatial audio head tracking, and real-time battery readouts—normally require Apple's private handshake. LibrePods reverse-engineers this protocol, handling the handshake directly on Android to unlock feature parity with iOS.

---

## Technical Architecture & How It Works

### Bluetooth Stack Interception & Permissions

LibrePods addresses two major architectural constraints on Android:

1. **Privileged System Permissions**: By installing as a systemless overlay in `/system/priv-app/LibrePods/`, the app is granted `BLUETOOTH_PRIVILEGED` and `MODIFY_PHONE_STATE` via `/system/etc/permissions/privapp-permissions-librepods.xml`. This enables the module to switch audio streams to loudspeaker when earbuds are disengaged and display system-level battery metrics.
2. **Fluoride Bluetooth Stack Hooking**: Android's standard Fluoride Bluetooth stack enforces strict SDP record lookups that drop connections with non-standard Apple vendor profiles. LibrePods hooks into `com.android.bluetooth` via an Xposed provider (LSPosed or Vector) to bypass this validation, intercepting the raw RFCOMM channel to exchange control packets with the Apple H1/H2 chips.
3. **VendorID Spoofing**: To communicate bidirectional commands (such as stem click gestures or ambient awareness toggles), the module emulates the expected VendorID exchange that AirPods expect from an authentic Apple host.

---

## Installation & Setup

### 1. Prerequisites Check
- Verify that your root environment (Magisk, KernelSU, or APatch) is operating normally.
- Install an active Xposed environment such as **LSPosed** or **Vector**.

### 2. Flash Module
1. Download the latest `LibrePods-FOSS-*-release.zip` from official releases.
2. Flash the zip in your root manager and reboot the device.
3. Upon reboot, launch your Xposed manager (LSPosed/Vector) and ensure LibrePods is enabled with the **Bluetooth** (`com.android.bluetooth`) scope checked.
4. Perform a final soft reboot to initialize the hook.

---

## Configuration & Usage

Once installed:
- **Pairing**: Connect your AirPods through Android's standard Bluetooth settings.
- **Listening Modes**: Switch between Noise Cancellation, Transparency, and Off either inside the LibrePods app or by adding the provided Quick Settings tile to your notification shade.
- **Ear Detection**: Enable automatic playback pause and speaker fallback when you remove one or both earbuds.
- **Stem Actions**: Configure short-press and long-press stem functions to match your desired action mappings.

---

## Troubleshooting & Common Issues

- **App fails to detect AirPods**: Ensure the `com.android.bluetooth` scope is actively selected in LSPosed. If you use a root-cloaking module (such as Shamiko or NeoZygisk DenyList), confirm that the system Bluetooth daemon is not being unmounted or isolated from Xposed.
- **Renaming AirPods**: When renaming AirPods in the LibrePods interface, you must disconnect and re-pair the earbuds once for Android's Bluetooth cache to refresh the local broadcast name.
