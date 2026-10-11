---
title: "Motorola Unlock Bootloader"
description: "Official tutorial for unlocking Bootloader on Motorola devices via official unlock key."
---

:::caution[Notice]
- Unlocking the Bootloader will wipe all device data. Back up critical data first!
:::

## Unlock Steps

### 1. Enable OEM Unlocking & USB Debugging
1. Go to **Settings – About Phone**, tap **Build Number** 7 times to enable Developer Options.

![Enabling Developer Options on Motorola](/images/e955f264cc0fd0f.png)
*Enabling Developer Options on Motorola*

2. Go to **Settings – System – Developer Options**.
3. Turn on **OEM Unlocking** and **USB Debugging**.

![OEM Unlocking and USB Debugging toggles](/images/ab3bd77857c21f0.png)
*OEM Unlocking and USB Debugging toggles*


### 2. Install Motorola Drivers & Platform-Tools
Download and install:
- [Motorola Official USB Drivers](https://motorola-global-portal.custhelp.com/app/answers/detail/a_id/88481)
- Official [Google Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)
- [7-Zip](https://www.7-zip.org/) for extracting archives

![adb-fastboot toolkit](/images/619f5d15df082ea.jpg)
*adb-fastboot toolkit*


### 3. Reboot to Bootloader
Connect phone to PC in File Transfer mode. In terminal, run:

```bash
adb reboot bootloader
```

### 4. Retrieve Device Unlock Data
In Fastboot mode, run:

```bash
fastboot oem get_unlock_data
```

The terminal will print 5 lines of hex strings:

![Retrieving unlock data in Fastboot](/images/366986d28396357.jpg)
*Retrieving unlock data in Fastboot*


Combine all 5 lines into a single continuous string without spaces or `(bootloader)`.

### 5. Request Unlock Key from Motorola Portal
1. Go to the [Official Motorola Bootloader Unlock Portal](https://motorola-global-portal.custhelp.com/app/standalone/bootloader/unlock-your-device-b).
2. Sign in with your Motorola account or Google account.
3. Paste the combined unlock data string into Field #6, and click **Can my device be unlocked?**.

![Pasting unlock data into portal](/images/961535f1ee027e2.png)
*Pasting unlock data into portal*

4. Agree to the terms and click **Request Unlock Key**.

![Requesting unlock key](/images/f314414643b68fc.png)
*Requesting unlock key*

5. Motorola will email a 20-character UNIQUE UNLOCK KEY to your email address.

![Receiving unlock key via email](/images/42158f4a80af32e.png)
*Receiving unlock key via email*


### 6. Execute Unlock Command
Return to your PC terminal and run:

```bash
fastboot oem unlock <YOUR_20_CHARACTER_KEY>
```

![Executing fastboot oem unlock command](/images/5b2cfb304e4ed09.png)
*Executing fastboot oem unlock command*


Confirm the warning prompt on device. The phone will display an unlocked warning and reboot!

![Bootloader successfully unlocked](/images/9baf18c0766954c.png)
*Bootloader successfully unlocked*

---

## Next Steps

Now that your Motorola bootloader is unlocked, proceed with Magisk installation:
- For devices on Android 12 or earlier: [Motorola boot.img Guide](/magisk/install/motorola-boot)
- For devices on Android 13+: [Motorola init_boot Guide](/magisk/install/motorola-init-boot)
