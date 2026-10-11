---
title: "OnePlus Unlock Bootloader (MediaTek)"
description: "Bootloader unlock guide for MediaTek-powered OnePlus devices."
---

:::caution[Notice]
- Applicable only to **MediaTek (MTK)** processor models.
- Unlocking the Bootloader will wipe all user data. Please back up your data!
:::

## Unlock Steps

### 1. Install PC Drivers
Install MediaTek USB VCOM / CDC drivers or official [Google USB Driver](https://developer.android.com/studio/run/win-usb).

### 2. Enable Developer Options & OEM Unlocking
1. Go to **Settings – About Phone – Version Information**, and tap **Build Number** 7 times.

![Enabling Developer Options](/images/ace62ba072e5a16.jpg)
*Enabling Developer Options*

2. Go to **Settings – Additional Settings – Developer Options**.
3. Enable **OEM Unlocking** and **USB Debugging**.

![Enabling OEM Unlocking and USB Debugging](/images/7e9abe434cef586.jpg)
*Enabling OEM Unlocking and USB Debugging*


### 3. Download Platform-Tools
Download official [Google Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools).

![Extracting adb-fastboot](/images/02e5e0821c8cb55.png)
*Extracting adb-fastboot*


### 4. Reboot to Bootloader
Connect phone to PC, open command prompt, and run:

```bash
adb reboot bootloader
```

### 5. Execute Unlock Command
In fastboot mode, run:

```bash
fastboot flashing unlock
```

![Terminal unlock command](/images/dc7c080f922cfa6.png)
*Terminal unlock command*


### 6. Confirm on Device Screen
Use Volume Up/Down keys to navigate to **UNLOCK THE BOOTLOADER**, and press the Power key to confirm. The device will wipe user data and reboot with an unlocked Bootloader.

![Confirming unlock on screen](/images/5387ad8e59b4bf8.png)
*Confirming unlock on screen*

---

## Next Steps

Now that your bootloader is unlocked, install Magisk:
- For devices on Android 12 or earlier: [OnePlus boot.img Guide](/magisk/install/oneplus-boot)
- For devices on OxygenOS 13+ (Android 13+): [OnePlus init_boot Guide](/magisk/install/oneplus-init-boot)
