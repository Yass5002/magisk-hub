---
id: "knoxpatch"
title: "KnoxPatch: Restore Samsung Knox Features on Rooted One UI"
sidebarTitle: "KnoxPatch"
description: "Comprehensive patcher restoring broken Samsung Knox features including Secure Folder, Samsung Pass, and Samsung Health on rooted Galaxy devices."
category: "system-environment"
tier: 1
searchQueries:
  - "knoxpatch magisk module"
  - "fix secure folder rooted samsung"
  - "samsung pass root fix one ui"
  - "salvogiangri knoxpatch guide"
  - "knox 0x1 bypass samsung health"
prerequisites:
  - "Samsung Galaxy device running official One UI firmware (Android 9 through Android 15)"
  - "Root access (Magisk, KernelSU, or APatch) with LSPosed or Vector framework active"
conflicts:
  - "Generic AOSP / non-Samsung ROMs (only functions on Samsung One UI software)"
configPaths:
  - "/data/adb/modules/knoxpatch/"
  - "/data/user/0/io.github.salvogiangri.knoxpatch/"
features:
  - "Restores broken Samsung proprietary services: Secure Folder, Samsung Pass, Private Share, Samsung Health"
  - "Patches Knox security daemons (`keystorage`, `sem_personamanager`) in-memory"
  - "Dynamic WSM hook injection requiring zero manual system partition decompression or deodexing"
  - "Companion app to configure individual app patches and diagnostics"
faq:
  - question: "Can KnoxPatch reset my physical Knox fuse from 0x1 back to 0x0?"
    answer: "No. The Samsung Knox warranty fuse is a physical e-fuse (hardware OTP - One-Time Programmable fuse) blown on the motherboard during bootloader unlock. KnoxPatch does not alter the hardware fuse; instead, it hooks the system framework and Knox APIs to lie to Samsung apps, telling them the device is intact and Knox verification succeeded."
  - question: "Why does Secure Folder fail to set up after flashing KnoxPatch?"
    answer: "Secure Folder requires both KnoxPatch (the Xposed module) and the KnoxPatch Enhancer (the Magisk module companion). The Enhancer patches early-boot Knox daemons, while the Xposed component handles the runtime framework. Ensure both are installed and active."
---

## Overview

Developed by **salvogiangri**, **KnoxPatch** is an essential utility for anyone rooting a Samsung Galaxy smartphone or tablet running One UI.

When the bootloader of a Samsung device is unlocked, hardware security logic blows the Knox e-fuse (`0x1`). In response, Samsung software permanently disables proprietary security apps: **Secure Folder**, **Samsung Pass**, **Samsung Health**, **Secure Wi-Fi**, and **Private Share**. KnoxPatch systematically restores functionality to these apps by hooking into Samsung's proprietary framework services and spoofing the security integrity checks.

---

## Technical Architecture & How It Works

### Samsung Framework & Daemon Interception

1. **Knox Daemon Patching (Enhancer Module)**:
   - Early in the boot process, Samsung's proprietary security daemons (`sec_keystorage`, `ss_conn_daemon`) verify the Knox warranty state via kernel sysfs.
   - The KnoxPatch Enhancer module injects library patches to bypass these daemon checks, ensuring credential vaults initialize properly.
2. **Framework Service Hooking (Xposed Component)**:
   - When Secure Folder or Samsung Pass launches, they call `SemPersonaManager` and `KnoxVpnEngineService`.
   - KnoxPatch hooks these APIs in memory, returning `STATUS_SUCCESS` and spoofing the Knox warranty bit as `0x0`.
3. **Keystore Software Fallback**:
   - Because Samsung Pass requires hardware-backed biometric verification that Knox disables when blown, KnoxPatch redirects cryptographic signature requests to a patched software keystore, restoring seamless biometric authentication.

---

## Installation & Setup

### Step 1: Install KnoxPatch Enhancer (Root Module)
1. Download `KnoxPatch-Enhancer-vX.zip`.
2. Flash the module in **Magisk**, **KernelSU**, or **APatch**.
3. Do not reboot yet.

### Step 2: Install KnoxPatch Manager (APK)
1. Install `KnoxPatch.apk` on your device.
2. Open **Vector Manager** or **LSPosed Manager**.
3. Enable **KnoxPatch** in the module list and ensure **System Framework** is checked in its scope.
4. Reboot your phone.

### Step 3: Configure Services
1. Open the **KnoxPatch** application from your app drawer.
2. Check the status indicators: both **Xposed Module** and **KnoxPatch Enhancer** should show green checkmarks.
3. Toggle on the features you want active (Secure Folder, Samsung Pass, Samsung Health).
4. Launch Secure Folder and proceed with the standard setup wizard.
