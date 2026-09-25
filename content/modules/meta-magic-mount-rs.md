---
id: "meta-magic-mount-rs"
title: "Magic Mount Metamodule (Rust): Systemless File Mounter"
sidebarTitle: "Magic Mount RS"
description: "High-performance Rust metamodule providing systemless file modification capabilities for KernelSU and APatch."
category: "root-management"
tier: 1
searchQueries:
  - "magic mount metamodule rust"
  - "meta magic mount rs"
  - "tools cx app magic mount"
  - "kernelsu apatch magic mount"
  - "custom bind rules metamodule"
prerequisites:
  - "KernelSU or APatch with metamodule support"
  - "Kernel with basic mount and tmpfs support"
conflicts:
  - "Other competing metamodules that manage global file overlays (e.g. Mountify in metamodule mode)"
configPaths:
  - "/data/adb/magic_mount/config.toml"
  - "/data/adb/magic_mount/custom"
features:
  - "Rust-native metamodule: engineered in Rust for extreme memory safety and instant boot execution"
  - "Custom rule system: define explicit ignore, bind, and file inclusion rules in /data/adb/magic_mount/custom"
  - "Partition isolation: specify target partitions (such as mi_ext or my_stock) for granular systemless modification"
  - "WebUI configuration: visual management dashboard for editing config.toml and reviewing active mounts"
  - "Atomic rollback: automatically rolls back and detaches temporary mounts if a bind operation fails"
faq:
  - question: "Why is a metamodule required for KernelSU and APatch?"
    answer: "Unlike traditional Magisk which includes a built-in magic mount daemon in its init binary, modern kernel-based root solutions like KernelSU and APatch delegate overlay mounting to modular metamodules, giving users control over how files are injected."
  - question: "How do custom bind rules work in Magic Mount Metamodule?"
    answer: "You can create customized bind instructions in /data/adb/magic_mount/custom. For example, using 'bind /data/local/tmp/file /system/etc/file' allows you to mount individual files without packaging them into a full module directory."
---

## Overview

Developed by **Tools-cx-app**, **Magic Mount Metamodule (Rust)** is a standalone implementation of Magisk's classic magic mount logic rewritten in Rust for **KernelSU** and **APatch**.

While KernelSU and APatch provide powerful kernel-level root and namespace isolation, they intentionally do not force a specific module mounting mechanism into the kernel core. Magic Mount Metamodule steps in as a metamodule, intercepting early boot initialization to construct clean systemless filesystem overlays for all installed modules.

---

## Technical Architecture & How It Works

### Rust-Powered Metamodule Engine

The module functions as a core boot coordinator:

1. **Metamodule Lifecycle**: Launches during early Android initialization via KernelSU/APatch metamodule hooks.
2. **Overlay Construction**: Traverses installed modules in `/data/adb/modules/`, mirror-binding files over system partitions (including vendor, product, and OEM-specific partitions like `mi_ext`).
3. **Custom Rule Parser**: Reads `/data/adb/magic_mount/custom` to execute fine-grained user directives:
   - `ignore <path>`: Skips mounting a specific file from a module.
   - `bind <source> <target>`: Creates a read-only bind mount from a custom location.
   - `file <rules_file>`: Recursively includes external rule files with circular loop protection.

---

## Installation & Setup

1. Verify that your device runs **KernelSU** or **APatch**.
2. Download the latest `meta-magic_mount-rs-*.zip` release.
3. Flash the module in your root manager.
4. Reboot your device.

---

## Configuration & Usage

Settings are stored in `/data/adb/magic_mount/config.toml`:
```toml
mountsource = "KSU"
umount = false
partitions = ["system", "vendor", "product"]
```
- **mountsource**: Mount source identifier (defaults to `"KSU"`).
- **umount**: Whether to attempt unmounting from DenyList apps via KernelSU umount.
- **partitions**: Array of partitions targeted for systemless overlays.

---

## Troubleshooting & Common Issues

- **Mount Fails with Error**: The target path in custom bind rules must be an absolute path and must not contain relative `..` segments. If a mount operation fails, the engine safely rolls back.
