---
id: "alwaysstrong"
title: "AlwaysStrong: All-in-One Strong Play Integrity Module"
sidebarTitle: "AlwaysStrong"
description: "Bundled solution integrating TEESimulator-RS and PlayIntegrityFork into a single module with automated keybox updates and WebUI management."
category: "root-management"
tier: 1
searchQueries:
  - "alwaysstrong magisk module"
  - "evoker0 alwaysstrong"
  - "pass strong integrity all in one"
  - "alwaysstrong webui"
  - "teesimulator-rs playintegrityfork bundle"
prerequisites:
  - "Magisk (with standalone ZygiskNext, ReZygisk, or NeoZygisk recommended over built-in Zygisk), KernelSU, or APatch"
  - "Zygisk implementation installed and active"
conflicts:
  - "Standalone installations of TEESimulator-RS or PlayIntegrityFork (AlwaysStrong bundles both; separate modules must be removed to avoid duplicate hooks)"
configPaths:
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/modules/tricky_store/"
features:
  - "Single-flash bundle: combines hardware KeyMint attestation simulation with framework fingerprint spoofing"
  - "Integrated WebUI: manage hourly auto-updates, view device status, and configure target packages across 15 languages"
  - "Action button automation: trigger immediate keybox rotation, target rebuilding, and process termination with one tap"
  - "Automated Google process cleanup: flushes cached attestation tokens across Play Services to force immediate re-evaluation"
  - "Multi-manager support: fully optimized for Magisk, KernelSU, SukiSU Ultra, and APatch"
faq:
  - question: "Why does AlwaysStrong use the module ID 'tricky_store'?"
    answer: "AlwaysStrong uses the tricky_store module ID to maintain drop-in compatibility with the existing ecosystem of root management tools and scripts that expect keybox files under /data/adb/tricky_store/."
  - question: "Should I keep Play Integrity Fix installed when using AlwaysStrong?"
    answer: "No. AlwaysStrong bundles PlayIntegrityFork and TEESimulator-RS together. You should uninstall standalone Play Integrity Fix/Fork modules before flashing AlwaysStrong to avoid duplicate property spoofing."
---

## Overview

Developed by **evoker0**, **AlwaysStrong** is an all-in-one packaging of the key integrity bypass components required to achieve `MEETS_STRONG_INTEGRITY` on rooted Android devices.

Passing Google's highest attestation tiers typically requires flashing, configuring, and updating multiple disparate modules—a hardware attestation simulator (like TEESimulator-RS) and a build fingerprint spoofer (like PlayIntegrityFork). AlwaysStrong unifies these components into a single package with an integrated WebUI.

---

## Technical Architecture & How It Works

### Unified Stack Orchestration

AlwaysStrong combines framework spoofing and hardware Keystore simulation:

1. **Integrated Core Engines**: Combines the Rust-based KeyMint simulation of TEESimulator-RS with the property manipulation rules of PlayIntegrityFork.
2. **Automated Action Scripting**: Tapping the Action button triggers a multi-stage maintenance pipeline that refreshes active keybox certificates, writes target packages into `/data/adb/tricky_store/target.txt`, and synchronizes security patch dates.
3. **WebUI Management**: Provides a built-in web dashboard on KernelSU and APatch, enabling users to schedule hourly keybox updates and toggle individual target applications without terminal intervention.

---

## Installation & Setup

1. Uninstall any standalone copies of TrickyStore, TEESimulator, or PlayIntegrityFix/Fork.
2. Ensure you have an active Zygisk engine running (such as **ZygiskNext**, **ReZygisk**, or **NeoZygisk**).
3. Download the latest `AlwaysStrong-*.zip` release.
4. Flash the module in your root manager and reboot.
5. Tap the **Action** button in your root manager to run the initialization routine.

---

## Configuration & Practical Usage

- **WebUI Interface**: On KernelSU or APatch, open the module's WebUI to configure automatic update intervals and select target applications.
- **Keybox Directory**: Active attestation keys and target lists are stored at:
  ```bash
  /data/adb/tricky_store/keybox.xml
  /data/adb/tricky_store/target.txt
  ```

---

## Troubleshooting & Common Issues

- **Detection Still Failing**: Open your root manager and run the Action button again to pull the latest unrevoked certificate bundle and kill cached Google Play Services instances.
- **Zygisk Recommendation**: Avoid using Magisk's built-in Zygisk implementation with AlwaysStrong. Built-in Magisk Zygisk is easily detected by modern anti-tamper SDKs; use a standalone loader like ZygiskNext instead.
