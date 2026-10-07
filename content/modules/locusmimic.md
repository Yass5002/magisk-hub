---
id: "locusmimic"
title: "LocusMimic Location & Route Simulator (com.locusmimic.app)"
description: "Advanced GPS location spoofing, customized route simulation, and per-app compatibility hook module for Android 11+ rooted devices via LSPosed."
category: "xposed-runtime-hooks"
author: "wchunlin1006"
version: "2.1.0"
updatedAt: "2026-10-04"
compatibility: ["LSPosed"]
---

## Overview & System Architecture

**LocusMimic** (`com.locusmimic.app`), developed and open-sourced on GitHub by wchunlin1006, is a sophisticated location simulation and navigation spoofing module designed specifically for Android 11 through Android 15 rooted devices running LSPosed.

Unlike standard developer mock-location applications—which trip anti-cheat and enterprise enterprise flags (`Location.isFromMockProvider()` returns true)—LocusMimic operates at the Java framework level via Xposed. It intercepts location requests in real time within the target application's runtime space, returning realistic GPS, NMEA sentence, Wi-Fi BSSID, and cellular tower coordinates that appear 100% authentic to the client app.

## Key Simulation Capabilities

1. **Zero-Mock Detection**: Bypasses standard Android mock location detection methods without needing Developer Options mock location settings.
2. **Realistic Route Interpolation**: Supports drawing custom travel routes with realistic speed variations, simulated altitude drift, and GPS bearing adjustments.
3. **Per-App Independent Profiles**: Assign unique coordinates or routes to individual applications simultaneously without affecting global system geolocation.
4. **Base Station & Wi-Fi Spoofing**: Simulates matching cell tower IDs (MCC/MNC/LAC/CID) and nearby Wi-Fi network scans to fool multi-mode location SDKs (e.g. Amap, Baidu Map, Google Play Services).
5. **Modern Jetpack Compose UI**: Fast, fluid user interface built with Material 3 and Jetpack Compose.

## Installation & Configuration

### Prerequisites
- Device running Android 11.0 or newer.
- Root access via Magisk, KernelSU, or APatch.
- **LSPosed Framework** installed and running in Zygisk mode.

### Step 1: Install APK
Download and install the latest `LocusMimic` release APK from GitHub.

### Step 2: LSPosed Activation
1. Open **LSPosed Manager**.
2. Select **LocusMimic**.
3. Toggle the module **ON**.
4. Check the applications you intend to simulate locations for (e.g. social networking, delivery, or fitness tracking apps).

### Step 3: Set Coordinates & Launch
1. Open the **LocusMimic** application.
2. Select a target location on the interactive map or enter exact latitude and longitude coordinates.
3. Choose stationary mode or configure a multi-point route.
4. Tap **Start Simulation** and open the target app.

## Verification

To verify that the target application receives simulated coordinates correctly:
```bash
# Dump location manager client states
dumpsys location | grep -A 5 "Last Known Locations"
```

## Security & Ethical Usage

- **Scope Security**: Never activate System Framework scope unless specifically instructed in module documentation; per-application scoping prevents system stability issues.
- **Compliance**: Intended for developer testing, privacy preservation, and app development.
