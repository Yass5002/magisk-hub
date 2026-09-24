---
id: "device-faker"
title: "Device Faker: Global & Per-App Hardware Identity Masking"
sidebarTitle: "Device Faker"
description: "Comprehensive privacy and anti-fingerprinting module that spoofs IMEI, MAC addresses, Android ID, and hardware serials on rooted devices."
category: "security-certificates"
tier: 1
searchQueries:
  - "device faker magisk module"
  - "spoof imei android id rooted android"
  - "seyud device faker guide"
  - "anti fingerprinting rooted phone"
  - "change device identifiers android 14"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "LSPosed or Vector framework active"
conflicts:
  - "Other Xposed-based identifier spoofers running concurrently"
configPaths:
  - "/data/adb/modules/device_faker/"
  - "/data/user/0/com.seyud.devicefaker/"
features:
  - "Spoofs IMEI, MEID, Serial Number, IMSI, and SIM Operator credentials"
  - "Masks MAC addresses (Wi-Fi and Bluetooth) and hardware sensor parameters"
  - "Randomizes Android ID (`Settings.Secure.ANDROID_ID`) per-app or globally"
  - "Generates real-world OEM hardware fingerprints from hundreds of pre-configured device templates"
faq:
  - question: "Does Device Faker permanently modify my phone's IMEI in hardware?"
    answer: "No. Modifying hardware baseband NVRAM/EFS partitions is illegal in many jurisdictions and can permanently destroy cellular connectivity. Device Faker operates purely in memory at the Android OS framework layer; apps querying telephony APIs receive spoofed strings, while your actual cellular hardware continues functioning normally."
  - question: "How do I randomize my identity for a single app?"
    answer: "Open the Device Faker companion app, select the target application, and choose 'Randomize Profile' or pick a specific OEM preset (e.g. Pixel 8 Pro, Galaxy S24 Ultra). Only that app will see the spoofed parameters."
---

## Overview

Developed by **Seyud**, **Device Faker** is an advanced privacy and anti-fingerprinting framework for rooted Android devices.

Advertising networks, gaming companies, and fraud prevention engines create persistent hardware fingerprints of your device by querying combinations of: **IMEI**, **Android ID**, **Wi-Fi MAC**, **Bluetooth MAC**, **CPU Serial**, and **Build Display IDs**. Even if you wipe app data or change IP addresses, these identifiers permanently link your activity. Device Faker intercepts these system queries, supplying randomized or realistic synthetic profiles.

---

## Technical Architecture & How It Works

### Framework API Interception

1. **TelephonyManager Hooks**: Intercepts `getDeviceId()`, `getImei()`, `getMeid()`, and `getSubscriberId()`, returning configured or randomized 15-digit Luhn-validated IMEI strings.
2. **Settings.Secure Provider**: Hooks `Settings.Secure.getString(contentResolver, "android_id")`, substituting a unique 64-bit hexadecimal string per target app.
3. **WifiInfo & BluetoothAdapter**: Intercepts `getMacAddress()`, returning randomized MAC addresses formatted to valid IEEE OUI standards.
4. **Build Property Cloaking**: Intercepts `android.os.Build` static reflection queries (`Build.SERIAL`, `Build.MODEL`, `Build.MANUFACTURER`), ensuring all hardware strings match the selected device preset.

---

## Installation & Setup

1. Open **Vector Manager** or **LSPosed Manager**.
2. Install `DeviceFaker.apk`.
3. Enable **Device Faker** in the module list, checking **System Framework** and your target applications in scope.
4. Reboot your phone.
5. Launch **Device Faker** from your app drawer to manage device profiles and randomize hardware fingerprints.
