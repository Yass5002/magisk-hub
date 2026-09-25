---
id: "wadbd"
title: "Wireless ADB Controller: Persistent Wi-Fi Debugging, Key Management & WebUI"
sidebarTitle: "Wireless ADB Controller (wadbd)"
description: "Controls the Android wireless ADB daemon via CLI or WebUI, providing persistent boot listeners, customizable network ports, and cryptographic ADB key import/export tools."
category: "system-utilities"
tier: 1
searchQueries:
  - "wireless adb controller magisk module"
  - "rhythmcache wadbd"
  - "persistent wireless adb android root"
  - "wadbd enable on boot"
  - "import adbkey pub android root"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
  - "Android device connected to a local Wi-Fi or hotspot network"
  - "Terminal emulator (e.g., Termux) or WebUI-capable root manager"
conflicts: []
configPaths:
  - "/data/adb/modules/wadbd/"
features:
  - "Session & persistent control: toggle wireless ADB instantly or configure automatic background startup across system reboots"
  - "Custom network port binding: specify arbitrary listening ports (defaults to 5555) to avoid network conflicts"
  - "Pre-authorized key management: import adbkey.pub files directly onto the device to authenticate developer workstations without confirmation popups"
  - "Credential security utilities: backup, restore, or purge all authorized ADB cryptographic keys via single-line commands"
  - "WebUI integration: includes an interactive dashboard for KernelSU, APatch, and MMRL interfaces"
---

## Overview

While Android includes native Developer Options for wireless ADB debugging, the stock implementation resets its network port after every disconnect and disables the service upon reboot. For developers, testers, and automated home lab rigs, manually toggling developer settings and re-pairing devices daily is an exercise in frustration.

Developed by rhythmcache, **Wireless ADB Controller (wadbd)** provides persistent, programmatic management over Android's native `adbd` service. Through a unified command-line utility (`wadbd`) and an interactive WebUI, users can pin wireless ADB to standard or custom ports, authorize development machines silently by importing public keys, and automate debugging availability across reboots.

## Command-Line Usage

Open Termux or an ADB root shell and invoke `wadbd` with superuser privileges (`su -c wadbd <subcommand>`):

### Daemon Control
```bash
# Start wireless ADB on default port (5555)
su -c wadbd on

# Start wireless ADB on a custom port
su -c wadbd on 5556

# Stop wireless ADB daemon
su -c wadbd off

# Inspect active status, IP address, and listening port
su -c wadbd status
```

### Boot Automation
```bash
# Enable wireless ADB automatically on device boot on port 5555
su -c wadbd enable-on-boot

# Enable on boot with a specific port
su -c wadbd enable-on-boot 5556

# Disable automatic startup on boot
su -c wadbd disable-on-boot
```

### ADB Key & Authentication Management
Standard wireless debugging requires tapping "Always allow from this computer" on the smartphone screen. `wadbd` allows you to inject public keys directly:

```bash
# Import a public key (adbkey.pub) from your development PC
su -c wadbd --import-key /sdcard/Download/adbkey.pub

# Backup current authorized ADB keys to storage
su -c wadbd --backup /sdcard/Download/adb_keys_backup

# Restore keys from a previous backup
su -c wadbd --restore /sdcard/Download/adb_keys_backup

# Revoke and delete all stored authorization keys
su -c wadbd --clear-keys
```

## Graphical Interface (WebUI)

For devices running **KernelSU**, **APatch**, or **MMRL**, `wadbd` provides a touch-friendly WebUI control center:
- Toggle wireless ADB on and off with a single tap.
- Inspect real-time device IP addresses and active port allocations.
- Manage persistent boot state without typing terminal commands.

## Installation & Setup

1. Flash the `wadbd` `.zip` in Magisk, KernelSU, or APatch.
2. Reboot the device.
3. Open Termux, acquire root with `su`, and execute `wadbd on` or access the WebUI directly inside your root manager.
4. From your development workstation, connect directly:
   ```bash
   adb connect <device-ip>:5555
   ```

## Security Best Practices

> [!IMPORTANT]
> Enabling wireless ADB opens a network listening socket on your local network. When connecting to untrusted public Wi-Fi networks (cafes, airports), disable wireless debugging using `su -c wadbd off` or configure a custom port to prevent unauthorized network scanning and access.
