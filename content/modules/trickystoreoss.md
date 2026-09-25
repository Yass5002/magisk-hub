---
id: "trickystoreoss"
title: "TrickyStoreOSS: Open-Source Keystore Attestation & Keybox Spoofer"
sidebarTitle: "TrickyStoreOSS"
description: "Fully open-source, GPLv3-licensed rewrite of TrickyStore providing Keystore HAL interception and custom keybox injection."
category: "root-management"
tier: 1
searchQueries:
  - "trickystoreoss magisk module"
  - "open source trickystore"
  - "beakthoven trickystoreoss"
  - "foss keybox attestation android"
  - "trickystoreoss target txt"
prerequisites:
  - "Android 10 or newer"
  - "Magisk, KernelSU, or APatch with Zygisk support"
  - "Valid, non-revoked OEM keybox.xml certificate bundle (optional for basic functionality, required for strong integrity)"
conflicts:
  - "Stated plainly: No documented conflicts with other modules; proprietary TrickyStore must be uninstalled prior to flashing"
configPaths:
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/tricky_store/security_patch.txt"
  - "/data/adb/modules/tricky_store/"
features:
  - "100% Free and Open Source (FOSS): zero closed-source binaries or proprietary telemetry blobs"
  - "Keystore 2.0 / Keymaster HAL hooking: intercepts attestation challenges directly at the system daemon layer"
  - "Live hot-reloading: changes made to target.txt and keybox.xml apply immediately without rebooting"
  - "Granular app filtering: target specific package names to receive forged certificate chains while preserving biometrics"
  - "Custom security patch configuration: override security patch dates via security_patch.txt"
faq:
  - question: "Why was TrickyStoreOSS created?"
    answer: "TrickyStoreOSS was authored by beakthoven as a completely transparent, GPLv3-licensed cleanroom rewrite of the proprietary TrickyStore module, eliminating closed-source blobs while matching feature parity."
  - question: "Can I run TrickyStore and TrickyStoreOSS together?"
    answer: "No. Both modules hook the same Keystore HAL service entry points and utilize the same /data/adb/tricky_store/ directory structure. You must uninstall the proprietary TrickyStore module before installing TrickyStoreOSS."
---

## Overview

Developed by **beakthoven**, **TrickyStoreOSS** is an open-source, GPLv3-licensed implementation of Keystore HAL interception for rooted Android devices.

When banking applications and Google Play Integrity demand hardware-backed security, Android invokes the Keystore HAL to generate an attestation certificate chain verifying boot state. TrickyStoreOSS intercepts these requests inside system daemons, forging valid attestation chains signed by a legitimate user-provided `keybox.xml` to fulfill `MEETS_STRONG_INTEGRITY`.

---

## Technical Architecture & How It Works

### Native Keystore Service Hooking

TrickyStoreOSS operates at the system service boundary:

1. **Binder Transaction Interception**: Injects hooks into Android's `keystore2` service daemon on Android 12+ (and legacy `keystore` on Android 10–11).
2. **Keybox Substitution**: When an application specified in `target.txt` initiates hardware key generation, TrickyStoreOSS synthesizes an X.509 certificate chain using the private keys and Google-issued attestation certificates stored in `keybox.xml`.
3. **Root of Trust Spoofing**: Injects verified boot flags (`Verified`, locked bootloader) into the ASN.1 attestation extension structure before returning the response to the caller.
4. **Immediate Configuration Synchronization**: Automatically detects filesystem write events on `/data/adb/tricky_store/`, updating internal memory buffers without requiring device reboots.

---

## Installation & Setup

1. Uninstall any existing proprietary TrickyStore installations.
2. Download and flash the latest `TrickyStoreOSS-*.zip` release in Magisk, KernelSU, or APatch.
3. Reboot your device.
4. Place an unrevoked hardware keybox at:
   ```bash
   /data/adb/tricky_store/keybox.xml
   ```
5. Specify target packages in:
   ```bash
   /data/adb/tricky_store/target.txt
   ```

---

## Configuration & Usage

Inside `/data/adb/tricky_store/`:
- **Target Declarations (`target.txt`)**: List the package names requiring forged attestation (e.g., `com.google.android.gms` and banking apps).
- **Patch Level (`security_patch.txt`)**: Specify an optional `YYYY-MM-DD` date string to override the security patch level reported inside attestation extensions.

---

## Troubleshooting & Common Issues

- **Attestation Revoked**: If Google blacklists your keybox serial number, attestation immediately fails. Replace `/data/adb/tricky_store/keybox.xml` with an active, unrevoked keybox bundle.
- **Biometric Authentication Fails**: Ensure system biometric framework packages (`com.android.settings`, `android`) are not included in `target.txt`.
