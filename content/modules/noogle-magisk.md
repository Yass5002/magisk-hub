---
id: "noogle-magisk"
title: "Noogle Magisk: Google Apps Replacement with MicroG on Stock Android"
sidebarTitle: "Noogle Magisk"
description: "Systemless Magisk suite by SelfRef that replaces Google Play Services with microG on stock Android 11 through 15, featuring automated permission setup and Google debloating."
category: "system-environment"
tier: 1
searchQueries:
  - "noogle magisk module"
  - "selfref noogle-magisk"
  - "replace google play services with microg magisk"
  - "stock android degoogle microg"
  - "noogle signature spoofing stock rom"
prerequisites:
  - "Android 11 through Android 15"
  - "Magisk root environment"
  - "Signature spoofing support enabled on the ROM (via native patch or companion module)"
conflicts: []
configPaths:
  - "/data/adb/modules/noogle-microg/"
  - "/system/priv-app/"
features:
  - "Systemless microG deployment: installs microG GmsCore, Services Framework Proxy (GsfProxy), and FakeStore directly into privileged system locations"
  - "Proprietary GMS neutralization: safely overlays and displaces stock Google services without breaking basic system framework dependencies"
  - "One-click permission provisioning: integrates with Magisk's Action button to automatically grant all required runtime permissions to microG"
  - "Preserves stock camera and firmware: enjoy a de-Googled, privacy-respecting environment while retaining stock OEM camera processing and vendor features"
---

## Overview

Noogle Magisk, authored by SelfRef, is a systemless suite designed to remove proprietary Google Play Services and replace them with the open-source microG framework on stock Android 11 through 15.

Historically, users wanting to escape Google's background telemetry had to unlock their bootloader, wipe user data, and flash a third-party custom ROM like LineageOS or GrapheneOS. However, custom ROMs frequently degrade proprietary camera processing algorithms, break specialized dual-screen hardware, and void manufacturer feature sets. Noogle Magisk allows users to retain their official stock OEM firmware while cleanly substituting Google's proprietary binaries with lightweight, open-source microG services.

## Prerequisites & Compatibility

- **Android Version**: Android 11 through Android 15.
- **Root Framework**: Magisk (stable or canary).
- **Signature Spoofing Requirement**: For microG to impersonate Google Play Services and allow third-party apps to function normally, your ROM must support **Signature Spoofing**. If your stock ROM does not support signature spoofing natively, you must flash a signature spoofing Zygisk module (such as FakeGApps or a compatible LSPosed hook) beforehand.

There are no documented module conflicts.

## Key Capabilities & Architecture

- **Privileged Systemless Overlay**: Mounts microG components into `/system/priv-app/`, granting microG the system privileges necessary to handle location providers, cloud messaging, and account synchronization.
- **Action Button Permission Automation**: Rather than requiring manual permission grants via `adb shell` or clicking through Android's settings menus, Noogle Magisk includes a Magisk Action button hook that grants all required permissions (`ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, battery optimization exemptions) in a single step.
- **Optional Debloating**: Includes modular debloating logic to suppress remaining Google system applications (such as Google Chrome, YouTube, or Google Photos), allowing users to install open-source alternatives from F-Droid.

## Installation & Setup Workflow

1. Ensure **ADB debugging** is enabled on your phone as a best practice before beginning.
2. Download the latest `noogle-microg.zip` package from the repository releases.
3. Install the module in Magisk Manager and reboot your device.
4. Open the Magisk app, navigate to the **Modules** tab, and press the **Action** button next to Noogle Magisk to automatically grant permissions.
5. Open the **microG Settings** app from your launcher and enter **Self-Check**:
   - Verify that all checkboxes are ticked.
   - Confirm that "System spoofs signature" is marked as active.
6. Register your Google account in microG if desired for push notifications and app purchases via FakeStore.
7. Active module files persist in:
   ```bash
   /data/adb/modules/noogle-microg/
   ```

## Troubleshooting & Common Pitfalls

- **Signatures Are Not Correct in Self-Check**: If the signature spoofing checkbox remains unchecked in microG Self-Check, your ROM lacks signature spoofing. Flash a signature spoofing module through Magisk or enable signature spoofing in your custom ROM settings.
- **MicroG Service Crashes on First Boot**: If microG services crash intermittently upon initial installation, you can install the standalone microG APKs as regular user applications alongside the module using the maintainer's bundled `install-user-apks.sh` script to resolve OEM package database conflicts.
