---
id: "pixelxpert-next"
title: "PixelXpert-Next: Xposed & Root SystemUI Customizer for Google Pixel"
sidebarTitle: "PixelXpert-Next"
description: "Continuation fork of PixelXpert bundling an Xposed companion app and root module to customize SystemUI, lock screen, quick settings, and framework behavior on stock Google Pixel ROMs."
category: "customization-ui"
tier: 1
searchQueries:
  - "pixelxpert next magisk module"
  - "pixelxpert android 16 17"
  - "pixel stock rom xposed customizer"
  - "sh.anirudhgupta109.pxn lsposed"
  - "pixelxpert next kernelsu setup"
prerequisites:
  - "Google Pixel device running stock Pixel firmware (Android 13–17+; QPR builds supported per release target)"
  - "Magisk v25.0+ (`minMagisk=25000`), KernelSU, or APatch"
  - "LSPosed framework installed and active (`/data/adb/lspd/config/modules_config.db`)"
conflicts:
  - "Legacy PixelXpert (`sh.siava.pixelxpert`) — automatically uninstalled by the installer"
  - "Custom AOSP ROMs (Pixel Experience, LineageOS, etc.) or non-Pixel OEM firmware (One UI, HyperOS, ColorOS)"
  - "Other SystemUI or framework Xposed modules hooking the same Quick Settings, status bar, or lock screen methods"
configPaths:
  - "/data/adb/modules/PixelXpert-Next/"
  - "/data/adb/lspd/config/modules_config.db"
  - "/data/adb/magisk.db"
  - "/product/priv-app/TipsPrebuilt*"
features:
  - "Modular Xposed hooks across Status Bar, Quick Settings panel, Lock Screen, Notifications, and Gesture Navigation"
  - "System framework tweaks for Phone & Dialer, Hotspot, Package Manager, and Display/Screen properties"
  - "Self-contained flashable ZIP bundling `PixelXpert-Next.apk` (`sh.anirudhgupta109.pxn`) and a static `sqlite3` binary"
  - "Automated Magisk `magisk.db` root policy provisioning and boot-time APK installation recovery"
faq:
  - question: "Why does PixelXpert-Next abort installation on non-Pixel or custom ROMs?"
    answer: "During flashing, `customize.sh` runs `assertPixelRom()`, which checks `/product/priv-app` for `TipsPrebuilt*`, and `assert16QPR()`, which validates `ro.build.id` against expected Pixel QPR build patterns (`[CD][DP][1-5]` in v6.1.5). Custom ROMs and third-party OEM skins alter SystemUI signatures and lack stock Pixel hooks, so the installer aborts to prevent bootloops."
  - question: "How does PixelXpert-Next handle root permissions on Magisk vs KernelSU or APatch?"
    answer: "On Magisk, both `customize.sh` and `service.sh` invoke the bundled `sqlite3` binary to insert or update a silent root grant (`policy = 2`) for `sh.anirudhgupta109.pxn` directly inside `/data/adb/magisk.db`. On KernelSU and APatch, automatic DB injection is skipped and you must grant Superuser access manually inside your root manager (enable 'Show system apps' if the companion package is not immediately listed)."
  - question: "What happens if `PixelXpert-Next.apk` fails to install during flashing?"
    answer: "If `pm install -r -d` fails in recovery/installer context or if Android strips a system-staged copy on reboot, `customize.sh` creates `$MODPATH/install_needed`. On the next boot, `service.sh` waits until `sys.boot_completed` reaches `1` and automatically retries `pm install -r -d $MODDIR/PixelXpert-Next.apk` before clearing the marker."
---

## Overview

**PixelXpert-Next** (`anirudhgupta109/PixelXpert-Next`) is the active continuation fork of the original `siavash79/PixelXpert` project, maintained to track newer Google Pixel stock firmware releases (including Android 16 QPR and Android 17+ builds, while older Android 12–16 builds remain covered by legacy releases).

Unlike standalone Xposed APKs, PixelXpert-Next ships as a hybrid **flashable Magisk/KernelSU/APatch module** (`PixelXpert-Next.zip`, module ID `PixelXpert-Next`) that pairs native root-level system provisioning with an embedded Xposed companion application (`PixelXpert-Next.apk`, package `sh.anirudhgupta109.pxn`).

---

## Technical Architecture & Payload Internals

Inspecting the `PixelXpert-Next.zip` release payload reveals a focused four-part architecture:

| Component | Role inside the Module |
| --- | --- |
| `PixelXpert-Next.apk` | Xposed module & UI (`sh.anirudhgupta109.pxn`) providing preferences, SystemUI/framework hooks, and live controls |
| `customize.sh` | Runs ROM compatibility assertions, legacy cleanup, APK deployment, and Magisk DB root provisioning |
| `service.sh` | Boot-time script ensuring Magisk root policy persistence, legacy package removal, and deferred APK installation |
| `sqlite3` | Bundled static SQLite CLI used by `customize.sh` and `service.sh` to query/update `/data/adb/magisk.db` |

### Installation Guards & Automated Provisioning

1. **Stock Pixel & Build Assertions**: Before modifying anything, `customize.sh` invokes `assertPixelRom()` (verifying `/product/priv-app/TipsPrebuilt*`) and `assert16QPR()` (checking `getprop ro.build.id` against `[CD][DP][1-5]` on current v6.1.5 builds). Incompatible ROMs abort cleanly before touching system state.
2. **Legacy Package Migration**: If the discontinued upstream package `sh.siava.pixelxpert` is detected via `pm list packages`, both `customize.sh` and `service.sh` remove it with `pm uninstall --user 0 sh.siava.pixelxpert` to avoid hook collisions.
3. **Silent Root Policy Injection (Magisk)**: Using the bundled `sqlite3` binary, `grantRootUID()` resolves the package UID via `pm list packages -U sh.anirudhgupta109.pxn --user 0` and writes `policy = 2, until = 0, logging = 1, notification = 0` into the `policies` table of `/data/adb/magisk.db`.
4. **LSPosed Verification**: `customize.sh` checks `/data/adb/lspd/config/modules_config.db` to confirm LSPosed is installed, printing a warning if the database is absent.

### Customization Scope

Once enabled in LSPosed, PixelXpert-Next hooks SystemUI and Android framework components to unlock modifications across:

- **Status Bar & Quick Settings**: Clock positioning, network traffic indicators, tile grid density, header layouts, and media/brightness slider behavior.
- **Lock Screen & Notifications**: Custom shortcuts, status indicators, lock screen clock/font adjustments, and notification snoozing/expansion rules.
- **Navigation, Dialer & System Utilities**: Gesture bar sizing/hiding, hotspot client/band controls, phone & dialer behavior, package manager tweaks, and screen property overrides.

---

## Installation & Configuration

1. Ensure **LSPosed** (Zygisk-based) is already installed and working on your stock Google Pixel ROM.
2. Download `PixelXpert-Next.zip` and flash it in **Magisk** (v25.0+), **KernelSU**, or **APatch**.
3. **KernelSU / APatch Note**: Watch the installer output—if you use KernelSU or APatch, do not let default module umount rules hide the module from target processes, and manually grant Superuser permission to **PixelXpert-Next** (`sh.anirudhgupta109.pxn`) in your manager app after rebooting.
4. Reboot your device.
5. Open **LSPosed Manager** → **Modules** → enable **PixelXpert-Next** (keep the recommended System Framework and SystemUI scopes active), then reboot or soft-reboot SystemUI for hooks to take effect.

---

## Common Issues & Troubleshooting

- **Module Aborts with "Installation aborted due to incompatibility"**: Your current firmware either lacks `/product/priv-app/TipsPrebuilt*` (custom ROM or non-Pixel device) or its `ro.build.id` does not match the QPR generation targeted by v6.1.5. Check upstream release notes for the build matching your Android version/QPR branch.
- **Companion App Opens Without Root Privileges (KernelSU/APatch)**: Open your root manager's Superuser tab, enable **Show system apps** if hidden, and grant root access to `sh.anirudhgupta109.pxn`.
- **Changes Not Applying in SystemUI**: Verify `/data/adb/lspd/config/modules_config.db` exists, confirm PixelXpert-Next is enabled in LSPosed with **SystemUI** (`com.android.systemui`) and **System Framework** (`android`) checked, and restart SystemUI from the app's menu.
