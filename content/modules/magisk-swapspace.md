---
id: "magisk-swapspace"
title: "Magisk SwapSpace: Persistent Virtual Memory & Swap Manager for Android"
sidebarTitle: "SwapSpace Manager"
description: "Allocates, configures, and manages persistent virtual swap memory on Android storage with customizable swappiness and priority."
category: "performance-kernel"
tier: 1
searchQueries:
  - "magisk swapspace"
  - "chkndrp magisk swapspace"
  - "create persistent swap file android root"
  - "magiskswap terminal command"
  - "virtual memory expansion kernelsu"
prerequisites:
  - "Root access via Magisk 27.0+ or KernelSU v0.9.4+"
  - "Sufficient free internal storage capacity for designated swap size"
conflicts: []
configPaths:
  - "/data/adb/modules/magisk-swapspace/"
features:
  - "Persistent swap allocation: generates and mounts dedicated swapfile allocations that survive device reboots"
  - "Configurable Linux swappiness: adjust vm.swappiness (0–200) to balance anonymous page eviction and active memory pressure"
  - "Interactive CLI tool (magiskswap): inspect swap status, activate, disable, or resize swap spaces directly from Termux"
  - "Priority chaining: set custom swap priority levels to orchestrate paging hierarchy alongside zRAM"
  - "Preservation flags: toggle swapfiles on and off without needlessly re-allocating or re-writing storage blocks"
---

## Overview

When running resource-intensive Android workloads—such as compiling software in Termux, hosting chroot Linux containers, running heavy emulation, or multitasking across RAM-constrained devices—available physical RAM and zRAM can quickly become exhausted, triggering abrupt Low Memory Killer (LMK) process terminations.

Created by chkndrp, **magisk-swapspace** is a systemless swap space management utility for rooted Android devices. It provides an intuitive command-line interface (`magiskswap`) to allocate, format, activate, and manage persistent swap storage on internal flash memory.

## Command Reference: `magiskswap`

Execute commands with root privileges inside Termux or an ADB shell:

```bash
su
magiskswap <COMMAND> <VALUE> [OPTIONS]
```

### Common Commands

- **Create Swap Space**:
  ```bash
  # Create a 4 GB swapfile, activate swapon, and persist across reboots
  magiskswap create 4
  ```
- **Check Status**:
  ```bash
  magiskswap status
  ```
  Outputs active swap partition paths, total allocated size, and currently utilized swap bytes.
- **Tune Swappiness**:
  ```bash
  # View current kernel swappiness
  magiskswap swappiness show

  # Set kernel swappiness to 60 (values 0-200)
  magiskswap swappiness 60
  ```
- **Remove Swap**:
  ```bash
  # Disable and delete the swapfile
  magiskswap remove

  # Disable swap while preserving the allocated file on disk
  magiskswap remove preserve
  ```

## Flash Wear Consideration

> **Important**: Modern Android devices use UFS or eMMC flash storage chips. Excessive and continuous paging to on-disk swapfiles can accelerate flash memory wear over extended lifespans. It is recommended to use moderate swappiness values and reserve swapfiles for specific memory-heavy scenarios rather than continuous thrashing.

## Installation

1. Download `magiskswapspace.zip` from GitHub releases.
2. Flash the module in **Magisk** (v27.0+) or **KernelSU** (v0.9.4+).
3. Reboot your device.
4. Launch Termux, run `su -c magiskswap create <size_GB>`, and verify with `free -m`.
