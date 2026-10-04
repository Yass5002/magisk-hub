---
id: "kernelsu"
title: "KernelSU: Next-Generation Kernel-Based Root Solution for Android"
sidebarTitle: "KernelSU"
description: "Revolutionary root solution by weishu/tiann operating in kernel space (Ring 0) with per-UID credential delegation, App Profile sandboxing, and OverlayFS module mounting."
category: "root-management"
tier: 1
searchQueries:
  - "kernelsu apk manager download"
  - "kernelsu gki installation guide"
  - "kernelsu vs magisk root"
  - "flash kernelsu boot image"
  - "kernelsu overlayfs modules"
prerequisites:
  - "Android GKI 2.0 device with Linux kernel 5.10, 5.15, or 6.1 (Legacy 4.14/4.19 kernels require custom kernel builds)"
  - "Unlocked bootloader and Fastboot flashing tools"
conflicts:
  - "Running concurrent Magisk su daemons on the same boot image"
  - "Custom kernels compiled without OverlayFS or kprobes support"
configPaths:
  - "/data/adb/ksu/"
  - "/data/adb/modules/"
  - "/data/adb/ksud"
features:
  - "Kernel-space su delegation: su binary only exists for whitelisted UIDs; ungranted apps observe zero traces of root"
  - "Hardware App Profiles: restrict root permissions per application, isolating capabilities, mount namespaces, and SELinux domains"
  - "Native OverlayFS mounting: replaces userspace magic mount with Linux kernel OverlayFS for faster, cleaner systemless overlays"
  - "GKI 2.0 universal boot patching: flashable across any standard Android 12, 13, 14, or 15 GKI device without custom ROM compilation"
faq:
  - question: "How do I check if my device supports KernelSU officially?"
    answer: "Open a terminal or run `uname -r`. If your kernel version is `5.10.x-android12-...`, `5.15.x-...`, or `6.1.x-...` (with the `-androidXX` GKI signature), your device is an official GKI 2.0 device supported out-of-the-box. Older 4.14 and 4.19 devices require building KernelSU source into a custom kernel."
  - question: "Why is KernelSU inherently stealthier than Magisk?"
    answer: "Magisk operates primarily in userland (Ring 3) by placing a global `su` binary on the file system and running background daemons that attempt to hide from detection lists. KernelSU operates in the Linux kernel (Ring 0): the kernel intercepts system calls directly and modifies the process credentials (`struct cred`) only for approved UIDs. Unapproved applications see no `su` binaries, no altered mounts, and no abnormal open sockets."
  - question: "How do I recover from a bootloop caused by an incompatible KernelSU module?"
    answer: "KernelSU provides built-in Safe Mode: during device boot, repeatedly press the Volume Down key as the OEM logo appears. KernelSU will detect key events and disable all third-party modules. Alternatively, flash your stock `boot.img` or `init_boot.img` via fastboot to restore a completely unrooted system."
---

## Overview

For nearly a decade, Magisk defined the state-of-the-art for Android rooting through its "systemless" userland architecture. However, as Google introduced hardware-backed security, strict SELinux policies, and anti-root heuristics in banking applications, hiding a userland `su` daemon running in Ring 3 became an endless cat-and-mouse game.

**KernelSU**, conceived and developed by renowned Android security engineer weishu (tiann), redefines Android rooting by moving privilege management into the **Linux Kernel (Ring 0)**.

Instead of running an always-on `magiskd` daemon in userspace, KernelSU patches the kernel directly. When an application attempts to gain superuser privileges, the kernel itself checks an internal UID authorization table and modifies process credentials (`uid`, `gid`, `capabilities`) in-place. Applications that have not been explicitly granted root cannot detect its presence through file system scans, socket inspections, or memory probes.

---

## Technical Architecture: Ring 0 vs Ring 3 Root

- **Application Layer (Userspace)**:
  - **Authorized Root App (UID)**: Granted full root shell access and custom App Profile mount namespaces.
  - **Non-Root App (e.g. Banking App)**: Stock environment; `su` binary does not exist in filesystem; clean mounts and unmodified process table.
- **Linux Kernel Space (Ring 0)**:
  - **KernelSU Core Engine**: Intercepts `sys_execve` and privilege escalation system calls directly in kernel code.
  - **Credential Elevation**: Overrides `struct cred` exclusively for authorized caller UIDs.
  - **OverlayFS Systemless Layering**: Merges systemless partitions at the Virtual File System (VFS) layer.

### 1. Zero File System Exposure
In KernelSU, the `su` binary does not exist on `/system/bin` or standard PATH directories for normal apps. When an unauthorized app attempts to run `which su` or `stat("/system/xbin/su")`, the kernel returns `ENOENT` (No such file or directory).

### 2. Linux Kernel OverlayFS
Rather than creating complex bind-mount hierarchies ("magic mount") in userspace, KernelSU leverages the Linux kernel's native **OverlayFS**. Modifications placed in `/data/adb/modules/<id>/system/` are merged directly with `/system` at the VFS (Virtual File System) layer, yielding instantaneous mount performance and pristine directory trees.

### 3. App Profile Security Isolation
KernelSU allows "caging" the root privilege:
- Restrict which Linux capabilities (e.g. `CAP_NET_ADMIN`, `CAP_SYS_ADMIN`) an app can exercise.
- Grant root inside a sandboxed mount namespace without exposing global storage.
- Enforce specific SELinux domain transitions.

---

## Installation Guide (GKI 2.0 Devices)

### Step 1: Verify GKI Compatibility
Ensure your device runs an Android 12, 13, 14, or 15 GKI kernel:
```bash
adb shell uname -r
# Expected output example: 5.10.198-android12-9-g8a3...
```

### Step 2: Patch & Flash Boot Image
1. Download the official **KernelSU Manager** (`KernelSU_v*.apk`) and install it.
2. Obtain your device's stock `boot.img` (or `init_boot.img` for devices launched with Android 13+).
3. Transfer the image to your phone and open the KernelSU app.
4. Tap **Install** -> Select and patch a file -> Choose your stock boot image.
5. Transfer the patched image (`kernelsu_boot.img`) back to your computer.
6. Reboot to bootloader and flash via Fastboot:
   ```bash
   fastboot flash boot kernelsu_boot.img
   # (Or for init_boot devices):
   fastboot flash init_boot kernelsu_boot.img
   fastboot reboot
   ```

---

## Managing Modules & Safe Mode Recovery

KernelSU supports standard flashable Magisk modules that adhere to modern systemless layouts. Modules are placed into `/data/adb/modules/`.

### Built-in Hardware Safe Mode
If a faulty module prevents Android from completing boot:
1. Turn off your device.
2. Press Power to turn on.
3. As soon as the manufacturer logo appears, press the **Volume Down** key multiple times until you feel vibration.
4. KernelSU will trap the key event, set the global module disable flag, and boot into Safe Mode with all modules deactivated.

### Fastboot Rescue
If Safe Mode fails, simply re-flash your original stock `boot.img` via fastboot to restore stock unrooted operation with zero data loss.
