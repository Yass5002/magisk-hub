---
id: "pui-interface-control-suite"
title: "PUI System Interface & Control Suite: ColorOS 15 & OxygenOS 15 Theme"
sidebarTitle: "PUI Interface Suite"
description: "Comprehensive system interface customization and control center theme overlay tailored for modern ColorOS 15 and OxygenOS 15 firmware builds."
category: "customization-ui"
tier: 1
searchQueries:
  - "pui for os15 magisk"
  - "coloros 15 theme module magisk"
  - "oxygenos 15 control center customize"
  - "pui theme customized root"
prerequisites:
  - "OnePlus, Oppo, or Realme device running ColorOS 15 or OxygenOS 15 (Android 15)"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other SystemUI overlay modules targeting ColorOS 15"
configPaths:
  - "/system/product/overlay/PUIThemeCustomized.apk"
  - "/system/system_ext/overlay/PUIThemeCustomized.apk"
features:
  - "Tailored specifically for the Android 15 visual hierarchy and Quick Settings redesign"
  - "Restyles Control Center brightness and volume sliders with refined ergonomic curves"
  - "Customizes notification cards, status bar icons, and quick setting toggle active states"
  - "Non-destructive RRO (Runtime Resource Overlay) architecture avoids framework binary patching"
faq:
  - question: "Can I use this module on older ColorOS 13 or 14 devices?"
    answer: "This suite is specifically compiled against the resource IDs and XML structures of ColorOS 15 and OxygenOS 15. Flashing on older Android versions may result in unapplied themes or SystemUI FC."
  - question: "Does this require an Xposed or LSPosed framework?"
    answer: "No. The module utilizes Android's native Runtime Resource Overlay (RRO) mechanism loaded systemlessly by Magisk, requiring zero hooked code or ART runtime patches."
---

## Overview

**PUI System Interface & Control Suite** (created by Tiansansha & PanL) is a bespoke theme modification tailored for the new generation of Oppo, OnePlus, and Realme devices running ColorOS 15 and OxygenOS 15.

Android 15 introduces significant architectural changes to SystemUI layout hierarchies and notification shade compositions. PUI Suite introduces an elegant, unified visual theme that enhances the transparency effects, slider dynamics, and quick-toggle geometry of the ColorOS 15 Control Center.

---

## Technical Architecture & How It Works

The module integrates seamlessly via Android's Runtime Resource Overlay (RRO) subsystem:

### 1. Overlay Injection

The module mounts pre-compiled APK overlays:

```bash
/system/product/overlay/PUIThemeCustomized.apk
```

These overlays hook directly into the framework resource tables of `com.android.systemui` and `com.oplus.systemui`, overriding visual dimensions, colors, and drawables without touching the compiled Java/smali bytecode.

### 2. Control Center Ergonomics

- **Slider Geometry**: Retunes the aspect ratio and corner radii of the brightness and audio sliders, providing a larger touch target.
- **Micro-Animations**: Enhances tactile visual feedback when toggling Bluetooth, Wi-Fi, and cellular tiles.

---

## Troubleshooting & Verification

- **Applying Changes**: A full system reboot is necessary for Android's `idmap2` daemon to register and link the new resource overlays.
- **Theme Conflicts**: If third-party Substratum or Theme Store themes are active, revert to the default system theme in Settings before activating this module.
