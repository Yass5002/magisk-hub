---
id: "adb-root"
title: "ADB Root: Insecure Rooted ADB Daemon for Production ROMs"
sidebarTitle: "ADB Root"
description: "Replaces system adbd with a patched AOSP binary on Android 9/10 to run adbd as root and bypass USB authentication."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "adb root magisk module"
  - "evdenis adb root"
  - "run adbd as root android 9 10"
  - "bypass adb usb auth root"
  - "adb remount disable verify module"
prerequisites:
  - "Android 9 (Pie) or Android 10 (Q) ONLY"
  - "64-bit architecture (arm64/aarch64)"
  - "Magisk root environment"
conflicts:
  - "Android 11 and newer (unsupported)"
  - "Android 8 (Oreo) and below (unsupported)"
  - "32-bit (armv7) or x86/x86_64 architectures (unsupported)"
configPaths:
  - "/data/adb/modules/adb_root/"
features:
  - "Rooted ADB daemon: runs the system adbd process with root UID/GID (root permissions by default)"
  - "USB authentication bypass: disables the RSA host key verification prompt when connecting to development computers"
  - "Remount and write access: unlocks adb remount and adb disable-verity commands on production vendor firmware"
  - "Pure AOSP patched binary: compiled from official Android Open Source Project tree with security drops removed"
  - "Developer utility: tailored for low-level firmware debugging and automated device provisioning"
faq:
  - question: "Why is ADB Root only compatible with Android 9 and 10?"
    answer: "Android 11 introduced major architectural changes to adbd, including dynamic linker namespace isolation and standalone APEX delivery (com.android.adbd). The patched binary bundled with this module specifically targets Android 9/10 userland libraries."
  - question: "Is this module safe to keep enabled permanently?"
    answer: "No. This module is explicitly designed as an insecure developer tool. Running adbd as root with USB authentication disabled allows any computer connected via USB to access full device storage and root privileges without unlocking the screen. Disable the module when not debugging."
---

## Overview

Developed by **evdenis**, **ADB Root** is a specialized development module that forces Android's ADB daemon (`adbd`) to run with native root privileges while skipping USB key authentication on production firmware.

On production ("user") builds of Android, running `adb root` from a host terminal returns `adbd cannot run as root in production builds`. ADB Root replaces the vendor `adbd` binary with an AOSP-compiled binary modified to bypass `ro.secure` and `ro.debuggable` checks, granting immediate root access over USB.

---

## Technical Architecture & How It Works

### Patched AOSP ADB Daemon

The module works by replacing the system adbd binary:

1. **Privilege Drop Removal**: The patched daemon removes calls to `should_drop_privileges()` and `should_drop_capabilities_bounding_set()`, ensuring `adbd` remains running under UID `0` (root) rather than dropping to the unprivileged `shell` user.
2. **Authentication Bypass**: Strips RSA host fingerprint checks, automatically granting debugging authorization upon USB connection.
3. **Magic Mount**: Replaces `/system/bin/adbd` systemlessly during boot.

---

## Installation & Setup

1. **Check Compatibility**: Ensure your device runs **Android 9 (Pie)** or **Android 10 (Q)** on **arm64/aarch64**. Do not attempt installation on Android 11+ or 32-bit hardware.
2. Download the latest `adb_root-*.zip` release.
3. Flash the module in Magisk.
4. Reboot the device.
5. Connect your device to your development computer and verify root status:
   ```bash
   adb shell whoami
   # Returns: root
   ```

---

## Configuration & Usage

The module requires no configuration. As soon as the device boots with the module active, `adbd` listens with root capabilities.

---

## Troubleshooting & Common Issues

- **Bootloop on Android 11+**: Attempting to flash this module on Android 11 or higher will cause system crashes because the system expects the APEX-packaged `adbd`. If your device fails to boot, remove the module using Magisk recovery mode or TWRP (`rm -rf /data/adb/modules/adb_root`).
