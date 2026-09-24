---
id: "playintegrityfix"
title: "PlayIntegrityFix (PIF): Native Zygisk Device Integrity Fix"
sidebarTitle: "PlayIntegrityFix"
description: "The mainline community fork of PlayIntegrityFix maintaining device attestation passes and GMS property spoofing on modern Android."
category: "root-management"
tier: 1
searchQueries:
  - "play integrity fix official download"
  - "playintegrityfix kowx712"
  - "fix meets device integrity magisk"
  - "play integrity fix update 2026"
prerequisites:
  - "Magisk 26.0+ (Zygisk enabled), KernelSU, or APatch with Zygisk Next"
  - "Active internet connection on device for initial GMS key negotiation"
conflicts:
  - "osm0sis/PlayIntegrityFork (choose one, do not install both)"
  - "Legacy SafetyNet Fix modules (discontinue use)"
configPaths:
  - "/data/adb/pif.json"
  - "/data/adb/modules/playintegrityfix/"
features:
  - "Automated injection into GMS DroidGuard attestation service via Zygisk"
  - "Pre-packaged with updated non-revoked device profile fingerprints"
  - "Compatible with companion scripts like Playcurl for automated fingerprint updates"
  - "Lightweight binary with zero background CPU or battery overhead"
faq:
  - question: "What is the difference between PlayIntegrityFix and PlayIntegrityFork?"
    answer: "PlayIntegrityFix focuses on a turnkey, streamlined experience with pre-tuned fingerprint profiles and wide community testing. PlayIntegrityFork by osm0sis provides more granular manual override capabilities for advanced users configuring custom multi-field pif.json schemas."
  - question: "Do I need to leave GMS in Magisk DenyList when using this module?"
    answer: "Do not add com.google.android.gms to DenyList when Enforce DenyList is enabled in Magisk. If Magisk isolates GMS from root, Zygisk cannot inject the module's companion hook into com.google.android.gms.unstable."
---

## Overview

Maintained by **KOWX712** following the deprecation of upstream repositories, **PlayIntegrityFix** (commonly abbreviated **PIF**) is the leading community-standard module for restoring `MEETS_DEVICE_INTEGRITY` on rooted Android hardware running Magisk, KernelSU, or APatch.

Google's Play Integrity API serves as the gatekeeper for banking applications, biometric security tokens, payment gateways (Google Wallet), and DRM-protected games. Unlocking the bootloader exposes the device status through hardware cryptographic checks. PlayIntegrityFix circumvents this validation by forcing DroidGuard attestation into software mode and masking property lookups with certified OEM build parameters.

---

## Technical Architecture & How It Works

### The Attestation Interception Flow

1. **Zygote Fork Detection**: When an app queries Play Integrity, Google Play Services spawns its specialized evaluation worker: `com.google.android.gms.unstable`.
2. **libc Hooking**: PlayIntegrityFix hooks the Android property service (`__system_property_get` and `__system_property_read_callback`).
3. **Targeted Spoofing**: When the DroidGuard engine asks for:
   - `ro.product.model`
   - `ro.product.brand`
   - `ro.build.fingerprint`
   - `ro.build.version.security_patch`
   The module intercepts these calls in-memory and supplies clean values matching a certified device profile. Non-GMS apps on the device continue to see your real device name, ensuring zero side-effects on cameras, display calibration, or OEM launchers.

---

## Installation & Setup

1. Open your root manager (**Magisk App**, **KernelSU App**, or **APatch**).
2. Ensure Zygisk is running:
   - Magisk: Enable **Zygisk** in Settings.
   - KernelSU / APatch: Verify that **Zygisk Next** is installed and active in your module list.
3. Flash the `PlayIntegrityFix_vX.zip` package and reboot.
4. Download a Play Integrity checker application (such as *Play Integrity API Checker* by YASNAC / dev community) from Google Play Store.
5. Tap **Check Integrity**. You should see both **MEETS_BASIC_INTEGRITY** and **MEETS_DEVICE_INTEGRITY** pass with green checkmarks.

---

## Maintaining Working Fingerprints

Google routinely updates its server-side revocation list, flagging fingerprints that originate from known open-source modules.

When a ban wave occurs:
1. Locate a clean, working fingerprint from an unrooted certified Android device (or via automated helpers like `playcurlNEXT`).
2. Save the properties to `/data/adb/pif.json`.
3. Kill Google Play Services:
   ```bash
   su -c "killall com.google.android.gms.unstable"
   ```
4. Re-check attestation status.
