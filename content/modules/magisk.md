---
id: "magisk"
title: "Magisk: The Universal Systemless Root Solution for Android"
sidebarTitle: "Magisk"
description: "The core open-source Android root solution providing systemless modifications, Zygisk API, and root access management."
category: "root-management"
tier: 1
searchQueries:
  - "how to root android with magisk"
  - "magisk official apk download"
  - "install magisk via boot.img patching"
  - "what is magisk zygisk"
  - "magisk vs kernelsu vs apatch"
prerequisites:
  - "Unlocked bootloader"
  - "Stock `boot.img` or `init_boot.img` corresponding to exact firmware build"
  - "Platform tools (fastboot / adb)"
conflicts:
  - "SuperSU (obsolete)"
  - "Directly flashing KingRoot or legacy system-modifying root apps"
configPaths:
  - "/data/adb/magisk.db"
  - "/data/adb/modules/"
  - "/data/adb/post-fs-data.d/"
  - "/data/adb/service.d/"
features:
  - "Systemless root interface with granular per-app superuser permissions"
  - "Magic Mount systemless filesystem overlay (/system partition unmodified)"
  - "Built-in Zygisk runtime enabling process code injection directly into the Zygote process"
  - "Resetprop engine allowing system properties modification (ro.* props)"
  - "DenyList mechanism to conceal root environment from selected processes"
faq:
  - question: "Does installing Magisk trip Samsung Knox or Google Play Integrity?"
    answer: "Unlocking the bootloader trips Samsung Knox hardware fuses (0x1) permanently. For Google Play Integrity, Magisk provides systemless isolation and Zygisk DenyList, but additional helper modules (such as PlayIntegrityFork or TrickyStore) are required to satisfy modern MEETS_DEVICE or MEETS_STRONG attestation checks."
  - question: "Should I patch boot.img or init_boot.img?"
    answer: "On devices launched with Android 13 or newer (Generic Kernel Image / GKI), Magisk must be installed into init_boot.img. On devices launched with Android 12 or older, patch the standard boot.img."
---

## Overview

Created by John Wu (@topjohnwu), **Magisk** is the defacto standard rooting platform for modern Android devices. Unlike legacy rooting utilities that physically modified the `/system` block device, Magisk operates **systemlessly**. It intercepts the Linux boot sequence by modifying the kernel ramdisk (`init`), pivoting the root filesystem into an overlay, and mounting custom binaries and module assets on top of existing system paths.

Magisk includes:
1. **`magiskd`**: The background root daemon handling superuser privilege escalation.
2. **Magisk App**: The management application for controlling root prompts, module installations, and DenyList targets.
3. **Zygisk**: A dynamic injection framework that hooks into Android's core Zygote process to permit module injection before application processes are spawned.
4. **Magic Mount**: A mechanism using Linux mount namespaces and overlayfs to replace or inject system files without altering read-only system partitions.

---

## Technical Architecture & How It Works

### The Systemless Hook Sequence

When an Android device powers on:
1. **Bootloader Verification**: The bootloader verifies the signed kernel and ramdisk. With an unlocked bootloader, custom or patched ramdisks are allowed execution.
2. **Init Hijacking**: Magisk patches `init` in the boot image. Magisk inserts its own entry point before handing off execution to the standard Android `/init` binary.
3. **Early Mount & SELinux Policy Injection**: Before Android's SELinux policy is compiled and enforced, Magisk live-patches the sepolicy rules to define its own domain (`magisk`), giving root processes unrestricted capability while keeping existing system SELinux policies intact.
4. **`post-fs-data` Stage**: Once Android mounts `/data`, Magisk executes scripts located in `/data/adb/post-fs-data.d/` and triggers module `post-fs-data.sh` scripts.
5. **Magic Mount Phase**: Magisk mounts module files located in `/data/adb/modules/<id>/system` over the corresponding paths in `/system` using loop devices and tmpfs/overlayfs mounts.
6. **Zygote Forking (Zygisk)**: When `zygote` starts, Zygisk hooks into the ART runtime. For every app process forked from Zygote, Zygisk determines whether to enforce DenyList unmounting or to load module companion libraries.

---

## Prerequisites & Installation

### Step 1: Obtain the Clean Boot Image
Download the exact stock firmware matching your device's currently installed build number. Extract `boot.img` (or `init_boot.img` on devices running Android 13+).

### Step 2: Patch the Image in Magisk App
1. Install the official Magisk APK (`Magisk-v30.x.apk`) on your device.
2. Tap **Install** $\rightarrow$ **Select and Patch a File**.
3. Select your extracted `boot.img` or `init_boot.img`.
4. Magisk will output `magisk_patched_[random_strings].img` to your `Download` folder.

### Step 3: Flash via Fastboot
Transfer the patched image to your PC and reboot your device into Fastboot mode:
```bash
# If device uses boot.img:
fastboot flash boot magisk_patched.img

# If device uses init_boot.img (Android 13+):
fastboot flash init_boot magisk_patched.img

# Reboot device
fastboot reboot
```

---

## Configuration & Practical Usage

### Managing Root Permissions
All superuser authorizations are stored inside the SQLite database at `/data/adb/magisk.db`. Root permissions can be managed from the Magisk App UI under the **Superuser** tab, or via command-line:
```bash
# Verify root environment
su -c "magisk -v"

# Check active mount status
su -c "magisk --mount-features"
```

### Enabling Zygisk & DenyList
1. Open **Magisk App** $\rightarrow$ tap the **Settings** gear icon.
2. Toggle **Zygisk** to ON.
3. Toggle **Enforce DenyList** to OFF (if using third-party hiders like Shamiko or Zygisk Assistant) or ON if relying strictly on native Magisk hiding.
4. Tap **Configure DenyList** to select target apps (e.g. banking apps, Google Play Services).

---

## Common Issues & Troubleshooting

### Bootloop Recovery
If a faulty module prevents the system from booting:
- **Fastboot Safe Mode**: On devices supporting hardware key combos during boot, hold Volume Down during the boot animation to enter Android Safe Mode; Magisk detects this and disables all modules automatically.
- **ADB Recovery Mode**: If ADB is accessible in recovery or early boot:
  ```bash
  adb wait-for-device
  adb shell "touch /data/adb/modules/.disable_magisk"
  adb reboot
  ```
- **Custom Recovery (TWRP / OrangeFox)**: Open the built-in file manager, navigate to `/data/adb/modules/`, and delete the folder of the offending module.
