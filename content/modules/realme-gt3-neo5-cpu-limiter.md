---
id: "realme-gt3-neo5-cpu-limiter"
title: "Realme GT3 & GT Neo 5 CPU Limiter: Snapdragon 8+ Gen 1 Power Tuning"
sidebarTitle: "Realme CPU Limiter"
description: "Customizes Snapdragon 8+ Gen 1 CPU frequencies, energy-efficient governors, and core offlining on Realme GT3 and GT Neo 5 to significantly extend battery life."
category: "performance-kernel"
tier: 1
searchQueries:
  - "realme gt3 cpu limiter magisk"
  - "realme gt neo 5 cpu limiter"
  - "quantom2 realme cpu limiter"
  - "snapdragon 8+ gen 1 underclock root"
  - "disable cpu cores android magisk"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "Realme GT3 or Realme GT Neo 5 (Qualcomm Snapdragon 8+ Gen 1 chipset)"
conflicts:
  - "Other kernel frequency locking modules or CPU tweakers with overlapping sysfs hooks"
configPaths:
  - "/data/adb/modules/Realme-GT3-neo5-CPU-limiter/"
features:
  - "CPU frequency cap: restricts maximum clock frequencies on Cortex-X2 Prime, Cortex-A710 Gold, and Cortex-A510 Silver clusters"
  - "Energy-efficient governors: switches active CPU scaling governors to Conservative or Powersave modes"
  - "Selective core offlining: shuts down up to 4 CPU cores completely to minimize baseline wattage during light usage"
  - "Screen-off core sleep: automatically powers down selected high-power cores when the display is off to reduce standby drain"
  - "Persistent settings: preserves your custom frequencies and active core profiles across module re-flashes and OTA updates"
---

## Overview

The Qualcomm Snapdragon 8+ Gen 1 (SM8475) powering the Realme GT3 and Realme GT Neo 5 is a powerhouse processor capable of exceptional computing throughput. For everyday smartphone tasks—such as web browsing, messaging, and audio streaming—its aggressive clock ramping and multi-core engagement often consume more power than necessary, leading to increased heat and reduced Screen-On Time (SOT).

Developed by Quantom2, **Realme-GT3-neo5-CPU-limiter** is a specialized performance and battery optimization module for Magisk and KernelSU. It enables Realme GT3 and GT Neo 5 owners to underclock, apply energy-conservative governors, and offline CPU cores on demand.

## Core Tuning Mechanisms

1. **Frequency Clamping**: Enforces hard upper frequency ceilings on the Cortex-X2 Prime core and Cortex-A710 Performance clusters via `/sys/devices/system/cpu/cpufreq/`.
2. **Governor Adjustments**: Switches the default interactive/schedutil scaling governor to a tuned Conservative or Powersave profile, preventing minor background spikes from spooling the CPU to peak frequencies.
3. **Core Offlining**: Disables up to 4 CPU cores systemlessly, transforming the octa-core processor into an ultra-efficient quad- or hexa-core engine for daily battery preservation.
4. **Screen-Off Sleep State**: Detects screen power state events and offlines high-power clusters as soon as the display turns off, virtually eliminating standby battery drain.

## Installation & Configuration

1. Download the latest `Realme-GT3-neo5-CPU-limiter_*.zip` from GitHub releases.
2. Install the archive in **Magisk** or **KernelSU**.
3. Follow the terminal installation prompts to configure your desired maximum frequencies and core profile.
4. Reboot your device to apply the power-saving limits.
