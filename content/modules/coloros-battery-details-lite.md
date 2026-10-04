---
id: "coloros-battery-details-lite"
title: "ColorOS Battery Details & Usage Display Lite: Technical Guide"
sidebarTitle: "ColorOS Battery Lite"
description: "Notification center battery telemetry daemon displaying live charging wattage, drain rate, and temperature statistics for ColorOS, Realme UI, and OxygenOS."
category: "system-utilities"
tier: 1
searchQueries:
  - "coloros battery details notification magisk"
  - "realme ui battery discharge monitor"
  - "coloros status bar power metrics"
  - "live charging wattage notification root"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Oppo ColorOS, Realme UI, or OnePlus OxygenOS"
conflicts:
  - "None"
configPaths:
  - "/data/adb/modules/ColorOS_details/service.sh"
  - "/data/adb/modules/ColorOS_details/Lite"
features:
  - "Persistent notification center widget showing real-time battery status"
  - "Calculates active current (mA) and discharge velocity during screen-on time"
  - "Displays accurate battery temperature and voltage telemetry"
  - "Extremely lightweight shell daemon with near-zero resource utilization"
faq:
  - question: "Does this require an external app installation?"
    answer: "No. The module uses Android's command-line notification publisher and system services directly, rendering metrics natively without APK dependencies."
  - question: "Is this compatible with Xiaomi or generic AOSP ROMs?"
    answer: "While specifically tuned for the ColorOS/Realme notification formatting and thermal nodes, generic AOSP devices with standard power_supply sysfs can also render the notification."
---

## Overview

**ColorOS Battery Details & Usage Display Lite** (authored by Everything by the sun) provides live battery telemetry directly in the Android notification shade on ColorOS, Realme UI, and OxygenOS devices.

---

## Technical Architecture & How It Works

The module executes a background polling script (`Lite`) launched via `service.sh`:

```bash
# Sample power telemetry from kernel sysfs
current_now=$(cat /sys/class/power_supply/battery/current_now) # uA
voltage_now=$(cat /sys/class/power_supply/battery/voltage_now) # uV
temp=$(cat /sys/class/power_supply/battery/temp)               # 0.1 C

# Compute real-time wattage
wattage=$(awk "BEGIN {print ($current_now / 1000000) * ($voltage_now / 1000000)}")
```

The script publishes formatted notifications using Android's internal notification channels, allowing instant glanceable access to charging rates and standby drain.
