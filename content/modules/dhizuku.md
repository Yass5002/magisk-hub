---
id: "dhizuku"
title: "Dhizuku: Share Android Device Owner (DPM) Privileges with Third-Party Apps"
sidebarTitle: "Dhizuku"
description: "Pioneering Android system service daemon by iamr0s that operates as the device's Device Owner and delegates DevicePolicyManager enterprise APIs to authorized client applications."
category: "system-utilities"
softwareType: "standalone-app"
tier: 1
searchQueries:
  - "dhizuku download apk"
  - "dhizuku device owner adb command"
  - "share device owner android"
  - "dhizuku vs shizuku"
  - "not allowed to set device owner accounts on device"
prerequisites:
  - "Android 8.0 (Oreo) through Android 15+"
  - "Activation via Root, Shizuku, or Rootless ADB Shell"
  - "No pre-existing Device Owner configured on the device"
conflicts:
  - "Existing Enterprise MDM enrollment (e.g. Microsoft Intune, VMware Workspace ONE)"
  - "Work Profile managers operating as conflicting device administrators"
configPaths:
  - "/data/system/device_owner_2.xml"
  - "com.rosan.dhizuku/.server.DhizukuDAReceiver"
features:
  - "DevicePolicyManager multiplexing: allows multiple third-party apps to access enterprise management APIs simultaneously"
  - "Silent package operations: enables client utilities (App Manager, Hail, Canta) to install, uninstall, or freeze apps without confirmation prompts"
  - "Rootless operation: fully functional on unrooted devices using ADB shell commands"
  - "Granular permission gating: prompts user confirmation before granting Device Owner API access to client applications"
faq:
  - question: "How does Dhizuku differ from Shizuku?"
    answer: "Shizuku shares ADB / Shell privileges (`android.permission.DUMP`, `pm`, `am`, `appops`) using an elevated system shell daemon. Dhizuku, by contrast, registers as the Android system's official **Device Owner** (`DevicePolicyManager`), exposing enterprise-grade APIs like silent app installation, background application freezing/hiding (`setApplicationHidden`), lock task mode, and status bar restrictions."
  - question: "How do I fix 'Not allowed to set the device owner because there are already some accounts on the device'?"
    answer: "Android security rules strictly forbid assigning a Device Owner if any user account is active. Go to Android **Settings -> Passwords & Accounts**, temporarily remove all Google, WhatsApp, Samsung, and cloud accounts, run the ADB command `adb shell dpm set-device-owner com.rosan.dhizuku/.server.DhizukuDAReceiver`, and then log back into your accounts."
  - question: "How can I completely remove Dhizuku without a factory reset?"
    answer: "Open Dhizuku -> Settings -> tap **Deactivate Device Owner**. Alternatively, revoke it via ADB using: `adb shell dpm remove-active-admin com.rosan.dhizuku/.server.DhizukuDAReceiver`. Once deactivated, the app can be uninstalled like any standard APK."
---

## Overview

**Dhizuku**, created by iamr0s, solves one of the oldest architectural limitations of the Android operating system: **Device Owner exclusivity**.

Under the Android Enterprise framework (`android.app.admin.DevicePolicyManager`), a single application can be designated as the system's "Device Owner". The Device Owner holds extraordinary administrative powers over the device:
- Silently installing and uninstalling applications without user confirmation
- Instantly freezing (hiding) background packages without battery drain
- Restricting network policies, camera usage, and notification banners
- Managing hardware keys and kiosk mode

Because Android enforces a strict one-owner rule, users historically had to choose between one specific freeze utility (like Island or Ice Box) or lock themselves out of other tools. Dhizuku acts as a **Device Owner Proxy Server**: it claims the single Device Owner slot and exposes a clean Binder IPC API to allow authorized client apps (Hail, Canta, App Manager, Install with Options) to safely share those administrative privileges.

---

## Technical Architecture & Binder Proxying

- **Android System Framework**: Hosts `android.app.admin.DevicePolicyManager` (DPM) providing enterprise-grade administrative APIs.
- **Dhizuku Server**:
  - Holds official Device Owner status via `DeviceAdminReceiver`.
  - Enforces per-application permission tokens and access policies.
  - Multiplexes IPC Binder requests between unprivileged clients and DPM.
- **Delegated Client Applications**:
  - **Hail**: Freezes, hides, or suspends apps using Device Policy Manager APIs without root.
  - **App Manager / Canta**: Manages user policies and system package lifecycles cleanly.

---

## Activation Methods

Dhizuku can be activated through three distinct vectors depending on your device setup:

### Method 1: Root Activation (Magisk, KernelSU, APatch)
If your device is rooted, open Dhizuku, select **Root Activation**, and tap Grant when your root manager dialog appears. Dhizuku automatically writes its component to `/data/system/device_owner_2.xml` and reloads policy caches.

### Method 2: Shizuku Activation
If you already run Shizuku:
1. Open Dhizuku.
2. Select **Activate via Shizuku**.
3. Authorize the Shizuku permission request.

### Method 3: Rootless ADB Shell (No Root Required)
For completely stock devices:
1. Enable **Developer Options** and **USB Debugging** on your phone.
2. Connect your device to a computer with Android SDK Platform-Tools.
3. Open a terminal and run:
   ```bash
   adb shell dpm set-device-owner com.rosan.dhizuku/.server.DhizukuDAReceiver
   ```
4. If successful, your terminal displays `Success: Device owner set to package...`.

> **Note**: If you receive `java.lang.IllegalStateException: Not allowed to set the device owner because there are already some accounts on the device`, you must temporarily remove all Google, Telegram, and corporate accounts under **Settings -> Passwords & Accounts**, run the command, and re-add them afterwards.

---

## Ecosystem Integration

Once activated, Dhizuku powers a rich suite of rootless open-source utilities:
- **Hail**: Instantly freezes bloatware and background games using `DevicePolicyManager.setApplicationHidden()`.
- **Canta**: Deep debloater that safely removes OEM system packages without bootloop risk.
- **Install with Options**: Enables silent downgrade, bypass of SDK version limits, and split APK installations without manual tapping.
