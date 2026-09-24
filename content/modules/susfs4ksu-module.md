---
id: "susfs4ksu-module"
title: "SUSFS: Kernel-Level Mount & Root Hiding for KernelSU & APatch"
sidebarTitle: "SUSFS"
description: "Kernel-level root hiding module utilizing kernel patch extensions to completely conceal mounts, paths, and process namespaces from userspace scanners."
category: "root-management"
tier: 1
searchQueries:
  - "susfs module kernelsu"
  - "susfs apatch guide"
  - "how to hide mounts with susfs"
  - "momo detection bypass susfs"
  - "kernel level root hiding"
prerequisites:
  - "Kernel compiled with SUSFS patches (e.g. `CONFIG_KSU_SUSFS=y`)"
  - "KernelSU or APatch manager installed"
conflicts:
  - "Stock unpatched kernels (module will exit with kernel unsupported warning)"
configPaths:
  - "/data/adb/susfs/"
  - "/data/adb/modules/susfs4ksu-module/"
features:
  - "Kernel-space mount point hiding: completely strips overlay and root mount entries from /proc/[pid]/mountinfo"
  - "Custom path hiding (`susfs_add_sus_path`): conceals custom directories and su binaries from readdir/stat calls"
  - "Kstat spoofing: hides abnormal ctime/mtime metadata on modified system files"
  - "Bypasses all advanced detection tools (Momo, Native Alpha, Applist Detector) without userspace ptrace hooks"
faq:
  - question: "Can I use SUSFS on standard Magisk?"
    answer: "No. Standard Magisk runs purely in userspace by patching init and ramdisk; it does not replace the Linux kernel. SUSFS requires a custom kernel compiled with specific kernel-level source code patches."
  - question: "How can I verify that SUSFS is active in my kernel?"
    answer: "Run `su -c 'which ksu_susfs'` or `su -c 'cat /proc/sys/fs/susfs/version'`. If the kernel has SUSFS enabled, it will output the version number (e.g., v1.5.x or newer)."
---

## Overview

Created by **sidex15**, **SUSFS** (Super User Secret File System) represents a generational leap in root concealment. 

Traditional hiding tools (like Shamiko or Magisk DenyList) operate in **userspace**. They rely on libc hooking, ptrace, or mount namespace unmounting within the target application's process. However, advanced anti-root engines can bypass userspace hooks by invoking direct raw assembly syscalls (e.g., `svc #0` in ARM64) to query the kernel directly, reading `/proc/self/mountinfo` or opening `/data/adb` directly.

SUSFS solves this by moving hiding logic directly into the **Linux Kernel**. Because the kernel is the ultimate authority over all filesystem and process queries, userspace applications cannot bypass kernel-level filtering regardless of what syscalls they execute.

---

## Technical Architecture & How It Works

### Kernel-Space Filesystem Interception

1. **VFS Syscall Hooking**: SUSFS patches core Virtual File System (VFS) functions in the Linux kernel:
   - `vfs_read` and `show_mountinfo`: Automatically filters out any mount point created by KernelSU or APatch before formatting `/proc/[pid]/mounts` or `/proc/[pid]/mountinfo`.
   - `vfs_statx` / `vfs_getattr`: Intercepts file attribute queries. When an app checks `/data/adb/ksu` or `/system/bin/su`, the kernel responds with `ENOENT` (No such file or directory) unless the calling process is a verified root manager.
2. **Kstat Spoofing**: Detection apps check inode metadata (modification dates, hardlink counts). SUSFS spoofs inode timestamps so system partitions appear unmounted and unmodified.
3. **Module Companion**: The `susfs4ksu-module` acts as the userspace bridge, reading module configurations at boot and sending `ioctl` commands to the kernel to register paths, loop devices, and processes that must be concealed.

---

## Prerequisites & Installation

### Step 1: Flash a SUSFS-Patched Kernel
Before installing this module, your device must be running a kernel built with SUSFS support:
1. Locate a custom kernel for your device model that includes SUSFS patches (e.g. WildKSU, GKI SUSFS, or your own compiled build).
2. Flash the kernel via fastboot or recovery:
   ```bash
   fastboot flash boot boot.img
   ```

### Step 2: Flash the SUSFS Module
1. Open **KernelSU** or **APatch**.
2. Go to **Modules** $\rightarrow$ **Install** $\rightarrow$ select `susfs4ksu-module-vX.zip`.
3. Reboot your device.

### Step 3: Verify Kernel Status
Run the following diagnostic command via terminal:
```bash
su -c "ksu_susfs show_version"
```
You should see: `ksu_susfs version: v1.5.x (or newer)`.

---

## Configuration & Custom Path Hiding

The module companion tool (`ksu_susfs`) allows dynamic configuration:

```bash
# Hide a specific custom path from untrusted apps:
su -c "ksu_susfs add_sus_path /data/local/tmp/my_tool"

# Hide a custom loop mount:
su -c "ksu_susfs add_sus_mount /system/etc/hosts"

# Check currently hidden mounts:
su -c "ksu_susfs show_sus_mount"
```
