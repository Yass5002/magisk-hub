---
id: "playintegrityfork"
title: "PlayIntegrityFork: Pass MEETS_DEVICE & Fix Attestation on Android 13-15"
sidebarTitle: "PlayIntegrityFork"
description: "Advanced fork of PlayIntegrityFix allowing custom pif.json build prop spoofing, spoofing field overrides, and passing Google Play Integrity device checks."
category: "root-management"
tier: 1
searchQueries:
  - "play integrity fork vs fix"
  - "how to pass device integrity magisk"
  - "custom pif.json guide"
  - "fix banking apps magisk play integrity"
  - "osm0sis playintegrityfork"
prerequisites:
  - "Magisk 26.0+ (with Zygisk enabled), KernelSU with Zygisk Next, or APatch with Zygisk Next"
  - "Google Play Store and Google Play Services (GMS) installed"
conflicts:
  - "KOWX712/PlayIntegrityFix (cannot run simultaneously)"
  - "MagiskHidePropsConf (obsolete and actively harmful to attestation)"
configPaths:
  - "/data/adb/pif.json"
  - "/data/adb/modules/playintegrityfork/"
features:
  - "Spoofs device properties specifically within Google Play Services DroidGuard/attestation processes"
  - "Dynamic pif.json parsing allowing custom un-banned device fingerprints without reinstalling the module"
  - "Custom field spoofing: selectively override PRODUCT, DEVICE, MANUFACTURER, BRAND, MODEL, FINGERPRINT, SECURITY_PATCH, and FIRST_API_LEVEL"
  - "Zero interference with non-GMS application processes"
faq:
  - question: "Why did my Play Integrity verdict revert from PASS to FAIL after a few days?"
    answer: "Google regularly blacklists public build fingerprints used in open-source modules once detection systems flag repeated hardware attestation mismatches. To restore MEETS_DEVICE_INTEGRITY, generate or extract a clean, non-public pif.json fingerprint from an unbanned certified device and place it in /data/adb/pif.json."
  - question: "Does PlayIntegrityFork give MEETS_STRONG_INTEGRITY?"
    answer: "No. MEETS_STRONG_INTEGRITY requires cryptographic proof signed by a physical Hardware Security Module / Trusted Execution Environment (TEE). On an unlocked bootloader, software-level prop spoofing cannot pass strong integrity alone. You must pair this module with a hardware keybox spoofer like TrickyStore."
---

## Overview

Maintained by renowned developer **osm0sis**, **PlayIntegrityFork** is an enhanced, highly flexible fork of the original PlayIntegrityFix engine. When an unlocked bootloader is detected, Google Play Services initiates cryptographic hardware-backed attestation (Key Attestation), immediately failing SafetyNet and Play Integrity evaluation.

PlayIntegrityFork intercepts requests made by Google's attestation process (`com.google.android.gms.unstable`), forcing the attestation client to fall back to legacy software-backed attestation. It then substitutes device identity fields with verified certified OEM build properties, satisfying Google's `MEETS_BASIC_INTEGRITY` and `MEETS_DEVICE_INTEGRITY` criteria.

---

## Technical Architecture & How It Works

### The DroidGuard Zygisk Interception

1. **Target Identification**: In Android, device integrity evaluation is orchestrated by a specialized sub-process of Google Play Services: `com.google.android.gms.unstable`.
2. **Native Library Injection**: When Zygisk initializes this process, PlayIntegrityFork injects a native companion library (`libplayintegrityfork.so`).
3. **Property Masking**: The module hooks `__system_property_get` and `__system_property_read` calls within libc. When Google Play Services queries build properties such as `ro.build.fingerprint` or `ro.product.model`, the hooked functions return values defined in `/data/adb/pif.json`.
4. **Attestation Fallback**: Android devices launched with older OS versions (typically Android 7.0 or earlier, or devices without hardware keymaster enforcement) did not mandate hardware-backed Keystore attestation. By presenting an older valid fingerprint with matching `FIRST_API_LEVEL` props, PlayIntegrityFork forces Google Play Services into software attestation mode.

---

## Prerequisites & Installation

### Step 1: Prepare Environment
1. Ensure your root solution has an active Zygisk implementation:
   - **Magisk**: Enable Zygisk in settings.
   - **KernelSU / APatch**: Install and verify **Zygisk Next** or **ReZygisk**.
2. Remove any obsolete props-spoofing modules (such as old PIF versions or MagiskHidePropsConf).

### Step 2: Flash the Module
1. Download the latest `PlayIntegrityFork-vX.zip` from releases.
2. In your root manager, go to **Modules** $\rightarrow$ **Install from Storage** $\rightarrow$ select the zip.
3. Reboot your device.

### Step 3: Clear GMS Cache
After rebooting, clear the cache and data for Google Play Services to flush cached integrity tokens:
```bash
su -c "pm clear com.google.android.gms"
su -c "killall com.google.android.gms.unstable"
```

---

## Configuration & Custom pif.json

PlayIntegrityFork includes a default fallback fingerprint, but using a custom `pif.json` is strongly recommended to prevent ban waves.

Create or edit `/data/adb/pif.json`:
```json
{
  "PRODUCT": "marlin",
  "DEVICE": "marlin",
  "MANUFACTURER": "Google",
  "BRAND": "google",
  "MODEL": "Pixel XL",
  "FINGERPRINT": "google/marlin/marlin:7.1.2/NJH47F/4146048:user/release-keys",
  "SECURITY_PATCH": "2017-08-05",
  "FIRST_API_LEVEL": "25"
}
```

Whenever you update `/data/adb/pif.json`, force-restart the unstable GMS process to apply new props immediately:
```bash
su -c "killall -9 com.google.android.gms.unstable"
```

---

## Common Issues & Troubleshooting

- **Banking App Still Detects Root**:
  Passing Play Integrity does not automatically conceal root binaries. Ensure your banking app is added to Magisk's **DenyList** or configured in **Shamiko / Zygisk Assistant**, and verify that the app does not detect the Magisk app package name (enable "Hide the Magisk app").
- **Play Store Shows 'Device is not certified'**:
  After passing `MEETS_DEVICE_INTEGRITY`, the Play Store app caches certification status for up to 24 hours. Go to **Settings** $\rightarrow$ **Apps** $\rightarrow$ **Google Play Store** $\rightarrow$ **Storage** $\rightarrow$ **Clear Storage**, then reboot.
