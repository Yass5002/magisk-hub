---
title: "Samsung Magisk Installation (Patch init_boot.img)"
description: "Magisk installation guide for Samsung Galaxy devices with kernel 5.15+ by patching init_boot.img.tar."
---

:::note[Compatibility Notice]
- This tutorial applies to Samsung devices with **kernel version 5.15.XX – 6.X.XX+** (Android 13+ / One UI 5.1+ / One UI 6+).
- **Check Kernel Version:** Settings – About Phone – Software Information – Kernel Version.
- If your kernel is below 5.15, use the [Samsung boot.img Guide](/magisk/install/samsung-boot).
- Generic ramdisk on newer Samsung devices is located in `init_boot.img.lz4`.
:::

## Demonstration Steps

### 1. Unlock Bootloader
Unlock your device's Bootloader: [Samsung BL Unlock Guide](/magisk/unlock/samsung).

### 2. Download Official Firmware
Download matching official firmware using [Frija](/magisk/extract/samsung-frija) or [SamFirm](/magisk/extract/samsung-samfirm).

### 3. Download Odin3 & Drivers on PC
Download [Samsung Odin3](https://samsungodin.com/) and install official [Samsung Android USB Drivers](https://developer.samsung.com/android-usb-driver) on your computer.

![Extracting Odin3](/images/b91ebf3f6055af5.png)
*Extracting Odin3*


### 4. Extract Firmware
Unpack the firmware archive to obtain the 5 component files (`AP`, `BL`, `CP`, `CSC`, `HOME_CSC`).

![Extracting firmware](/images/f3ada80d5c4ee70.png)
*Extracting firmware*


### 5. Enter Downloading Mode
Power off phone, hold **Volume Up + Volume Down**, connect USB to PC, press **Volume Up** on Warning screen to enter **Downloading mode**.

![Samsung Downloading mode](/images/78d9ea7869aa447.jpg)
*Samsung Downloading mode*


### 6. Flash Full Firmware Test
Load BL, AP, CP, CSC in Odin3 and flash to verify firmware integrity.

![Flashing full firmware test](/images/cb6409af44de70e.jpg)
*Flashing full firmware test*


### 7. Install Magisk App
Install Magisk app on the phone: [Download Magisk](/magisk/guide/download).

### 8. Install 7-Zip on PC
Install [7-Zip](https://www.7-zip.org/) on your computer.

### 9. Extract `init_boot.img.lz4` from AP
Right-click `AP_xxx.tar.md5`, select **7-Zip -> Open archive**, and drag out `init_boot.img.lz4`.

![Extracting init_boot.img.lz4](/images/4dcbf789034606a.jpg)
*Extracting init_boot.img.lz4*


### 10. Repack `init_boot.img.lz4` into TAR
Right-click `init_boot.img.lz4`, select **7-Zip -> Add to archive...**, choose format **tar**, and save as `init_boot.img.tar`.

![Packing init_boot into tar](/images/2089faba0cd0fc8.jpg)
*Packing init_boot into tar*


### 11. Copy TAR to Phone
Copy `init_boot.img.tar` into your phone's `Download` directory.

![Copying tar to phone](/images/131c412e4f631dd.jpg)
*Copying tar to phone*


### 12. Patch in Magisk
Open Magisk on your phone: tap **Install** – **Select and Patch a File** – choose `init_boot.img.tar` – tap **LET'S GO**.
Magisk will patch the file and output `magisk_patched-xxx.tar` into `Download`.

### 13. Copy Patched TAR to PC
Copy `magisk_patched-xxx.tar` to your computer.

![Copying patched tar to PC](/images/1caecb18967bc73.jpg)
*Copying patched tar to PC*


### 14. Flash Patched File via Odin3
Reboot phone into **Downloading mode**, open Odin3, select `magisk_patched-xxx.tar` in the **AP** slot, and click **Start**.

![Flashing patched tar in Odin3 AP slot](/images/779232e2d4cb5bb.jpg)
*Flashing patched tar in Odin3 AP slot*


### 15. Reboot & Verify
After Odin shows **PASS**, reboot phone and open Magisk to verify root status!

![Odin3 PASS output](/images/5414bfb7a22e23f.jpg)
*Odin3 PASS output*


![Magisk Root verified on Samsung](/images/ff07a7a245f3d87.jpg)
*Magisk Root verified on Samsung*

---

## Troubleshooting & Safety Net

- **Samsung USB Connection Issues**: If Odin does not detect your phone, install the [Samsung USB Driver](/magisk/troubleshooting/samsung-usb-driver).
- **Error -45 during boot**: On One UI 5 / 6, if the device halts with Error -45, follow the [Samsung Error -45 Fix](/magisk/troubleshooting/samsung-error-45).
- **Bootloop Recovery**: Put the phone back into Downloading mode and flash the stock unmodified `AP_...tar.md5` file in the Odin AP slot to recover normal booting.
