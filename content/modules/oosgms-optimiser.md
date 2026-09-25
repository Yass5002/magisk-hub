---
id: "oosgms-optimiser"
title: "OOSGMS Optimizer: Privacy & Battery Optimization for OxygenOS & GMS"
sidebarTitle: "OOSGMS Optimizer"
description: "Disables background telemetry trackers, wake locks, and analytical bloat across Google Play Services (GMS), OxygenOS (OOS), and popular third-party apps."
category: "performance-kernel"
tier: 1
searchQueries:
  - "oosgms optimiser magisk"
  - "oxygenos gms tracker blocker root"
  - "epicmann24 oosgms optimiser"
  - "google play services battery drain fix magisk"
  - "debloat trackers oneplus oxygenos"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "OnePlus smartphone running OxygenOS or devices running Google Play Services"
conflicts: []
configPaths:
  - "/data/adb/modules/oosgms-optimiser/"
features:
  - "Comprehensive tracker mitigation: disables telemetry receivers and analytics components in Google Play Services (GMS) and OxygenOS (OOS)"
  - "Third-party application de-tracking: restricts background tracking in high-telemetry apps (Instagram, TikTok, Facebook, Reddit, Telegram, Temu, and X/Twitter)"
  - "Idle battery drain reduction: prevents repetitive wake locks and background polling alarms from holding the CPU awake"
  - "Non-destructive service toggling: uses Android package component manager commands rather than deleting essential system binaries"
  - "Safe uninstallation workflow: includes a dedicated action routine (executable in KernelSU or MMRL) to cleanly restore disabled components"
---

## Overview

Google Play Services (GMS) and OEM system skins like OnePlus's OxygenOS (OOS) operate dozens of background diagnostic services, analytics reporters, and location-polling receivers. Over time, these background tasks frequently become stuck in loops, causing elevated battery drain and keeping the device from entering deep Linux kernel sleep states.

Created by epicmann24, **OOSGMS-OPTIMISER** is a targeted optimization module designed to disable invasive telemetry, tracking services, and unnecessary background wakelocks in both Google Play Services and OxygenOS.

## Coverage & Targeted Packages

Beyond silencing core GMS analytics, the module applies component-level disable rules to common third-party apps known for heavy background telemetry:
- **Core Google Frameworks**: `com.google.android.gms`, `com.google.ar.core`, `com.google.android.projection.gearhead` (Android Auto), `com.google.android.play.games`
- **Social & Media Apps**: Instagram (`com.instagram.android`), TikTok (`com.zhiliaoapp.musically`), Facebook (`com.facebook.katana`), Reddit (`com.reddit.frontpage`), Telegram (`org.telegram.messenger`), and X (`com.twitter.android`)
- **Shopping & Miscellaneous**: Temu (`com.einnovation.temu`), AliExpress (`com.alibaba.aliexpresshd`), eBay (`com.ebay.mobile`), and Coinbase (`com.coinbase.android`)

## Installation & Safe Uninstallation

### Installation
1. Download `OOSGMS-OPTIMISER.zip` from GitHub releases.
2. Install the archive via **Magisk** or **KernelSU**.
3. Reboot your device.

### Safe Uninstallation
Because the module disables individual Android component receivers via package manager hooks, uninstallation requires cleanly restoring those component flags first:
1. In **KernelSU** (or using the **MMRL** manager app), tap the module to trigger the built-in restoration action.
2. Once the action script confirms components have been restored, uninstall the module normally and reboot.
