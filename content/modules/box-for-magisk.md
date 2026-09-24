---
id: "box-for-magisk"
title: "Box for Magisk: Transparent Core Proxy Platform (Sing-box / Xray / Clash)"
sidebarTitle: "Box for Magisk"
description: "Systemless proxy suite turning rooted Android into a transparent gateway using Sing-box, Xray, V2Ray, and Clash with native iptables routing."
category: "networking-proxies"
tier: 1
searchQueries:
  - "box for magisk guide"
  - "transparent proxy rooted android"
  - "sing box magisk module"
  - "clash for magisk transparent proxy"
  - "taamarin box for magisk download"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "Linux kernel with iptables, tproxy, and cgroup socket matching enabled"
conflicts:
  - "Other transparent proxy modules (e.g. clash-for-magisk, NetProxy) running simultaneously"
configPaths:
  - "/data/adb/box/"
  - "/data/adb/box/scripts/box.config"
features:
  - "Multi-core architecture: supports Sing-box, Xray-core, V2Ray-core, and Clash.Meta (Mihomo)"
  - "True systemless transparent proxying using kernel `TPROXY` and `REDIRECT` iptables/nftables rules"
  - "Per-app proxy routing via Android UID filtering and cgroup matching"
  - "Zero reliance on Android's VpnService API: keeps VPN slot free and eliminates VPN connection notifications"
faq:
  - question: "How does transparent proxying differ from standard VPN apps?"
    answer: "Android VPN apps use the Android VpnService framework, which creates a virtual tun interface in userspace, displays a persistent key icon in the status bar, and can be easily blocked or detected by anti-proxy applications. Box for Magisk operates directly at the Linux kernel packet routing level (iptables/nftables), transparently rerouting outbound TCP/UDP packets through your proxy core without Android even knowing a proxy is running."
  - question: "Where do I put my proxy subscription or config file?"
    answer: "Place your configuration file in /data/adb/box/clash/config.yaml (if using Clash/Mihomo) or /data/adb/box/sing-box/config.json (if using Sing-box). You can edit these directly in Termux or using any root file explorer."
---

## Overview

Maintained by **taamarin**, **Box for Magisk** is an all-in-one transparent proxy infrastructure for rooted Android devices.

Unlike typical client applications that route traffic through Android's `VpnService` interface, Box for Magisk utilizes native Linux networking tools (**iptables**, **nftables**, **ip route**, and **cgroups**) to route network traffic directly into high-performance proxy cores: **Sing-box**, **Xray**, **V2Ray**, or **Mihomo (Clash.Meta)**. This delivers zero-latency proxying, bypasses VPN detection, and leaves your device's single VPN slot completely free for work or local adblockers.

---

## Technical Architecture & How It Works

### Kernel TPROXY & Cgroup Redirection

1. **Traffic Interception**: During boot or when started via `service.sh`, Box for Magisk configures iptables/nftables PREROUTING and OUTPUT chains.
2. **UID-Based Rules**: It inspects Android app UIDs. You can configure:
   - Global mode: All apps routed through proxy.
   - Whitelist mode: Only specified apps (e.g. browsers, social media, messaging).
   - Blacklist mode: Bypass proxy for local banking or gaming apps to minimize latency.
3. **Loopback Avoidance**: Using Linux `cgroup` marks, packets originating from the proxy core itself are marked and exempted from redirection, preventing infinite routing loops.
4. **DNS Leak Prevention**: Intercepts port 53 (UDP/TCP) DNS traffic, routing queries through fake-ip or encrypted DNS (DoH/DoT) resolvers configured inside the proxy core.

---

## Installation & Setup

1. Open your root manager (**Magisk**, **KernelSU**, or **APatch**).
2. Download and flash the latest `box4magisk-vX.zip`.
3. Reboot your device.
4. Add your configuration:
   - For Sing-box: `/data/adb/box/sing-box/config.json`
   - For Clash: `/data/adb/box/clash/config.yaml`
5. Edit `/data/adb/box/scripts/box.config` to choose your active core:
   ```bash
   bin_name="sing-box" # or "clash" or "xray"
   network_mode="tproxy" # or "redirect"
   proxy_mode="whitelist" # or "blacklist" or "global"
   ```

---

## Control Commands (CLI)

Manage the service from **Termux** or any root terminal:
```bash
# Start proxy service
su -c "/data/adb/box/scripts/box.service start"

# Stop proxy service
su -c "/data/adb/box/scripts/box.service stop"

# Restart proxy service
su -c "/data/adb/box/scripts/box.service restart"

# View real-time connection log
su -c "tail -f /data/adb/box/run/box.log"
```
