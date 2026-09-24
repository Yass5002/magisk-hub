---
id: "shamiko"
title: "Shamiko: High-Stealth Zygisk Root & Mount Hiding Module"
sidebarTitle: "Shamiko"
description: "The premier closed-source root-hiding module developed by the LSPosed team to completely conceal Magisk, KernelSU, and root traces from detection mechanisms."
category: "root-management"
tier: 1
searchQueries:
  - "shamiko magisk module download"
  - "how to install shamiko"
  - "shamiko whitelist mode guide"
  - "shamiko vs magisk denylist"
  - "hide root banking apps shamiko"
prerequisites:
  - "Magisk 26.0+ with Zygisk enabled, KernelSU with Zygisk Next, or APatch with Zygisk Next"
  - "Enforce DenyList disabled in Magisk settings (Shamiko reads the list directly)"
conflicts:
  - "Enforce DenyList enabled simultaneously (creates hook conflicts)"
configPaths:
  - "/data/adb/shamiko/whitelist"
  - "/data/adb/modules/shamiko/"
features:
  - "Deep root environment concealment (hides su binaries, magisk mount points, and modified init processes)"
  - "Supports Blacklist mode (hide root from selected apps) and Whitelist mode (hide root globally except for specified apps)"
  - "Advanced ptrace and memory inspection protection against anti-cheat and banking security SDKs"
  - "Bypasses detectors like Native Root Checker, Momo, and Riru/Zygisk detection probes"
faq:
  - question: "Why does Shamiko require 'Enforce DenyList' to be turned OFF in Magisk?"
    answer: "If 'Enforce DenyList' is enabled, Magisk unmounts Zygisk from the target process before any modules can execute. Turning it OFF allows Zygisk to load Shamiko into the process, allowing Shamiko to apply much more sophisticated, dynamic root masking before unhooking itself."
  - question: "How do I switch Shamiko into Whitelist mode?"
    answer: "Create an empty file named 'whitelist' in /data/adb/shamiko/: su -c 'touch /data/adb/shamiko/whitelist'. In whitelist mode, root is hidden from every app on your device except those explicitly unchecked in your DenyList/Config."
---

## Overview

Developed by the **LSPosed Developer Group**, **Shamiko** is the gold standard in stealth root concealment for modern Android devices. While Magisk's native DenyList simply unmounts Magisk's tmpfs partitions from target processes, sophisticated banking apps, anti-cheat frameworks, and security SDKs (such as Promon, DexGuard, and SecNeo) inspect kernel mount namespaces, scan `/proc/self/mountinfo`, test `/dev/pts` descriptors, and evaluate syscall timings to detect root environments.

Shamiko operates inside the Zygote process via Zygisk. It dynamically scrubs traces of superuser binaries, hides Magisk's modified loop devices, masks SELinux permissive states, and conceals open file descriptors before handing execution over to the app's native code.

---

## Technical Architecture & How It Works

### The Pre-Execution Stealth Hook

1. **Zygote Injection**: When Android's Zygote receives a fork request to create an application process, Shamiko hooks into the process initialization lifecycle.
2. **DenyList Reading**: Even though "Enforce DenyList" is turned off in Magisk settings, Shamiko reads the target package list directly from Magisk's SQLite database (`/data/adb/magisk.db`).
3. **Namespace & Mount Scrubbing**: If the newly spawned package is on the target list, Shamiko:
   - Sanitizes `/proc/self/mounts` and `/proc/self/mountinfo`, replacing Magisk overlay mount records with stock system records.
   - Masks or unmounts `/system/bin/su`, `/system/xbin/su`, and `/sbin` directories.
   - Cleans up lingering file descriptors (`/dev/pts`, `/dev/socket/magisk`) that betray root existence.
4. **Self-Destruction (Unlinking)**: After securing the process environment, Shamiko unlinks its own injection libraries from memory and removes its hook trampolines so security scanners looking for Zygisk module signatures find zero traces.

---

## Installation & Setup

### Step 1: Configure Magisk Settings
1. Open **Magisk App** $\rightarrow$ tap the **Settings** gear icon.
2. Ensure **Zygisk** is **ENABLED**.
3. Ensure **Enforce DenyList** is **DISABLED** (do not leave it checked).
4. Tap **Configure DenyList** and select the applications from which you wish to hide root (e.g., banking apps, government apps, games).

### Step 2: Install Shamiko
1. Download the latest release from the official LSPosed repository (`Shamiko-vX.zip`).
2. In Magisk / KernelSU, flash the zip from the **Modules** tab.
3. Reboot your device.

### Step 3: Verify Status
Check the module status in Magisk:
- If correctly configured, Shamiko will display: `Shamiko is working as normal (Blacklist mode)` or `(Whitelist mode)`.

---

## Whitelist vs Blacklist Mode

- **Blacklist Mode (Default)**:
  Root is visible everywhere except for apps checked in your DenyList. Recommended for casual users who only need to bypass a few specific banking apps.
- **Whitelist Mode (Recommended for Hardcore Stealth)**:
  Root is hidden globally from all applications on the device, and only granted to apps that are explicitly granted superuser permissions.
  ```bash
  # Activate Whitelist mode:
  su -c "mkdir -p /data/adb/shamiko && touch /data/adb/shamiko/whitelist"

  # Revert back to Blacklist mode:
  su -c "rm -f /data/adb/shamiko/whitelist"
  ```
