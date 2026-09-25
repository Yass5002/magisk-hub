---
id: "deepsuppressor"
title: "DeepSuppressor: Granular Background Sub-Process Throttling & AMMF2 WebUI"
sidebarTitle: "DeepSuppressor"
description: "Background process manager built on AMMF2, targeting rogue secondary app processes (push services, analytics, sub-threads) with per-process JSON rules and WebUI controls."
category: "performance-kernel"
tier: 1
searchQueries:
  - "deepsuppressor magisk module"
  - "aurora nasa deepsuppressor"
  - "suppress background processes android root"
  - "ammf2 webui background manager"
  - "android appbrand sub-process killer"
prerequisites:
  - "Root access via KernelSU or Magisk"
  - "Android 9.0 or higher"
  - "WebUI provider (KernelSU Manager, KsuWebUIStandalone, or MMRL)"
conflicts: []
configPaths:
  - "/data/adb/modules/DeepSuppressor/"
  - "/data/adb/modules/DeepSuppressor/module_settings/suppress_config.json"
features:
  - "Sub-process precision: targets isolated secondary background processes (e.g., :push, :channel, :video) without killing main app services"
  - "AMMF2 modular framework: engineered on Aurora-Magisk-Modules-Framework-2 for low CPU and RAM footprint"
  - "KernelSU WebUI integration: provides a graphical dashboard to toggle suppression policies on a per-app basis"
  - "JSON rule configuration: customize targeted processes and enabled states in suppress_config.json"
---

## Overview

Modern social, media, and commerce applications frequently spawn numerous distinct secondary sub-processes (such as `:push`, `:analytics`, `:mini_program`, `:channel`, and `:video`). Even when an app is minimized or swiped away from the Recents menu, these background helper processes remain resident in memory, continuously waking CPU cores, executing scheduled background jobs, and wasting battery life.

Developed by Aurora-Nasa-1 and powered by the **Aurora-Magisk-Modules-Framework-2 (AMMF2)**, **DeepSuppressor** is an intelligent background process monitoring and suppression tool. Rather than brutally killing parent applications—which breaks push notifications and causes apps to crash when reopened—DeepSuppressor targets and freezes only the auxiliary sub-processes defined in user rules.

## JSON Configuration Schema (`suppress_config.json`)

All app targeting and process rules are structured within `/data/adb/modules/DeepSuppressor/module_settings/suppress_config.json`:

```json
{
  "com.tencent.tim": {
    "enabled": true,
    "processes": [
      "com.tencent.tim:appbrand0",
      "com.tencent.tim:video"
    ]
  },
  "com.example.bloatapp": {
    "enabled": true,
    "processes": [
      "com.example.bloatapp:pushservice",
      "com.example.bloatapp:downloader"
    ]
  }
}
```

- **`enabled`**: Sets whether suppression is active for the target package (`true` or `false`).
- **`processes`**: An array of explicit sub-process identifiers that DeepSuppressor will intercept and suppress whenever the main application transitions to the background.

## WebUI Interface

DeepSuppressor integrates directly with **KernelSU WebUI**, **KsuWebUIStandalone**, and **MMRL**:
- View all installed packages and their associated sub-processes.
- Toggle suppression policies on or off with a single tap.
- Save rule adjustments instantly without manual JSON syntax editing.

## Installation & Setup

1. Download the latest `DeepSuppressor` `.zip` archive from the release channel.
2. Flash the module using **KernelSU** or **Magisk**.
3. Reboot your Android device.
4. Launch your root manager's WebUI view to inspect detected applications and toggle suppression rules.
