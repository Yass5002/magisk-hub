---
id: "aurora"
title: "Aurora: System-Wide Transparent Proxy Launcher for Sing-Box & Mihomo"
sidebarTitle: "Aurora Proxy"
description: "Deploys high-performance proxy engines (sing-box, mihomo) systemlessly, establishing transparent routing via TProxy and TUN network interfaces."
category: "networking-proxies"
tier: 1
searchQueries:
  - "aurora magisk module"
  - "tkocean aurora proxy"
  - "sing-box transparent proxy android root"
  - "mihomo tproxy kernelsu"
  - "systemwide vpn routing magisk"
prerequisites:
  - "Android 12 or newer"
  - "Root access via Magisk, KernelSU, or APatch"
  - "Kernel supporting iptables/nftables and TProxy / TUN socket options"
conflicts: []
configPaths:
  - "/data/adb/modules/aurora/"
  - "/data/adb/aurora/"
features:
  - "Dual proxy core deployment: integrates sing-box and mihomo binaries for modern multi-protocol proxy routing"
  - "Advanced network modes: supports high-throughput TProxy (TCP + UDP) and TUN virtual interface routing"
  - "Automated firewall rule management: applies and clears iptables routing tables dynamically during startup and teardown"
  - "Modular configuration structure: custom configuration files stored safely under /data/adb/aurora/ across updates"
---

## Overview

Configuring system-wide transparent proxy routing on Android typically involves third-party VPN apps that require persistent foreground notifications, consume battery through Android's VpnService abstraction layer, and frequently drop connections during network handoffs.

Developed by Tkocean, **Aurora** transforms an Android device into a native routing gateway. Operating directly at the Linux networking layer through Magisk, KernelSU, or APatch, Aurora orchestrates modern proxy cores—specifically **sing-box** and **mihomo**—to handle all system inbound and outbound network packets using kernel-level TProxy and TUN socket tables.

## Network Routing Modes

Aurora routes traffic systemlessly without utilizing Android's battery-intensive `VpnService` API:

- **TProxy (TCP + UDP)**: Intercepts network packets at the kernel netfilter stage and redirects them to the local proxy port while preserving the original packet headers and destination IP addresses.
- **TUN Virtual Adapter**: Allocates a virtual network interface managed directly by the proxy core, providing complete protocol coverage for applications that bypass standard socket tables.

## Directory Structure & Configuration

Core binaries, scripts, and runtime files are isolated in the module tree, while persistent user configurations are stored in `/data/adb/aurora/`:

- **`/data/adb/aurora/config/`**: Directory where your custom `sing-box` (`config.json`) or `mihomo` (`config.yaml`) configuration files reside.
- **`/data/adb/aurora/scripts/`**: Network init scripts handling iptables rules, routing policy databases (ip rule), and interface lifecycle.

## Installation & Setup

1. Ensure your device is running **Android 12** or higher with a compatible root manager.
2. Download and flash the **Aurora** `.zip` package.
3. Place your proxy configuration file (sing-box JSON or mihomo YAML) into `/data/adb/aurora/`.
4. Reboot the device. The background daemon will start automatically and apply kernel routing tables.

## Troubleshooting

- **No Internet Connectivity After Boot**: If network traffic fails to resolve, verify that your proxy configuration contains valid server endpoints and that your DNS upstream is reachable without proxy routing.
- **Kernel Lacks TProxy Support**: If logcat indicates iptables failures (`No chain/target/match by that name`), your kernel may lack `xt_TPROXY` modules; switch your configuration mode to TUN in the module configuration.
