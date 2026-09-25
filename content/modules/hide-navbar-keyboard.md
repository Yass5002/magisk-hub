---
id: "hide-navbar-keyboard"
title: "Hide Navbar Keyboard: Immersive Keyboard Typing Without Navigation Bar"
sidebarTitle: "Hide Navbar Keyboard"
description: "Hides the system navigation bar when the keyboard appears on Android 10–15+, delivering an edge-to-edge typing experience without blank chin space."
category: "customization-ui"
tier: 1
searchQueries:
  - "hide navbar keyboard magisk"
  - "hide nav bar when typing android"
  - "unknuw hide navbar keyboard"
  - "remove keyboard chin magisk"
  - "hyperos aosp hide navigation bar keyboard"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "Android 10 to 15+ (AOSP, One UI, MIUI, or HyperOS)"
  - "Gesture navigation mode enabled"
conflicts: []
configPaths:
  - "/data/adb/modules/hide-navbar-keyboard/"
features:
  - "Automatic navbar suppression: eliminates the bottom navigation pill and spacer whenever an input method editor (IME) is active"
  - "Zero blank space: reclaims display real estate under Gboard, SwiftKey, and other virtual keyboards"
  - "Multi-ROM compatibility: universally functions across AOSP, LineageOS, MIUI, and HyperOS without hardcoded OEM string checks"
  - "Integrated gesture overlays: incorporates Android Q and R gesture styles for smooth entry and exit animations"
  - "Systemless installation: overlays display framework configurations without modifying core system partitions"
---

## Overview

On modern Android devices utilizing full-screen gesture navigation, the operating system frequently inserts a persistent navigation bar spacer—often referred to as the "keyboard chin"—directly beneath virtual keyboards. While this spacer originally prevented inadvertent touches on curved displays, on contemporary devices it creates unnecessary blank vertical space and pushes the keyboard layout uncomfortably high.

Developed by UNKNUW, **Hide-Navbar-Keyboard** is a systemless Magisk and KernelSU module that dynamically hides the navigation bar whenever the on-screen keyboard appears. Supporting Android versions from Android 10 through Android 15+, the module provides an immersive, full-width typing canvas on stock AOSP, Pixel firmware, Xiaomi MIUI/HyperOS, and custom OEM distributions.

## How It Works

The module deploys system runtime resource overlays (RRO) that intercept the Android window manager's keyboard insets and navigation bar visibility flags:

1. **IME State Detection**: Whenever the Input Method Editor (IME) window is requested by a foreground app, the overlay suppresses the bottom navigation inset.
2. **Dynamic Inset Reallocation**: The keyboard layout shifts downward to rest naturally against the bottom glass edge of the display, eliminating the empty black padding bar.
3. **Universal Compatibility**: Unlike older OEM-specific modifications that relied on hardcoded MIUI framework hooks, Hide-Navbar-Keyboard implements clean, platform-standard overlay declarations compatible with standard Android gesture navigation logic.

## Installation

1. Verify that your device runs Android 10 or later and has gesture navigation enabled.
2. Download the latest `Hide-Navbar-Keyboard_v*.FINAL.zip` release from GitHub.
3. Open **Magisk Manager** or **KernelSU Manager**, navigate to the **Modules** tab, and select **Install from storage**.
4. Select the downloaded archive and confirm flashing.
5. Reboot your device to apply the runtime overlay.

## Troubleshooting & Verification

- **Keyboard chin remains visible**: Ensure you are using gesture navigation rather than legacy 3-button navigation. Open **Settings > System > Gestures > System Navigation** and select **Gesture navigation**.
- **Keyboard clips with display curves**: Some third-party keyboards allow adjusting keyboard height or padding. In Gboard settings, open **Preferences > Keyboard height** to fine-tune spacing if bottom-row keys sit too close to rounded device corners.
- **Uninstallation**: Remove the module via Magisk/KernelSU Manager or delete `/data/adb/modules/hide-navbar-keyboard/` and reboot.
