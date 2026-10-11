---
title: "Realme Unlock Bootloader (MediaTek)"
description: "Bootloader unlock guide for MediaTek-powered Realme devices."
---

:::caution[Notice]
- Applicable only to **MediaTek (MTK)** processor models.
- Unlocking will wipe all user data. Please back up your files!
:::

## Unlock Steps

1. Install the [Realme In-Depth Test App](/magisk/unlock/realme-app) and apply for unlock permissions.

![Applying in Deep Testing App](/images/1ab214c7c86f463.jpg)
*Applying in Deep Testing App*

2. Enable **Developer Options**, **OEM Unlocking**, and **USB Debugging** in system settings.

![Developer Options](/images/ace62ba072e5a16.jpg)
*Developer Options*


![OEM Unlock and USB Debugging](/images/7e9abe434cef586.jpg)
*OEM Unlock and USB Debugging*

3. Download `adb-fastboot` on PC and extract.

![Extracting adb-fastboot](/images/02e5e0821c8cb55.png)
*Extracting adb-fastboot*

4. Once approved in the app, tap **Start In-Depth Test** to enter Fastboot mode.

![Starting In-Depth Test](/images/afc7c22b4cfcaaa.jpg)
*Starting In-Depth Test*

5. Connect phone to PC, open terminal, and run:
   ```bash
   fastboot flashing unlock
   ```
6. Select **UNLOCK THE BOOTLOADER** using the volume buttons, and press Power to confirm.

![Confirming unlock](/images/5387ad8e59b4bf8.png)
*Confirming unlock*
