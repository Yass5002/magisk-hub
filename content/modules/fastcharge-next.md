---
id: "fastcharge-next"
title: "FastCharge Next: Kernel Charging Current Optimization & Thermal Safety Safeguards"
sidebarTitle: "FastCharge Next"
description: "Optimizes kernel thermal current limits and USB power supply parameters to maximize fast-charging throughput within safe thermal boundaries."
category: "performance-kernel"
tier: 1
searchQueries:
  - "fastcharge next magisk module"
  - "dev97633 fastcharge-next"
  - "increase android charging current root"
  - "speed up charging speed magisk"
  - "safe fast charge kernel optimizer"
prerequisites:
  - "Android 9.0 or higher"
  - "Root access via Magisk, KernelSU, or APatch"
  - "Kernel supporting sysfs power supply current scaling nodes"
conflicts: []
configPaths:
  - "/data/adb/modules/fastcharge-next/"
features:
  - "Elevated charging current ceilings: unlocks conservative vendor charging caps across USB-PD, Quick Charge, and proprietary OEM protocols"
  - "Thermal throttle curve relaxation: prevents the kernel from slashing charging speeds during moderate ambient warmth"
  - "Integrated battery safety boundaries: respects maximum voltage ceilings and emergency cutoff temperatures to prevent cell swelling"
  - "Universal root framework compatibility: functions identically across Magisk, KernelSU, and APatch"
---

## Overview

Modern Android smartphones feature fast-charging battery controllers and high-wattage wall adapters, but OEM software frequently throttles charging currents far below hardware limits. Many vendor kernels aggressively reduce charging rates down to standard 5W/10W levels as soon as the battery temperature reaches 36°C, or clamp USB charging current when connected to third-party Power Delivery (USB-PD) bricks.

Developed by Dev97633, **FastCharge Next** tunes system and kernel power parameters to unlock faster, more consistent charging throughput. By safely adjusting current scaling policies across kernel `power_supply` nodes, it cuts total charge times while maintaining hardware thermal protections.

## Core Mechanisms & Safeguards

FastCharge Next adjusts kernel parameters located under `/sys/class/power_supply/`:
- **Current Scaling Adjustments**: Overrides artificial input current ceilings on USB and AC charging paths (`current_max`, `constant_charge_current_max`), allowing the battery manager to draw full negotiated wattage.
- **Graduated Thermal Stepping**: Replaces abrupt step-down throttling with smoother, wider thermal bands, allowing devices to sustain peak charging speeds longer.
- **Safety Boundaries**: The module respects underlying hardware battery management IC (PMIC) voltage ceilings (such as 4.35V/4.45V caps) and emergency thermal shutdowns, preventing dangerous overvoltage conditions or battery degradation.

## Installation & Setup

1. Verify that your device is rooted with **Magisk**, **KernelSU**, or **APatch**.
2. Download the `chargeboost-magisk` / `Fastcharge-next` `.zip` from the GitHub releases page.
3. Flash the archive via your root manager and reboot.
4. Plug your phone into its OEM or high-speed USB-PD charger.
5. Monitor charging amperage using diagnostic tools (such as Ampere or Franco Kernel Manager) to observe the increased current throughput.
