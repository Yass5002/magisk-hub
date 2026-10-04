---
id: "minecraft-boot-animation"
title: "Minecraft Pixel Boot Animation: Retro Crafting Startup Mod"
sidebarTitle: "Minecraft Boot"
description: "Retro 8-bit Minecraft block generation and crafting boot sequence systemless replacement for Magisk, KernelSU, and APatch."
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "minecraft boot animation magisk"
  - "pixel art startup animation android root"
  - "minecraft grass block bootanimation zip"
  - "retro gaming boot animation root"
prerequisites:
  - "Magisk 16.6+, KernelSU, or APatch"
  - "Any Android smartphone display"
conflicts:
  - "Other modules modifying /system/media/bootanimation.zip"
configPaths:
  - "/system/media/bootanimation.zip"
features:
  - "Isometric pixel art Minecraft block crafting and building animation"
  - "Ultra-lightweight 185 KB footprint with lightning-fast storage read times"
  - "Zero battery or CPU strain during system initialization"
  - "Universal support across all Android ROMs and root environments"
faq:
  - question: "Why is this module so small (under 200 KB)?"
    answer: "Pixel art assets compress with extraordinary efficiency. By utilizing indexed color palettes, the entire multi-frame animation achieves high visual fidelity with negligible storage and memory overhead."
---

## Overview

**Minecraft Pixel Boot Animation** (packaged by Wei Bin Guo / 魏斌过) brings nostalgic pixelated gaming flair to rooted Android devices.

The module replaces standard OEM splash sequences with an animated pixel-art Minecraft block crafting progression, rendering an isometric dirt and grass block assembled piece by piece before transitioning into the Android system lockscreen.

---

## Technical Architecture & How It Works

The module mounts a compact `bootanimation.zip` into `/system/media/`:

```text
bootanimation.zip (185 KB)
├── desc.txt
├── part0/            # Pixel block assembly sequence
└── part1/            # Subtle animated pixel shimmer loop
```

Because of the tiny footprint, memory allocation overhead for SurfaceFlinger's texture buffer is under 4 MB, making it ideal for older devices or performance-conscious users.
