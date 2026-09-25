---
id: "sam"
title: "SAM: Integrated SmartDNS, AdGuard Home & Mihomo Proxy Suite"
sidebarTitle: "SAM (DNS & Proxy)"
description: "Comprehensive 3-in-1 Magisk module by 5MayRain integrating SmartDNS, AdGuard Home, and Mihomo into a unified DNS filtering and transparent proxy pipeline."
category: "networking-proxies"
tier: 1
searchQueries:
  - "sam magisk module"
  - "5mayrain sam"
  - "smartdns adguard home mihomo android"
  - "transparent proxy adguard magisk"
  - "sam dns pipeline configuration"
prerequisites:
  - "Rooted Android device with Magisk, KernelSU, or APatch"
  - "Accessible ports for web administration panels"
conflicts:
  - "Concurrent standalone DNS forwarding modules or competing transparent proxy managers"
configPaths:
  - "/data/adb/modules/SAM/"
  - "/data/adb/modules/SAM/etc/mihomo/base.yaml"
features:
  - "Unified 3-in-1 network architecture: seamlessly interconnects SmartDNS, AdGuard Home, and Mihomo (Clash Meta) in a single root module"
  - "Dual pipeline topologies: toggle between `SmartDNS > Mihomo > AdGuardHome` and `SmartDNS > AdGuardHome > Mihomo` routing chains"
  - "Real-time hosts hot-reload: detects edits to system hosts files and reapplies DNS filter rules instantaneously without restarting daemons"
  - "Network interface and app exclusion: blacklist specific Wi-Fi networks and define per-application proxy routing rules"
  - "Web administration dashboards: accessible browser interfaces for monitoring AdGuard Home DNS queries and managing Mihomo proxy nodes"
---

## Overview

SAM (SmartDNS + AdGuardHome + Mihomo), developed by 5MayRain (棕果核), is a comprehensive networking, ad-blocking, and transparent proxy suite built for rooted Android platforms. While running standalone instances of DNS engines or proxy tools often leads to port conflicts, DNS routing loops, and battery drain, SAM orchestrates all three tools into a single, cohesive systemless pipeline.

Depending on your requirements, services can be run individually, paired together, or operated concurrently as a full filtering and proxy stack.

## Prerequisites & Compatibility

- **Root Framework**: Magisk, KernelSU, or APatch.
- **Port Availability**: Ensures ports 53 (DNS), 3000 (AdGuard Home web dashboard), and 9090 (Mihomo control) are not hijacked by other processes.

### Conflict Notice

Do not run SAM concurrently with other standalone transparent proxy modules (such as MagicNet or Surfing) or standalone DNS redirectors (such as AdGuardHomeForRoot). Running multiple modules attempting to bind port 53 or route iptables will result in network failure.

## Service Topologies & Priority Flow

SAM supports two primary routing structures:

1. **`SmartDNS > Mihomo > AdGuardHome`**:
   - Queries hit SmartDNS first for intelligent domain resolution and nearest-IP selection.
   - Traffic flows through Mihomo for rule-based proxy routing.
   - AdGuard Home performs last-mile ad and tracker filtration.
2. **`SmartDNS > AdGuardHome > Mihomo`**:
   - Traffic hits AdGuard Home for filtering before passing to Mihomo for proxy traversal.

### Core Service Behavior
- **SmartDNS**: Possesses lowest forwarding priority; when other services are active, it acts as an upstream resolver.
- **AdGuardHome**: Provides systemwide local ad blocking, DNS query logging, and custom blocklist management.
- **Mihomo**: Serves as the transparent proxy core, routing network sockets through configured proxy nodes.

## Configuration & Dashboards

1. Flash `SAM-*.zip` in your root manager and reboot.
2. The default web interface credentials for bundled services are:
   - **Username**: `root`
   - **Password**: `root`
3. Access AdGuard Home web interface at `http://127.0.0.1:3000`.
4. Mihomo core configuration resides at:
   ```bash
   /data/adb/modules/SAM/etc/mihomo/base.yaml
   ```
   > [!IMPORTANT]
   > Do not delete or indiscriminately modify `base.yaml`; SAM relies on specific anchor structures within this file to bind transparent proxy ports.
5. All module assets and configuration files persist in:
   ```bash
   /data/adb/modules/SAM/
   ```

## Troubleshooting & Verification

- **Loss of Internet Connectivity**:
  - Toggle Airplane Mode on and off to reset Android's network interfaces.
  - Open the AdGuard Home query log (`http://localhost:3000`) and check whether queries are being blocked or if the upstream DNS server is unreachable.
- **Exempting Specific Wi-Fi Networks**: Use SAM's Wi-Fi blacklist feature to prevent the proxy from engaging when connected to trusted local LANs or enterprise networks.
