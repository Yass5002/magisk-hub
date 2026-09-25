---
id: "onyxzygisk"
title: "OnyxZygisk: Ptrace Zygisk Runtime with Local WebUI & Hot-Swappable FN Modules"
sidebarTitle: "OnyxZygisk"
description: "Kernel-independent Zygisk implementation utilizing ptrace zygote injection, offering a zero-reboot hotplug architecture, embedded WebUI, and two-layer stealth DenyList."
category: "root-management"
tier: 1
searchQueries:
  - "onyxzygisk magisk module"
  - "onyxzygisk ptrace zygote injection"
  - "zygisk hotplug without reboot"
  - "onyxzygisk kernelsu apatch webui"
  - "functional node fn modules zygisk"
prerequisites:
  - "Android 8.1 through Android 15+"
  - "Root access via APatch, KernelSU (including LKM late-load), or Magisk"
  - "No proprietary kernel patches or custom kernel modules required"
conflicts:
  - "Other standalone Zygisk injection modules (ZygiskNext, NeoZygisk) active simultaneously"
configPaths:
  - "/data/adb/modules/OnyxZygisk/"
  - "/data/adb/onyx/"
features:
  - "Universal ptrace injection: hooks into the Android Zygote process via standard Linux ptrace without requiring kernel-level hooks"
  - "Zero-reboot hot-plugging: enable, disable, or reload Zygisk modules on the fly without rebooting the Android OS"
  - "Functional Node (FN) architecture: supports scoped, declarative module extensions taking immediate effect on target app launch"
  - "Embedded WebUI dashboard: rich control interface built with React, Vite, and Tailwind, rendered directly inside root managers without network daemon ports"
  - "Dual-layer stealth DenyList: combines Zygote filesystem unmounting with fallback mount namespace switching via setns"
---

## Overview

Traditional Zygisk runtimes—whether built into official Magisk or implemented via kernel-assisted modules—frequently suffer from two operational pain points: they require full device reboots whenever a module is enabled or disabled, and they often demand specific kernel-level features or root-solution-specific integrations.

**OnyxZygisk** reimagines the Zygisk environment as an agnostic, standalone runtime. Operating entirely via userspace Linux `ptrace` system calls, OnyxZygisk injects its API bridge into the Android Zygote process across Magisk, KernelSU, and APatch alike. It introduces dynamic hot-plugging, an integrated local WebUI, and a next-generation Functional Node (FN) module format.

## Core Capabilities & Architectural Design

### 1. Ptrace-Powered Universal Injection
Because OnyxZygisk relies on standard Linux `ptrace` primitives to intercept Zygote process forks, it is fully decoupled from the underlying root implementation. It supports:
- **Magisk**: Replaces built-in Zygisk to unlock hot-plug capabilities.
- **KernelSU & APatch**: Functions seamlessly even in late-load LKM configurations where kernel-level Zygote hooks might be delayed.

### 2. Zero-Reboot Module Hot-Plugging & FN Nodes
- **Dynamic Reloading**: Unlike legacy Zygisk implementations where state changes demand a reboot, OnyxZygisk allows users to toggle installed modules on and off in real time. Changes take effect the next time target applications fork from Zygote.
- **FN (Functional Node) Modules**: A lightweight, declarative extension standard that allows small scoped hooks to attach to individual application sandboxes without compiling full-blown Zygisk binaries.

### 3. Dual-Layer Stealth DenyList
To protect sensitive applications (banking clients, enterprise MDMs) from detecting root mounts and Zygisk hooks, OnyxZygisk implements a multi-stage isolation boundary:
1. **Zygote Unmount**: Unmounts module directories and root paths from the process mount namespace upon forking.
2. **Namespace Switch (`setns`)**: As a fallback for advanced detection vectors, isolates the process into an untouched parent mount namespace before executing Dalvik/ART initialization code.

### 4. Fully Local WebUI
Packaged with an embedded single-page application built with React, Vite, and Tailwind CSS, OnyxZygisk renders directly inside KernelSU Manager, APatch Manager, or MMRL. It runs completely offline without spawning local HTTP servers or binding vulnerable network ports.

## Installation & Setup

1. If running Magisk, navigate to **Magisk Settings** and disable the built-in **Zygisk** switch.
2. If using alternative Zygisk providers (such as ZygiskNext or NeoZygisk), disable or uninstall them to prevent injection collisions.
3. Flash the **OnyxZygisk** `.zip` package through your root manager.
4. Reboot the smartphone.
5. Access the WebUI through your manager's module interface to configure the DenyList, inspect active module status, and monitor live logcat events.

## Troubleshooting

- **Collision with Other Zygisk Engines**: If Zygote crashes or enters a bootloop, ensure no secondary Zygisk injection provider is running concurrently.
- **SELinux Denials in Ptrace**: On highly restrictive custom ROMs with custom SELinux policies, verify that your root manager allows ptrace calls across root-to-zygote process domains.
