---
title: "Xiaomi / Redmi Magisk Installation (Patch init_boot.img)"
description: "Magisk installation guide for Xiaomi and Redmi phones by patching init_boot.img."
---

:::note[Compatibility Notice]
- This tutorial applies only to devices with **Linux kernel versions 5.15.XX – 6.X.XX+** (Android 13+).
- *This refers to the kernel Android version, not the system Android version.*
- **Check Kernel Version:** Go to **Settings – My Device – All Specs – Kernel Version**.
- If your kernel is below 5.15, use the [Xiaomi boot.img Guide](/magisk/install/xiaomi-boot).
- On devices launching with Android 13+, the generic ramdisk is moved out of `boot.img` and placed into a dedicated `init_boot.img`.
:::

## Demonstration Steps

### 1. Unlock Bootloader
Unlock your device's Bootloader: [Xiaomi BL Unlock Guide](/magisk/unlock/xiaomi).

### 2. Extract `init_boot.img`
Extract `init_boot.img` from your device's official ROM package using [payload-dumper-go init_boot.img](/magisk/extract/payload-dumper-init-boot).

### 3. Copy `init_boot.img` to Phone
Connect phone to PC in **File Transfer (MTP)** mode, and copy `init_boot.img` into your phone's `Download` directory.

### 4. Install Magisk App
Download and install Magisk on your phone: [Download Magisk](/magisk/guide/download).

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
Copy `magisk_patched-xxx.img` from phone `Download` to PC's `adb-fastboot` directory.

![Copying patched init_boot file to adb-fastboot](/images/e042a2185c1242f.png)
*Copying patched init_boot file to adb-fastboot*


### 8. Enter Bootloader Mode
Power off phone, hold **Power + Volume Down** until Fastboot screen appears, then connect to PC.

![Xiaomi Fastboot mode](/images/5617427dce0c230.png)
*Xiaomi Fastboot mode*


### 9. Flash Patched Image
In your command terminal inside the `platform-tools` directory, run:

```bash
fastboot flash init_boot <magisk_patched_filename.img>
```

> **Important:** Notice the partition name is `init_boot`, not `boot`!

### 10. Reboot Device
When terminal shows `OKAY`, run:

```bash
fastboot reboot
```

![Terminal flashing init_boot output](/images/afc075c16a71484.png)
*Terminal flashing init_boot output*


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
