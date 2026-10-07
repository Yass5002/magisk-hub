---
id: "battery-health-query"
title: "Battery Health Diagnostics & Cycle Monitor: Complete Sysfs Guide"
sidebarTitle: "Battery Health Query"
description: "Real-time battery diagnostic daemon that reads Linux power supply sysfs registers to display true capacity retention, charge cycles, and battery state-of-health in Magisk Manager."
category: "battery-power-charging"
tier: 1
searchQueries:
  - "battery health query magisk"
  - "check battery cycle count android root"
  - "qcom battery soh sysfs"
  - "charge full design battery health"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Qualcomm, MediaTek, or Exynos Android smartphone"
conflicts:
  - "None"
configPaths:
  - "/data/adb/modules/custom.battery/service.sh"
  - "/data/adb/modules/custom.battery/custom_script.sh"
  - "/sys/class/power_supply/battery/charge_full"
  - "/sys/class/power_supply/battery/charge_full_design"
  - "/sys/class/qcom-battery/soh"
features:
  - "Reads Qualcomm State of Health (SOH) hardware registers directly from kernel sysfs"
  - "Calculates true battery capacity degradation (charge_full vs charge_full_design)"
  - "Dynamically writes real-time health metrics and timestamps into module.prop for Magisk UI display"
  - "Includes standalone interactive query script for instant ADB/terminal telemetry"
faq:
  - question: "Why is the displayed health percentage different from OEM system settings?"
    answer: "OEM battery health algorithms frequently apply software smoothing and conservative calibration curves. This module queries raw kernel sysfs nodes directly from the battery gas-gauge IC, delivering true unadulterated hardware telemetry."
  - question: "Does this module run a heavy background loop?"
    answer: "No. The daemon updates metrics on a gentle timer and upon boot completion, consuming 0% idle CPU and zero measurable battery power."
---

## Overview

**Battery Health Diagnostics & Cycle Monitor** (authored by Wo Bu Shi Chen Sang & Duo Rou Yu Yuan Pu Tao) provides accurate, hardware-level battery health information on rooted Android devices.

Instead of relying on proprietary OEM health estimates or third-party battery monitor apps that keep wakelocks active, this module interacts directly with kernel sysfs nodes exposed by the hardware power management IC (PMIC).

---

## Technical Architecture & How It Works

### 1. Kernel Sysfs Gas-Gauge Reading

The diagnostic script (`custom_script.sh`) evaluates several hardware sysfs nodes depending on the SoC platform:

```bash
# Qualcomm State of Health (SOH) register
soh=$(cat /sys/class/qcom-battery/soh 2>/dev/null)

# Factory design capacity (uAh -> mAh)
charge_full_design=$(( $(cat /sys/class/power_supply/battery/charge_full_design) / 1000 ))

# Current maximum charge retention capacity (uAh -> mAh)
charge_full=$(( $(cat /sys/class/power_supply/battery/charge_full) / 1000 ))

# True capacity retention percentage
retention=$(( (charge_full * 100) / charge_full_design ))
```

### 2. Live Magisk Description Injection

Rather than requiring an APK interface, the daemon dynamically updates its own `module.prop` description field:

```bash
sed -i "s/^description=.*/description=[${timestamp}] SOH: ${soh}% | Real: ${charge_full}\/${charge_full_design} mAh (${retention}%)/" $custombattery_Path/module.prop
```

Users can observe their current battery health simply by opening Magisk Manager, KernelSU Manager, or APatch WebUI.

---

## Verification & Manual Query

Execute the standalone diagnostic script directly via root terminal:

```bash
su -c sh /data/adb/modules/custom.battery/点我直接查询.sh
```
