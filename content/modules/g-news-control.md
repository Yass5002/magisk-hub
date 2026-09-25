---
id: "g-news-control"
title: "G-News Control: Toggle Google Discover Feed via Action Button & CLI"
sidebarTitle: "G-News Control"
description: "Selectively enables or disables the leftmost Google Discover home screen feed without disabling the Google App or breaking Assistant functionality."
category: "customization-ui"
tier: 1
searchQueries:
  - "g-news control magisk module"
  - "mango0oo g-news control"
  - "disable google discover minus one screen root"
  - "gnc switch command android"
  - "toggle google news feed kernelsu action button"
prerequisites:
  - "Android 8.0 or higher"
  - "Root access via Magisk or KernelSU"
  - "Device launcher integrating the Google Discover feed"
conflicts: []
configPaths:
  - "/data/adb/modules/g-news-control/"
features:
  - "One-tap Action button toggle: switch Google Discover on or off directly from the root manager module card without rebooting"
  - "Terminal CLI commands: inspect status or switch states using 'gnc' and 'gnc switch'"
  - "Google App integrity preserved: disables the minus-one feed while keeping Google Search, Lens, and Assistant 100% operational"
  - "Persistent memory: remembers your preferred feed visibility state across system reboots"
---

## Overview

On many Android stock and OEM launchers (such as Pixel Launcher, Motorola, Nothing OS, and Sony Xperia), swiping right on the home screen reveals the **Google Discover** (Google News) feed. While convenient for some, many users find the feed distracting, privacy-invasive, and battery-consuming. However, many OEM launchers provide no native toggle to hide the screen—forcing users either to disable the entire Google App (breaking Assistant and Voice Search) or switch to a third-party launcher.

Developed by mango0oo, **G-News Control** provides seamless, non-destructive control over the Google Discover minus-one screen. It allows users to toggle the feed on or off on demand via an interactive root manager Action button or quick terminal commands, without touching Google App permissions or deleting package components.

## How to Toggle the Feed

G-News Control disables Google News immediately upon initial installation. You can toggle the feed back and forth anytime using two methods:

### 1. Root Manager Action Button
For devices running **KernelSU**, **APatch**, or **MMRL**:
- Navigate to the **Modules** tab.
- Locate the **G-News Control** module card.
- Tap the **Action** button to switch the feed state instantly.

### 2. Terminal Commands (`gnc`)
Open Termux or an ADB root shell:
```bash
# Query the current Google News feed state
su -c gnc

# Toggle between enabled and disabled
su -c gnc switch
```

## Non-Destructive Architecture

Unlike crude debloater scripts that execute `pm disable com.google.android.googlequicksearchbox`:
- G-News Control toggles only the internal framework overlay and feed provider component.
- Google Search, Google Assistant, voice transcription, Circle to Search, and Google Lens remain completely unaffected and functional.

## Installation & Setup

1. Download the `G-News Control` `.zip` from the GitHub releases page.
2. Flash the module in **Magisk** or **KernelSU**.
3. Reboot your device.
4. Swipe right on your home screen; the Google Discover feed will be gone.
