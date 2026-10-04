---
id: "meta-overlayfs-kernelsu"
title: "OverlayFS MetaModule for KernelSU"
description: "Next-generation OverlayFS meta-module engine for KernelSU and APatch providing high-performance systemless file mounting, real-time kernel inspection, and native WebUI."
category: "system-environment"
author: "AshBorn & KernelSU Devs"
version: "1.3.4"
updatedAt: "2026-10-04"
compatibility: ["KernelSU", "APatch"]
---

## Overview & System Architecture

The **OverlayFS MetaModule** (`meta-overlayfs`), collaboratively engineered by AshBorn (@Ripper_Hybrid) and the KernelSU development community, is a core infrastructure metamodule for KernelSU and APatch.

Traditional Magisk modules rely on `magic mount` (bind mount loops across filesystem nodes), which can cause mounting overhead, inode exhaustion, and detection by sophisticated integrity verifiers. The OverlayFS MetaModule leverages Linux's native `overlayfs` kernel driver to merge module directories into system partitions transparently at the VFS layer.

## Key Architectural Advantages

1. **Native VFS Overlay**: Unifies upperdir and lowerdir mount layers natively without generating hundreds of separate loopback bind mounts.
2. **High I/O Performance**: File lookups and reads operate with near zero overhead compared to multi-layered bind mounts.
3. **WebUI Integration**: Features an integrated WebUI accessible directly inside the KernelSU Manager for real-time mount inspection and conflict diagnostics.
4. **Clean Metamodule Lifecycle**: Implements `metamount.sh`, `metainstall.sh`, and `metauninstall.sh` standardized hooks.

## Installation & Verification

### Step 1: Flashing the Metamodule
Install `meta-overlayfs_v1.3.4_13400.zip` via KernelSU or APatch Manager.

### Step 2: Verification of Active Overlays
After rebooting, verify that `overlay` filesystem mounts are active:
```bash
mount | grep -i overlay
```

### Step 3: KernelSU WebUI Inspection
Open **KernelSU Manager > Modules > OverlayFS Enhanced > WebUI** to inspect the live status of all systemless partition merges.

## Compatibility & Requirements

- **Linux Kernel**: Requires Linux kernel version 4.9 or higher with `CONFIG_OVERLAY_FS=y`.
- **Root Provider**: Strictly designed for KernelSU and APatch; not required on standard Magisk (which uses its own internal magic mount implementation).
