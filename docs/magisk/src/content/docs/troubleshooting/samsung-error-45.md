---
title: "Samsung One UI 5 / 6 Magisk Boot Error -45 Fix"
description: "How to fix the Samsung activation wizard error -45 preventing desktop access after flashing Magisk."
---

When rooting China-region (CHC) or specific regional Samsung Galaxy firmware on One UI 5 or One UI 6, the system setup wizard may throw error `-45` after first boot and refuse to load the home screen desktop.


![Samsung One UI error -45 screen](/images/38daadb56baccb7.png)
*Samsung One UI error -45 screen*


## Recovery Procedure

### 1. Bypass to Browser via TalkBack
1. On the setup wizard error screen, enable Accessibility: tap **Accessibility -> TalkBack -> Settings -> Braille keyboard -> Set up braille keyboard -> GBoard**.
2. Tap the hyperlink inside GBoard settings to force-open Samsung Internet Browser.
3. In the browser address bar, enter the download URL for the activation patch:
   `the official module repository or community mirror`

### 2. Install Magisk
1. Download and install the Magisk APK.
2. Open Magisk, allow initial setup, tap **OK**, and let the device reboot.

### 3. Install Activation Bypass Module
1. After reboot, repeat Step 1 to enter the browser.
2. Download the `Samsung-Activation-Bypass` zip module.
3. Open Magisk, go to **Modules -> Install from storage**, select the downloaded zip, flash it, and reboot.
4. The system will now bypass verification and boot straight into the One UI desktop with root intact!
