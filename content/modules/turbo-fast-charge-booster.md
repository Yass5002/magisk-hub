---
id: "turbo-fast-charge-booster"
title: "Turbo Fast Charge Current Step Booster: Low-Level Charging Guide"
sidebarTitle: "Turbo Charge Booster"
description: "Kernel power supply parameter tuning module that locks maximum input current steps across AC, USB, and wireless power inputs using init.d sysfs directives."
category: "battery-power-charging"
tier: 1
searchQueries:
  - "turbo fast charge magisk module"
  - "boost charging current android root"
  - "ac charging 2000ma sysfs"
  - "increase usb charge rate magisk"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Device with kernel power_supply sysfs support"
conflicts:
  - "Conflicting charging thermal engine modules"
configPaths:
  - "/data/adb/modules/KSCD/common/service.sh"
  - "/sys/class/power_supply/battery/current_max"
features:
  - "Locks AC charging input current ceiling to 2000mA (2.0A)"
  - "Boosts USB data port charging rate from 500mA to 1100mA (1.1A)"
  - "Boosts wireless charging current ceiling to 1100mA"
  - "Lightweight one-shot boot script without background daemon CPU usage"
faq:
  - question: "Can this force a standard 5W charger to output 18W?"
    answer: "No. Power delivery depends on charger negotiation. This module prevents the Android kernel from unnecessarily throttling current to 500mA when connected to capable power sources."
  - question: "Does this generate excess heat?"
    answer: "Higher charging current naturally increases battery temperature slightly. Ensure adequate ventilation during rapid charging."
---

## Overview

**Turbo Fast Charge Current Step Booster** (authored by XLIVE) optimizes charging input limits on rooted devices where conservative manufacturer kernel policies throttle charging current on USB and AC ports.

---

## Technical Architecture & How It Works

During boot initialization, the module executes a series of sysfs tuning writes:

```bash
# Configure maximum allowable charging currents across interfaces
for node in /sys/class/power_supply/*; do
    [ -f "$node/current_max" ] && echo 2000000 > "$node/current_max"
    [ -f "$node/hw_current_max" ] && echo 2000000 > "$node/hw_current_max"
done
```

This prevents the kernel battery driver from stepping down to lower current buckets when background processes generate minor thermal fluctuations.
