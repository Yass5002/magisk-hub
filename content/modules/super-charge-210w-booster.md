---
id: "super-charge-210w-booster"
title: "210W Screen-On Extreme Fast Charging Mod: Complete Architecture Guide"
sidebarTitle: "210W Fast Charge"
description: "Advanced vendor thermal engine tuning module that removes artificial screen-on charging current caps up to 210W on Xiaomi and Redmi smartphones while enforcing strict 80°C hardware safety boundaries."
category: "battery-power-charging"
tier: 1
searchQueries:
  - "210w fast charge magisk module"
  - "screen on fast charging xiaomi root"
  - "bypass charging current limit miui"
  - "thermal engine fast charge override"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Xiaomi, Redmi, or POCO smartphone (Snapdragon or MediaTek)"
  - "High-wattage GaN / HyperCharge charger and compatible 6A/10A cable"
conflicts:
  - "Other aggressive thermal engine disablers or thermal configuration mods"
configPaths:
  - "/system/vendor/etc/thermal-*.conf"
  - "/system/vendor/bin/thermal-engine-v2"
  - "/system/vendor/lib/modules/thermal_pause.ko"
  - "/data/adb/modules/鹤征/service.sh"
features:
  - "Eliminates artificial screen-on current drop (e.g. throttling from 67W/120W down to 15W when screen is awake)"
  - "Unlocks full multi-tier fast charging profiles: 18W, 33W, 55W, 67W, 120W, and 210W"
  - "Replaces vendor thermal configs across /vendor/etc/ and /vendor/etc/thermal/"
  - "Hardware Safety Guard: Enforces hard current cut-off at 80°C to prevent battery degradation"
faq:
  - question: "Will this damage my smartphone or battery?"
    answer: "The module removes software throttling caps that lower charging speed when the screen is turned on. However, because battery charging generates heat, the module includes a strict 80°C emergency cut-off to prevent thermal runaway. Using a phone cooling fan during intense gaming while fast-charging is strongly recommended."
  - question: "Can a 33W phone suddenly charge at 210W with this module?"
    answer: "No. Charging wattage is fundamentally governed by device hardware (battery charge pump ICs, dual-cell configurations, and power management PMIC). The module allows each phone to reach its maximum physical charging ceiling while the screen is on, rather than being artificially throttled."
---

## Overview

**210W Screen-On Extreme Fast Charging Mod** (authored by He Zheng & Class 6 Grade 1 / 酷安@鹤征 二改@六年级一班) is a comprehensive low-level charging power unlocker designed for Xiaomi, Redmi, and POCO smartphones.

In stock MIUI and HyperOS builds, Xiaomi aggressively throttles fast charging whenever the display screen is turned on—often reducing a 67W or 120W connection down to a sluggish 15W–18W to minimize surface temperatures. This module reconstructs the device thermal engine rules, allowing users to experience full-speed charging while gaming, navigating, or streaming videos.

---

## Technical Architecture & How It Works

The module executes a thorough multi-tier vendor systemless override across kernel modules, user-space daemons, and configuration files:

### 1. Thermal Engine Replacement & Binary Daemons

The module patches vendor thermal binaries located under `/system/vendor/bin/`:
- `thermal-engine-v2`
- `mi_thermald`
- `thermal_manager`

These binaries interface with Linux sysfs nodes (`/sys/class/power_supply/battery/current_now` and `/sys/class/qcom-chg/`) to modulate charging step currents.

### 2. Vendor Policy Overrides

The module supplies comprehensive configuration overrides across `/system/vendor/etc/`:
- `thermal-global-u-chg-only.conf`
- `thermal-global-u-nolimits.conf`
- `thermal_configs.xml` (game engine integration)

Under these customized policies, step-down throttling thresholds during screen illumination are removed, instructing the charge controller to maintain maximum negotiation wattage.

### 3. Safety Guardrails (80°C Hardware Protection)

Fast charging without OEM throttling demands hardware safeguards. The module implements:
- **80°C Emergency Threshold**: If battery temperature sensor telemetry crosses 80°C, the daemon cuts charging current for 10 seconds or switches to trickle charging, ensuring absolute protection against thermal runaway.

---

## Verification & Monitoring

Monitor live charging current and wattage while the screen is awake:

```bash
# Query active battery charging metrics
cat /sys/class/power_supply/battery/current_now
cat /sys/class/power_supply/battery/voltage_now

# Calculate real-time charging wattage:
# (current_now [uA] / 1,000,000) * (voltage_now [uV] / 1,000,000) = Watts
```
