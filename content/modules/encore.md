---
id: "encore"
title: "Encore Tweaks: Dynamic Gaming & Battery Governor Optimizer"
sidebarTitle: "Encore Tweaks"
description: "Intelligent performance management engine dynamically maximizing gaming frame rates while conserving battery life during everyday tasks."
category: "performance-kernel"
tier: 1
searchQueries:
  - "encore tweaks magisk module"
  - "rem01gaming encore"
  - "android gaming governor optimizer"
  - "encore webui mmrl"
  - "encore tweaks ksu"
prerequisites:
  - "Android 8.0 or newer"
  - "Magisk, KernelSU, or APatch"
  - "Compatible with standalone WebUI managers: KsuWebUI, WebUI-X, and MMRL"
conflicts:
  - "Conflicting third-party CPU/GPU frequency boosters or aggressive task killer modules"
configPaths:
  - "/data/adb/modules/encore/"
  - "/data/adb/modules/encore/config/"
features:
  - "Dynamic workload scaling: seamlessly ramps up frequencies during gaming and down-clocks during static reading"
  - "Modern WebUI dashboard: customize governor profiles and tune mitigation settings via KsuWebUI or MMRL"
  - "Device mitigation engine: contains per-device mitigation rules to prevent thermal runaway and overheating"
  - "Low idle power consumption: fine-tunes deep sleep wakeups and cpufreq governor responsiveness"
  - "Action button integration: trigger quick mode changes and status diagnostics directly from your root manager"
faq:
  - question: "Does Encore Tweaks require a custom kernel?"
    answer: "No. Encore Tweaks operates through standard Linux kernel sysfs interfaces and Android power HAL interfaces, providing tangible performance enhancements on both stock and custom kernels."
  - question: "How do I access the Encore Tweaks dashboard on Magisk?"
    answer: "Because official Magisk does not provide a native WebUI environment, Magisk users can manage Encore Tweaks using standalone WebUI hosts such as MMRL or WebUI-X."
---

## Overview

Developed by **Rem01Gaming**, **Encore Tweaks** is a dynamic Android performance optimization module designed to balance gaming smoothness with daily battery efficiency.

Rather than forcing permanent overclocking states that drain batteries and induce thermal throttling, Encore Tweaks continuously adapts CPU, GPU, and memory bus parameters based on active foreground demands. During gaming sessions, it ensures sustained frame pacing; when using social apps or reading, it prioritizes energy conservation.

---

## Technical Architecture & How It Works

### Adaptive Energy Scaling & Hardware Governors

Encore Tweaks operates at the intersection of Linux kernel governors and Android runtime frameworks:

1. **Active Scene Detection**: Identifies game packages and high-demand applications, triggering optimized interactive governor tunables and higher minimum clock floors.
2. **Device Mitigation Engine**: Leverages `/data/adb/modules/encore/config/device_mitigation.json` to prevent aggressive thermal throttling spikes by moderating sustained power limits.
3. **Cpuset & Memory Management**: Optimizes low-memory killer (LMK) thresholds and virtual memory caching parameters to minimize stutter during app switches.

---

## Installation & Setup

1. Download the latest `Encore-Tweaks-*.zip` release.
2. Flash the module in Magisk, KernelSU, or APatch.
3. Reboot your device.
4. Launch your root manager's WebUI (or open **MMRL**) to configure your initial power profiles.

---

## Configuration & Usage

- **Performance Modes**: Choose between Battery Saver, Balanced, and Gaming profiles.
- **WebUI Configuration**: Fine-tune GPU governors, CPU cluster scaling rates, and memory management through the integrated WebUI dashboard.

---

## Troubleshooting & Common Issues

- **High Battery Drain**: If battery consumption rises unexpectedly, ensure you have not left other performance-boosting modules or competing thermal disablers active simultaneously.
