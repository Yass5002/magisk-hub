---
id: "pixelupdater"
title: "Pixel Updater: Native A/B OTA Engine for Rooted Google Pixel Devices"
sidebarTitle: "Pixel Updater"
description: "Seamless Over-The-Air (OTA) updater for rooted Google Pixel devices that streams updates directly to inactive A/B slots via native update_engine while preserving Magisk root."
category: "system-environment"
tier: 1
searchQueries:
  - "pixelupdater magisk"
  - "rooted pixel ota updater"
  - "google pixel automatic ota root"
  - "update_engine pixel updater"
  - "pixelupdater selinux policy"
prerequisites:
  - "Google Pixel smartphone supporting A/B or Virtual A/B partitioning"
  - "Android 13 or higher"
  - "Magisk root environment"
conflicts:
  - "Non-Google Pixel hardware (Samsung, Xiaomi, OnePlus, Motorola, etc.)"
  - "KernelSU and APatch (currently unsupported due to Magisk-specific boot patching hooks)"
configPaths:
  - "/system/priv-app/com.github.pixelupdater.pixelupdater/"
  - "/sdcard/Android/com.github.pixelupdater.pixelupdater/files/"
  - "/data/local/tmp/pixelupdater_selinux.log"
features:
  - "Direct `update_engine` integration: streams official Google monthly security updates and major OS upgrades directly to the inactive slot"
  - "Automated Magisk retention: automatically patches the updated inactive slot during the OTA process to maintain root access across reboots"
  - "Targeted SELinux domain isolation: establishes an isolated `pixelupdater_app` policy on boot to communicate with `update_engine` without exposing elevated system permissions"
  - "Rollback index validation: inspects OTA metadata (`metadata.pb`, `payload_metadata.bin`) to protect Android Verified Boot (AVB) against catastrophic downgrades"
  - "Advanced maintenance controls: hidden debug options enable reinstallation of matching OS fingerprints, log extraction, and pre-reboot update cancellations"
---

## Overview

Pixel Updater is an open-source, systemless OTA utility developed specifically for rooted Google Pixel devices. Traditionally, applying monthly Google security updates on a rooted Pixel involved tedious manual steps: pausing the update, downloading full factory or OTA images to a computer, manually patching the init_boot or boot partition via Magisk, and flashing through fastboot.

Pixel Updater automates this entire lifecycle on-device. Operating as a privileged system application paired with Magisk boot hooks, it interfaces directly with Android's native `update_engine` daemon. It checks for official Google OTA packages, streams and verifies partition payloads into the inactive A/B slot, automatically applies Magisk root to the new slot, and prompts you to reboot seamlessly.

## Prerequisites & Compatibility

- **Hardware**: Official Google Pixel devices (Pixel 6 series, Pixel 7 series, Pixel 8 series, Pixel 9 series, and newer).
- **Android Version**: Android 13 or higher.
- **Root Solution**: **Magisk**. KernelSU and APatch are currently unsupported because Pixel Updater specifically relies on Magisk's slot patching integration.

### Incompatibility Notice

Pixel Updater is built around Google's official Pixel OTA distribution infrastructure and metadata schemas. Flashing this module on devices from other manufacturers (such as Samsung, Xiaomi, or OnePlus) will fail and will not receive updates.

## Technical Architecture & Security Model

To interact with Android's low-level `update_engine` without creating system security vulnerabilities, Pixel Updater implements a least-privilege architecture:

1. **Custom SELinux Domain**: During early boot (`post-fs-data.sh`), a native binary (`pixelupdater_selinux`) creates a dedicated SELinux domain called `pixelupdater_app` based on the restricted `untrusted_app` profile, rather than using broad `priv_app` permissions.
2. **Context Association**: The module binds package `com.github.pixelupdater.pixelupdater` to `pixelupdater_app` in `/dev/selinux/apex_seapp_contexts`.
3. **Payload Verification**: Before passing the update to `update_engine`, Pixel Updater downloads `metadata.pb` and `payload_metadata.bin` to verify header checksums, device fingerprint compatibility, and security patch timestamps. This ensures that incompatible images or accidental downgrades (which could trigger AVB rollback index bricking) are blocked.

## Installation & Workflow

1. Flash the `PixelUpdater-*-release.zip` package via Magisk Manager and reboot.
2. Launch the **Pixel Updater** application from your app drawer.
3. Tap **Check for updates** to poll Google's official update servers.
4. When an update is detected, press **Install**. Pixel Updater will stream the payload to the inactive slot, verify partition checksums, and patch Magisk root into the new slot.
5. Once complete, tap the notification or app button to reboot into your updated system.

## Diagnostic Logs & Debug Menu

Pixel Updater includes built-in logging and debugging capabilities:

- **Enable Debug Mode**: Long-press the version number inside the app settings to reveal hidden toggles.
- **Reverting an Update**: If an update was installed but you have not yet rebooted, enable debug mode and select **Revert completed update** to cancel the bootloader slot switch.
- **Log Locations**:
  - Operational logs (`check.log`, `install.log`, `revert.log`, `crash.log`) reside in:
    ```bash
    /sdcard/Android/com.github.pixelupdater.pixelupdater/files/
    ```
  - Early-boot SELinux policy modification logs are saved to:
    ```bash
    /data/local/tmp/pixelupdater_selinux.log
    ```
  - To trace live `update_engine` operations from your PC:
    ```bash
    adb logcat '*:S' update_engine
    ```
