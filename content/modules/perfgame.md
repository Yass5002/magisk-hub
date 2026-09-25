---
id: "perfgame"
title: "PerfGame: Android Game Mode Interventions & Custom Resolution Engine"
sidebarTitle: "PerfGame"
description: "Applies native Android Game Mode interventions to dynamically scale down rendering resolutions, unlock frame rates, and optimize performance profiles per game."
category: "performance-kernel"
tier: 1
searchQueries:
  - "perfgame magisk"
  - "android game mode interventions root"
  - "adivenxnataly perfgame"
  - "downscale game resolution android root"
  - "unlock 90 120 fps android games"
prerequisites:
  - "Root access via Magisk"
  - "Android 12 or newer (Android Game Service framework enabled)"
conflicts: []
configPaths:
  - "/data/adb/modules/perfgame/"
features:
  - "Native Game Mode Interventions: utilizes the Android GameManager service framework to apply per-game graphics adjustments"
  - "Resolution downscaling: scales internal 3D render target resolutions down to 70% or 80%, substantially reducing GPU load and heat"
  - "Custom FPS targets: overrides hardcoded 30 or 60 FPS caps to unlock smooth 90 or 120 FPS rendering on high-refresh displays"
  - "Thermal throttle alleviation: lowers peak GPU heat generation during extended gaming sessions to prevent aggressive thermal downclocking"
  - "Systemless XML deployment: injects game intervention definitions systemlessly into the system configuration path"
---

## Overview

Modern Android releases (Android 12 and newer) incorporate an official **Game Mode Interventions** framework within `GameManagerService`. This framework allows the operating system to dynamically intercept game rendering pipelines—modifying resolution scaling factors, locking specific frame rates, or steering graphics to specific Vulkan/OpenGL backends—without requiring modifications to the game's actual APK.

Developed by adivenxnataly, **PerfGame** is a systemless Magisk module that empowers rooted users to configure and unlock these game interventions across popular titles (such as Genshin Impact, PUBG Mobile, Call of Duty, and Honkai Star Rail).

## How Game Interventions Work

Instead of brute-forcing CPU/GPU clocks to maximum frequency (which quickly induces thermal throttling), PerfGame works intelligently within Android's graphics pipeline:

1. **Resolution Downscaling (`downscaleFactor`)**: Scales 3D game buffers down slightly (for instance, rendering at 0.8x or 0.7x while preserving native UI text sharpness). This drastically cuts pixel fill-rate demands on the GPU.
2. **Target Frame Rate Clamping (`fps`)**: Restricts or unlocks frame rates to match your display's native refresh rate (60Hz, 90Hz, 120Hz), eliminating micro-stutters and uneven frame pacing.
3. **Thermal Longevity**: By reducing continuous GPU rendering pressure, your smartphone stays cooler for longer, sustaining maximum frame rates throughout prolonged gaming sessions.

## Installation & Setup

1. Verify that your device runs Android 12 or newer.
2. Download `PerfGamev*.zip` from GitHub releases.
3. Install the module in **Magisk Manager**.
4. Reboot your device.
5. Launch your game. Android will automatically load the optimized intervention parameters defined in the module's configuration tables.
