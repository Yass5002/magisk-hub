---
id: "neozygisk"
title: "NeoZygisk: Ptrace-Based Lightweight Zygote Injector & Stealth DenyList"
sidebarTitle: "NeoZygisk"
description: "Minimalist, ptrace-based Zygote injection framework providing Zygisk API compatibility with clean namespace unmounting and trace removal."
category: "root-management"
tier: 1
searchQueries:
  - "neozygisk magisk module"
  - "neozygisk kernelsu apatch"
  - "ptrace zygote injection android"
  - "neozygisk denylist namespace unmount"
  - "jingmatrix neozygisk"
prerequisites:
  - "KernelSU, APatch, or Magisk"
conflicts:
  - "Magisk's built-in 'Enforce DenyList' option (must be disabled to prevent namespace collisions and broken isolation)"
  - "Magisk's built-in Zygisk feature (must be turned off in Magisk settings when using standalone NeoZygisk)"
configPaths:
  - "/data/adb/modules/neozygisk/"
  - "Per-application 'Umount modules' toggles in KernelSU / APatch Manager"
  - "Configure DenyList menu in Magisk Manager"
features:
  - "Ptrace-based Zygote injection: hooks into the Android zygote process at the Linux syscall level without modifying the core zygote binary"
  - "Complete trace cleaning: cleans all injection artifacts and unmaps loader memory once modules finish execution"
  - "Direct Zygote unmounting: attempts pre-specialization unmounting of root mounts directly inside Zygote before app fork"
  - "Namespace switching fallback: uses setns syscall to switch target applications into a clean, cached mount namespace"
  - "Full Zygisk API compatibility: runs standard Zygisk modules designed for Magisk across APatch and KernelSU"
faq:
  - question: "Why must Magisk's 'Enforce DenyList' be turned off when using NeoZygisk?"
    answer: "Magisk's Enforce DenyList runs its own separate mount hiding daemon, which interferes with NeoZygisk's namespace isolation. NeoZygisk reads the target packages listed in Magisk's Configure DenyList menu automatically, but enforcing the list through Magisk's engine causes conflicting mount states."
  - question: "How does NeoZygisk hide root and module mounts from banking applications?"
    answer: "NeoZygisk first attempts to cleanly unmount root overlays directly from the Zygote process prior to app specialization. If an unmount would compromise critical system assets, it falls back to calling setns after fork, switching the application process into a completely clean, isolated Linux mount namespace where no root or overlay filesystem nodes exist."
---

## Overview

Developed by **JingMatrix**, **NeoZygisk** is a high-performance, minimalist implementation of the Android Zygisk API designed for **APatch**, **KernelSU**, and **Magisk**.

Rather than relying on intrusive framework hooks or daemon wrappers that introduce detectable telemetry, NeoZygisk uses Linux's native `ptrace` system call to inject code cleanly into the Android `zygote` process. It provides full API compatibility for third-party Zygisk modules while prioritizing memory cleanup and root cloaking.

---

## Technical Architecture & How It Works

### Ptrace Injection & Two-Tier DenyList Isolation

NeoZygisk operates with four foundational design principles:

1. **Ptrace Syscall Attachment**: NeoZygisk hooks into the 32-bit and 64-bit Zygote daemons at runtime via `ptrace`, injecting the module loader without altering on-disk zygote binaries.
2. **Post-Load Trace Cleaning**: Once all registered Zygisk modules finish execution during process initialization, NeoZygisk unmaps its loader memory, cleans up memory descriptors, and removes its own footprints from the target application's `/proc/[pid]/maps`.
3. **Primary Isolation Strategy (Direct Zygote Unmount)**: For applications listed on the DenyList, NeoZygisk attempts to unmount root and module filesystem overlays directly from the Zygote process *before* the application process is specialized. If an overlay provides critical system resources (such as `/product` runtime dependencies), this step is automatically aborted to preserve system stability.
4. **Fallback Isolation Strategy (Namespace Switching)**: If direct unmounting is bypassed for safety, NeoZygisk invokes the `setns` system call immediately after `fork`. This switches the child application process into an isolated, cached Linux mount namespace that contains an unmodified, pristine view of system partitions with zero module mounts.

---

## Installation & Setup

### 1. Flash the Module
1. Download the latest `NeoZygisk-v*.zip` from the project's official releases.
2. Flash the module in your root manager (Magisk, KernelSU, or APatch).
3. If you are using **Magisk**:
   - Open Magisk Settings and ensure **Zygisk** is toggled **OFF** (to avoid running two conflicting Zygisk engines simultaneously).
   - Ensure **Enforce DenyList** is toggled **OFF**.
4. Reboot the device.

---

## Configuration & Practical Usage

Hiding root and modules from sensitive applications is controlled through your root manager's native user interface:

- **On APatch or KernelSU**: Open your manager app, find your target application in the list, and turn on the **Umount modules** toggle.
- **On Magisk**: Open Magisk Manager, navigate to **Configure DenyList**, and check the target application along with its individual sub-processes. Do not enable "Enforce DenyList" in settings.

Once configured, NeoZygisk isolates the selected packages inside clean mount namespaces automatically upon launch.

---

## Troubleshooting & Common Issues

- **Detection in Banking Apps**: If an app still detects root, confirm that all sub-processes (such as isolated background services or companion processes) are selected in the DenyList. Ensure Magisk's built-in "Enforce DenyList" remains disabled, as it conflicts with NeoZygisk's namespace isolation.
- **Zygisk Modules Not Loading**: Confirm that the target module is compiled for the architecture of your device's Zygote process (`arm64-v8a` or `armeabi-v7a`). Verify in your root manager that NeoZygisk is actively enabled.
