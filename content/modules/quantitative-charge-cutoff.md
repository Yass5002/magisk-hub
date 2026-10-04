---
id: "quantitative-charge-cutoff"
title: "BH Quantitative Charging Cutoff: Advanced Battery Protection Guide"
sidebarTitle: "Quantitative Cutoff"
description: "Kernel-level charging limit controller that toggles power supply charging switches at user-defined thresholds (e.g. stop at 80%, resume at 70%) to preserve battery lifespan."
category: "battery-power-charging"
tier: 1
searchQueries:
  - "limit battery charging 80 percent magisk"
  - "quantitative charging cutoff root"
  - "input suspend battery charge control"
  - "battery protection charge limiter android"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Kernel supporting battery input_suspend or charging_enabled sysfs nodes"
conflicts:
  - "Other charging bypass or charge limiter daemons (e.g. ACC, Battery Charge Limit)"
configPaths:
  - "/data/media/0/Android/BHcharging/files.conf"
  - "/data/adb/modules/BHcccc/service.sh"
  - "/data/adb/modules/BHcccc/B.sh"
  - "/sys/class/power_supply/battery/charging_enabled"
features:
  - "Configurable charge termination ceiling (e.g. stop at 80% to eliminate high-voltage lithium stress)"
  - "Configurable recharge resumption floor (e.g. resume charging when capacity drops to 75%)"
  - "Hardware switch support: handles both input_suspend and charging_enabled sysfs nodes"
  - "Live status feedback written directly to module.prop display in root managers"
faq:
  - question: "Why is limiting charge to 80% beneficial?"
    answer: "Lithium-ion cells experience the highest chemical degradation and cathode degradation when held between 4.2V and 4.45V (typically above 80% state-of-charge). Capping charging at 80% can extend cell cycle life by 200% to 300%."
  - question: "How do I change the stop threshold?"
    answer: "Edit /data/media/0/Android/BHcharging/files.conf and adjust the Stop_charging value to your preferred percentage."
---

## Overview

**BH Quantitative Charging Cutoff & Battery Guard** (authored by Bu Tai Hui Qi Wang Ming & HChai / 不太会起网名 && HChai) is an automated charge controller engineered to protect lithium-ion batteries from overcharging and high-voltage heat stress.

The module runs as a background watchdog that continuously samples battery state-of-charge (SOC). Upon reaching the user-configured limit, it dispatches a hardware cutoff command directly to the Linux kernel power supply subsystem.

---

## Technical Architecture & How It Works

### 1. Sysfs Charging Switch Negotiation

The daemon (`B.sh`) locates the active hardware charging control node:

```bash
# Common Qualcomm / MediaTek sysfs control nodes:
# 1. /sys/class/power_supply/battery/charging_enabled (1=enable, 0=disable)
# 2. /sys/class/power_supply/battery/input_suspend (0=enable, 1=suspend)

echo 0 > /sys/class/power_supply/battery/charging_enabled
# or
echo 1 > /sys/class/power_supply/battery/input_suspend
```

### 2. State Watchdog Loop

The daemon evaluates `capacity` against thresholds declared in `/data/media/0/Android/BHcharging/files.conf`:

```bash
if [ "$current_capacity" -ge "$Stop_charging" ]; then
    echo 0 > "$USBpath"
    sed -i "s/状态：.*/状态：已停充 (${current_capacity}%)]/g" "$module"
elif [ "$current_capacity" -le "$Resume_charging" ]; then
    echo 1 > "$USBpath"
    sed -i "s/状态：.*/状态：充电中 (${current_capacity}%)]/g" "$module"
fi
```

---

## Configuration & Verification

Inspect current charging switch state:

```bash
# Check charging switch state (0 = charging disabled)
cat /sys/class/power_supply/battery/charging_enabled
```
