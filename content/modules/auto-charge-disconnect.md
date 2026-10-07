---
id: "auto-charge-disconnect"
title: "Automated Full-Charge Disconnect Guard: Battery Longevity Guide"
sidebarTitle: "Auto Disconnect Guard"
description: "Zero-dependency shell watchdog that automatically halts battery charging at 100% and resumes at 95% to eliminate overnight trickle stress."
category: "battery-power-charging"
tier: 1
searchQueries:
  - "auto stop charging at 100 magisk"
  - "prevent overnight overcharge root"
  - "input suspend charging disconnect"
  - "battery overcharge protection magisk"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Linux kernel supporting input_suspend or charging_enabled"
conflicts:
  - "Other charging limiters"
configPaths:
  - "/data/adb/modules/Charge_control/data.sh"
  - "/data/adb/modules/Charge_control/service.sh"
features:
  - "Automated 100% charge cutoff preventing continuous high-voltage trickle current"
  - "Automatic 95% reconnection restoring charging before significant battery loss"
  - "Dual node compatibility checking both input_suspend and charging_enabled"
  - "Pure POSIX shell script execution requiring no third-party binaries or daemons"
faq:
  - question: "Why is overnight charging harmful without this module?"
    answer: "Holding a battery at 100% capacity under continuous voltage stress causes electrolyte decomposition and accelerated lithium plating. Disconnecting power once full avoids this degradation."
  - question: "Can I adjust the threshold from 100% to 90%?"
    answer: "Yes. Open /data/adb/modules/Charge_control/data.sh and adjust Stop=90 and Start=85."
---

## Overview

**Automated Full-Charge Disconnect Guard** (authored by Jiu Shi Long Xia) protects smartphones that remain connected to chargers for extended periods (such as overnight charging).

---

## Technical Architecture & How It Works

The watchdog script (`data.sh`) monitors `/sys/class/power_supply/battery/capacity`:

```bash
Charging_control=/sys/class/power_supply/battery/input_suspend
Charging_control2=/sys/class/power_supply/battery/charging_enabled

# When capacity hits upper limit:
echo 1 > $Charging_control 2>/dev/null || echo 0 > $Charging_control2

# When capacity drops to resumption floor:
echo 0 > $Charging_control 2>/dev/null || echo 1 > $Charging_control2
```
