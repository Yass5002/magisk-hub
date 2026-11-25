---
id: "librepods"
title: "LibrePods: AirPods Feature Integration for Rooted Android"
sidebarTitle: "LibrePods"
description: "Open-source standalone Android app and LSPosed hook bringing Apple-exclusive AirPods features like ANC toggling, ear detection, and battery reporting to Android."
category: "system-utilities"
tier: 1
searchQueries:
  - "librepods apk download"
  - "airpods features on android root"
  - "librepods lsposed bluetooth hook"
  - "airpods battery status android"
  - "librepods noise cancellation android"
prerequisites:
  - "Magisk, KernelSU, or APatch (for root-assisted privileged Bluetooth access)"
  - "LSPosed (libxposed API 101) with scope set to Bluetooth (`com.android.bluetooth`) and Settings on Android versions prior to Android 17"
conflicts:
  - "Root-hiding modules configured to unmount or hide from `com.android.bluetooth` (prevents `libfluoride_hooks.so` from attaching)"
  - "Incompatible older v1 zip-based builds signed with a different key"
configPaths:
  - "/data/adb/lspd/"
  - "/data/data/me.kavishdevar.librepods/"
features:
  - "v2 rewrite standalone APK (`me.kavishdevar.librepods`) shipping `AirPodsQSService` for Quick Settings listening-mode tiles and `LibrePodsService` for background protocol handling"
  - "Native Fluoride Bluetooth stack hooking via `libfluoride_hooks.so` (arm64-v8a, armeabi-v7a, x86, x86_64) and libxposed API 101 (`KotlinModule`)"
  - "Active Noise Cancellation, Transparency, Adaptive, and Off listening-mode toggling directly from Quick Settings, widgets (`NoiseControlWidget`), or the app UI"
  - "Optical in-ear detection with automatic media pause/resume and loudspeaker routing via `MODIFY_AUDIO_ROUTING` and `LibrePodsAccessibilityService`"
  - "Real-time left bud, right bud, and charging case battery monitoring with home-screen `BatteryWidget` support"
faq:
  - question: "Why does LibrePods require LSPosed on current Android versions?"
    answer: "Due to Apple's non-standard Bluetooth implementation and a bug in Android's Fluoride Bluetooth stack, standard third-party apps cannot establish the custom L2CAP/RFCOMM control channel required by AirPods. LibrePods bundles a libxposed API 101 module (`me.kavishdevar.librepods.XposedService`) and `libfluoride_hooks.so` to patch `com.android.bluetooth` at runtime until the upstream fix lands in Android 17."
  - question: "What changed in the LibrePods v2 rewrite APK?"
    answer: "Instead of shipping only a systemless flashable zip, the v2 rewrite distributes `LibrePods-FOSS-v2.0.0-alpha.4-200000004-release.apk` (`me.kavishdevar.librepods`) as a unified standalone app and embedded libxposed module, complete with `AirPodsQSService`, `LibrePodsService`, and native widgets (`BatteryWidget`, `NoiseControlWidget`)."
---

## Overview

Maintained under **librepods-org/librepods**, **LibrePods** is an open-source implementation of Apple's proprietary accessory communication protocol for AirPods on Android.

While AirPods work as generic Bluetooth A2DP headphones on any Android device, hardware-level features—such as switching between Active Noise Cancellation (ANC) and Transparency modes, optical in-ear detection, conversational awareness, and accurate per-bud/case battery readouts—rely on Apple's private vendor protocol. The **v2 rewrite** (`me.kavishdevar.librepods`) packages the full Android client, Quick Settings tile service, widgets, and LSPosed Bluetooth stack hooks into a single FOSS APK (`LibrePods-FOSS-v2.0.0-alpha.4-200000004-release.apk`).

---

## Technical Architecture & How It Works

### Unified App + libxposed API 101 Architecture

Inspecting the `me.kavishdevar.librepods` APK reveals how the v2 rewrite coordinates app services with system Bluetooth hooking:

1. **Core Services (`LibrePodsService` & `AirPodsQSService`)**:
   - `me.kavishdevar.librepods.services.LibrePodsService` runs as a `connectedDevice` foreground service (`FOREGROUND_SERVICE_CONNECTED_DEVICE`), maintaining the bidirectional AirPods control session, battery state parsing, and audio routing triggers.
   - `me.kavishdevar.librepods.services.AirPodsQSService` implements Android's `TileService` (`BIND_QUICK_SETTINGS_TILE`), allowing one-tap switching of ANC, Transparency, and Off modes directly from the notification shade.
   - `me.kavishdevar.librepods.services.LibrePodsAccessibilityService` assists with media/system interaction hooks when configured.
2. **libxposed API 101 Integration (`XposedService` & `KotlinModule`)**:
   - The APK declares `minApiVersion=101` and `targetApiVersion=101` with `staticScope=true` in `META-INF/xposed/module.prop`, exposing `io.github.libxposed.service.XposedProvider` and `me.kavishdevar.librepods.XposedService`.
   - `me.kavishdevar.librepods.utils.KotlinModule` initializes Java-side hooks alongside `libfluoride_hooks.so` (`META-INF/xposed/native_init.list`) and `libhiddenapi.so` across `arm64-v8a`, `armeabi-v7a`, `x86`, and `x86_64`.
3. **Bluetooth Stack Scope**:
   - `META-INF/xposed/scope.list` targets `com.android.bluetooth`, `com.android.settings`, and `com.google.android.settings` so the Fluoride stack bypasses strict SDP filtering and allows Apple VendorID packet exchange.

---

## Installation & Setup

### 1. Prerequisites Check
- Ensure your device is rooted with **Magisk**, **KernelSU**, or **APatch**.
- Install an **LSPosed** build supporting **libxposed API 101**.

### 2. Install and Enable LibrePods
1. Download `LibrePods-FOSS-v2.0.0-alpha.4-200000004-release.apk` from the official `librepods-org/librepods` release.
2. Install the APK normally on your device (`adb install LibrePods-FOSS-v2.0.0-alpha.4-200000004-release.apk` or via your package installer).
3. Open **LSPosed Manager** -> **Modules**, enable **LibrePods**, and verify that `com.android.bluetooth` (and Settings if prompted) is checked in the Scope list.
4. Reboot your device so the native `libfluoride_hooks.so` hook loads cleanly into the Bluetooth process.

---

## Configuration & Usage

- **Pairing & Permissions**: Pair your AirPods through Android Bluetooth settings, then open LibrePods (`MainActivity`) to grant nearby device (`BLUETOOTH_CONNECT` / `BLUETOOTH_SCAN`), notification, and optional root/accessibility permissions.
- **Quick Settings & Widgets**: Add the **AirPods** Quick Settings tile backed by `AirPodsQSService`, or place `BatteryWidget` and `NoiseControlWidget` on your home screen.
- **Listening Modes & Ear Detection**: Toggle ANC/Transparency modes, configure stem press actions, and enable automatic pause/resume on ear removal.

---

## Troubleshooting & Common Issues

- **AirPods features fail to connect**: Confirm LibrePods is enabled in LSPosed and that `com.android.bluetooth` is selected in Scope. If you use root-hiding tools (such as Shamiko or DenyList enforcement), verify that `com.android.bluetooth` is not excluded from Zygisk/LSPosed injection.
- **Upgrading from older v1 builds**: Uninstall legacy v1 systemless zip modules or conflicting Play Store packages before installing the v2 rewrite APK to avoid signature mismatches.
