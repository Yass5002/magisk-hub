---
id: "disable-flag-secure"
title: "DisableFlagSecure (Enable Screenshot): Bypass FLAG_SECURE & Detection"
sidebarTitle: "DisableFlagSecure"
description: "Official LSPosed module (io.github.lsposed.disableflagsecure) for Android 12–16 that enables screenshots in FLAG_SECURE apps and blocks screenshot and screen-recording detection."
category: "xposed-runtime-hooks"
tier: 1
searchQueries:
  - "disableflagsecure lsposed download"
  - "enable screenshot lsposed module"
  - "bypass flag secure android 15 16"
  - "disable screenshot detection android 14"
  - "hyperos coloros oneui screenshot restriction bypass"
prerequisites:
  - "Official LSPosed framework supporting libxposed API 101 (unofficial LSPosed forks are explicitly unsupported)"
  - "Stock or OEM Android 12–16 firmware (including Xiaomi HyperOS, OPlus ColorOS/RealmeUI/OxygenOS, and Samsung One UI; custom ROMs are not supported)"
conflicts:
  - "Unofficial LSPosed forks or legacy Xposed frameworks"
  - "Other modules hooking `WindowManagerService` or `FLAG_SECURE` window flags simultaneously"
configPaths:
  - "/data/adb/lspd/"
features:
  - "Enables screenshots and screen recording inside banking, streaming, and messaging apps guarded by `WindowManager.LayoutParams.FLAG_SECURE`"
  - "Disables Android 14+ `registerScreenCaptureCallback` screenshot detection notifications"
  - "Disables Android 15+ screen-recording detection APIs (`ScreenRecordingCallback`)"
  - "Broad OEM stock support across Android 12–16: AOSP, Xiaomi HyperOS, OPlus OS (ColorOS, RealmeUI, OxygenOS), and Samsung One UI"
  - "Minimalist, zero-bloat libxposed API 101 module (`io.github.lsposed.disableflagsecure`, ~20 KB APK) with `staticScope=true`"
faq:
  - question: "Which apps should I select in LSPosed Scope for DisableFlagSecure?"
    answer: "Select ONLY the recommended system processes listed in the module's scope (`system`, `com.android.systemui`, `com.miui.screenshot`, `com.oplus.screenshot`, `com.oplus.appplatform`, `com.flyme.systemuiex` as applicable to your OEM). Do NOT check third-party user apps—doing so is unnecessary and unsupported."
  - question: "Are custom ROMs or unofficial LSPosed builds supported?"
    answer: "No. Per the official `LSPosed/DisableFlagSecure` README, unofficial LSPosed versions and custom ROMs are explicitly not supported. The module targets official LSPosed on Android 12–16 stock/OEM builds (HyperOS, ColorOS/RealmeUI/OxygenOS, One UI)."
  - question: "Why does the module have no launcher icon?"
    answer: "DisableFlagSecure (`io.github.lsposed.disableflagsecure`) is a pure, configuration-free libxposed runtime hook (`app-release.apk`, ~20.8 KB) with no settings UI. Once enabled in LSPosed with the recommended scope and rebooted, it operates automatically."
---

## Overview

**Enable Screenshot** (widely known by its repository name **DisableFlagSecure**, `LSPosed/DisableFlagSecure`) is an official Xposed module maintained by the **LSPosed** developers.

Android applications routinely set `WindowManager.LayoutParams.FLAG_SECURE` to prevent screenshots, screen recordings, and recents-screen previews—turning captures black or triggering system blocks. Furthermore, **Android 14** introduced official screenshot detection callbacks (`Activity.ScreenCaptureCallback`), and **Android 15** expanded this with active screen-recording detection callbacks so apps know when you capture their interface.

DisableFlagSecure patches the system window and capture-notification pipeline at runtime, allowing screenshots and screen recordings across protected windows while suppressing OS-level capture detection on **Android 12 through Android 16**.

---

## Technical Architecture & How It Works

### libxposed API 101 & OEM Scope Targeting

Inspecting the `v5.0.1` payload (`app-release.apk` for `io.github.lsposed.disableflagsecure`) highlights its ultra-lightweight design:

- **Minimalist Footprint**: At roughly 20.8 KB (`classes.dex`, `AndroidManifest.xml`, `resources.arsc`, and `META-INF/xposed/*`), the APK contains no native libraries and no background user-facing launcher UI.
- **libxposed API 101 Static Scope**: `META-INF/xposed/module.prop` specifies `minApiVersion=101`, `targetApiVersion=101`, and `staticScope=true`.
- **Predefined System & Screenshot Scope (`META-INF/xposed/scope.list`)**:
  - `system` (Android System Framework / `WindowManagerService` & capture detection services)
  - `com.android.systemui` (SystemUI screenshot & recents handling)
  - `com.miui.screenshot` (Xiaomi HyperOS / MIUI Screenshot)
  - `com.oplus.screenshot` & `com.oplus.appplatform` (OPlus ColorOS / RealmeUI / OxygenOS)
  - `com.flyme.systemuiex` (Meizu Flyme SystemUI)

By hooking directly inside the system framework and OEM screenshot services rather than individual third-party apps, DisableFlagSecure handles `FLAG_SECURE` enforcement and Android 14+/15+ capture callbacks uniformly without needing per-app scope maintenance.

---

## Supported Operating Systems

Per upstream `LSPosed/DisableFlagSecure` documentation:
- **Android 12 – 16** (Stock/OEM builds; **Custom ROMs are not supported**)
- **Xiaomi HyperOS**
- **OPlus OS**: **ColorOS**, **RealmeUI**, and **OxygenOS**
- **Samsung One UI**
- **Framework Requirement**: Official **LSPosed** only (unofficial LSPosed builds are not supported)

---

## Installation & Usage

1. Download `app-release.apk` (`v5.0.1` or latest) from `LSPosed/DisableFlagSecure`.
2. Install the APK on your rooted device:
   ```bash
   adb install app-release.apk
   ```
3. Open **LSPosed Manager** -> **Modules** -> **Enable Screenshot / DisableFlagSecure**.
4. Toggle the module **ON** and select **ONLY** the recommended system packages pre-selected in Scope (do not check third-party apps).
5. **Reboot** your device for the `system` and SystemUI hooks to take effect.

---

## Troubleshooting & Notes

- **Screenshots still blocked or black on a Custom ROM**: Custom ROMs often alter `WindowManagerService` or `SurfaceFlinger` signatures outside AOSP/OEM baselines and are explicitly unsupported upstream.
- **App still detects screenshots on Android 14/15+**: Double-check that `system` is selected in Scope, you are running an official LSPosed build, and you rebooted after enabling the module. Note that hardware-backed Widevine L1 DRM video surfaces (e.g., encrypted Netflix video layers) may still render black at the SurfaceFlinger/composer hardware layer even with `FLAG_SECURE` disabled.
