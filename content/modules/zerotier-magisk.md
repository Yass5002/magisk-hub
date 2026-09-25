---
id: "zerotier-magisk"
title: "ZeroTier for Magisk: Systemless Mesh VPN Daemon & Controller"
sidebarTitle: "ZeroTier for Magisk"
description: "Systemless ZeroTier One background daemon for Magisk by eventlOwOp, establishing secure P2P mesh network connections without occupying Android's VPN slot."
category: "networking-proxies"
tier: 1
searchQueries:
  - "zerotier magisk module"
  - "eventlowop zerotier-magisk"
  - "zerotier without vpn slot android"
  - "self hosted zerotier planet root android"
  - "zerotier-one android background daemon"
prerequisites:
  - "Android 9.0 (API 28) or newer"
  - "ARMv7-A or ARMv8-A (AArch64) processor architecture"
  - "Rooted Android device with Magisk"
  - "Companion Controller APK installed (for graphical UI management)"
conflicts: []
configPaths:
  - "/data/adb/zerotier/"
  - "/data/adb/zerotier/home/planet"
  - "/data/adb/modules/zerotier-magisk/"
features:
  - "Daemon-level mesh execution: runs the native `zerotier-one` binary directly on boot as a Linux system daemon"
  - "Non-exclusive network operation: creates a virtual network interface without claiming Android's system VpnService, permitting concurrent use of traditional VPNs"
  - "Custom Moon & Planet support: supports self-hosted root infrastructure by replacing the local `planet` definition file"
  - "Zero-privilege controller: configure 16-character Network IDs and monitor connection states via an unprivileged companion application"
---

## Overview

ZeroTier for Magisk, developed by eventlOwOp, ports the enterprise peer-to-peer (P2P) mesh networking daemon `zerotier-one` directly to rooted Android devices. Standard user-space ZeroTier clients for Android utilize the system's `VpnService` API, which forces Android to treat ZeroTier as a standard VPN—monopolizing the single available VPN slot and preventing users from running privacy VPNs, WireGuard profiles, or local DNS adblockers simultaneously.

This Magisk module launches `zerotier-one` at the Linux kernel and network stack level. It initializes a persistent virtual Ethernet interface on boot, allowing your Android phone to participate directly in private, encrypted LANs across mobile data and Wi-Fi networks without occupying the system VPN slot.

## Prerequisites & Compatibility

- **Android Version**: Android 9.0 (Pie, API 28) and newer.
- **CPU Architecture**:
  - `arm64-v8a` (AArch64)
  - `armeabi-v7a` (32-bit ARM)
- **Root Solution**: Magisk (stable or canary).

There are no documented module conflicts; it coexists peacefully alongside third-party VPN apps and firewall managers.

## Key Architecture & Features

- **Background Daemon**: The native daemon launches during late boot (`service.sh`) and maintains lightweight, peer-to-peer UDP punch-through connections to remote nodes (laptops, home NAS, servers).
- **Private Root Servers (Planets & Moons)**: For users operating private, self-hosted ZeroTier controllers (such as ztncui or custom planet definitions), custom network topology files can be deployed directly to `/data/adb/zerotier/home/planet`.
- **SSO Integration**: The AArch64 GCC build supports single sign-on authentication (`zeroidc`) for enterprise identity verification.

## Installation & Configuration

1. Download the `zerotier-magisk.zip` module package and the companion `controller.apk` from the GitHub releases page.
2. Install the module in Magisk Manager and install the Controller APK as a standard user application.
3. Reboot your device to initialize the networking daemon.
4. Launch the **ZeroTier Controller** app:
   - Enter your 16-character ZeroTier Network ID.
   - Tap **Join**.
5. Log into your ZeroTier network management web console (e.g. `my.zerotier.com`) and authorize the new Android node.
6. The Android device will receive a private IP address and can immediately ping or access services across the mesh network.
7. Active daemon states, keys, and planet configurations reside in:
   ```bash
   /data/adb/zerotier/
   ```

## Troubleshooting & Verification

- **Node Not Appearing in ZeroTier Console**:
  - Verify that the daemon is active from an ADB root shell:
    ```bash
    su -c zerotier-cli status
    # Should return: 200 info <node_id> <version> ONLINE
    ```
- **Custom Planet Not Loading**: If using a custom root server, place your compiled `planet` binary in `/data/adb/zerotier/home/planet`, restart the daemon (`su -c killall zerotier-one`), and verify connectivity using `zerotier-cli peers`.
