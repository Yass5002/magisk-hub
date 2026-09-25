---
id: "magicnet"
title: "MagicNet: Root-Controlled Sing-Box Proxy Engine with TUN & eBPF"
sidebarTitle: "MagicNet"
description: "High-performance transparent proxy engine powered by a customized sing-box fork that routes Android traffic via TUN or eBPF without occupying the system VPN slot."
category: "networking-proxies"
tier: 1
searchQueries:
  - "magicnet magisk module"
  - "lightjunction magicnet sing-box"
  - "ebpf transparent proxy android root"
  - "sing-box proxy without vpn slot"
  - "magicnet cli commands"
prerequisites:
  - "Rooted Android device running Magisk, KernelSU, or APatch"
  - "Android 'Private DNS' must be set to OFF (not Automatic)"
  - "Valid proxy subscription (HTTPS URL, Clash YAML, or sing-box JSON)"
conflicts: []
configPaths:
  - "/data/adb/modules/MagicNet/"
  - "/data/adb/modules/MagicNet/cli"
features:
  - "VPN-less transparent proxy: routes device network traffic through a customized sing-box core without consuming Android's system VpnService slot"
  - "Dual traffic engines: switch explicitly between TUN mode (`magicnet0`) and kernel-level eBPF packet redirection with automatic failure rollback"
  - "Universal subscription intake: supports up to five simultaneous sources across remote HTTPS links, Clash/Mihomo YAML, sing-box JSON, and base64 strings"
  - "Per-app policy routing: assign applications into Proxy, Direct, or Bypass groups with hotspot tethering sharing support"
  - "Rich administration tooling: full-featured multilingual WebUI, comprehensive terminal CLI (`cli`), and authenticated MCP server integration"
---

## Overview

MagicNet, developed by LIghtJUNction, is a powerful transparent proxy and traffic management suite for rooted Android devices. Built on top of a customized fork of the open-source `sing-box` network core, MagicNet intercepts and routes network traffic directly at the Linux kernel level.

Unlike user-space VPN apps that occupy Android's single system VPN slot—preventing users from running local adblockers, WireGuard, or enterprise VPN clients simultaneously—MagicNet operates invisibly behind the scenes. It transparently captures and routes packets using either a virtual TUN interface or Linux extended Berkeley Packet Filters (eBPF), leaving the system VPN slot completely available for other applications.

## Prerequisites & Critical Setup Rules

1. **Root Manager**: Compatible with Magisk, KernelSU, and APatch.
2. **Mandatory Android Setting**: Navigate to **Settings > Network & internet > Private DNS** and turn it **OFF**. Leaving Private DNS on "Automatic" causes DNS leaks and routing blackholes because Android's DNS resolver will attempt to bypass local transparent proxy ports.
3. **Proxy Node Access**: MagicNet is a proxy client engine; users must provide their own authorized proxy nodes or subscription links.

There are no documented module conflicts.

## Architecture: TUN vs eBPF Modes

MagicNet allows users to toggle between two routing mechanisms:

- **TUN Mode (Default)**: Creates a virtual network adapter named `magicnet0`. Inbound and outbound packets are forwarded through `magicnet0` to the sing-box core via policy routing. Recommended for general compatibility across all devices and kernels.
- **eBPF Mode**: Utilizes modern Linux kernel eBPF cgroup and Traffic Control (TC) filters to intercept socket connections directly at the socket layer. eBPF mode reduces packet copying overhead and lowers battery consumption on compatible kernels. If eBPF initialization fails, MagicNet automatically rolls back to TUN mode.

## Installation & Configuration

1. Download the latest release from the official repository and flash it through your root manager.
2. Ensure Android **Private DNS is disabled**.
3. Reboot your device.
4. Open the MagicNet WebUI from your manager interface (or via WebUI X / MMRL on Magisk).
5. In the **Subscriptions** tab, add your subscription URL or import a local Clash/Mihomo YAML file.
6. Save and start the service.
7. Active module assets and binary tools reside in:
   ```bash
   /data/adb/modules/MagicNet/
   ```

## CLI Management & Diagnostics

MagicNet provides a comprehensive command-line utility accessible via `su`:

- **Check Service Health & Interfaces**:
  ```bash
  su -c /data/adb/modules/MagicNet/cli health
  ```
- **Inspect Transparent Proxy Status**:
  ```bash
  su -c /data/adb/modules/MagicNet/cli transparent status
  ```
- **Quick Headless Setup**:
  ```bash
  su -c '/data/adb/modules/MagicNet/cli setup "https://your-subscription-url"'
  ```
- **Update Subscription & Core**:
  ```bash
  su -c /data/adb/modules/MagicNet/cli sub update sing-box
  ```

## Troubleshooting & Verification

- **No Internet Access After Enabling**:
  - Confirm that **Private DNS** is set to **Off** in Android settings.
  - Run the health check: `su -c /data/adb/modules/MagicNet/cli health`. If sing-box fails to start, verify that your subscription file contains valid node configurations.
- **Hotspot Clients Not Proxied**: In the WebUI under Hotspot settings, enable downstream proxy sharing so tethered laptops or secondary phones route through MagicNet's active proxy rules.
