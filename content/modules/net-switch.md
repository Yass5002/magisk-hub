---
id: "net-switch"
title: "Net Switch: Per-App Internet Access Isolation Firewall"
sidebarTitle: "Net Switch"
description: "Standalone iptables-based network firewall allowing users to isolate applications from the internet without requiring a battery-draining VPN service."
category: "security-certificates"
tier: 1
searchQueries:
  - "net switch magisk module"
  - "rem01gaming net switch"
  - "per app firewall root iptables"
  - "isolate apps internet no vpn"
  - "net switch webui mmrl"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "WebUI host for management (KsuWebUI or MMRL on Magisk)"
conflicts:
  - "Stated plainly: No documented conflicts with other modules; does not use Android VpnService, so it coexists cleanly with VPN clients"
configPaths:
  - "/data/adb/modules/net-switch/"
features:
  - "Per-app internet isolation: toggle network transmission permissions independently for each installed app"
  - "Zero-VPN architecture: operates completely via Linux iptables packet filtering without battery drain"
  - "Profile management: save and restore collections of isolated applications for rapid policy switching"
  - "Integrated backup manager: export and import network isolation configurations safely across devices"
  - "Modern responsive WebUI: sleek, animated interface for live toggling without requiring reboots"
faq:
  - question: "Why is Net Switch better than VPN-based firewalls like AFWall+?"
    answer: "AFWall+ and standard firewall apps often run a continuous local VPN service or background daemon that consumes battery, adds processing overhead, and blocks you from connecting to authentic VPNs. Net Switch applies raw Linux iptables drop rules directly to application UIDs, operating with zero battery overhead."
  - question: "How do I access the Net Switch interface on Magisk?"
    answer: "Since official Magisk lacks an embedded WebUI viewer in its manager, you can open Net Switch's WebUI using standalone WebUI hosts such as MMRL or KsuWebUIStandalone."
---

## Overview

Developed by **Rem01Gaming**, **Net Switch** is a systemless firewall utility designed to isolate individual Android applications from accessing mobile data and Wi-Fi networks.

Many Android apps transmit telemetry, analytics, and background ads even when not in active use. While conventional firewalls rely on Android's `VpnService`—which drains battery, increases latency, and prevents concurrent VPN usage—Net Switch applies native Linux `iptables` drop chains directly at the kernel network boundary.

---

## Technical Architecture & How It Works

### UID-Based Iptables Filtering

Net Switch operates at the Linux packet-filtering layer:

1. **UID Group Resolution**: Every Android application runs under a unique Linux User ID (UID). Net Switch maps packages to their assigned UIDs.
2. **Iptables Chain Injection**: Creates custom filter chains (`OUTPUT -m owner --uid-owner <UID> -j DROP`) to discard outgoing socket requests from isolated apps immediately.
3. **Instant Rule Switching**: Changes applied in the WebUI take effect instantly in kernel memory without requiring device reboots.

---

## Installation & Setup

1. Download the latest `Net-Switch-*.zip` release.
2. Flash the module in Magisk, KernelSU, or APatch.
3. Reboot your device.
4. Launch the WebUI (from KernelSU/APatch manager or via MMRL on Magisk).

---

## Configuration & Usage

Inside the Net Switch WebUI:
- **Application Toggles**: Tap any installed application to toggle its internet connectivity.
- **Profiles**: Group apps into profiles (e.g. "Work Mode", "Offline Games") to switch firewall policies with a single tap.
- **Backup & Restore**: Export your isolation rules as JSON to restore them after ROM flashes.

---

## Troubleshooting & Common Issues

- **Isolated App Still Connecting**: Ensure you have selected all auxiliary helper packages associated with the app (e.g. companion media downloaders or sync daemons).
