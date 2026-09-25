---
id: "surfing"
title: "Surfing: Multi-Core Transparent Proxy & Clash Gateway"
sidebarTitle: "Surfing"
description: "All-in-one systemless transparent proxy module orchestrating Clash/mihomo, sing-box, Xray, and Hysteria with REDIRECT, TPROXY, and TUN routing."
category: "networking-proxies"
tier: 1
searchQueries:
  - "surfing magisk module"
  - "clash transparent proxy android root"
  - "mihomo tproxy module kernelsu"
  - "surfing box bll config yaml"
  - "surfingtile proxy manager android"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "Root permissions granted to the SurfingTile desktop companion APK"
  - "Up-to-date Android System WebView (com.google.android.webview) for web dashboard rendering"
conflicts:
  - "bypass_via_iptables='true' in box.config conflicts when proxy_method is set to TUN"
  - "enable_ssid_filter and enable_mac_filter are mutually exclusive options (enabling both prioritizes SSID filtering)"
configPaths:
  - "/data/adb/box_bll/clash/config.yaml"
  - "/data/adb/box_bll/scripts/box.config"
  - "/data/adb/box_bll/run/"
  - "/data/adb/modules/Surfing/"
features:
  - "Multi-core routing engine: supports Clash/mihomo, sing-box, v2ray, Xray, and Hysteria backends"
  - "Flexible interception modes: REDIRECT (TCP), TPROXY (TCP+UDP), TUN virtual adapter, and hybrid routing"
  - "Network interface filtering: granular policy rules based on Wi-Fi SSID, MAC address, cellular status, and hotplug bypass"
  - "SurfingTile management app: local dashboard for managing subscriptions, manual node switching, and routing logs"
  - "User and package blacklisting/whitelisting: bypass specific Android apps or multi-user profiles directly from box.config"
faq:
  - question: "Why does the management dashboard fail to display in SurfingTile?"
    answer: "The management panel relies on modern Chromium features. If the dashboard fails to render or displays a blank screen, update the com.google.android.webview package through the Google Play Store."
  - question: "Can I use both Wi-Fi SSID filtering and MAC address filtering at the same time?"
    answer: "No. According to box.config documentation, SSID filtering and MAC address filtering are mutually exclusive. When both are enabled simultaneously, SSID filtering takes priority over MAC filtering."
---

## Overview

Developed by **GitMetaio**, **Surfing** is an advanced network redirection module that transforms rooted Android devices into full-fledged transparent routing gateways.

Instead of running battery-draining VPN interfaces that monopolize Android's single VpnService slot, Surfing operates directly at the Linux kernel firewall layer. Using native iptables and nftables rule chains, it intercepts socket traffic at the network stack and directs it into high-performance core daemons including **Clash.Meta (mihomo)**, **sing-box**, **Xray**, or **Hysteria**.

---

## Technical Architecture & How It Works

### Kernel Firewall Interception & Core Forwarding

Surfing isolates its configuration, runtime binaries, and routing rules inside `/data/adb/box_bll/`:

1. **Proxy Modes**:
   - **TPROXY (Default)**: Leverages `iptables -t mangle -A PREROUTING -p tcp/udp -j TPROXY` to redirect both TCP and UDP sockets transparently to local port `1536` without touching application headers.
   - **REDIRECT**: Fallback TCP-only redirection to local port `7891`.
   - **TUN**: Emulates a virtual network device (`Meta`) for protocols incompatible with socket splicing.
2. **Network State Automation**: The helper daemon monitors network interface transitions (switching from Wi-Fi to cellular, roaming between Wi-Fi SSIDs). Rules dynamically disable or enable proxy chains based on the whitelist/blacklist definitions in `box.config`.
3. **App Isolation & UID Exclusions**: Uses Linux cgroups and `net_admin` GIDs to exempt the core proxy binary and specified Android application packages from being looped back into the proxy listener.

---

## Installation & Setup

### 1. Flash the Module
1. Download `Surfing-v*.zip` from the project's official releases.
2. Flash the module via Magisk, KernelSU, or APatch.
3. Reboot your device.

### 2. Configure Subscriptions
Before network redirection takes effect, you must provide a valid proxy subscription:
1. Open the **SurfingTile** application on your home screen and grant it superuser access.
2. In **Menu > Config Override**, paste your provider subscription URL and trigger an update.
3. Alternatively, place your raw configuration directly into:
   ```bash
   /data/adb/box_bll/clash/config.yaml
   ```
4. Restart the service or reboot to apply the routing configuration.

---

## Configuration & Practical Usage

Fine-tuning is handled directly in `/data/adb/box_bll/scripts/box.config`:

- **Proxy Method Selection**:
  ```bash
  proxy_method="TPROXY" # Options: REDIRECT, TPROXY, TUN, or MIXED
  ```
- **App Bypass List**:
  Exclude specific application UIDs and user profiles from proxy interception:
  ```bash
  user_packages_list=("0:com.android.captiveportallogin" "0:com.google.android.gms")
  ```
- **Wi-Fi Filtering**:
  Automatically disable the proxy on trusted home or enterprise networks:
  ```bash
  enable_ssid_filter="true"
  use_wifi_list_mode="blacklist"
  blacklist_wifi_ssids="Home_Network,Office_5G"
  ```

---

## Troubleshooting & Common Issues

- **No Internet Access After Boot**: Check `/data/adb/box_bll/run/clash.pid` to ensure the core binary started successfully. If your subscription fails to fetch due to strict remote validation, try changing the user agent setting (`Ua`) in your configuration profile.
- **Hotplug Bypass Conflicts**: When using `proxy_method="TUN"`, ensure that `bypass_via_iptables` is set to `"false"` in `box.config` to prevent routing loop conflicts between TUN interfaces and iptables mangle chains.
