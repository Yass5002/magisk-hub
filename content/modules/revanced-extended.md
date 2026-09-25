---
id: "revanced-extended"
title: "ReVanced Extended: Systemless YouTube & Music Enhancement"
sidebarTitle: "ReVanced Extended"
description: "Systemless module automating the deployment and overlay mounting of ReVanced Extended (Morphe) patched YouTube and YouTube Music."
category: "customization-ui"
tier: 1
searchQueries:
  - "revanced extended magisk module"
  - "morphe youtube module root"
  - "revanced extended youtube music module"
  - "systemless revanced mount"
  - "noname exe revanced extended"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "Stock YouTube (com.google.android.youtube) or YouTube Music base APK matching the supported release version"
  - "zygisk-detach recommended to prevent Google Play Store from overwriting the mounted version"
conflicts:
  - "No documented conflicts with other root modules (automatic Google Play Store updates will overwrite the mounted app if not detached)"
configPaths:
  - "/data/adb/modules/yt-morphe/"
  - "/data/adb/modules/ytm-morphe/"
  - "/data/adb/modules/yt-morphe/disabled_by_action"
  - "/data/adb/post-fs-data.d/"
features:
  - "Systemless APK mount: replaces stock YouTube binaries with zero modifications to system partition files"
  - "Comprehensive ad-blocking: strips video, banner, search, and audio stream advertisements"
  - "Background and PiP playback: enables screen-off audio listening and picture-in-picture video without a subscription"
  - "MicroG independence for root: interfaces directly with official Google Play Services without requiring Vanced MicroG"
  - "Automated odex recompilation: pre-compiles dex/odex files on install to prevent stutter on first launch"
faq:
  - question: "Do I need MicroG when using the ReVanced Extended root module?"
    answer: "No. Because the root module mounts the modified APK over the legitimate system app package name (com.google.android.youtube), it hooks directly into your device's authentic Google Play Services account architecture, making MicroG completely unnecessary."
  - question: "Why does the app revert back to the unpatched version after a while?"
    answer: "Google Play Store automatically checks for app updates in the background and replaces the base APK. To prevent this, install the zygisk-detach module to hide YouTube and YouTube Music from the Play Store update queue."
---

## Overview

Maintained by **NoName-exe**, the **ReVanced Extended** (Morphe) module provides a streamlined, fully automated systemless integration for patched YouTube and YouTube Music on rooted Android devices.

Unlike non-root standalone APK modifications that require renaming package identifiers and relying on standalone microG services for account synchronization, this module dynamically overlays the patched binaries directly over the stock application. This preserves native Google Play Services authorization, Cast protocol compatibility, and system-level intents.

---

## Technical Architecture & How It Works

### Dynamic Mount & Service Lifecycle

The module functions by orchestrating file replacement during early userland initialization:

1. **Architecture & Version Validation**: During flashing, `customize.sh` evaluates the host ABI (`arm64-v8a` or `armeabi-v7a`), detects whether the target package (`com.google.android.youtube` or `com.google.android.apps.youtube.music`) is installed as a system app or user app, and uninstalls any conflicting system updates if necessary.
2. **Late Boot Mount (`service.sh`)**: The module waits until `sys.boot_completed` equals `1` and `/sdcard/Android` becomes accessible. It then queries the package manager for the base APK path (`get_basepath`) and executes a tmpfs bind-mount to cleanly overlay the pre-compiled, optimized ReVanced Extended APK onto the stock installation directory.
3. **Optimized Bytecode Pre-compilation**: The installer triggers ART compilation (`cmd package compile -m speed`) on newly mounted modules, ensuring startup speed matches or exceeds unpatched OEM builds without initial JIT stutter.

---

## Installation & Setup

### 1. Prepare Stock Application
- Ensure you have the stock version of YouTube or YouTube Music installed that corresponds to the version tag of the module release.
- If your device came with YouTube as a factory system app, uninstall all Google Play updates via **Settings > Apps > YouTube > Uninstall Updates**.

### 2. Flash Module
1. Download the release package (`youtube-morphe-module-*.zip` or `youtube-music-morphe-module-*.zip`) from the official releases repository.
2. Flash the module within Magisk, KernelSU, or APatch.
3. Reboot your device.

### 3. Detach from Play Store
To keep Google Play Store from automatically downloading stock updates over your patched mount:
- Flash **zygisk-detach** and configure it to detach `com.google.android.youtube` and `com.google.android.apps.youtube.music`.

---

## Configuration & Usage

ReVanced Extended settings can be configured directly inside the YouTube application:
- Navigate to **Settings > ReVanced Extended** (or **Morphe Settings**).
- **Ad Blocker**: Toggle granular video, overlay, and feed advertisement filters.
- **SponsorBlock**: Enable crowdsourced skipping of intros, sponsor segments, and non-music sections.
- **Return YouTube Dislike**: Restore community dislike counts across all video watch screens.
- **Video Playback**: Configure custom default video resolutions for Wi-Fi and mobile networks.

---

## Troubleshooting & Common Issues

- **App fails to open / crashes immediately on launch**: Verify that the version of the stock YouTube app installed on your device matches the version required by the module release. A version mismatch will cause binder interface failures.
- **Temporarily disabling the module**: If you need to temporarily disable the mount without uninstalling, touch `/data/adb/modules/yt-morphe/disabled_by_action` and reboot.
