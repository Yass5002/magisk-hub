---
id: "multi-oem-bootanimation"
title: "Multi-OEM Dynamic Boot Animation: Custom Startup Engine with Crash Guard"
sidebarTitle: "Multi-OEM Bootanim"
description: "Systemless boot sequence customizer supporting Xiaomi MIUI/HyperOS, OPPO ColorOS, and Realme UI with random animation cycling and an autonomous 60-second crash watchdog."
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "bootanimation magisk module"
  - "miui custom boot animation"
  - "coloros boot animation changer"
  - "bootanimation watchdog anti brick"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Device running MIUI/HyperOS, ColorOS, Realme UI, or AOSP"
conflicts:
  - "Other boot animation replacers targeting /system/media/bootanimation.zip"
configPaths:
  - "/data/adb/modules/bootanimation/random_animation.sh"
  - "/data/adb/modules/bootanimation/service.sh"
  - "/data/adb/modules/bootanimation/bootanimation.zip"
features:
  - "Replaces OEM boot sequences without modifying physical system or product partitions"
  - "Compatible with complex multi-stage boot animation structures used in MIUI, ColorOS, and Realme UI"
  - "Dynamic randomizer (random_animation.sh) selects a different animation sequence on every startup"
  - "Integrated 60-second init watchdog prevents bootloops if a corrupted ZIP file is encountered"
  - "Autonomous unmount mechanism (umount.sh) detaches overlays during boot failures without user intervention"
faq:
  - question: "What happens if a custom bootanimation.zip is corrupted or invalid?"
    answer: "The built-in service watchdog monitors init.svc.bootanim. If the animation daemon runs continuously for over 60 seconds (a standard indicator that the OS cannot progress to SurfaceFlinger/SystemUI), the script automatically drops a disable flag, triggers umount.sh to detach the faulty animation, and safely reboots the device."
  - question: "How do I add multiple boot animations for the randomizer to choose from?"
    answer: "Place additional boot animation ZIP archives directly in the module directory (/data/adb/modules/bootanimation/). During each shutdown or reboot cycle, the random_animation.sh script will pick one at random and prepare it for the subsequent boot sequence."
---

## Overview

**Multi-OEM Dynamic Boot Animation** (authored by Stinky Panda, Coolapk profile: https://www.coolapk.com/u/22627121) provides a reliable, systemless framework for customizing Android boot sequences across diverse OEM interfaces, including Xiaomi (MIUI/HyperOS), OPPO (ColorOS), Realme (Realme UI), and generic AOSP firmware.

Installing custom boot animations has traditionally been one of the most common causes of bootloops for modders. Mismatched frame dimensions, unsupported image compression (such as deflated rather than store-only ZIP compression), or missing `desc.txt` terminating newlines cause the native Android `bootanimation` binary to fault or enter infinite replay loops.

Multi-OEM Dynamic Boot Animation eliminates this vulnerability by wrapping the animation delivery in an autonomous health-check watchdog that monitors startup timing and disengages the overlay if any fault occurs.

---

## Technical Architecture & How It Works

The module operates across three complementary components:

### 1. Multi-Stage Animation Overlay

Android loads boot animations from prioritized locations:
1. `/product/media/bootanimation.zip`
2. `/system/media/bootanimation.zip`

The module establishes systemless mounts on these locations, injecting animations packaged with the requisite part structures (`part0`, `part1`, etc.) and non-compressed format (`zip -0`) essential for hardware surface decoders.

### 2. Startup Watchdog (service.sh)

The module's late-service daemon monitors the core Android init system property:

```bash
sleep 60
if [[ "`getprop init.svc.bootanim`" = "running" ]]; then
    # Boot animation is still looping after 60 seconds -> potential hang
    echo > $MODDIR/disable
    sh $MODDIR/umount.sh
    echo "Device startup failure detected. Module disabled automatically." > $MODDIR/boot_failure.log
    exit
else
    # Startup successful -> execute random animation selection for next boot
    sh $MODDIR/random_animation.sh
fi
```

If the animation daemon is still actively spinning after 60 seconds, the module concludes that the system has hung, immediately calls `umount.sh` to unmount the overlay from memory, and writes a recovery flag.

### 3. Dynamic Animation Shuffler (random_animation.sh)

When the phone reaches normal operation, `random_animation.sh` scans the module directory for alternate animation archives, randomly selects one using `$RANDOM`, and stages it as the primary `bootanimation.zip` for the subsequent device restart.

---

## Adding Custom Animations

To introduce your own animations:
1. Ensure the animation archive is stored using 0% compression (`Store` method in 7-Zip or `zip -0 -r bootanimation.zip desc.txt part*`).
2. Verify that `desc.txt` includes a trailing blank line.
3. Copy the archive into `/data/adb/modules/bootanimation/` with a distinct filename (e.g. `cyberpunk.zip`).
