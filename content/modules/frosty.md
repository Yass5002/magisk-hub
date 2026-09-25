---
id: "frosty"
title: "Frosty: Advanced Google Play Services Freezer & Battery Optimizer"
sidebarTitle: "Frosty"
description: "Comprehensive battery optimization suite for Magisk, KernelSU, and APatch that freezes background GMS bloat, enforces Deep Doze, and tunes kernel memory subsystems via WebUI."
category: "performance-kernel"
tier: 1
searchQueries:
  - "frosty magisk module"
  - "frosty drsexo github"
  - "gms freezer battery saver magisk"
  - "deep doze enforcer kernelsu"
  - "stop google play services drain root"
prerequisites:
  - "Android 9 (Pie) or higher"
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Google Play Services installed (for GMS freezing functions; kernel/doze features work standalone)"
  - "WebUI support (KernelSU / APatch built-in, or KsuWebUI / WebUI-X on Magisk)"
conflicts: []
configPaths:
  - "/data/adb/modules/frosty/"
  - "/data/adb/modules/frosty/config/"
features:
  - "Granular GMS service control: disables Google Play Services components across 8 distinct categories (Telemetry, Background, Location, Cloud, Payments, Wearables, etc.)"
  - "Intelligent Deep Doze: forces device idle states when locked, enables JobScheduler flex-idle on Android 13+, and monitors wakelocks without waking for ambient glance displays"
  - "Screen-off automation: optionally suspends radios (Wi-Fi, Bluetooth, cellular data, GPS) and executes memory compaction after a user-configured delay"
  - "Kernel & RAM tuning: auto-optimizes ZRAM compression, LMKD / PSI pressure thresholds, and VM writeback parameters"
  - "Battery Saver refresh rate preservation: allows fine-tuning Android's native Battery Saver to maintain high refresh rates (90/120Hz) while saving power"
---

## Overview

Frosty, developed by Drsexo, is a feature-rich power management and Google Play Services (GMS) optimization module engineered for rooted Android devices. On modern stock and custom ROMs, Google Play Services is notorious for background battery consumption, constantly waking the CPU for analytics, Clearcut telemetry, Phenotype flag synchronization, and location polling.

Frosty addresses this drain without breaking the core Android experience. Managed through a comprehensive WebUI, Frosty allows users to selectively freeze specific GMS components, apply aggressive Deep Doze policies, optimize Linux VM and scheduler parameters, and automate radio power states when the screen is locked.

## Prerequisites & Compatibility

- **Operating System**: Android 9.0 through current Android versions.
- **Root Solutions**: Magisk 20.4 or higher, KernelSU, or APatch.
  - On **KernelSU** and **APatch**, Frosty supports hot installs without requiring an immediate reboot.
  - On **Magisk**, a device reboot is required following initial installation.
- **WebUI Interface**:
  - In KernelSU and APatch, open the WebUI directly from the module tile.
  - In Magisk, access the WebUI via [KsuWebUI](https://github.com/KOWX712/KsuWebUIStandalone) or [WebUI-X](https://github.com/MMRLApp/WebUI-X-Portable).

There are no documented module conflicts. All features are disabled by default upon first install, ensuring complete user control over which tweaks are activated.

## Key Capabilities & Architecture

### 1. Granular GMS Freezing
Frosty segments Google Play Services background tasks into 8 distinct functional categories:

| Category | Impact & Details |
| :--- | :--- |
| **Telemetry** | **Safe**. Blocks GMS analytics, Clearcut telemetry, Phenotype polling, and ad tracking without breaking user apps. |
| **Background** | **Safe**. Reduces periodic background updates and sync polls. |
| **Location** | May impact Google Maps navigation accuracy, geofencing, and Find My Device. |
| **Connectivity** | Controls Chromecast casting, Quick Share, and Fast Pair protocols. |
| **Cloud** | Controls Google Account sign-in, cloud backups, and autofill synchronization. |
| **Payments** | Controls Google Wallet, NFC contactless payments, and transit cards. |
| **Wearables** | Controls Wear OS companion sync and Google Fit data recording. |
| **Games** | Controls Google Play Games achievement tracking and cloud save games. |

### 2. Deep Doze & App Doze
Frosty rewrites Android's internal Doze constants. Unlike stock Android—which exits idle states whenever motion sensors fire in a pocket—Frosty aligns Doze strictly with screen lock states. Glancing at the ambient display or checking notifications will not break Doze; restrictions only lift when the device is unlocked. On Android 13+, it automatically engages JobScheduler flex-idle policies.

### 3. Kernel, RAM, and Logging Tweaks
- **RAM Optimizer**: Auto-tunes ZRAM compression algorithms, low-memory killer daemon (LMKD) thresholds, and Pressure Stall Information (PSI) triggers.
- **Log Killing**: Shuts down unneeded debug logging daemons (`logd`, trace services) to prevent constant CPU wakeups and reduce memory churn.
- **Battery Saver Tuner**: Lets you customize Android's built-in Battery Saver, including an option to keep high display refresh rates (e.g. 120Hz) enabled while power-saving modes are active.

## Configuration & Usage

1. Flash `Frosty-*.zip` in your root manager.
2. Open the Frosty WebUI from your manager.
3. Review the available panels:
   - **System Tweaks**: Enable kernel optimizations, log killing, and RAM optimizer settings.
   - **Doze**: Configure App Doze exemptions and select your preferred Deep Doze level (Moderate or Maximum).
   - **Screen Off Optimization**: Set delays and pick which radios to disable when locked.
   - **GMS Categories**: Toggle individual categories.
4. Frosty configuration files and persistence state are saved in:
   ```bash
   /data/adb/modules/frosty/
   /data/adb/modules/frosty/config/
   ```

## Troubleshooting & Verification

- **Delayed Push Notifications**: If third-party messaging apps (e.g., Telegram, Signal, WhatsApp) experience delayed notifications, add them to the Deep Doze whitelist within the WebUI. GMS/Firebase itself is whitelisted by default, but individual chat apps may be throttled if Deep Doze Maximum is selected.
- **Using on Non-Google Devices (MicroG / No GApps)**: If running a de-Googled ROM without Play Services, all non-GMS features (Deep Doze, Kernel Tweaks, RAM Optimizer, Screen-off actions) remain completely functional.
