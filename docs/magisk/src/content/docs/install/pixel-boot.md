---
title: "Google Pixel Magisk Installation (Patch boot.img)"
description: "Magisk installation guide for Google Pixel phones (Pixel 6 and earlier) by patching boot.img."
---

:::note[Important Note]
- In theory, all Android devices can be flashed as long as the **Bootloader** can be unlocked.
- **General Workflow:** `Unlock Bootloader` > `Patch boot.img` > `Fastboot flash patched image`.
- For **Pixel 7, Pixel 8, and Pixel 9 series**, please see the [Google Pixel init_boot Guide](/magisk/install/pixel-init-boot).
- Universal tutorial for Pixel 6 series and earlier running Stock Android.
:::

## Demonstration Steps

### 1. Unlock Bootloader
Unlock your device's Bootloader: [Google Pixel BL Unlock Guide](/magisk/unlock/pixel).

### 2. Extract `boot.img`
Extract `boot.img` from the official factory image or full OTA using [payload-dumper-go boot.img](/magisk/extract/payload-dumper-boot).

### 3. Copy `boot.img` to Phone
Copy `boot.img` into your phone's `Download` directory.

### 4. Install Magisk App
Download and install Magisk: [Download Magisk](/magisk/guide/download).

### 5. Patch `boot.img`
In Magisk, tap **Install** – **Select and Patch a File** – choose `boot.img` – tap **LET'S GO**.
The output file `magisk_patched-xxx.img` is saved in `Download`.

![Patching boot.img in Magisk](/images/a1bd2ef6dbcc0ef.jpg)
*Patching boot.img in Magisk*


### 6. Download Platform-Tools on PC
Download official [Google Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools) and extract it using [7-Zip](https://www.7-zip.org/).

:::tip[Beginner Terminal Tip]
Open the extracted `platform-tools` folder in Windows File Explorer, click directly on the address bar at the top, type `cmd`, and press **Enter**. This opens Command Prompt directly in the tools directory.
:::
![Extracting adb-fastboot](/images/02e5e0821c8cb55.png)
*Extracting adb-fastboot*


### 7. Copy Patched File to PC
Copy `magisk_patched-xxx.img` to the PC's `adb-fastboot` directory.

![Copying patched file to PC](/images/bdb4e2a5c4bfb97.png)
*Copying patched file to PC*


### 8. Enter Bootloader Mode
Power off phone, hold **Power + Volume Down** until Fastboot appears, then connect to PC.

![Google Pixel Fastboot mode](/images/86a68e5b22d0f1c.png)
*Google Pixel Fastboot mode*


### 9. Flash Patched Image
In your command terminal inside the `platform-tools` directory, run:

```bash
fastboot flash boot <magisk_patched_filename.img>
```

### 10. Reboot Device
When terminal shows `OKAY`, run `fastboot reboot`.

![Terminal flashing output](/images/a39401275d1b300.png)
*Terminal flashing output*


### 11. Verify Root
Open Magisk. If the version number is displayed, Magisk is successfully active!

![Magisk successfully verified](/images/33e75ff09dd601b.jpg)
*Magisk successfully verified*


:::tip[Recovery Instructions (Emergency Restore)]
If your phone fails to boot or gets stuck in a bootloop after flashing:
1. Power off and hold **Power + Volume Down** to return to Fastboot mode.
2. Flash your unmodified stock backup image:
   ```bash
   fastboot flash boot boot.img
   ```
3. Run `fastboot reboot`. Normal startup will be restored immediately with no data loss.
:::
