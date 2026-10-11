---
title: "Google Pixel Unlock Bootloader"
description: "Official tutorial for unlocking Bootloader on Google Pixel devices."
---

:::caution[Notice]
- Unlocking the Bootloader will completely wipe your Pixel device.
- Ensure OEM Unlocking is not grayed out (carrier-locked devices like Verizon cannot be unlocked).
:::

## Unlock Steps

### 1. Enable OEM Unlocking & USB Debugging
1. Go to **Settings – About Phone**, tap **Build Number** 7 times.

![Enabling Developer Options on Pixel](/images/4bd0098db0d027f.png)
*Enabling Developer Options on Pixel*

2. Go to **Settings – System – Developer Options**.
3. Toggle on **OEM Unlocking** and **USB Debugging**.

![Pixel OEM Unlock and USB Debugging toggles](/images/d16f64ae0ceedff.jpg)
*Pixel OEM Unlock and USB Debugging toggles*


### 2. Enter Fastboot Mode
Download official [Google Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools), connect phone, and run:

```bash
adb reboot bootloader
```

![Extracting adb-fastboot](/images/02e5e0821c8cb55.png)
*Extracting adb-fastboot*


*(Or power off phone, press and hold **Power + Volume Down**).*

### 3. Execute Unlock Command
In fastboot terminal, run:

```bash
fastboot flashing unlock
```

![Fastboot flashing unlock command](/images/b9113bf5d189032.jpg)
*Fastboot flashing unlock command*


### 4. Confirm on Screen
Use the Volume keys to select **Unlock the bootloader**, and press the Power button to confirm.

![Confirming unlock on Pixel screen](/images/00cd77a7a0654fe.png)
*Confirming unlock on Pixel screen*


The Pixel will format its data partition and reboot unlocked!

![Pixel unlocked boot screen](/images/1c68cd9ca0b27ea.png)
*Pixel unlocked boot screen*

---

## Next Steps

Now that your Pixel bootloader is unlocked, install Magisk:
- For Pixel 6 and earlier: [Google Pixel boot.img Guide](/magisk/install/pixel-boot)
- For Pixel 7, 8, 9+: [Google Pixel init_boot Guide](/magisk/install/pixel-init-boot)
