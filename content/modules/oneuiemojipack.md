---
id: "oneuiemojipack"
title: "OneUI Emoji Pack: Systemless Samsung Emoji Font for Android"
sidebarTitle: "OneUI Emoji Pack"
description: "Systemlessly replaces default AOSP and Google emoji typography with Samsung OneUI emojis across all applications and system keyboards."
category: "customization-ui"
tier: 1
searchQueries:
  - "oneui emoji pack magisk"
  - "samsung emoji font root"
  - "aloozchips oneuiemojipack"
  - "replace google emojis with samsung oneui"
  - "oneui emoji kernelsu apatch"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
conflicts:
  - "FontLoader modules on KernelSU 2.0+ (metamodule layering conflicts may cause system instability)"
  - "Other Magisk font modules modifying system emoji font files"
configPaths:
  - "/data/adb/modules/oneuiemojipack/"
features:
  - "Authentic Samsung styling: replaces generic NotoColorEmoji with the official Samsung OneUI emoji typeface"
  - "System-wide integration: renders OneUI emojis across WhatsApp, Telegram, Instagram, social apps, and virtual keyboards (Gboard)"
  - "Universal root support: fully compatible with Magisk, KernelSU, and APatch root managers"
  - "Zero partition modification: mounts font assets systemlessly to preserve dm-verity and seamless OTA updates"
  - "Instant toggle: disable or remove the module to restore stock system emojis immediately"
---

## Overview

Samsung's OneUI skin is widely praised for its cheerful, rounded, and expressive emoji design language. While Google's stock NotoColorEmoji provides wide Unicode coverage, many users prefer the visual flair and clarity of Samsung's emojis in social feeds and messaging chats.

Developed by AloozChips, **OneUI Emoji Pack** is a systemless root module that replaces the default Android system emoji typeface (`NotoColorEmoji.ttf` or OEM variant) with the authentic OneUI emoji pack.

## Compatibility & Caution

- **Root Managers**: Functions across **Magisk**, **KernelSU**, and **APatch**.
- **Important KernelSU 2.0+ Notice**: If running KernelSU 2.0 or higher with metamodule support, do **not** run this module alongside separate `fontloader` modules. Combining both modules can cause font configuration conflicts and system framework crashes.
- **Font Conflicts**: Avoid running simultaneous emoji replacement modules (e.g., iOS Emoji packs or Twemoji packs) to prevent font definition conflicts.

## Installation

1. Download the latest `OneUI_Emoji_Pack-v*.zip` archive from GitHub releases.
2. Open your root manager (**Magisk**, **KernelSU**, or **APatch**).
3. Navigate to **Modules > Install from storage**, select the zip archive, and confirm flashing.
4. Reboot your device to apply the new emoji font system-wide.
