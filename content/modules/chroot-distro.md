---
id: "chroot-distro"
title: "chroot-distro: GNU/Linux Distribution Manager for Android"
sidebarTitle: "chroot-distro"
description: "Powerful terminal utility for installing and running full GNU/Linux distributions (Debian, Arch, Ubuntu, Alpine) inside a native chroot environment on Android."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "chroot distro magisk module"
  - "run linux chroot android root"
  - "debian ubuntu on android chroot"
  - "chroot distro terminal manager"
  - "proot distro alternative root"
prerequisites:
  - "Rooted Android device (any root implementation)"
  - "BusyBox for Android NDK (v1.36.1 recommended; avoid v1.32.1)"
  - "Terminal environment: Termux, MT Manager, MiXplorer, or ADB shell"
conflicts:
  - "Stated plainly: No documented conflicts with other modules; requires functional BusyBox NDK binaries to download rootfs images"
configPaths:
  - "/data/local/chroot-distro/"
  - "/data/local/chroot-distro/.config/"
features:
  - "True chroot execution: runs Linux binaries with native kernel performance, eliminating the ptrace overhead of PRoot"
  - "Multi-distribution catalog: install Debian, Ubuntu, Arch Linux, Alpine, Fedora, and Kali Linux with simple commands"
  - "Automated filesystem isolation: mounts /dev, /dev/pts, /proc, /sys, and storage partitions into the container automatically"
  - "RAM disk optimization: support for binding container rootfs onto RAM disks for ultra-low I/O latency"
  - "Backup and restore: built-in archiving tools to export and restore installed Linux distributions"
faq:
  - question: "How does chroot-distro differ from Termux's proot-distro?"
    answer: "PRoot works without root by intercepting system calls with ptrace, which adds significant CPU overhead. chroot-distro uses Linux's native chroot system call, running Linux processes directly on the kernel with zero translation overhead and full root capabilities."
  - question: "Why is BusyBox for Android NDK required?"
    answer: "chroot-distro scripts rely on standard GNU/Linux command flags (in tar, wget, grep, and mount) that Android's default toybox/toolbox implementation does not support. Osm0sis's BusyBox NDK provides full POSIX command parity."
---

## Overview

Maintained by **Magisk-Modules-Alt-Repo**, **chroot-distro** is an advanced distribution deployment utility that brings native GNU/Linux operating systems to rooted Android devices.

Inspired by the workflow of PRoot Distro but designed for root users, chroot-distro leverages Linux's native `chroot` system call. This allows developers to run complete Linux server stacks, compilers, network analysis tools, and desktop environments at bare-metal speeds directly alongside Android.

---

## Technical Architecture & How It Works

### Native Containerization & Mount Namespaces

chroot-distro manages containerized environments under `/data/local/chroot-distro/`:

1. **Rootfs Bootstrapping**: Downloads minimal official rootfs tarballs for selected Linux distributions directly from upstream mirrors.
2. **System Node Binding**: Mounts virtual filesystems into the distribution root:
   - `/proc` and `/sys` for kernel state inspection.
   - `/dev` and `/dev/pts` for pseudoterminal handling and hardware access.
   - `/sdcard` or `/data/media/0` for shared storage access.
3. **Android Environment Bridges**: Bridges DNS configuration (`/etc/resolv.conf`) and user permissions between Android and the Linux container.

---

## Installation & Setup

1. Flash the **BusyBox for Android NDK** module (version 1.36.1 recommended).
2. Download and flash the `chroot-distro-*.zip` module in your root manager.
3. Open **Termux** or any root terminal app and run:
   ```bash
   su
   chroot-distro help
   ```

---

## Configuration & Usage

### Installing a Distribution
```bash
# List available distributions
chroot-distro list

# Install Debian or Ubuntu
chroot-distro install debian
```

### Entering the Linux Environment
```bash
chroot-distro login debian
```
Inside the container, you have a full standard APT package manager:
```bash
apt update && apt install python3 git build-essential htop
```

---

## Troubleshooting & Common Issues

- **Download or Extraction Fails**: Ensure you have installed BusyBox NDK. Using Android's stock Toybox `tar` command will fail on distribution symlinks and hardlinks.
- **Permission Denied on Android Storage**: To enable access to your phone's internal storage inside the chroot, configure `android_bind` in `/data/local/chroot-distro/.config/`.
