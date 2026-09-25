---
id: "azenith"
title: "AZenith: All-In-One Dynamic Kernel, Process & Thermal Optimizer for Android"
sidebarTitle: "AZenith"
description: "Universal Android performance optimization module featuring foreground game prioritization, intelligent background freezing, Thermalcore FPS stabilization, and a dedicated control dashboard."
category: "performance-kernel"
tier: 1
searchQueries:
  - "azenith magisk module"
  - "liliya2727 azenith"
  - "android thermalcore game fps stabilizer"
  - "android game preload governor optimizer"
  - "azenith performance balanced eco profile"
prerequisites:
  - "Android 11 or higher"
  - "Root access via Magisk, KernelSU, or APatch"
  - "Optional companion APK for graphical dashboard configuration"
conflicts: []
configPaths:
  - "/data/adb/modules/azenith/"
  - "/data/adb/modules/azenith/azenithApplist.json"
features:
  - "Dynamic process prioritization: elevates thread scheduling for active foreground titles while suspending resource-heavy background processes"
  - "Thermalcore governor service: smooths out hardware thermal throttling steps to sustain a consistent minimum framerate floor"
  - "Automated game profile switching: transitions between ECO, Balanced, and Performance modes upon package launch"
  - "Shared library preloading: accelerates game stage and level loading times by pre-caching critical native libraries in memory"
  - "Kernel subsystem control: exposes direct tuning for CPU frequency caps, CPU governors, and block I/O schedulers"
---

## Overview

Developed by Liliya2727, **AZenith** is an All-In-One (AIO) performance orchestration module engineered to bridge the gap between high-refresh-rate gaming stability and daily battery efficiency. Unlike rigid static scripts that permanently lock CPU cores to maximum frequencies—triggering rapid overheating and steep thermal throttling—AZenith combines an intelligent daemon with a companion app dashboard to make context-sensitive kernel and userspace adjustments.

When a game or demanding app is focused, AZenith prioritizes its render threads, preloads linked shared libraries into RAM, and engages its proprietary **Thermalcore** service to eliminate jarring framerate dips.

## Core Architecture & Features

### 1. Dynamic Process & Memory Management
- **Foreground Prioritization**: Automatically maps active game processes to higher CPU scheduling weights, reducing input latency and frame drops.
- **Background Bloatware Suspension**: Temporarily freezes dormant background services without terminating them, eliminating context-switch jitter while preserving user multitasking state.
- **Game Preload Engine**: Caches frequently accessed native `.so` libraries upon application launch, resulting in faster initial boot and level-transition times.

### 2. Thermalcore Service
Standard OEM thermal engines employ aggressive step-down throttling: once temperature passes a safety boundary, CPU and GPU clocks are instantly slashed, creating sudden frame drops. Thermalcore manages thermal curves gradually, maintaining a stable baseline frequency that avoids thermal spikes while keeping frame rates consistent throughout prolonged gaming sessions.

### 3. Subsystem Tuning & Operating Profiles
AZenith includes three calibrated operating profiles:
- **Performance**: Elevates governor ramp speeds, optimizes I/O queue depths, and reserves compute clusters for the foreground task.
- **Balanced**: Standard operational mode providing responsive touch dispatch and smooth UI animations while conserving battery life.
- **ECO**: Caps maximum frequencies by a user-defined percentage, enforces aggressive idle downclocking, and curtails background wakeups.

## Configuration & App Dashboard

Users can manage AZenith either via its dedicated companion application or by editing module configuration files:

- **Automatic Mode**: By default, AZenith monitors package lifecycle events and applies optimized parameters automatically whenever an entry in `azenithApplist.json` is launched.
- **Manual Mode**: To enforce a single static profile (e.g., locking Balanced or ECO globally), navigate to **AZenith Settings** in the app dashboard and select **Disable Auto Mode**.
- **Hardware Knobs**:
  - **CPU Governor**: Select between available kernel governors (`schedutil`, `walt`, etc.).
  - **I/O Scheduler**: Toggle between `mq-deadline`, `kyber`, or `bfq` storage schedulers.
  - **CPU Frequency Limiter**: Define a percentage ceiling to restrain thermals on hot-running chipsets.

## Installation & Setup

1. Verify that your device runs Android 11 or higher with Magisk, KernelSU, or APatch.
2. Install the AZenith module `.zip` through your root manager.
3. Reboot your device to allow the daemon and kernel hooks to initialize.
4. *(Recommended)* Install the companion APK to view live telemetry, customize your game whitelist, and tune governor parameters.

## Troubleshooting

- **Games Not Triggering Performance Mode**: Verify that your game's package identifier is registered in `/data/adb/modules/azenith/azenithApplist.json` or add it manually via the companion app dashboard.
- **Unexpected Battery Drain**: Ensure that manual Performance Mode has not been permanently locked. Re-enable Auto Mode so the system returns to Balanced or ECO states when idle.
