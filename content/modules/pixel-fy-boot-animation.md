---
id: "pixel-fy-boot-animation"
title: "Pixel-fy Boot Animation: Authentic Google Pixel Boot Screen Systemless Module"
sidebarTitle: "Pixel-fy Boot Animation"
description: "Systemless boot animation module by wacko1805 replacing OEM boot screens with the authentic, smooth Google Pixel startup animation across AOSP and custom ROMs."
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "pixel boot animation magisk module"
  - "google pixel bootanimation zip root"
  - "pixel-fy boot animation download"
  - "replace boot animation magisk"
  - "systemless boot animation android"
prerequisites:
  - "Android 8.0 (Oreo) or newer"
  - "Root access via Magisk, KernelSU, or APatch"
  - "AOSP-based boot animation binary (Standard Android surfaceflinger bootanimation)"
conflicts:
  - "Samsung One UI stock firmware (uses proprietary QMG format instead of bootanimation.zip)"
  - "Competing boot animation modules mounting over /system/media/bootanimation.zip"
configPaths:
  - "/data/adb/modules/pixel-fy-boot-animation/"
  - "/system/media/bootanimation.zip"
  - "/product/media/bootanimation.zip"
features:
  - "Systemless overlay: replaces default OEM boot screens without altering system partition read-only blocks"
  - "Authentic Google Pixel visual styling featuring minimalist Google 'G' logo sequence"
  - "Universal scaling: surfaceflinger dynamically scales frame coordinates to fit device aspect ratios"
  - "Zero performance overhead: terminates automatically as soon as Android system server and zygote finish booting"
faq:
  - question: "Does this boot animation work on Samsung Galaxy devices?"
    answer: "No, standard Samsung One UI stock ROMs use Samsung's proprietary QMG bitmap format (`bootsamsung.qmg`) rather than AOSP's standard `bootanimation.zip`. Pixel-fy will only work on Samsung hardware if you are running an AOSP-based custom ROM (such as LineageOS or PixelOS)."
  - question: "Why is bootanimation.zip packaged with zero compression?"
    answer: "The Android early boot daemon (`/system/bin/bootanimation`) spawned by `surfaceflinger` reads animation frames sequentially during early userspace startup. Compressed ZIP files require extra CPU overhead and decompression memory that can delay the visual startup sequence, which is why Android specification mandates stored (`zip -0`) uncompressed archives."
  - question: "What if the boot animation causes a black screen or hang?"
    answer: "Media replacement modules rarely cause system hangs. However, if your display controller fails to initialize the frames, reboot into Safe Mode (holding Volume Down during device power-on) to automatically disable all Magisk/KernelSU modules, or delete `/data/adb/modules/pixel-fy-boot-animation` via custom recovery."
---

## Overview

The **Pixel-fy Boot Animation** module, developed by wacko1805, delivers the clean, minimalist Google Pixel startup animation to rooted Android devices.

When Android boots, the init process starts the graphics compositor daemon (`surfaceflinger`), which subsequently executes `/system/bin/bootanimation`. This binary displays an animation sequence while Zygote preloads classes and the Android system server initializes runtime services.

Many OEM manufacturer skins (such as Xiaomi HyperOS/MIUI, OnePlus OxygenOS, and Motorola) bundle loud, heavily branded, or cluttered boot sequences. Pixel-fy systemlessly overlays standard OEM media paths with the authentic Google Pixel sequence, delivering a clean, uniform stock Google startup experience.

---

## Technical Architecture & Boot Sequence

Android's boot animation architecture operates under strict constraints during early userspace:

```
┌────────────────────────────────────────────────────────┐
│                      init (PID 1)                      │
└───────────────────────────┬────────────────────────────┘
                            │ spawns
┌───────────────────────────▼────────────────────────────┐
│                     surfaceflinger                     │
└───────────────────────────┬────────────────────────────┘
                            │ launches
┌───────────────────────────▼────────────────────────────┐
│               /system/bin/bootanimation                │
│  - Inspects /product/media/bootanimation.zip           │
│  - Inspects /system/media/bootanimation.zip            │
│  - Reads desc.txt for resolution and playback rules    │
│  - Streams uncompressed PNG frames into framebuffer    │
└───────────────────────────┬────────────────────────────┘
                            │ listens for 'service.bootanim.exit'
┌───────────────────────────▼────────────────────────────┐
│                   System Server / UI                   │
│  Sets sys.boot_completed=1 -> bootanimation terminates │
└────────────────────────────────────────────────────────┘
```

### The `desc.txt` Specification

Inside `bootanimation.zip`, playback timing and screen scaling are defined by a plain-text configuration file named `desc.txt`:

```
1080 2340 60
p 1 0 part0
p 0 0 part1
```

- **Line 1 (`1080 2340 60`)**: Specifies the target width, target height, and frame rate (FPS). Android's boot animation renderer automatically scales these dimensions up or down to match your physical panel's native resolution.
- **Line 2 (`p 1 0 part0`)**: Play `part0` once (`1`), with a pause delay of `0` frames before advancing.
- **Line 3 (`p 0 0 part1`)**: Loop `part1` infinitely (`0`) until the system server signals boot completion by setting the property `service.bootanim.exit` to `1`.

---

## Compatibility & Limitations

| Platform / ROM | Compatibility | Notes |
| :--- | :--- | :--- |
| **Google Pixel ROMs / AOSP** | Compatible | Native support for standard zip format |
| **LineageOS / ArrowOS / PixelOS** | Compatible | Directly replaces ROM boot animations |
| **Xiaomi / HyperOS / MIUI** | Compatible | Overlays default MIUI/HyperOS startup media |
| **OnePlus / OxygenOS** | Compatible | Overlays OxygenOS boot animations |
| **Samsung One UI (Stock)** | Incompatible | Uses proprietary `.qmg` format; incompatible unless running AOSP ROM |

---

## Installation & Safe Removal

### Installation
1. Download the latest `pixel-boot-animation.zip` release from Magisk Hub.
2. Open **Magisk**, **KernelSU**, or **APatch** app.
3. Navigate to **Modules** -> **Install from storage**.
4. Select `pixel-boot-animation.zip` and tap **Reboot**.
5. Upon device restart, the Google Pixel boot sequence will display immediately following the bootloader splash.

### Safe Removal
If you wish to restore your device's original OEM boot screen:
1. Open your root manager app.
2. Locate **Pixel-fy Boot Animation** in the module list and toggle **Remove** (or Disable).
3. Reboot your device. The systemless overlay will unmount, restoring your factory boot animation without modifying any system files.
