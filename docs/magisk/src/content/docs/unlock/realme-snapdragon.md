---
title: "Realme Unlock Bootloader (Snapdragon)"
description: "Bootloader unlock guide for Snapdragon-powered Realme devices."
---

:::caution[Notice]
- Applicable only to **Qualcomm Snapdragon** processor models.
- Unlocking will wipe all user data. Please back up important files!
:::

## Unlock Steps

### 1. Apply via In-Depth Test App
Install the [Realme In-Depth Test App](/magisk/unlock/realme-app), tap **Apply for In-Depth Test**, submit application, and await review approval.

![Submitting application in Realme Deep Testing app](/images/1ab214c7c86f463.jpg)
*Submitting application in Realme Deep Testing app*


### 2. Install PC Drivers
Install fastboot drivers via [Google USB Driver](https://developer.android.com/studio/run/win-usb).

### 3. Enable OEM Unlocking & USB Debugging
Once approved:
1. Tap Build Number 7 times in **Settings – About Phone** to unlock Developer Options.

![Enabling Developer Options](/images/ace62ba072e5a16.jpg)
*Enabling Developer Options*

2. Go to **Settings – Additional Settings – Developer Options**.
3. Enable **OEM Unlocking** and **USB Debugging**.

![Enabling OEM Unlocking and USB Debugging](/images/7e9abe434cef586.jpg)
*Enabling OEM Unlocking and USB Debugging*


### 4. Download Platform-Tools on PC
Download official [Google Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools).

![Extracting adb-fastboot](/images/02e5e0821c8cb55.png)
*Extracting adb-fastboot*


### 5. Start In-Depth Test
Open the Deep Testing app, check review status, and tap **Start In-Depth Test**. The phone will reboot into Fastboot mode.

![Starting in-depth testing from app](/images/afc7c22b4cfcaaa.jpg)
*Starting in-depth testing from app*


### 6. Run Unlock Command
Connect the phone to PC via USB. In your PC's `platform-tools` folder, open terminal and execute:

```bash
fastboot flashing unlock
```

### 7. Confirm on Device
On the phone screen, navigate with Volume keys to **UNLOCK THE BOOTLOADER** and press Power to confirm.

![Selecting UNLOCK THE BOOTLOADER on screen](/images/c6abc27255c1a09.jpg)
*Selecting UNLOCK THE BOOTLOADER on screen*


### 8. Finish
The phone wipes data and restarts unlocked!

---

## Next Steps

Now that your bootloader is unlocked, install Magisk:
- For Realme UI 3 or earlier: [Realme boot.img Guide](/magisk/install/realme-boot)
- For Realme UI 4+ / Android 13+: [Realme init_boot Guide](/magisk/install/realme-init-boot)
