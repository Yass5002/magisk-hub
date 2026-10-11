---
title: "Fastboot \"waiting for any device\" Driver Fix"
description: "How to fix the Fastboot / ADB \"waiting for any device\" error when flashing Magisk."
---

When executing `fastboot flash boot ...` or `fastboot devices`, the terminal may hang indefinitely on:

```text
< waiting for any device >
```


![waiting for any device terminal](/images/cb05cab65afefab.png)
*waiting for any device terminal*


This occurs due to one of three common causes:

---

## Cause 1: USB 3.0 Chipset Incompatibility
Fastboot protocols on certain AMD or newer Intel USB 3.0/3.1 controllers fail to establish handshakes with Android bootloader interfaces.

### Solutions:
1. **Use a USB 2.0 Port:** Plug your cable directly into a black USB 2.0 port on your computer (preferably on the rear I/O panel of the motherboard, avoiding front-case ports or USB 3.0 blue ports).
2. **Use a USB 2.0 Port:** Plug your cable into a standard black USB 2.0 port (usually located on the rear I/O panel of a desktop PC).
3. **Use a USB 2.0 Hub:** Plugging through an unpowered USB 2.0 hub forces the controller into USB 2.0 legacy mode.

---

## Cause 2: Faulty or Charge-Only Cable
Many cheap USB-C cables lack data lines and only connect charging pins.

### Solutions:
1. Re-seat the USB cable or try a different port.
2. Use the phone's **original OEM cable** (Xiaomi, OnePlus, etc.) that supports high-speed data transfer.

---

## Cause 3: Missing Android Fastboot USB Drivers
Windows has not bound the Google Android Fastboot interface driver to your device in Device Manager.

### Solution:
1. Download the driver package: [Official Google USB Driver](https://developer.android.com/studio/run/win-usb) or [Official MiFlash Driver Tool](https://miuirom.org/updates/mi-flash-tool).
2. Extract the archive and launch `XiaoMiFlash.exe`.
3. Click the **Driver** tab in the top navigation, and click **Install**.


![Installing Universal Android Bootloader Drivers in MiFlash](/images/772ae80e9cbb06e.png)
*Installing Universal Android Bootloader Drivers in MiFlash*


This automatically registers universal drivers for:
- Google Android Bootloader Interface
- NVIDIA USB Debugging Bridge
- Microsoft MTP Device
- Qualcomm HS-USB Diagnostic and QDLoader 9008
