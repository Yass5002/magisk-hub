---
title: "What is Magisk?"
description: "An introduction to Magisk, its systemless architecture, core features, and how it works."
---

**Magisk** is an open-source suite of tools for customizing Android, created and maintained by John Wu ([@topjohnwu](https://github.com/topjohnwu)). It is the de-facto standard solution for Android root access, operating systemlessly without modifying the device's physical `/system` or `/vendor` partitions.

By leaving physical partitions intact, Magisk allows users to gain root permissions, install powerful system mods, and pass system integrity checks.

---

## Features

### Systemless Modifications
Magisk does not modify read-only system partitions directly. Instead, it injects modifications at boot time using overlay filesystems. This ensures your partitions remain clean and allows seamless uninstallation or updates.

### MagiskSU (Root Management)
A built-in root manager that provides root access to apps requesting elevated privileges. MagiskSU gives users granular control over which apps are granted root, with timeout management, logging, and biometrics confirmation.

### Magisk Modules
A modular framework for system modifications. Modules can modify system files, inject audio configurations, replace fonts, add system apps, and customize framework behavior without directly touching system files.

### Zygisk
Zygote-level code injection framework. Zygisk allows module developers to run code directly within every Android app's process through the Android Zygote daemon.

### DenyList
A built-in security feature that hides Magisk and root permissions from selected applications, helping prevent detection by security-sensitive applications such as banking and enterprise apps.

---

## How Magisk Works

```
[Device Power On]
       │
       ▼
[Bootloader verifies & loads boot.img / init_boot.img]
       │
       ▼
[Magiskinit intercepts early boot process]
       │
       ├─ Sets up overlay mounts
       ├─ Injects Magisk binary & rules
       └─ Restores original init
       │
       ▼
[Normal Android system boot with Magisk services active]
```

1. **Ramdisk Injection**: When you install Magisk, it patches your stock `boot.img` (or `init_boot.img` on Android 13+) to include `magiskinit`.
2. **Early Boot Interception**: When the device boots, the kernel executes `magiskinit` before the Android `init` system starts.
3. **Overlay & SELinux Policy**: `magiskinit` sets up overlay file systems, patches SELinux policies in memory, and hands control over to the system `init`.
4. **Daemon Launch**: Once system boots, the `magiskd` daemon handles root requests, module mounting, and Zygisk hooks.

---

## Getting Started

To get started with Magisk on your Android device:

1. **[Universal Installation Overview](/magisk/guide/overview)** – Understand the general workflow, partition checks, and safety net recovery.
2. **[Download Magisk](/magisk/guide/download)** – Download the latest official Magisk APK from GitHub releases.
3. **Unlock Your Bootloader**:
   - [Xiaomi / Redmi / POCO](/magisk/unlock/xiaomi)
   - [Google Pixel](/magisk/unlock/pixel)
   - [OnePlus (Snapdragon)](/magisk/unlock/oneplus-snapdragon) / [OnePlus (MediaTek)](/magisk/unlock/oneplus-mediatek)
   - [Realme (Snapdragon)](/magisk/unlock/realme-snapdragon) / [Realme (MediaTek)](/magisk/unlock/realme-mediatek)
   - [Motorola](/magisk/unlock/motorola)
   - [Samsung Galaxy](/magisk/unlock/samsung)
4. **Choose Your Device Guide**:
   - **Xiaomi / Redmi**: [boot.img Guide](/magisk/install/xiaomi-boot) · [init_boot.img Guide](/magisk/install/xiaomi-init-boot)
   - **Google Pixel**: [boot.img Guide](/magisk/install/pixel-boot) · [init_boot.img Guide](/magisk/install/pixel-init-boot)
   - **OnePlus**: [boot.img Guide](/magisk/install/oneplus-boot) · [init_boot.img Guide](/magisk/install/oneplus-init-boot)
   - **Realme**: [boot.img Guide](/magisk/install/realme-boot) · [init_boot.img Guide](/magisk/install/realme-init-boot)
   - **Motorola**: [boot.img Guide](/magisk/install/motorola-boot) · [init_boot.img Guide](/magisk/install/motorola-init-boot)
   - **Samsung**: [boot.img Guide](/magisk/install/samsung-boot) · [init_boot.img Guide](/magisk/install/samsung-init-boot)
   - **Locked Bootloader**: [LightSpeed Virtual Machine Guide](/magisk/install/virtual-machine)
