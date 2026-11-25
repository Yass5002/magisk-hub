---
id: "meta-magic-mount-rs"
title: "Magic Mount-rs: Rust Systemless Metamodule"
sidebarTitle: "Magic Mount RS"
description: "High-performance Rust metamodule from Tools-cx-app implementing Magic Mount systemless file overlays, custom bind rules, and WebUI configuration."
category: "root-management"
tier: 1
searchQueries:
  - "magic mount metamodule rust"
  - "meta magic mount rs"
  - "tools-cx-app magic mount"
  - "kernelsu apatch metamodule"
  - "custom bind rules metamodule"
prerequisites:
  - "KernelSU or APatch with metamodule support (primary target; Magisk already provides native Magic Mount)"
  - "Supported architecture: arm64-v8a, armeabi-v7a, x86_64, or riscv64"
conflicts:
  - "Other competing metamodules managing global module file overlays (e.g., meta-overlayfs or Mountify in metamodule mode)"
configPaths:
  - "/data/adb/magic_mount/config.toml"
  - "/data/adb/magic_mount/custom"
  - "/data/adb/modules/magic_mount_rs/"
features:
  - "Rust-native metamodule: compiles native magic_mount_rs binaries for arm64-v8a, armeabi-v7a, x86_64, and riscv64"
  - "Metamodule lifecycle integration: implements metainstall.sh, metamount.sh, and metauninstall.sh with SHA-256 verification"
  - "Custom rule engine: define ignore, bind, and external file inclusion directives without rebuilding full modules"
  - "WebUI management: built-in webroot dashboard to edit config.toml and inspect mount state"
  - "APatch & KernelSU tuned defaults: ships dedicated config.toml (KSU) and config_apatch.toml (APatch) templates"
faq:
  - question: "Why is a metamodule required for KernelSU and APatch?"
    answer: "Unlike Magisk which builds Magic Mount into its init binary, modern KernelSU and APatch architectures delegate module filesystem mounting to a dedicated metamodule, letting users choose between OverlayFS and Magic Mount."
  - question: "Does Magic Mount-rs work on Magisk?"
    answer: "Note that Magisk ships its own built-in Magic Mount engine, and meta-magic_mount-rs's customize.sh explicitly checks for KernelSU ($KSU) or APatch ($APATCH) during installation."
  - question: "How do custom bind rules work?"
    answer: "Rules placed under /data/adb/magic_mount/custom allow directives such as ignoring specific module paths or binding individual files without packaging a separate module."
---

## Overview

Developed by **Tools-cx-app**, **Magic Mount-rs** (`v4.1.12`) is a standalone implementation of Magisk's Magic Mount systemless mounting logic written in **Rust** (`id=magic_mount_rs`, `metamodule=1`).

While **KernelSU** and **APatch** provide kernel-level root and namespace isolation, they delegate systemless module filesystem mounting to a user-selected metamodule. Magic Mount-rs acts as that metamodule, handling module installation layout normalization (`metainstall.sh`), early-boot mounting (`metamount.sh`), and cleanup (`metauninstall.sh`).

---

## Technical Architecture & How It Works

### Rust-Powered Metamodule Engine

Magic Mount-rs coordinates module overlays cleanly during early Android boot:

1. **Verified Extraction (`customize.sh` + `verify.sh`)**: Checks for an active KernelSU or APatch environment, selects the matching `magic_mount_rs` binary (`arm64-v8a`, `armeabi-v7a`, `x86_64`, or `riscv64`), and verifies package integrity against `.sha256` digests.
2. **Partition Symlink Normalization (`metainstall.sh`)**: Exports `KSU_HAS_METAMODULE="true"` (`KSU_METAMODULE="mmrs"`), handles self-mounting blocklisted modules by marking `skip_mount`, and normalizes `/system/{vendor,product,system_ext}` paths when `/system/$part` is a symlink.
3. **Boot Mounting (`metamount.sh`)**: Invokes the native Rust binary and calls `/data/adb/ksud kernel notify-module-mounted` upon success so KernelSU/APatch track mounted state accurately.
4. **WebUI & Soft Reboot Helper**: Includes `webroot/` for GUI configuration and `emulated-soft-reboot.sh` for faster iteration.

---

## Installation & Setup

1. Ensure your device runs **KernelSU** or **APatch** with metamodule support (and remove any competing metamodule first).
2. Download `magic_mount_rs-4.1.12-959-universal.zip` from `Tools-cx-app/meta-magic_mount-rs`.
3. Flash the module in your root manager.
4. Reboot your device.

---

## Configuration & Usage

Default settings live in `/data/adb/magic_mount/config.toml` (with `mountsource = "APatch"` when initialized from `config_apatch.toml`):

```toml
mountsource = "KSU"
umount = false
partitions = []
extra_mount = []
```

- **`mountsource`**: Mount source label (`"KSU"` or `"APatch"`).
- **`umount`**: Controls whether mounts should be unmounted for non-root target apps.
- **`partitions`** & **`extra_mount`**: Arrays specifying additional partitions (such as `mi_ext` or `my_stock`) and custom mount entries.

---

## Troubleshooting & Common Issues

- **Unsupported Platform Abort**: If `customize.sh` prints `! unsupported root platform`, ensure you are flashing inside KernelSU or APatch rather than Magisk or a custom recovery.
- **Mount Failures**: Check that custom rule paths in `/data/adb/magic_mount/custom` are valid absolute paths without relative `..` segments.
