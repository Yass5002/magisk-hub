---
id: "smbootfx"
title: "SMbootFX: Systemless Custom QMG Boot & Shutdown Animations for Samsung One UI"
sidebarTitle: "SMbootFX"
description: "Systemless boot and shutdown animation replacement framework for rooted Samsung Galaxy devices running One UI, utilizing Samsung's proprietary QMG graphics format."
category: "system-environment"
tier: 1
searchQueries:
  - "smbootfx magisk module"
  - "john0n1 smbootfx"
  - "samsung qmg boot animation magisk"
  - "custom boot animation one ui root"
  - "bootsamsung qmg systemless replacement"
prerequisites:
  - "Samsung Galaxy smartphone or tablet running One UI / TouchWiz (Android 7 through 16)"
  - "Root access via Magisk v27+ or KernelSU"
  - "Device firmware utilizing Samsung's proprietary .qmg boot graphics engine"
conflicts:
  - "Non-Samsung OEM devices (Google Pixel, Xiaomi, OnePlus, Motorola) and pure AOSP ROMs (strictly require standard bootanimation.zip)"
configPaths:
  - "/data/adb/modules/smbootfx/"
  - "/system/media/bootsamsung.qmg"
  - "/system/media/bootsamsungloop.qmg"
  - "/system/media/shutdown.qmg"
features:
  - "Native Samsung QMG engine support: replaces proprietary bootsamsung.qmg, bootsamsungloop.qmg, and shutdown.qmg systemlessly"
  - "Curated theme library: offers diverse visual themes ranging from retro Android and CyanogenMod to NetHunter and cyberpunk designs"
  - "Coordinated shutdown animations: synchronizes power-down sequences to match startup visuals"
  - "Zero partition modification: binds custom animation assets over /system/media/ without tripping system partition verification"
---

## Overview

Unlike the broader Android ecosystem—which uses standardized ZIP archives containing sequenced PNG frames and a `desc.txt` timing descriptor (`bootanimation.zip`)—Samsung Galaxy firmware utilizes an entirely proprietary graphics pipeline. Samsung's bootloader and `bootchecker` binaries render boot and shutdown sequences via compiled `.qmg` (Qualcomm Multimedia Graphics) image containers located in `/system/media/`.

Because of this proprietary format, standard AOSP boot animation modules do not work on Samsung One UI.

Created by John0n1, **SMbootFX** is a specialized systemless customization framework engineered specifically for Samsung Galaxy devices. Provided as ready-to-flash Magisk and KernelSU modules, SMbootFX overlays high-definition, professionally converted `.qmg` assets over Samsung's stock startup and shutdown animations without altering read-only system partitions.

## Compatibility & Format Constraints

- **Samsung Exclusivity**: This module is built strictly for Samsung Galaxy handsets and tablets running stock One UI or Samsung-based custom ROMs (from Android 7 up to Android 16).
- **Non-Samsung Incompatibility**: Devices from Google, Xiaomi, Motorola, Sony, or OnePlus, as well as AOSP-based custom ROMs (LineageOS, PixelOS), rely on standard `bootanimation.zip` archives and cannot interpret `.qmg` assets.
- **Root Managers**: Requires Magisk v27+ or KernelSU.

## Themed Visual Profiles

SMbootFX packages a wide collection of themed visual styles, each providing both boot and shutdown graphics:

- **Classic & Modern Android**: Android Purple, Android Red, Android Green on Black, Android White on Plum, KitKat Classic, and KitKat Easter Egg.
- **Custom ROM Heritage**: CyanogenMod Android, AOKP, and AOKP Magical.
- **Cyberpunk & Security Aesthetics**: Kali NetHunter, NetHunter Glitch, CTOS (Watchdogs), and NSA Terminal.
- **Minimalist & Brand Themes**: Apple Static Black, Apple Static White, and MIUI Multi-Color variants.

## How Samsung QMG Animations Are Structured

The module mounts pre-rendered, high-framerate `.qmg` files into `/system/media/`:
- **`bootsamsung.qmg`**: The initial introductory splash animation executed immediately after kernel handoff.
- **`bootsamsungloop.qmg`**: The looping animation displayed while Android services and ART compilation warm up.
- **`shutdown.qmg`**: The smooth power-down animation triggered when the device is rebooted or switched off.

## Installation & Setup

1. Verify that your Samsung device is rooted with Magisk v27+ or KernelSU.
2. Download your preferred theme package (e.g., `android-bootfx-*-magisk.zip` or `nethunter-bootfx-*-magisk.zip`) from the official SMbootFX repository releases.
3. Open your root manager and flash the module ZIP.
4. Reboot your phone. The initial bootloader splash will transition smoothly into your custom `.qmg` animation sequence.

## Troubleshooting

- **Animation Remains Stock Samsung**: Verify in your root manager that the module is enabled. On certain newer One UI versions, ensure that your root manager's mount namespace has not isolated the `/system/media` path from the system server.
- **Stuck on Samsung Logo**: If the boot animation hangs, verify that your device has sufficient RAM allocated during early boot and that no secondary boot animation module is conflicting in `/system/media/`.
