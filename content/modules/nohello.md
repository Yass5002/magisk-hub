---
id: "nohello"
title: "Zygisk NoHello: Stealth Root & Module Detection Cloaking"
sidebarTitle: "NoHello"
description: "Zygisk-based anti-detection module designed to hide root binaries, Zygisk traces, and module mount modifications from sensitive apps."
category: "root-management"
tier: 1
searchQueries:
  - "nohello zygisk module"
  - "mhmrdd nohello"
  - "hide root zygisk nohello"
  - "nohello mount rule system"
  - "bypass root detection nohello"
prerequisites:
  - "KernelSU, KernelSU Next, APatch, or Magisk (v28.0+ recommended)"
  - "Active Zygisk provider (ZygiskNext or ReZygisk strongly recommended)"
conflicts:
  - "Enforce DenyList in Magisk settings (must be disabled)"
  - "Enforce DenyList in ZygiskNext or ReZygisk settings (must be disabled)"
configPaths:
  - "/data/adb/nohello/"
  - "/data/adb/modules/nohello/"
features:
  - "Stealth root hiding: conceals su binaries, daemons, and package manager signatures from target apps"
  - "Custom mount rule system: allows fine-grained rules to unmount or disguise specific filesystem modifications"
  - "Whitelisting support: configure whitelist mode to isolate all applications by default except trusted tools"
  - "Zygisk injection obfuscation: erases runtime memory hooks and module entry points after execution"
  - "Cross-manager compatibility: designed to work seamlessly across KernelSU, APatch, and Magisk"
faq:
  - question: "Why must 'Enforce DenyList' be turned off when using NoHello?"
    answer: "NoHello manages its own unmounting and isolation routines. Enabling Enforce DenyList in Magisk or Zygisk providers activates competing mount namespaces that conflict with NoHello's cloaking logic."
  - question: "Should I use the debug or release build of NoHello?"
    answer: "Always use the release build for daily use. The debug build contains verbose logging routines and exported symbols that can trigger security detections in anti-cheat and banking applications."
---

## Overview

Developed by **MhmRdd**, **Zygisk NoHello** is a specialized anti-detection module engineered to hide root privileges, Zygisk runtime artifacts, and systemless filesystem mounts from modern application integrity checks.

Standard root-hiding approaches frequently fail against modern multi-vector detection suites that scan for open ports, inspect `/proc/mounts`, analyze loaded shared libraries, and test execution permissions. NoHello operates at the Zygisk level to intercept detection routines before applications can complete their startup scans.

---

## Technical Architecture & How It Works

### Process Isolation & Mount Rules

NoHello hooks into application processes during the Zygote fork lifecycle:

1. **Mount Unmounting**: For applications flagged in your manager's DenyList or target configuration, NoHello detaches module overlays and mounts from the process mount namespace.
2. **Dynamic Rule Processing**: Features a rule-based engine allowing users to specify exact path masking, file redirections, and property overrides for specific detection vectors.
3. **Trace Eradication**: Cleans up internal hooking stubs and resets process capabilities before control is handed over to the application's main entry point.

---

## Installation & Setup

### For KernelSU & APatch Users
1. Install an active Zygisk implementation (**ZygiskNext** or **ReZygisk**).
2. Ensure the **Umount modules** toggle is enabled for your target application in the Manager.
3. Disable **Enforce DenyList** in ZygiskNext/ReZygisk settings if present.
4. Flash the NoHello module and reboot.

### For Magisk Users
1. Magisk v28.0+ is recommended for optimal namespace isolation.
2. Use **ZygiskNext** or **ReZygisk** (recommended over built-in Zygisk).
3. Turn **OFF** `Enforce DenyList` in Magisk settings.
4. Add your target application to Magisk's **Configure DenyList**.

---

## Configuration & Practical Usage

- **Whitelisting Mode**: On version 0.0.4+, you can invert the operating policy to whitelist mode so all applications are isolated by default unless explicitly granted root visibility.
- **Custom Mount Rules**: Place specialized unmount and masking instructions in `/data/adb/nohello/rules` to handle non-standard device modifications.

---

## Troubleshooting & Common Issues

- **Detection Persists**: Confirm that all background services and auxiliary processes of the target app are selected in the DenyList. Ensure `Enforce DenyList` is disabled across all manager settings.
- **Manager App Crashes**: Do not enable module unmounting for the root manager itself (KernelSU Manager, APatch, or Magisk).
