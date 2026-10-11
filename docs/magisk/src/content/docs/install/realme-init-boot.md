---
title: "Realme Magisk Installation (Patch init_boot.img)"
description: "Magisk installation guide for Realme phones with kernel 5.15+ by patching init_boot.img."
---

:::note[Compatibility Notice]
- This tutorial applies to devices with **kernel version 5.15.XX – 6.X.XX+** (Android 13+).
- **Check Kernel Version:** Settings – About Phone – Version Info – Kernel Version.
- If your kernel is below 5.15, use the [Realme boot.img Guide](/magisk/install/realme-boot).
:::

## Demonstration Steps

### 1. Unlock Bootloader
Unlock your device's Bootloader:
- [Realme Snapdragon BL Unlock](/magisk/unlock/realme-snapdragon)
- [Realme MediaTek BL Unlock](/magisk/unlock/realme-mediatek)

### 2. Extract `init_boot.img`
Extract `init_boot.img` using [payload-dumper-go init_boot.img](/magisk/extract/payload-dumper-init-boot).

### 3. Copy `init_boot.img` to Phone
Copy `init_boot.img` into your phone's `Download` directory.

### 4. Install Magisk App
Download and install Magisk: [Download Magisk](/magisk/guide/download).

### 5. Patch `init_boot.img`
In Magisk, tap **Install** – **Select and Patch a File** – choose `init_boot.img` – tap **LET'S GO**.
The output file `magisk_patched-xxx.img` is saved in `Download`.

![Patching init_boot.img in Magisk](/images/ee704ee121cf031.jpg)
*Patching init_boot.img in Magisk*


### 6. Download Platform-Tools on PC
Download official [Google Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools) and extract it using [7-Zip](https://www.7-zip.org/).

:::tip[Beginner Terminal Tip]
Open the extracted `platform-tools` folder in Windows File Explorer, click directly on the address bar at the top, type `cmd`, and press **Enter**. This opens Command Prompt directly in the tools directory.
:::
![Extracting adb-fastboot](/images/02e5e0821c8cb55.png)
*Extracting adb-fastboot*


### 7. Copy Patched File to PC
Copy `magisk_patched-xxx.img` to the PC's `adb-fastboot` directory.

![Copying patched init_boot file to adb-fastboot](/images/e042a2185c1242f.png)
*Copying patched init_boot file to adb-fastboot*


### 8. Enter Bootloader Mode
Power off phone, hold **Power + Volume Down** until Fastboot appears, then connect to PC.

![Realme Fastboot mode](/images/a78cc09d9d93a14.jpg)
*Realme Fastboot mode*


### 9. Flash Patched Image
In your command terminal inside the `platform-tools` directory, run:

```bash
fastboot flash init_boot <magisk_patched_filename.img>
```

### 10. Reboot Device
When terminal shows `OKAY`, run `fastboot reboot`.

![Terminal flashing output](/images/afc075c16a71484.png)
*Terminal flashing output*


### 11. Verify Root
Open Magisk. If the version number is displayed, Root is active!

![Magisk successfully verified](/images/33e75ff09dd601b.jpg)
*Magisk successfully verified*


:::tip[Recovery Instructions (Emergency Restore)]
If your phone fails to boot or gets stuck in a bootloop after flashing:
1. Power off and hold **Power + Volume Down** to return to Fastboot mode.
2. Flash your unmodified stock backup image:
   ```bash
   fastboot flash init_boot init_boot.img
   ```
3. Run `fastboot reboot`. Normal startup will be restored immediately with no data loss.
:::
