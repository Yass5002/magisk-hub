---
id: "bindhosts"
title: "Bindhosts: Fast, Systemless Hosts Adblocking Engine"
sidebarTitle: "Bindhosts"
description: "High-performance systemless hosts redirector for Android that binds custom adblocking blocklists into /system/etc/hosts with zero battery impact."
category: "networking-proxies"
tier: 1
searchQueries:
  - "bindhosts magisk module"
  - "systemless hosts adblock android"
  - "how to block ads rooted android"
  - "adaway alternative magisk"
  - "bindhosts custom txt guide"
prerequisites:
  - "Magisk, KernelSU, or APatch"
  - "Root access via shell or terminal"
conflicts:
  - "Legacy Systemless Hosts module (included inside Magisk settings)"
  - "Other hosts-replacing modules installed concurrently"
configPaths:
  - "/data/adb/bindhosts/custom.txt"
  - "/data/adb/bindhosts/whitelist.txt"
  - "/data/adb/bindhosts/sources.txt"
features:
  - "Native bind mount architecture: direct zero-overhead hosts redirection without background VPN services"
  - "Multiple curated upstream blocklist sources (StevenBlack, AdGuard, OISD, GoodbyeAds)"
  - "On-device WebUI and CLI interface for instant blocklist updating (`su -c bindhosts -r`)"
  - "Granular whitelist and blacklist support without risking bootloops or connectivity deadlocks"
faq:
  - question: "Does Bindhosts drain battery like VPN-based adblockers?"
    answer: "Zero battery drain. VPN adblockers (like AdGuard app or personal VPNs) run a local tun interface that inspects every network packet in userspace. Bindhosts operates at the OS kernel resolver level via /system/etc/hosts; blocked domains resolve instantly to 0.0.0.0 without any background packet parsing."
  - question: "How do I whitelist a domain that broke an app?"
    answer: "Add the broken domain to /data/adb/bindhosts/whitelist.txt (one domain per line), then run `su -c bindhosts -r` in Termux to recompile the hosts file immediately."
---

## Overview

Maintained by the **bindhosts** open-source team, **Bindhosts** is the modern successor to traditional hosts adblockers on rooted Android devices.

While legacy tools like AdAway required complex local web servers or full partition remounts, Bindhosts uses direct Linux kernel bind mounts (`mount --bind`). It compiles millions of verified ad, tracker, telemetry, and malware domains into a single unified `/system/etc/hosts` table that the Android Bionic libc DNS resolver uses natively across all applications.

---

## Technical Architecture & How It Works

### The Systemless Bind Mount

1. **Compilation Phase**: Bindhosts fetches curated domain blocklists from high-reputation providers (StevenBlack, OISD, 1Hosts).
2. **Deduplication & Sanitization**: The internal engine deduplicates entries, removes invalid syntax, merges user custom rules from `custom.txt`, and strips any domains specified in `whitelist.txt`.
3. **Loop Mount Staging**: The compiled hosts file is written to `/data/adb/bindhosts/hosts`.
4. **Namespace Redirection**: During the early boot phase (`post-fs-data.sh` and `service.sh`), Bindhosts executes:
   ```bash
   mount --bind /data/adb/bindhosts/hosts /system/etc/hosts
   ```
5. **Universal Enforcement**: Because `/system/etc/hosts` is read by Android's DNS resolver for every outbound network call, ads, trackers, and telemetry pings fail to resolve instantly with zero CPU latency.

---

## Installation & Setup

1. Open your root manager (**Magisk**, **KernelSU**, or **APatch**).
2. Download and flash the latest `bindhosts-vX.zip`.
3. Reboot your device.
4. Open a terminal app (like **Termux**) and run the initialization command:
   ```bash
   su -c bindhosts -r
   ```
5. Bindhosts will download the latest upstream lists, merge them, and apply the new hosts file immediately without requiring a reboot.

---

## Configuration & Custom Rules

All configuration files reside in `/data/adb/bindhosts/`:

- **`custom.txt`**: Add custom domains you want blocked:
  ```text
  0.0.0.0 telemetry.example.com
  0.0.0.0 ads.targetapp.com
  ```
- **`whitelist.txt`**: Add false-positive domains you want unblocked:
  ```text
  s.youtube.com
  login.live.com
  ```
- **Updating via CLI**:
  ```bash
  # Quick update
  su -c bindhosts -r

  # Check active hosts file size & count
  su -c bindhosts -s

  # Temporarily disable adblocking
  su -c bindhosts -d

  # Re-enable adblocking
  su -c bindhosts -e
  ```
