---
id: "nothing-euicc"
title: "Nothing EUICC Enabler: Force eSIM & System LPA on Nothing Devices"
sidebarTitle: "Nothing EUICC Enabler"
description: "Force-enables eSIM functionality and system Local Profile Assistant (LPA) on Nothing OS devices using physical smart eSIM cards like eSTK.me and 5ber."
category: "networking-proxies"
tier: 1
searchQueries:
  - "nothing euicc force enabler magisk"
  - "reindex ot nothing euicc"
  - "enable esim nothing phone 1 2"
  - "system lpa nothing os estk"
  - "5ber esim nothing phone magisk"
prerequisites:
  - "Root access via Magisk"
  - "Nothing Phone (1) or Nothing Phone (2) with Qualcomm processor"
  - "Physical programmable eSIM card adapter (e.g., eSTK.me or 5ber)"
conflicts: []
configPaths:
  - "/data/adb/modules/nothing-euicc/"
features:
  - "System LPA activation: enables Android's native Local Profile Assistant framework for seamless eSIM profile downloading and switching"
  - "Removable smart eSIM integration: full support for eSTK.me and 5ber physical eSIM chips placed in SIM trays"
  - "Direct OS management: manage eSIM profiles directly within Nothing OS network settings without relying solely on companion apps"
  - "Qualcomm telephony optimization: specifically utilizes Qualcomm modem and radio interface layer (RIL) configurations"
  - "Systemless deployment: injects telecommunication framework configurations without modifying system partition partitions"
---

## Overview

While modern smartphones increasingly favor eSIM technology for international travel and multi-carrier setups, certain Nothing devices lack native eSIM capability out of the box or do not expose the system-level Local Profile Assistant (LPA) required to manage digital cellular profiles directly through the OS.

Developed by reindex-ot, **nothing-euicc** (Nothing EUICC Force Enabler) is a specialized Magisk module that force-enables eSIM services and system LPA functionality on Nothing OS devices when paired with removable physical eSIM smart cards (such as eSTK.me and 5ber).

## Hardware Compatibility & Limitations

### Tested & Supported Devices
- **Nothing Phone (1)**: Full system LPA and profile downloading/switching supported.
- **Nothing Phone (2)**: Full system LPA and profile downloading/switching supported.
- **Nothing Phone (2a) & CMF Phone 1**: Hardware is powered by MediaTek processors; **system LPA is not functional** on MediaTek chipsets.
- **Nothing Phone (3)**: System LPA operates, but internal embedded eSIM on slot 2 is given priority by the modem.

### Supported Physical eSIM Cards
- **eSTK.me**: Supports both direct profile downloading and profile switching. In the SIM ToolKit (STK) menu, ensure "Announce as eUICC" or "eUICC Mark" in ATR mode is toggled on to allow system LPA downloads.
- **5ber eSIM**: Supports active eSIM profile switching.

## Installation & Setup

1. Insert your physical programmable eSIM card into the SIM tray of your Nothing device.
2. Download the latest `nothing-euicc.zip` from GitHub releases.
3. Flash the module in **Magisk Manager**.
4. Reboot your phone.
5. Open **Settings > Network & internet > SIMs**. The native Android eSIM setup and QR-code scanning interface will now be available.
