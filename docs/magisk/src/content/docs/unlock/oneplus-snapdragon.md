---
title: "OnePlus Unlock Bootloader (Snapdragon)"
description: "Bootloader unlock guide for Snapdragon-powered OnePlus devices."
---

:::caution[Notice]
- Applicable only to **Qualcomm Snapdragon** processor models.
- Unlocking the Bootloader will wipe all user data. Please back up important files!
- Devices shipping with ColorOS 14+ / 15+ may require applying through the [OnePlus In-Depth Test App](/magisk/unlock/oneplus-app).
:::

## Unlock Steps

### 1. Install PC Drivers
Install ADB and Fastboot drivers via the [Google USB Driver](https://developer.android.com/studio/run/win-usb) or vendor drivers.

### 2. Enable Developer Options
Go to **Settings – About Phone – Version Information**, and tap **Build Number** 7 times rapidly to activate Developer Options.

![Enabling Developer Options](/images/ace62ba072e5a16.jpg)
*Enabling Developer Options*


### 3. Enable OEM Unlocking & USB Debugging
Go to **Settings – Additional Settings (System Settings) – Developer Options**, and toggle on:
- **OEM Unlocking**
- **USB Debugging**

![Enabling OEM Unlocking and USB Debugging](/images/7e9abe434cef586.jpg)
*Enabling OEM Unlocking and USB Debugging*


### 4. Download Platform-Tools on PC
Download the official [Google Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools) and extract using [7-Zip](https://www.7-zip.org/).

![Extracting adb-fastboot](/images/02e5e0821c8cb55.png)
*Extracting adb-fastboot*


### 5. Reboot to Bootloader
Connect your phone to PC in **File Transfer** mode. In your command terminal inside the `platform-tools` directory, run:

```bash
adb reboot bootloader
```

### 6. Run Unlock Command
Once the phone is on the Fastboot screen, run:

```bash
fastboot flashing unlock
```

![Running fastboot flashing unlock command](/images/b9113bf5d189032.jpg)
*Running fastboot flashing unlock command*


### 7. Confirm on Phone
On your phone's screen, use the **Volume Keys** to select **UNLOCK THE BOOTLOADER**, then press the **Power Key** to confirm.

![Selecting UNLOCK THE BOOTLOADER on screen](/images/c6abc27255c1a09.jpg)
*Selecting UNLOCK THE BOOTLOADER on screen*


### 8. Boot & Finish
When the phone reboots, an orange/yellow boot warning screen confirms that the Bootloader is unlocked!

---

## Next Steps

Now that your bootloader is unlocked, install Magisk:
- For devices on Android 12 or earlier: [OnePlus boot.img Guide](/magisk/install/oneplus-boot)
- For devices on OxygenOS 13+ (Android 13+): [OnePlus init_boot Guide](/magisk/install/oneplus-init-boot)
