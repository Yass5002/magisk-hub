---
id: "camera2api-hal3-mtk"
title: "Camera2API HAL3 Enabler - Universal MTK"
sidebarTitle: "Camera2API MTK"
description: "Systemless Magisk, KernelSU, and APatch module that force-enables Camera2 API HAL3 and EIS on MediaTek Android 8–14 devices via system.prop, post-fs-data.sh, and a brand-aware service daemon."
category: "system-environment"
tier: 1
searchQueries:
  - "camera2api hal3 mtk magisk module"
  - "enable camera2api mediatek android 14"
  - "gcam mediatek hal3 eis magisk"
  - "camera2api_mtk_universal"
  - "resetprop persist.vendor.camera.HAL3.enabled"
prerequisites:
  - "MediaTek (MTK) SoC device running Android 8.0 through Android 14"
  - "Magisk v19.0+ (`minMagisk=1900`), KernelSU, or APatch"
conflicts:
  - "Other Camera2 API enabler or vendor camera prop modules modifying `persist.vendor.camera.HAL3.enabled`"
configPaths:
  - "/data/adb/modules/camera2api_mtk_universal/system.prop"
  - "/data/adb/modules/camera2api_mtk_universal/permission_trigger.sh"
  - "/data/adb/camera2api_mtk.log"
features:
  - "Sets core Camera2 HAL3 and Electronic Image Stabilization (EIS) properties via `system.prop` and early `post-fs-data.sh` `resetprop` hooks"
  - "Runs a persistent `service.sh` daemon every 20 seconds inspecting `ro.product.brand` to enforce OEM-specific MediaTek camera properties (`samsung`, `xiaomi`/`redmi`/`poco`, `oppo`/`realme`, `vivo`, `infinix`/`tecno`/`itel`)"
  - "Includes `permission_trigger.sh` helper to grant `CAMERA` and `RECORD_AUDIO` runtime permissions for Google Camera, stock camera, and Snap packages"
  - "Logs device detection, applied vendor profile, and enforcement state to `/data/adb/camera2api_mtk.log`"
faq:
  - question: "Why does Camera2 API Probe still show `LEGACY` or `LIMITED` after flashing this module?"
    answer: "While this module aggressively sets HAL3 and EIS system properties and re-applies them every 20 seconds to prevent vendor resets, some OEMs (especially certain Samsung, Oppo, and Vivo MediaTek builds) disable HAL3 inside closed-source camera HAL `.so` binaries or device firmware. If the underlying vendor HAL hard-blocks HAL3, property overrides alone cannot upgrade the hardware level to `FULL` or `LEVEL_3`."
  - question: "Does the 20-second loop in `service.sh` drain battery?"
    answer: "Each iteration runs a lightweight shell `case` branch with `resetprop` calls and sleeps for 20 seconds, resulting in minimal CPU wake overhead, though it writes a status line to `/data/adb/camera2api_mtk.log` on every cycle."
---

## Overview

**Camera2API HAL3 Enabler - Universal MTK** (`camera2api_mtk_universal`), created by **AnasBex**, is an aggressive systemless module targeting **MediaTek (MTK)** smartphones and tablets running **Android 8 through Android 14**. Many budget and mid-range MediaTek devices ship with Camera2 API restricted to `LEGACY` or `LIMITED` modes—blocking manual exposure, RAW capture, and Google Camera (GCam) ports—even when the ISP supports higher capabilities.

The module combines static `system.prop` overrides, early `post-fs-data.sh` initialization, and a brand-aware `service.sh` loop to prevent vendor services from resetting HAL3 properties back to `0`.

---

## Technical Architecture & How It Works

Inspecting `Camera2API-MTK-v2026.0102.0421.zip` shows five coordinated components:

### 1. Installer Cleanup (`META-INF/com/google/android/update-binary`)
During installation, `update-binary` removes legacy `/data/adb/modules/Camera2API-MTK` installations and unpacks `module.prop`, `system.prop`, `post-fs-data.sh`, `service.sh`, and `permission_trigger.sh` with `0755` executable permissions on all shell scripts.

### 2. Static Property Overrides (`system.prop`)
Sets baseline HAL3 and EIS flags at module mount:
```ini
persist.vendor.camera.HAL3.enabled=1
ro.vendor.camera.HAL3.enabled=1
persist.camera.HAL3.enabled=1
camera.hal3.enabled=1

persist.vendor.camera.eis.enable=1
persist.vendor.camera.is_mode=4
persist.vendor.camera.enableBusDC=1
persist.vendor.camera.stats.test=5
```

### 3. Early Boot Patching (`post-fs-data.sh`)
Before Zygote starts, `post-fs-data.sh` initializes `/data/adb/camera2api_mtk.log`, records `ro.product.brand`, `ro.product.model`, and `ro.product.vendor.manufacturer`, and forces the base HAL3 and EIS properties via `resetprop`.

### 4. Brand-Aware Enforcement Daemon (`service.sh`)
After boot, `service.sh` reads `ro.product.brand` (lowercased) and loops every `20` seconds applying OEM-specific property sets via `resetprop`:
- **`samsung`**: Enforces `persist.vendor.camera.HAL3.enabled`, `ro.vendor.camera.HAL3.enabled`, and `persist.vendor.camera.eis.enable`.
- **`xiaomi` | `redmi` | `poco`**: Enforces `persist.vendor.camera.HAL3.enabled`, `persist.vendor.camera.manufacturer_id`, and `persist.vendor.camera.enableBusDC`.
- **`oppo` | `realme`**: Sets `persist.vendor.cam.hal3.enabled`, `persist.vendor.camera.HAL3.enabled`, and `vendor.camera.aux.packagelist "*"`.
- **`vivo`**: Sets `persist.vendor.camera.HAL3.enabled` and `persist.camera.HAL3.enabled`.
- **`infinix` | `tecno` | `itel`**: Sets `persist.vendor.camera.HAL3.enabled` and `persist.vendor.camera.eis.enable`.
- **Generic AOSP / Other MTK**: Applies `persist.vendor.camera.HAL3.enabled` and `persist.camera.HAL3.enabled`.

### 5. Permission Helper (`permission_trigger.sh`)
An optional standalone script in `$MODPATH/permission_trigger.sh` that grants `android.permission.CAMERA` and `android.permission.RECORD_AUDIO` via `pm grant` to `com.google.android.GoogleCamera`, `com.android.camera`, and `org.cyanogenmod.snap` if present.

---

## Installation & Verification

1. Flash `Camera2API-MTK-v2026.0102.0421.zip` in **Magisk**, **KernelSU**, or **APatch**.
2. Reboot your device.
3. Verify property state and daemon log output via root shell:

```bash
# Inspect boot and daemon enforcement log
su -c "tail -n 30 /data/adb/camera2api_mtk.log"

# Verify active HAL3 & EIS properties
getprop persist.vendor.camera.HAL3.enabled
getprop ro.vendor.camera.HAL3.enabled
getprop persist.vendor.camera.eis.enable
```

4. Open **Camera2 API Probe** to confirm your hardware support level (`LEVEL_3` or `FULL` indicates full HAL3 support; `LIMITED` or `LEGACY` indicates remaining vendor HAL firmware locks).
