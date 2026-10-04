---
id: "acc"
title: "Advanced Charging Controller: Extend Battery Life via Kernel Charging Controls"
sidebarTitle: "Advanced Charging Controller"
description: "Sophisticated power management daemon by VR25 that manipulates kernel power supply nodes to enforce charging capacity thresholds, current limits, and idle mode."
category: "battery-power-charging"
tier: 1
searchQueries:
  - "advanced charging controller magisk module"
  - "acc battery limits root"
  - "android limit charge to 80 percent"
  - "vr25 acc download"
  - "acc charging idle mode"
prerequisites:
  - "Android 5.0 (Lollipop) or newer"
  - "Root access via Magisk, KernelSU, or APatch"
  - "Kernel supporting writable power supply sysfs switches (/sys/class/power_supply/)"
conflicts:
  - "OEM aggressive charging daemon conflicts (some OnePlus WARP / Oppo VOOC proprietary daemons force-override current limits)"
  - "Concurrent execution of competing battery-limiting modules"
configPaths:
  - "/data/adb/vr25/acc-data/config.txt"
  - "/data/adb/vr25/acc-data/disable"
  - "/data/adb/modules/acc/"
features:
  - "Capacity threshold control: automatically halts charging at user-defined battery levels (e.g. 80%) and resumes at lower levels"
  - "Battery idle mode (bypass charging): powers the motherboard directly from the USB charger without charging or stressing the battery"
  - "Current & voltage throttling: dynamically drops charging wattage to prevent battery overheating during gaming or heavy usage"
  - "Automatic switch testing: scans all kernel power_supply nodes to discover stable charging control switches"
faq:
  - question: "Why is limiting charging to 80% beneficial for my device?"
    answer: "Lithium-ion cells experience exponential electrochemical stress when charged above 4.10V (approx. 80-85% state-of-charge). By capping charging at 80% and avoiding high-temperature saturation phases, ACC can increase battery cycle lifespan by 300% to 500%."
  - question: "What should I do if my phone reboots when charging stops?"
    answer: "Some device kernels panic when an incompatible charging switch is toggled. Run `su -c acc -t` in a terminal; this automated test systematically tests every charging switch in `/sys/class/power_supply/` and automatically blacklists switches that cause reboots."
  - question: "How does the emergency disable safety feature work?"
    answer: "ACC incorporates a 60-second safety delay after boot animation stops before starting the daemon. If you ever experience issues upon boot, you have a full minute to run `su -c accd -x` or `touch /data/adb/vr25/acc-data/disable`, which immediately halts and prevents the daemon from launching."
---

## Overview

The **Advanced Charging Controller (ACC)**, developed by VR25, is the most comprehensive, versatile power management daemon available for rooted Android devices.

Standard Android operating systems charge lithium-ion batteries to 100% capacity at maximum permissible voltages (often 4.35V to 4.45V) and sustain high charging currents even as internal temperatures rise. This rapid charging and high-voltage saturation accelerates battery degradation, causing premature cell swelling, permanent capacity loss, and decreased discharge endurance.

ACC transforms your device's power behavior by interfacing directly with the Linux kernel's power supply subsystem (`/sys/class/power_supply/`). It enables fine-grained control over charging thresholds, maximum charging current (milliamps), voltage cutoffs, and battery thermal policies.

---

## Technical Architecture & Kernel Power Switches

Modern Android devices manage power through hardware PMICs (Power Management Integrated Circuits) controlled by kernel drivers. These drivers expose writable attribute nodes in `sysfs`:

```
┌────────────────────────────────────────────────────────┐
│                   acc daemon (accd)                    │
│   - Reads battery temperature & capacity               │
│   - Enforces pause/resume rules                        │
└───────────────────────────┬────────────────────────────┘
                            │ writes 0 or 1
┌───────────────────────────▼────────────────────────────┐
│      Kernel Sysfs Power Nodes (/sys/class/power_supply)│
│  - battery/charging_enabled                            │
│  - battery/input_suspend                               │
│  - bms/charge_control_limit_max                        │
└───────────────────────────┬────────────────────────────┘
                            │ I2C / SPMI bus
┌───────────────────────────▼────────────────────────────┐
│           Hardware PMIC (Qualcomm / MediaTek)          │
│  Directs electrical current to battery vs motherboard  │
└────────────────────────────────────────────────────────┘
```

When the battery capacity reaches your configured threshold (e.g. 80%), `accd` writes the appropriate disable byte to the kernel charging switch. If the kernel supports **Battery Idle Mode**, charging current to the battery drops to 0 mA while the device draws operational current directly from the wall charger.

---

## Installation & Initial Configuration

### Installation
1. Download `acc_v*.zip` from the official release page.
2. Flash the module in **Magisk**, **KernelSU**, or **APatch**.
3. Reboot your device.

### Verifying Installation & Status
Open any root terminal emulator (e.g. Termux or Material Terminal) and run:
```bash
su
acc -i
```
This displays real-time battery diagnostics:
- Current capacity (%)
- Real-time current flow (mA)
- Battery temperature (°C)
- Current charging status and active charging switch

---

## Essential CLI Commands & Common Configurations

ACC provides a rich CLI interface via the `acc` binary:

### 1. Setting Capacity Thresholds
To pause charging at 80% and resume charging when the battery drops to 70%:
```bash
su -c acc 80 70
```

### 2. Setting Maximum Charging Current
To protect battery health during overnight charging by restricting maximum current to 1500 mA (1.5A):
```bash
su -c acc -s c_max=1500
```

### 3. Setting Temperature Limits
To prevent battery degradation caused by high ambient heat or heavy gaming, halt charging if temperature exceeds 40°C and resume at 37°C:
```bash
su -c acc -s temp=40-37
```

### 4. Running the Switch Discovery Test
To ensure your device uses the most stable kernel charging switch:
```bash
su -c acc -t
```
ACC will test each available switch, monitor current draw, verify whether the phone enters true idle mode, and blacklist switches that trigger sudden reboots.

---

## Hardware Warnings & OEM Quirks

### Xiaomi Devices (Poco X3 Pro & Similar PMICs)
- **Known Issue**: Certain Xiaomi devices have buggy PMIC hardware that can occasionally lock up if charging is suspended while the battery is extremely low.
- **Guideline**: Ensure the low-battery auto-shutdown threshold is maintained (default is 5% capacity):
  ```bash
  su -c acc -s shutdown_capacity=5
  ```
- If charging ever becomes non-responsive, boot the device into Fastboot/Bootloader mode and select *Reboot System* to reset the hardware PMIC registers.

---

## Emergency Recovery & Safe Disabling

ACC is engineered with fail-safe mechanisms to prevent unrecoverable bootloops:

1. **60-Second Post-Boot Timer**: The daemon waits 60 seconds after the boot animation ends before loading the charging configuration.
2. **Instant Emergency Disable**:
   Connect via ADB:
   ```bash
   adb wait-for-device shell
   su
   touch /data/adb/vr25/acc-data/disable
   reboot
   ```
3. **Module Uninstallation**:
   ```bash
   rm -rf /data/adb/modules/acc
   rm -rf /data/adb/vr25
   ```
