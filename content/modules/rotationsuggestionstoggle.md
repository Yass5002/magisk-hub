---
id: "rotationsuggestionstoggle"
title: "Rotation Suggestions Toggle: Control Android's Floating Rotation Prompt"
sidebarTitle: "Rotation Suggestions Toggle"
description: "Systemlessly configures or suppresses the floating screen rotation suggestion button in the Android navigation bar and gesture pill."
category: "customization-ui"
tier: 1
searchQueries:
  - "rotation suggestions toggle magisk"
  - "astoritin rotationsuggestionstoggle"
  - "disable rotation button navigation bar root"
  - "hide floating rotation icon android"
  - "android disable rotate prompt kernelsu"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
conflicts: []
configPaths:
  - "/data/adb/modules/rotationsuggestionstoggle/"
features:
  - "Intrusive prompt suppression: permanently silences or toggles the floating rotation suggestion button in the navigation bar"
  - "Accidental tap mitigation: eliminates unwanted screen rotations triggered by accidentally bumping the corner rotation icon while lying down"
  - "Universal root support: compatible with Magisk, KernelSU, and APatch implementations"
  - "Non-destructive framework patch: applies configuration flags cleanly without altering system partition integrity"
  - "Instant reversal: uninstalling or disabling the module immediately restores stock Android rotation suggestion behavior"
---

## Overview

Starting in Android 9 Pie, Android introduced a context-aware rotation suggestions feature: when auto-rotate is turned off and the user tilts their smartphone, a small floating rotation button appears in the bottom corner of the navigation bar or next to the gesture pill. While convenient for some, for users reading in bed, playing games, or browsing horizontally, this button frequently pops up uninvited and leads to accidental, jarring screen rotations when tapped mistakenly.

Developed by Astoritin, **RotationSuggestionsToggle** is a systemless root module that provides fine-grained control over this feature. It allows rooted users to cleanly suppress or toggle the rotation suggestion icon across stock AOSP, Pixel firmware, and OEM Android skins.

## Why Suppress Rotation Suggestions?

1. **Accidental Triggers**: When holding a phone horizontally while auto-rotate is locked, the suggestion button occupies space near bottom navigation buttons or keyboard dismissal zones, leading to accidental orientation changes.
2. **Immersive Full-Screen Experience**: Eliminates visual clutter near the bottom screen corners when watching video feeds or playing games.
3. **Pure Systemless Toggling**: Uses framework overlay configuration flags rather than intrusive binary patching, guaranteeing zero interference with Android dm-verity or Google Play Integrity.

## Installation & Root Support

- **Compatibility**: Fully tested and supported on **Magisk**, **KernelSU**, and **APatch**.
- **Installation Steps**:
  1. Download `RotationSuggestionsToggle-*.zip` from GitHub releases.
  2. Open your preferred root manager app and install the zip from local storage.
  3. Reboot your device to apply the new rotation configuration.
