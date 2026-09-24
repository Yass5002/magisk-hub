---
id: "netproxy-magisk"
title: "NetProxy: Full-Featured Sing-Box Transparent Proxy & WebUI"
sidebarTitle: "NetProxy"
description: "Sing-box transparent proxy engine featuring an interactive on-device WebUI dashboard, automatic subscription updates, and smart routing."
category: "networking-proxies"
tier: 1
searchQueries:
  - "netproxy magisk module"
  - "sing box webui rooted android"
  - "transparent proxy webui magisk"
  - "fanju6 netproxy download"
  - "sing-box dashboard android"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "Sing-box subscription or compatible JSON config"
conflicts:
  - "Other transparent proxy modules (e.g. Box for Magisk, Clash for Magisk) active simultaneously"
configPaths:
  - "/data/adb/modules/netproxy-magisk/"
  - "/data/adb/netproxy/"
features:
  - "Embedded lightweight WebUI dashboard accessible via mobile browser on `http://127.0.0.1:9090`"
  - "High-performance native Sing-box core with support for Shadowsocks, VLESS, VMess, Trojan, and Hysteria2"
  - "Automated remote subscription updating on scheduled intervals"
  - "Smart rule-based routing: automatically split direct domestic traffic and proxied international traffic"
faq:
  - question: "How do I access the NetProxy WebUI?"
    answer: "After flashing and starting the module, open your mobile browser (Chrome/Firefox) and navigate to http://127.0.0.1:9090 (or tap the WebUI shortcut in KernelSU / Magisk App if supported)."
  - question: "Can I use Hysteria2 and TUIC protocols?"
    answer: "Yes. NetProxy packages the latest multi-protocol Sing-box binary with full UDP/QUIC support and TPROXY routing enabled."
---

## Overview

Developed by **Fanju6**, **NetProxy-Magisk** is a cutting-edge proxy suite bringing the speed and flexibility of **Sing-box** to rooted Android devices with a polished, built-in WebUI management dashboard.

Managing command-line proxy modules can be tedious on a mobile phone. NetProxy bridges this gap by bundling an on-device local web dashboard. Users can import remote subscription links, toggle nodes, view live traffic graphs, and inspect active TCP/UDP connections directly from their mobile browser without touching a terminal.

---

## Technical Architecture & How It Works

### High-Performance Sing-box TPROXY Gateway

1. **Kernel Routing Setup**: NetProxy initializes Linux `ip rule` and `iptables` / `nftables` tables on boot.
2. **Sing-box Engine**: Launches the compiled Sing-box binary as a supervised root background daemon.
3. **Inbound TPROXY**: Intercepts outbound device traffic using Linux kernel TPROXY (Transparent Proxy), preserving original source and destination IP addresses.
4. **Local WebUI Dashboard**: Serves an on-device responsive web dashboard over localhost (`127.0.0.1:9090`), exposing node selection, latency testing, routing rule management, and real-time connection logs.

---

## Installation & Quickstart

1. Flash `NetProxy-vX.zip` in **Magisk**, **KernelSU**, or **APatch**.
2. Reboot your device.
3. Open your mobile browser and visit:
   `http://127.0.0.1:9090`
4. Paste your Sing-box subscription URL into the **Subscription** tab and tap **Update**.
5. Select your desired node and toggle **Proxy Status** to ON.
