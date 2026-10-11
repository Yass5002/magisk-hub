---
title: "Samsung Magisk Installation (Patch boot.img)"
description: "Magisk installation guide for Samsung Galaxy devices by patching boot.img.tar via Odin."
---

:::note[Important Note]
- In theory, all Android devices can be flashed as long as the **Bootloader** can be unlocked.
- **Samsung Workflow:** `Unlock Bootloader` > `Extract boot.img.lz4` > `Pack to boot.img.tar` > `Patch via Magisk` > `Flash patched tar via Odin3 AP slot`.
- For models with kernel versions `5.15.XX` - `6.X.XX`, see the [Samsung init_boot Guide](/magisk/install/samsung-init-boot).
- Universal tutorial for Samsung Galaxy and One UI.
:::

## Demonstration Steps

### 1. Unlock Bootloader
Unlock your device's Bootloader first: [Samsung BL Unlock Guide](/magisk/unlock/samsung).

### 2. Download Official Firmware
Download matching official firmware using [Frija Firmware Downloader](/magisk/extract/samsung-frija) or [SamFirm](/magisk/extract/samsung-samfirm).

### 3. Download Odin3 & Drivers on PC
Download [Samsung Odin3](https://samsungodin.com/) and install official [Samsung Android USB Drivers](https://developer.samsung.com/android-usb-driver) on your computer.

![Extracting Odin3](/images/b91ebf3f6055af5.png)
*Extracting Odin3*


### 4. Extract Firmware
Unpack the downloaded firmware archive using [7-Zip](https://www.7-zip.org/).

![Extracting Samsung firmware](/images/f94cf164209d706.png)
*Extracting Samsung firmware*


### 5. Enter Downloading Mode
Power off phone, hold **Volume Up + Volume Down**, plug USB cable into PC, and press **Volume Up** on the Warning screen to enter **Downloading mode**.

![Samsung Downloading mode](/images/78d9ea7869aa447.jpg)
*Samsung Downloading mode*


### 6. Flash Firmware Test via Odin3
Load BL, AP, CP, and CSC into Odin3, and flash to verify firmware integrity.

![Odin3 flashing firmware](/images/cb6409af44de70e.jpg)
*Odin3 flashing firmware*


### 7. Install Magisk App
Install Magisk app on phone: [Download Magisk](/magisk/guide/download).

### 8. Install 7-Zip on PC
Download and install [7-Zip](https://www.7-zip.org/) on your computer.

### 9. Extract `boot.img.lz4` from AP
Right-click `AP_xxx.tar.md5`, select **7-Zip -> Open archive**, and drag out `boot.img.lz4`.

![Extracting boot.img.lz4 from AP](/images/f3ac227d636d09d.png)
*Extracting boot.img.lz4 from AP*


### 10. Repack `boot.img.lz4` into TAR
Right-click `boot.img.lz4`, select **7-Zip -> Add to archive...**, choose format **tar**, and save as `boot.img.tar`.

![Repacking boot.img.lz4 into tar format](/images/3dec696c5e49e6e.jpg)
*Repacking boot.img.lz4 into tar format*


### 11. Copy `boot.img.tar` to Phone
Copy `boot.img.tar` into your phone's `Download` folder.

### 12. Patch in Magisk
Open Magisk, tap **Install** – **Select and Patch a File** – choose `boot.img.tar` – tap **LET'S GO**.
The patched file `magisk_patched-xxx.tar` is saved in `Download`.

![Patching boot.img.tar in Magisk](/images/b4ef61a92f8cbb3.jpg)
*Patching boot.img.tar in Magisk*


### 13. Copy Patched TAR to PC
Copy `magisk_patched-xxx.tar` to your PC.

![Copying patched tar to PC](/images/1caecb18967bc73.jpg)
*Copying patched tar to PC*


### 14. Flash Patched File via Odin3
Put phone into **Downloading mode**, open Odin3, select `magisk_patched-xxx.tar` in the **AP** slot, and click **Start**.

![Flashing patched tar in Odin3 AP slot](/images/779232e2d4cb5bb.jpg)
*Flashing patched tar in Odin3 AP slot*


### 15. Verify Root
Once Odin reports **PASS**, reboot phone and open Magisk to verify root!

![Odin3 PASS output](/images/5414bfb7a22e23f.jpg)
*Odin3 PASS output*


![Magisk Root verified on Samsung](/images/ff07a7a245f3d87.jpg)
*Magisk Root verified on Samsung*

---

## Troubleshooting & Safety Net

- **Samsung USB Connection Issues**: If Odin does not detect your phone, install the [Samsung USB Driver](/magisk/troubleshooting/samsung-usb-driver).
- **Error -45 during boot**: On One UI 5 / 6, if the device halts with Error -45, follow the [Samsung Error -45 Fix](/magisk/troubleshooting/samsung-error-45).
- **Bootloop Recovery**: Put the phone back into Downloading mode and flash the stock unmodified `AP_...tar.md5` file in the Odin AP slot to recover normal booting.
