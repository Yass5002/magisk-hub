---
id: "playstoreselfupdateblocker"
title: "PlayStoreSelfUpdateBlocker: Real-Time Play Store Self-Update Suppression"
sidebarTitle: "Play Store Update Blocker"
description: "Prevents Google Play Store from silently updating itself in the background, preserving specific versions required for Play Integrity attestation."
category: "system-environment"
tier: 1
searchQueries:
  - "play store self update blocker magisk"
  - "pusblocker himanshujjp"
  - "stop google play store auto update root"
  - "play integrity play store version lock"
  - "prevent play store silent update kernelsu"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
conflicts: []
configPaths:
  - "/data/adb/modules/playstoreselfupdateblocker/"
features:
  - "Active background watchdog: monitors Google Play Store package changes on a 30-second cadence with minimal CPU overhead"
  - "Automated rollback trigger: detects unauthorized silent background updates and immediately restores the designated pinned build"
  - "Play Integrity safeguarding: prevents newer Play Store releases from enforcing aggressive hardware attestation checks"
  - "Broad root manager support: runs reliably across Magisk, KernelSU, and APatch environments"
  - "Clean systemless architecture: intercepts package staging and installation without modifying underlying system partitions"
---

## Overview

For rooted Android users maintaining Google Play Integrity certification (MEETS_DEVICE_INTEGRITY / MEETS_STRONG_INTEGRITY), pinning a specific version of the Google Play Store (`com.android.vending`) is often vital. Google routinely pushes silent, unnotified self-updates to the Play Store client that introduce stricter server-side attestation checks, breaking customized fingerprints or PlayIntegrityFix hooks without warning.

Authored by himanshujjp, **PlayStoreSelfUpdateBlocker** (PUSBlocker) is a systemless background watchdog module designed to permanently prevent Google Play Store from silently updating itself.

## How PUSBlocker Functions

1. **Lightweight Monitoring Loop**: Operates a low-overhead background service that checks the installed version code and APK hash of `com.android.vending` approximately every 30 seconds.
2. **Instant Staging Interception**: When Google Play Services downloads a new Play Store APK into staging caches, PUSBlocker blocks the update transaction or cleans up the staged APKs.
3. **Automated Rollback**: If Google successfully pushes an update while the device is sleeping, the daemon detects the version mismatch upon wake and automatically executes a clean rollback to your target pinned release.

## Compatibility & Installation

- **Root Compatibility**: Fully compatible with **Magisk**, **KernelSU**, and **APatch**.
- **Installation Procedure**:
  1. Downgrade or install your desired target Play Store APK version.
  2. Download the latest `PlayStoreSelfUpdateBlocker-v*.zip` from GitHub releases.
  3. Flash the module in your root manager and reboot.
  4. The watchdog service will immediately lock the current Play Store build in place.
