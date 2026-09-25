---
id: "background-app-slayer"
title: "Background App Slayer (BAS): Automated Background Task Termination for Gaming"
sidebarTitle: "Background App Slayer"
description: "Game-aware background process termination daemon offering three aggression tiers to eliminate background memory churn and CPU preemption during gameplay."
category: "performance-kernel"
tier: 1
searchQueries:
  - "background app slayer magisk"
  - "unknuw background app slayer"
  - "auto kill background apps android gaming"
  - "smartappclose magisk replacement"
  - "background app killer kernelsu"
prerequisites:
  - "Android 8.0 or higher"
  - "Root access via Magisk or KernelSU"
conflicts: []
configPaths:
  - "/data/adb/modules/background-app-slayer/"
features:
  - "Automated game detection: triggers aggressive memory freeing routines immediately upon foreground game launch"
  - "Three calibrated aggression tiers: toggle between Normal (safe), Aggressive (deep closure), and Extreme (complete background termination)"
  - "Plaintext configuration: customize app whitelists and operational parameters using simple text configuration files"
  - "Zero terminal dependencies: runs autonomously after boot without requiring manual Termux command invocations"
---

## Overview

Modern Android mobile games—such as competitive battle royales and heavy open-world titles—require uninterrupted access to CPU cores and available system memory. However, background messaging services, social media refreshers, and bloatware daemons constantly wake up to poll notifications, leading to sudden frame pacing spikes and stuttering during gameplay.

Developed by UNKNUW as a complete architectural rewrite of the earlier SmartAppClose project, **Background App Slayer (BAS)** is an automated task termination daemon designed specifically for mobile gamers. When a game enters the foreground, BAS monitors process tables and selectively terminates non-essential background processes according to user-defined severity modes.

## Operating Modes

BAS allows users to configure termination severity through simple numeric mode flags:

1. **Mode 1 (Normal)**:
   - Light and conservative.
   - Clears common cached tasks, temporary web services, and non-essential caches while preserving background messengers, audio players, and alarm services.
2. **Mode 2 (Aggressive)**:
   - Closes standard consumer social applications, browser instances, and media streamers running behind the active game.
3. **Mode 3 (Extreme)**:
   - Terminates all third-party background applications except those explicitly protected in the whitelist, delivering maximum free RAM and unconstrained CPU thread scheduling for the active game.

## Configuration & Whitelisting

Configuration is handled entirely through plain-text files located in `/data/adb/modules/background-app-slayer/`:
- **Mode Selection**: Edit the configuration file to select mode `1`, `2`, or `3`.
- **Game Detection List**: Add target game package names (e.g., `com.tencent.ig`, `com.miHoYo.GenshinImpact`) to tell the daemon which applications should trigger the slayer routine.
- **Whitelist Protection**: Add critical applications (music streaming, VPNs, voice chat clients like Discord) that should never be killed during game sessions.

## Installation & Setup

1. Download the latest `Background-App-Slayer` `.zip` archive from the official repository.
2. Flash the module in **Magisk** or **KernelSU**.
3. Reboot your device.
4. *(Optional)* Open the configuration directory in `/data/adb/modules/background-app-slayer/` to adjust your operating mode or whitelist specific background audio players.
