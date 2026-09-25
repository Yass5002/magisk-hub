---
id: "stellar-tweaks"
title: "Stellar Tweaks: Rust-Engineered Performance, FEAS Scheduling & Hardware Orchestrator"
sidebarTitle: "Stellar Tweaks"
description: "High-performance Android daemon written in Rust, combining Fast Energy Aware Scheduling (FEAS), GPU governor orchestration, bypass charging, and an offline Material You WebUI."
category: "performance-kernel"
tier: 1
searchQueries:
  - "stellar tweaks magisk module"
  - "kanaodnd stellar tweaks"
  - "android rust performance daemon root"
  - "fast energy aware scheduling feas android"
  - "stellar tweaks webui kernelsu"
prerequisites:
  - "Android 9.0 or higher"
  - "Root access via KernelSU, Magisk, or APatch (grants full kernel/FEAS access)"
  - "Qualcomm Snapdragon, MediaTek, Samsung Exynos, or Unisoc processor"
conflicts:
  - "Concurrent third-party performance modules or conflicting governor optimizer scripts (causes parameter collisions with Stellar's DVFS controller)"
configPaths:
  - "/data/adb/modules/stellar-tweaks/"
features:
  - "Fast Energy Aware Scheduling (FEAS): monitors render thread throughput in real time and aligns frequency ramping to prevent dropped frames"
  - "Cluster-aware thread affinity: directs critical render threads to Prime and Big CPU cores while confining background workers to efficiency clusters"
  - "Multi-architecture GPU orchestration: provides independent GPU governor profiles across Adreno, Mali, Devfreq, and KGSL drivers"
  - "Hardware bypass charging: allows compatible handsets to draw operating current directly from the charger without routing energy through the battery"
  - "Display pipeline controller: forces high refresh rates across Xiaomi, Samsung, BBK/OPlus, and Transsion devices while enforcing 60Hz limits in Battery Saver"
  - "Material You 3 WebUI: completely offline, single-file dark interface rendered inside root managers"
---

## Overview

Traditional Android optimization scripts predominantly consist of shell scripts that execute periodic loops using `dumpsys` or brute-force sysfs writes. These scripts waste CPU cycles through continuous context switching, introduce micro-stutters during heavy animation sequences, and fight against Android's native framework scheduler.

Engineered entirely in **Rust** by kanaodnd, **Stellar Tweaks** is a deterministic systems daemon designed for low-latency kernel and framework orchestration. Running silently in the background, Stellar integrates directly with Linux userspace and kernel interfaces across Qualcomm Snapdragon, MediaTek, Samsung Exynos, and Unisoc architectures. It replaces uncoordinated scheduler hacks with genuine Fast Energy Aware Scheduling (FEAS), intelligent display rate overrides, and hardware-level battery isolation.

## Architecture & Core Innovations

### 1. Fast Energy Aware Scheduling (FEAS)
- **Real-Time Render Monitoring**: Rather than reacting after a frame has already dropped, Stellar tracks the throughput and latency of the active application's `RenderThread`. If a sudden complex frame is detected, it ramps CPU frequencies ahead of the draw call deadline.
- **Cluster Affinity Mapping**: Automatically pins high-priority game and UI threads to Prime and Big CPU performance clusters while shunting non-critical background jobs to Little efficiency cores.
- **Cooperative Idle Snapping**: Gracefully steps hardware into minimum power states when the screen is static without relying on aggressive `evdev` event loops.

### 2. Cross-Platform GPU & I/O Control
Stellar provides tailored governor logic across all major mobile graphics architectures—including Qualcomm Adreno (KGSL), ARM Mali, and generic Devfreq nodes:
- **Gaming Profile**: Locks high GPU minimum clocks and activates bypass charging.
- **Balanced Profile**: Retains fluid 120Hz scrolling while lowering power consumption during reading and static media viewing.
- **Powersaver Profile**: Enforces strict frequency ceilings and locks the display panel to 60Hz.

### 3. Thermal Bypass & Charging Management
During extended gaming sessions, battery heat is the primary catalyst for severe SoC thermal throttling. Stellar activates **Bypass Charging** (Idle Battery State) on supported hardware, allowing the device to draw power directly from the connected USB charger without routing current into the lithium cell, reducing internal operating temperatures.

### 4. Multi-Vendor Display Pipeline
OEM display managers (MIUI/HyperOS, One UI, ColorOS/OxygenOS, HiOS/XOS) frequently drop display refresh rates to 60Hz inside games or third-party web browsers. Stellar overrides vendor display lockouts to enforce chosen refresh rates while automatically respecting Android's system Battery Saver mode.

## User Interface (M3 WebUI)

Stellar includes an embedded **Material You 3 (M3)** WebUI dashboard. Compiled as a self-contained distribution, it requires zero external internet access, runs entirely offline, and renders natively inside **KernelSU Manager**, **APatch Manager**, or **MMRL**.

Users can inspect live CPU/GPU frequencies, toggle operational profiles, manage per-app overrides, and execute component cleanups directly from the interface.

## Installation & Best Practices

1. Ensure no conflicting performance or battery governor modules are installed.
2. Flash the **Stellar Tweaks** `.zip` via your preferred root manager.
3. Reboot your device to let Stellar inspect display refresh boundaries and kernel sysfs nodes.
4. Open your root manager's module panel to launch the Stellar WebUI.
5. Customize profile rules or allow the auto-adaptive scheduler to manage workloads automatically.

> [!WARNING]
> Because Stellar actively coordinates CPU/GPU governors, EAS task placement, and DVFS curves, running other performance scripts or scheduler modules simultaneously will cause parameter collisions and frame pacing volatility.
