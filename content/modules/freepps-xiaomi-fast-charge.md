---
id: "freepps-xiaomi-fast-charge"
title: "FreePPS Xiaomi Public PPS Fast Charge Protocol Unlocker"
description: "KernelSU & Magisk module unlocking open standard USB-PD Programmable Power Supply (PPS) protocol fast charging on Xiaomi and Redmi smartphones."
category: "battery-power-charging"
author: "Seyud"
version: "v1.7.0"
updatedAt: "2026-10-04"
compatibility: ["KernelSU", "APatch", "Magisk"]
---

## Overview & System Architecture

**FreePPS**, developed by Seyud, is an open-source battery and charging subsystem module engineered to unlock and enable full public **PPS (Programmable Power Supply)** protocol fast charging on Xiaomi, Redmi, and POCO smartphones.

OEM Xiaomi firmware deliberately restricts third-party USB-PD chargers to basic 18W–27W charging profiles, reserving ultra-fast charging (33W, 67W, 120W) exclusively for proprietary Xiaomi Charge Turbo adapters. FreePPS removes these vendor charging restrictions by modifying kernel charge negotiation parameters and sysfs power supply limits, enabling compatible third-party multi-port GaN chargers with PPS support to deliver up to 55W–65W+ charging speeds.

## Key Charging Capabilities

1. **PPS Negotiation Bypass**: Overrides vendor power supply constraints in `/sys/class/power_supply/battery/` and `/sys/class/qcom-battery/`.
2. **Third-Party GaN Compatibility**: Allows standard Anker, Baseus, Ugreen, and CUKTECH PPS-enabled USB-PD chargers to charge Xiaomi devices at maximum supported hardware wattage.
3. **Screen-On Charging Acceleration**: Prevents drastic charging rate reduction when the display panel is illuminated.

## Installation & Verification

### Step 1: Flashing the Package
Flash `FreePPS_v1.7.0.zip` via KernelSU, APatch, or Magisk.

### Step 2: Verification After Reboot
Connect a verified 65W+ or 100W PPS-capable USB-PD charger and execute:
```bash
cat /sys/class/power_supply/battery/current_now
cat /sys/class/power_supply/battery/voltage_now
```
Calculate active wattage: `(current_now * voltage_now) / 10^12 = Watts`.

### Step 3: Inspect Charge Protocol Log
```bash
dmesg | grep -iE "pps|pd_policy|charge" | tail -n 20
```

## Hardware Safety & Temperature Controls

- The device's primary hardware battery protection IC remains fully functional and will prevent over-voltage or thermal runaway.
- It is recommended to monitor battery temperature during initial fast-charge cycles to ensure ambient cooling is adequate.
