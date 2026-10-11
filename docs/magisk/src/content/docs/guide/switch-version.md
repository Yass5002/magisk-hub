---
title: "Switching Magisk Versions"
description: "How to switch between different versions, Alpha, Delta, or upgrade/downgrade Magisk."
---

:::note[Applicable Scenarios]
Use this method to switch between different versions of Magisk (e.g., downgrading, upgrading, or switching between Official, Alpha, and Kitsune Mask / Delta variants).
:::

## Steps

1. **Verify Existing Root:** Your device must already have Magisk installed and running.
2. **Download Target APK:** Download the desired Magisk installer `.apk` (older version, Alpha, Delta, etc.).
3. **Rename APK to ZIP:** Change the extension of `Magisk.apk` to `Magisk.zip`.
4. **Copy to Phone:** Move `Magisk.zip` into your phone's `Download` directory.
5. **Flash as Module:**
   - Open Magisk app.
   - Go to **Modules** tab.
   - Tap **Install from storage**.
   - Select `Magisk.zip` to flash it.
   - Tap **Reboot**.

![Flashing Magisk.zip through Magisk Modules](/images/46a9925b02fd0ea.jpg)
*Flashing Magisk.zip through Magisk Modules*

6. **Replace Manager App:** After the phone boots up, uninstall the previous Magisk Manager app, then install the `.apk` corresponding to the version you just flashed. Version switching is complete!
