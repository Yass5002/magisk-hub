---
id: "magicalprotection"
title: "MagicalProtection: Zero-Config Systemless Hosts Adblocker"
sidebarTitle: "MagicalProtection"
description: "Provides automated, zero-configuration systemless hosts-based ad and tracker blocking without requiring companion apps or Systemless Hosts."
category: "networking-proxies"
tier: 1
searchQueries:
  - "magicalprotection magisk"
  - "programminghoch10 magicalprotection"
  - "zero config adblock magisk module"
  - "systemless hosts adblocker android"
  - "energized protection alternative magisk"
prerequisites:
  - "Root access via Magisk"
conflicts:
  - "Other systemless hosts managers (such as AdAway in root hosts mode or EnergizedProtection)"
configPaths:
  - "/data/adb/modules/MagicalProtection/"
features:
  - "Zero configuration: install and reboot with zero setup wizards, shell commands, or companion app configuration required"
  - "Self-contained hosts mount: directly mounts the curated blocking table over /system/etc/hosts without requiring Magisk's Systemless Hosts toggle"
  - "Automated CI/CD releases: updates and filter consolidations are generated automatically via GitHub Actions pipelines"
  - "Dual-component versioning: tracks both the core module codebase (mv) and the underlying filter hostlist database (hv)"
  - "Comprehensive domain protection: blocks advertising networks, third-party analytics trackers, telemetry endpoints, and known malicious domains"
---

## Overview

While tools like EnergizedProtection and AdAway offer powerful ad-blocking capabilities, they frequently require manual terminal interaction, companion app permissions, or external server dependencies.

Created by programminghoch10, **MagicalProtection** provides a streamlined, set-and-forget approach to system-wide adblocking. Inspired by the convenience of EnergizedProtection and the architecture of Magisk Magic Mount, MagicalProtection bundles a pre-compiled, highly optimized hosts file directly into the module. It requires no configuration, no companion APK, and operates completely systemlessly.

## Architectural Advantages

- **No Systemless Hosts Dependency**: Unlike AdAway which requires enabling Magisk's internal Systemless Hosts toggle in settings, MagicalProtection directly binds its curated `/system/etc/hosts` file during boot.
- **Dual Version Tracking**: Release tags utilize an explicit two-tier format—such as `mv19-hv121`—where `mv` denotes the module script version and `hv` denotes the hosts database revision.
- **Automated Upstream Sync**: The module repository utilizes automated GitHub Actions pipelines to pull, validate, and deduplicate authoritative blocking lists on a recurring schedule.
- **POSIX-Compliant Shell Logic**: Clean, standards-compliant shell scripts eliminate boot stalls and syntax errors across different Android Toybox and BusyBox environments.

## Installation

1. Download the latest `MagicalProtection-mv*-hv*.zip` package from GitHub releases.
2. Open **Magisk Manager**, navigate to **Modules > Install from storage**, and select the zip archive.
3. Reboot your Android device.
4. Ad and tracker blocking is immediately active across all browsers, web views, and native applications.

## Uninstallation

To restore stock host resolution, simply disable or remove MagicalProtection from Magisk Manager and reboot. The stock `/system/etc/hosts` file will remain completely untouched.
