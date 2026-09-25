---
id: "selinux-permissive"
title: "SELinux Permissive: Development Mode Switch with Detection Masking"
sidebarTitle: "SELinux Permissive"
description: "Developer utility by Denis Efremov that switches Android SELinux to permissive mode on boot while restricting sysfs read access and masking properties from non-root inspection."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "selinux permissive magisk module"
  - "evdenis selinux_permissive"
  - "switch selinux permissive android root"
  - "hide selinux permissive status"
  - "config_always_enforce samsung magisk"
prerequisites:
  - "Rooted Android device with Magisk"
  - "Linux kernel compiled without `CONFIG_ALWAYS_ENFORCE=y`"
conflicts:
  - "Stock Samsung kernels compiled with mandatory `CONFIG_ALWAYS_ENFORCE=y`"
configPaths:
  - "/data/adb/modules/selinux_permissive/"
features:
  - "Dual-stage execution: switches SELinux to permissive during early `post-fs-data` and ensures state retention during late `service` stage"
  - "Anti-detection measures: restricts world-read permissions on `/sys/fs/selinux/enforce` so unprivileged apps cannot read enforcement status"
  - "Property spoofing: leverages Magisk `resetprop` to spoof `ro.boot.selinux` to `enforcing`"
  - "Clean rollback logic: dedicated uninstaller restores original sysfs attributes and boot properties when the module is removed"
---

## Overview

SELinux Permissive, authored by kernel engineer Denis Efremov (`@evdenis`), is a specialized systemless module designed for developers, ROM porters, and root tool authors. In Android's standard enforcing mode, Security-Enhanced Linux (SELinux) blocks and audits any system action not explicitly declared in the device's sepolicy rules.

While invaluable for production device security, enforcing mode frequently blocks new device bring-ups, custom vendor HAL debugging, or complex instrumentation tools. This module switches SELinux to permissive mode on boot—allowing audited calls to proceed rather than failing—while simultaneously masking this status from standard user-space applications to reduce detection flags.

> [!WARNING]
> Permissive mode intentionally lowers the security boundaries of your device. Do not use this module on daily-driver devices containing sensitive banking credentials unless required for specific development or troubleshooting workflows.

## Prerequisites & Compatibility

- **Root Framework**: Magisk (stable or canary).
- **Kernel Support**: The device kernel must allow runtime mode switching.

### Documented Incompatibilities

- **Samsung Stock Kernels**: The module **will not work** on stock Samsung kernels compiled with `CONFIG_ALWAYS_ENFORCE=y` in their kernel configuration. Samsung's Knox security model prevents changing SELinux mode even when running with full root privileges. On these devices, a custom permissive-capable kernel must be flashed first.

## Architecture & Masking Mechanism

Standard permissive toggles simply run `setenforce 0`. However, banking apps and anti-cheat engines routinely check two common indicators to detect permissive devices:
1. They read the `/sys/fs/selinux/enforce` file directly.
2. They inspect the bootloader property `ro.boot.selinux`.

SELinux Permissive applies a hardened two-pronged approach:

1. **Permission Restriction**: In both `post-fs-data.sh` and `service.sh`, it executes `chmod 640 /sys/fs/selinux/enforce` or reassigns DAC ownership so that unprivileged apps receive a `Permission Denied` error when querying the node, rather than reading a `0` value.
2. **Property Masking**: Uses `resetprop` to overwrite `ro.boot.selinux` with `enforcing`, neutralizing straightforward property inspection checks.

## Installation & Verification

1. Download the latest release from the repository or Magisk repository.
2. Flash the module within Magisk Manager and reboot.
3. To verify current SELinux status from a root shell (`su`):
   ```bash
   getenforce
   # Returns: Permissive
   ```
4. Verify non-root access is restricted by running as a standard shell user without `su`:
   ```bash
   cat /sys/fs/selinux/enforce
   # Returns: Permission denied
   ```

## Uninstallation

To remove the module and revert SELinux to default enforcing security:
1. Uninstall the module via Magisk Manager.
2. The module's `uninstall.sh` automatically restores standard world-read permissions on `/sys/fs/selinux/enforce` and resets properties before the device reboots.
