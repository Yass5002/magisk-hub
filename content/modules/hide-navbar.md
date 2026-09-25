---
id: "hide-navbar"
title: "NavTweaks: Fullscreen Gesture & Navigation Bar Customizer"
sidebarTitle: "NavTweaks"
description: "Customizes the appearance of Android navigation bars, enabling true fullscreen gesture navigation by hiding the gesture pill and keyboard spacer."
category: "customization-ui"
tier: 1
searchQueries:
  - "hide navbar magisk module"
  - "navtweaks fullscreen gestures android"
  - "hide gesture pill android 14 15"
  - "danglvk navtweaks"
  - "remove keyboard bar gap magisk"
prerequisites:
  - "Android 10 through Android 15"
  - "Magisk 20+ or KernelSU / APatch"
  - "KernelSU users must have SystemUI present in the root list with 'unmount modules' disabled"
conflicts:
  - "GSI ROMs (inconsistent GSI overlay mounting behavior)"
  - "Navbar dynamic coloring (light/dark adaptiveness) is not guaranteed on Android 11+"
configPaths:
  - "/data/adb/modules/HideNavBar/"
features:
  - "True fullscreen immersive gestures: removes the navigation bar pill and reclaimed display space"
  - "Keyboard spacer elimination: removes the empty space beneath the software keyboard during typing"
  - "Interactive volume-key installer: select custom gesture bar heights, sensitivities, and overlay modes during flashing"
  - "Systemless overlay mounting: applies display metric changes without modifying framework APKs on disk"
  - "Broad OS compatibility: actively supports Android 10 (Q) through Android 15 (V)"
faq:
  - question: "Why does SystemUI crash or fail to apply on KernelSU?"
    answer: "KernelSU isolates applications using mount namespaces. To allow NavTweaks overlays to attach to SystemUI, you must ensure the SystemUI package is added to KernelSU's profile list with the 'unmount modules' option disabled."
  - question: "Can I change my gesture bar options after installing?"
    answer: "Yes. Simply re-flash the module in your root manager without uninstalling. The volume key selector will prompt you to pick your preferred bar height and spacing configuration again."
---

## Overview

Developed by **DanGLVK**, **NavTweaks** (formerly *Fullscreen/Immersive Gestures*) is a systemless interface module designed to customize the navigation bar and gesture pill across Android 10 through Android 15.

While Android's stock gesture navigation provides full-screen gestures, it leaves a persistent visual navigation bar ("gesture pill") and an artificial blank spacer beneath keyboards. NavTweaks injects targeted framework overlays to eliminate the gesture bar and restore genuine edge-to-edge screen real estate.

---

## Technical Architecture & How It Works

### Runtime Resource Overlay (RRO) Customization

NavTweaks operates through Android's Runtime Resource Overlay system:

1. **Volume Key Interactive Installer**: During installation via `customize.sh`, the module queries the hardware volume rocker to let users select custom overlay parameters (e.g. completely hidden pill, slim pill, keyboard gap removal, or tablet layouts).
2. **Framework Overlay Injection**: Builds and mounts customized `android.overlay` packages over `/system/overlay/` or `/product/overlay/`.
3. **Metric Overrides**: Redefines Android framework dimension integers (`navigation_bar_height`, `navigation_bar_frame_height`, `navigation_bar_gesture_height`) to zero or custom values, adjusting UI layout boundaries dynamically.

---

## Installation & Setup

1. Download the latest `NavTweaks-*.zip` release from official channels.
2. Flash the module in Magisk, KernelSU, or APatch.
3. Use your device's **Volume Up** (Select) and **Volume Down** (Confirm) keys to pick your desired visual style during terminal installation.
4. Reboot the device to apply framework overlays.

---

## Configuration & Usage

- **KernelSU Specific Requirement**: In KernelSU Manager, verify that `com.android.systemui` is included in your app list and that `Umount modules` is toggled off for it.
- **Reconfiguration**: To modify your bar height, keyboard gap, or corner radius later, simply flash the module zip again and choose different options in the installer prompt.

---

## Troubleshooting & Common Issues

- **GSI ROM Issues**: Generic System Images (GSIs) often employ non-standard overlay priority ordering, which may cause navigation bar tweaks to be ignored.
- **Navbar Coloring Inconsistencies**: On Android 11 and above, adaptive light/dark navbar tinting may behave inconsistently depending on OEM launcher theming.
