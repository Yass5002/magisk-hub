---
id: "blurclosed"
title: "Blur Closed: Systemless Android UI & SurfaceFlinger Blur Disabler"
sidebarTitle: "Blur Closed"
description: "GPL-3.0 Magisk, KernelSU, and APatch module that disables real-time window and background blur across AOSP SurfaceFlinger and major OEM ROMs via resetprop and WindowManager."
category: "customization-ui"
tier: 1
searchQueries:
  - "blurclosed magisk module"
  - "disable android background blur root"
  - "ro.surface_flinger.force_disable_blur resetprop"
  - "disable blurs miui hyperos coloros oneui"
  - "cmd window disable-blur 1"
prerequisites:
  - "Magisk v20.4+, KernelSU, or APatch"
  - "Android 11+ recommended (`API < 30` shows a compatibility warning during installation)"
conflicts:
  - "UI customization modules that force-enable SurfaceFlinger or launcher blur (`enable_blurs_on_windows=1`)"
configPaths:
  - "/data/adb/modules/blurclosed/post-fs-data.sh"
  - "/data/adb/modules/blurclosed/uninstall.sh"
features:
  - "Applies `resetprop -n` during `post-fs-data.sh` only on properties that already exist on the device (`check_and_resetprop`), avoiding unnecessary property pollution"
  - "Disables AOSP and SurfaceFlinger blur flags including `disableBlurs=1`, `disableBackgroundBlur=1`, `enable_blurs_on_windows=0`, `ro.surface_flinger.force_disable_blur=1`, and `persist.sys.sf.disable_blurs=1`"
  - "Covers OEM-specific blur properties for MIUI/HyperOS (`ro.miui.has_blur`, `persist.sysui.miui_blur_enabled`), ColorOS/OnePlus/Oppo, Samsung OneUI, and Flyme"
  - "Invokes `cmd window disable-blur 1` (`API >= 29`) at install/boot and cleanly restores `disable-blur 0` via `uninstall.sh`"
faq:
  - question: "Why does Blur Closed check whether a property already exists before calling `resetprop -n`?"
    answer: "In `post-fs-data.sh`, `check_and_resetprop()` reads the current property via `resetprop \"$prop_name\"` and returns early if the string is empty or already matches the target value. This ensures OEM-specific keys (such as MIUI or Samsung flags) are only rewritten on ROMs that actually define them."
  - question: "Will uninstalling Blur Closed restore normal background blur?"
    answer: "Yes. Because property overrides are applied systemlessly via `resetprop` at boot and `uninstall.sh` executes `cmd window disable-blur 0` (or `cmd wm disable-blur 0` on older SDKs), removing the module in Magisk, KernelSU, or APatch and rebooting restores stock blur behavior."
---

## Overview

**Blur Closed** (`blurclosed`), developed by **Astoritin**, is a lightweight, open-source (GPL-3.0) module built to eliminate GPU-intensive real-time Gaussian blur effects across Android's WindowManager, SurfaceFlinger, and OEM UI layers. On mid-range SoCs or high-refresh-rate displays, rendering multi-pass background blur behind notification shades, app drawers, and dialogs can introduce frame drops and extra GPU power draw.

By disabling window and surface blur at the `post-fs-data` stage before Zygote initializes, Blur Closed reduces compositor overhead without modifying any system APKs.

---

## Technical Architecture & Property Matrix

Inspecting `BlurClosed-1.1.1.zip` confirms SHA-256 verified installation (`customize.sh`), a targeted `post-fs-data.sh` property patcher, and clean restoration in `uninstall.sh`:

### 1. Conditional Property Patching (`check_and_resetprop`)
Instead of blindly injecting dozens of foreign properties into the kernel property area, `post-fs-data.sh` defines:
```sh
check_and_resetprop() {
    local prop_name=$1
    local prop_expect_value=$2
    local prop_current_value=$(resetprop "$prop_name")
    [ -z "$prop_current_value" ] && return 1
    [ "$prop_current_value" = "$prop_expect_value" ] && return 0
    resetprop -n "$prop_name" "$prop_expect_value"
}
```
Only properties present on the running firmware whose value differs from the target are updated with `resetprop -n`.

### 2. Targeted Blur Properties
- **AOSP / SurfaceFlinger / WindowManager**:
  - `disableBlurs=1`, `disableBackgroundBlur=1`, `enable_blurs_on_windows=0`
  - `ro.surface_flinger.force_disable_blur=1`, `ro.surface_flinger.supports_background_blur=0`, `persist.sys.sf.disable_blurs=1`
  - `ro.sf.blurs_are_costly=1`, `ro.sf.blurs_are_expensive=1`, `ro.launcher.blur.appLaunch=0`
  - `windowBlurBehindEnabled=false`, `windowBlurBehindRadius=0`
- **Generic System / Background Blur**:
  - `persist.sys.background_blur_supported=0`, `persist.sys.background_blur_status_default=0`, `persist.sys.background_blur_version=0`, `persist.sys.add_blurnoise_supported=0`, `persist.sys.enable_third_blur=0`, `persist.sys.dynamic_blur_enabled=0`, `persist.perf.wm_static_blur=false`, `persist.sys.static_blur_mode=true`, `persist.vendor.sf.blur.type=none`, `persist.sys.disable_blur_view=true`, `persist.sys.disable_glass_blur=true`, `sys.use_frost_effect=0`
- **OEM UI Frameworks**:
  - **MIUI / HyperOS**: `persist.sysui.miui_blur_enabled=0`, `ro.miui.has_blur=0`, `ro.miui.has_real_blur=0`, `ro.miui.backdrop_sampling_enabled=0`, `persist.miui.ui.optimize_blur=0`
  - **Oplus / OnePlus / Oppo**: `persist.sys.oneplus.blur.enabled=0`, `persist.sys.oplus.ui.blur=0`, `persist.sys.oppo.blur.enable=0`
  - **Samsung OneUI**: `persist.sys.samsung.blur.disable=1`
  - **Meizu Flyme**: `persist.meizu.gpu_blur=0`

### 3. WindowManager Runtime Command
Both `customize.sh` and `post-fs-data.sh` execute:
```sh
[ "$API" -ge "29" ] && cmd window disable-blur 1 || cmd wm disable-blur 1
```
During module removal, `uninstall.sh` resets the WindowManager flag back to `0`.

---

## Installation & Verification

1. Flash `BlurClosed-1.1.1.zip` in **Magisk**, **KernelSU**, or **APatch**.
2. Reboot your device so `post-fs-data.sh` runs prior to UI startup.
3. Verify that key blur properties are disabled via ADB shell:

```bash
# Check AOSP/SurfaceFlinger blur properties
getprop ro.surface_flinger.force_disable_blur
getprop persist.sys.sf.disable_blurs
getprop enable_blurs_on_windows

# Inspect WindowManager blur state
dumpsys window | grep -i blur
```
