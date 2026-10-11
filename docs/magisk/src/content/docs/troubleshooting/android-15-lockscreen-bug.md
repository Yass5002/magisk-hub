---
title: "Android 15 Post-Unlock Lock Screen & App Install Bug"
description: "Fix the issue where lock screen PIN/passwords cannot be set and APKs cannot be installed on Android 15 after BL unlock."
---

On Android 15, performing a **Factory Reset (Format Data)** or **Bootloader Unlock** may cause a bug where you **cannot set a lock screen password or PIN**, and third-party apps fail to install.

## Root Cause: Google FRP (Factory Reset Protection) Lock
If you perform a factory reset without logging out of your Google account beforehand, Android 15's Factory Reset Protection (FRP) partition gets locked in an unauthenticated state, blocking credential storage and package manager write permissions.

---

## Solutions

### Method 1: Re-authenticate Google Account (Recommended)
1. Go to **Settings – Google Services** and toggle on Google Play Services.
2. Connect your phone to Wi-Fi with internet access (use a local proxy if Google is blocked in your network).
3. Log in with the **same Google account** originally on the device.
4. Once verified, credential storage unlocks, and lock screen passwords and APK installations immediately function normally.

### Method 2: Erase FRP Partition (Requires Unlocked Bootloader)
If you cannot log into the previous Google account:
1. Connect phone in Fastboot mode.
2. In PC terminal, erase the FRP partition:
   ```bash
   fastboot erase frp
   ```
3. Reboot phone:
   ```bash
   fastboot reboot
   ```
4. The credential storage lock will be cleared.
