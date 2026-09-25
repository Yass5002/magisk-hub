---
id: "adguardhomeforroot"
title: "AdGuardHome for Root: On-Device DNS Server & Ad-Blocking Engine"
sidebarTitle: "AdGuardHome for Root"
description: "Standalone AdGuard Home server running natively on Android with systemwide iptables DNS redirection without VPN overhead."
category: "networking-proxies"
tier: 1
searchQueries:
  - "adguardhome for root magisk"
  - "local adguard home android iptables"
  - "adguardhome android root webui 3000"
  - "twoone3 adguard home root"
  - "systemwide dns adblock android root"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "Architecture: arm64-v8a or armeabi-v7a"
  - "Android Private DNS must be disabled (Off) in system network settings to prevent DNS-over-TLS from bypassing iptables redirection"
conflicts:
  - "Stated plainly: No documented conflicts with other proxy software (explicitly coexists with NekoBox, FlClash, Box for Magisk, and akashaProxy)"
  - "Built-in Android Private DNS (DoT) will bypass the local DNS server if left active"
configPaths:
  - "/data/adb/agh/settings.conf"
  - "/data/adb/agh/AdGuardHome.yaml"
  - "/data/adb/agh/bin/agh.pid"
  - "/data/adb/modules/AdGuardHome/"
features:
  - "Native local DNS filtering: runs official AdGuard Home on-device without consuming Android's VPN slot"
  - "AWAvenue ad-filtering rules: pre-configured with lightweight, power-efficient rulesets optimized for low false positives"
  - "Full web management interface: accessible at http://127.0.0.1:3000 with real-time query logging, upstream DNS selection, and custom blocklists"
  - "Fallback startup safety: includes a 120-second listener timeout that skips iptables redirection if the daemon fails to start, preventing loss of device connectivity"
  - "Proxy coexistence: integrates alongside third-party proxy solutions like FlClash and NekoBox"
faq:
  - question: "Why must I turn off Android's 'Private DNS' setting?"
    answer: "Android's built-in Private DNS feature routes DNS requests over encrypted TLS (DoT) via port 853 directly to upstream providers. This completely bypasses standard port 53 UDP/TCP iptables redirection. Turning Private DNS Off allows AdGuard Home to capture and filter all device queries locally."
  - question: "What are the default login credentials for the WebUI?"
    answer: "When accessing the management dashboard at http://127.0.0.1:3000 for the first time, both the default username and password are set to root / root."
---

## Overview

Maintained by **twoone3**, **AdGuardHome for Root** brings the full capabilities of the enterprise-grade **AdGuard Home** DNS sinkhole directly to rooted Android devices.

Standard mobile ad blockers typically establish a dummy local VPN tunnel via Android's `VpnService` API to intercept DNS queries. This approach introduces battery consumption overhead, adds network latency, and prevents users from connecting to genuine VPNs or proxy clients simultaneously. AdGuardHome for Root eliminates this limitation by running an authentic compiled AdGuard Home daemon locally and redirecting system DNS via native Linux `iptables` rules.

---

## Technical Architecture & How It Works

### Standalone DNS Daemon & Firewall Redirection

AdGuardHome for Root sets up a fully self-contained networking architecture inside `/data/adb/agh/`:

1. **Native Binary Daemon**: Runs the official compiled ARM Linux binary of AdGuard Home as a persistent background service managed by `service.sh`.
2. **Iptables Port Redirection**: When `enable_iptables=true` is set in `settings.conf`, the module executes firewall rules to redirect outgoing DNS requests on port 53 (UDP and TCP) directly to AdGuard Home's internal listener on port `5591`.
3. **Loop Prevention & GID Bypass**: The daemon process runs under a dedicated `net_raw` group ID, allowing its own upstream queries (to encrypted DNS resolvers like Cloudflare or Quad9) to exit without looping back into the local redirect chain.
4. **Fail-Safe Listener Timeout**: During device startup, `service.sh` waits up to 120 seconds for the DNS daemon to bind its listening socket. If the daemon fails to start, iptables rules are automatically skipped, ensuring the phone retains working internet connectivity rather than experiencing a total DNS blackout.

---

## Installation & Setup

### 1. Disable Private DNS
Before installing, ensure Android's native DNS-over-TLS client is disabled:
- Go to **Settings > Network & Internet > Private DNS**.
- Select **Off**.

### 2. Flash Module
1. Download the latest release from the official repository.
2. Flash the module in Magisk, KernelSU, or APatch.
3. Reboot the device.

### 3. Access Web Dashboard
Once the device boots, open any mobile browser and navigate to:
```text
http://127.0.0.1:3000
```
Log in using the default administrative credentials:
- **Username**: `root`
- **Password**: `root`

---

## Configuration & Practical Usage

### Module Settings (`settings.conf`)

Fine-tune daemon behavior in `/data/adb/agh/settings.conf`:
- **Disable Built-in Iptables**: If you only wish to use AdGuard Home as a local server without redirecting device traffic, set `enable_iptables=false`.
- **IPv6 DNS Blocking**: Set `block_ipv6_dns=true` to force IPv6 DNS queries to resolve through IPv4 filtering rules.
- **Bypass Addresses**: Append specific IP addresses to `ignore_dest_list` or `ignore_src_list` to bypass AdGuard Home filtering.

### Filter Rules
By default, the module bundles **AWAvenue-Ads-Rule**, an optimized mobile ad-blocking list designed for minimal RAM footprint and low false positives. Additional community blocklists can be subscribed to directly through the WebUI at `http://127.0.0.1:3000/#filters`.

---

## Troubleshooting & Common Issues

- **Total Loss of Internet / DNS Resolution**: Confirm that `Private DNS` is completely disabled in system settings. If DNS resolution fails, inspect `/data/adb/agh/bin/agh.pid` to check if the daemon is alive, or review error output in the AdGuard Home query logs.
- **Port Conflict with Other DNS Daemons**: If another module or local service is already listening on port 53 or 3000, modify `redir_port` and web bind ports inside `/data/adb/agh/AdGuardHome.yaml`.
