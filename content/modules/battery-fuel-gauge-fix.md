---
id: "battery-fuel-gauge-fix"
title: "Battery Fuel Gauge Fix: Qualcomm BMS Calibration and UI Synchronization"
sidebarTitle: "Battery Gauge Fix"
description: "Kernel driver synchronization utility that resolves battery percentage drift by querying Qualcomm BMS hardware registers and forcing Android BatteryService alignment."
category: "battery-power-charging"
tier: 1
searchQueries:
  - "battery capacity fix magisk"
  - "qualcomm bms capacity_raw fix"
  - "fix android battery percentage jumping"
  - "calibrate battery level magisk module"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Qualcomm Snapdragon device with hardware BMS sysfs interface"
conflicts:
  - "Other aggressive battery percentage spoofers"
configPaths:
  - "/sys/class/power_supply/bms/capacity_raw"
  - "/sys/class/power_supply/bms/capacity"
  - "/data/adb/modules/bat_capacity_fix/service.sh"
features:
  - "Reads hardware coulomb counter data directly from Qualcomm BMS kernel sysfs nodes"
  - "Continuously synchronizes system BatteryService state via dumpsys battery set level"
  - "Dynamic polling cycle: 5-second interval during active charging, 20-second interval on discharge"
  - "Includes compiled native companion binary bat_capacity_fix for lightweight background execution"
  - "Prevents sudden battery percentage drops (e.g. jumping from 20% to 1% or shutdown)"
faq:
  - question: "Why does the Android battery percentage drift from the actual charge?"
    answer: "Android relies on algorithmic estimation integrating battery voltage, open-circuit curves, and load compensation. On heavily used or replaced battery cells, the system-level software estimator drifts significantly from the hardware fuel gauge (BMS coulomb counter), causing abrupt shutdowns or inaccurate status bar readings."
  - question: "Does this module fix physically degraded battery cells?"
    answer: "No. The module does not restore chemical capacity to worn battery cells. It ensures that the percentage displayed on your screen accurately reflects the real-time electrical charge calculated by the physical battery management IC."
---

## Overview

**Battery Fuel Gauge Fix** (authored by DuduSki) is a low-level battery calibration module designed to eliminate discrepancies between Android's status bar battery percentage and the physical battery management system (BMS).

On devices powered by Qualcomm Snapdragon platforms, the Power Management Integrated Circuit (PMIC) maintains a dedicated Battery Monitoring System (BMS). The hardware BMS measures charge entering and exiting the cell via a precision sense resistor (coulomb counting). However, Android's framework daemon (`BatteryService`) applies complex smoothing algorithms that can become desynchronized after custom ROM installations, kernel swaps, or aging battery health.

This desynchronization leads to frustrating issues: phones suddenly turning off while displaying 15% charge, or charging indicators remaining stuck at 100% for hours before plummeting. Battery Fuel Gauge Fix bypasses framework smoothing by binding the UI directly to kernel BMS telemetry.

---

## Technical Architecture & How It Works

The module establishes a supervisory daemon during the `late_start` service stage:

### 1. Hardware Register Discovery

The module inspects the kernel power supply class hierarchy in `/sys`:

```bash
# Primary Qualcomm BMS raw capacity node (measured in basis points: e.g., 8500 = 85.00%)
/sys/class/power_supply/bms/capacity_raw

# Secondary fallback hardware capacity node
/sys/class/power_supply/bms/capacity

# Real-time charging state node
/sys/class/power_supply/battery/status
```

### 2. Synchronization Loop

1. **Telemetry Sampling**: The background daemon divides the raw integer from `capacity_raw` by 100 to extract the true single-percentage integer value.
2. **Framework Alignment**: When a change in true capacity is detected, the script updates Android's battery state machine via standard shell IPC:
   ```bash
   dumpsys battery set level <calibrated_level>
   ```
3. **Adaptive Power Scheduling**:
   - **Discharging**: The daemon sleeps for 20-second intervals to minimize CPU wakeups and prevent idle drain.
   - **Charging**: The polling interval shortens to 5 seconds to provide smooth, responsive progression as the battery charges.

### 3. Native Binary Acceleration

In addition to the POSIX shell monitor in `service.sh`, the module packages an optimized native binary `bat_capacity_fix`. On supported kernels, this executable hooks directly into kernel sysfs events, eliminating shell invocation overhead entirely.

---

## Verification & Manual Testing

To verify that your kernel supports the BMS sysfs nodes utilized by the module, run:

```bash
su -c "cat /sys/class/power_supply/bms/capacity_raw"
```

If your device returns an integer (e.g. `7842` for ~78.4%), the Qualcomm hardware fuel gauge is accessible and active.
