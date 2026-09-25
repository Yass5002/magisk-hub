---
id: "teesimulator-rs"
title: "TEESimulator-RS: Rust-Native Hardware Keybox & Keystore Attestation Simulation"
sidebarTitle: "TEESimulator-RS"
description: "High-performance Rust rewrite of TEESimulator embedding AOSP's reference KeyMint trusted application directly into keystore daemons."
category: "root-management"
tier: 1
searchQueries:
  - "teesimulator rs magisk module"
  - "teesimulator rust keybox"
  - "enginex0 teesimulator rs"
  - "keystore hardware attestation rust"
  - "pass strong integrity teesimulator-rs"
prerequisites:
  - "Android 10 or newer"
  - "64-bit architecture (arm64-v8a or x86_64)"
  - "Magisk, KernelSU, or APatch"
  - "Valid hardware-backed keybox.xml certificate bundle"
conflicts:
  - "Stated plainly: No documented conflicts with other modules; software-only fallback occurs if no keybox is configured"
configPaths:
  - "/data/adb/teesim/config.json"
  - "/data/adb/teesim/keybox.xml"
  - "/data/adb/teesim/target.txt"
  - "/data/adb/teesim/security_patch.txt"
features:
  - "Rust-native implementation: memory-safe, high-speed execution reducing Binder latency during KeyMint transactions"
  - "Embedded AOSP reference KeyMint TA: runs kmr-ta in-process inside Android's keystore2 or legacy keystore daemons"
  - "Flexible targeting modes: supports target.txt package declarations and dynamic security patch level spoofing"
  - "Live configuration reloading: monitors configuration files and updates daemon memory without requiring a reboot"
  - "Zero-footprint passthrough: unlisted applications communicate directly with physical hardware TEE chips untouched"
faq:
  - question: "What is the difference between TEESimulator and TEESimulator-RS?"
    answer: "TEESimulator-RS is an optimized rewrite in Rust developed by Enginex0. It maintains complete configuration and cryptographic compatibility with the original project while lowering memory overhead and improving hooking performance."
  - question: "Will TEESimulator-RS work if I do not have a keybox.xml file?"
    answer: "No. Without a hardware-backed keybox.xml, the module cannot forge valid cryptographic signatures signed by Google's attestation root of trust, causing strict verification checks to fail."
---

## Overview

Maintained by **Enginex0**, **TEESimulator-RS** is a Rust implementation of the TEESimulator architecture designed to satisfy Android hardware-backed Key Attestation challenges.

Modern attestation verifies bootloader integrity cryptographically inside hardware secure enclaves. TEESimulator-RS intercepts key creation calls at the system keystore level, executing AOSP's reference KeyMint Rust engine (`kmr-ta`) inside the daemon to produce cryptographically authentic attestation certificates using a user-supplied `keybox.xml`.

---

## Technical Architecture & How It Works

### In-Process KeyMint Routing

TEESimulator-RS injects a native Rust interception engine into Android's keystore services:

1. **Binder Transaction Hooking**: On Android 12+, the module hooks `AIBinder_transact` inside `keystore2`. When a declared target app requests key generation, transactions are routed to an in-process `IKeyMintDevice` handling `kmr-ta`.
2. **Selective App Scoping**: Non-targeted applications (such as device biometric unlock, Widevine DRM, and FIDO credentials) bypass the simulator completely and talk directly to the real hardware TEE.
3. **Patch Level Harmonization**: The module reads `/data/adb/teesim/security_patch.txt` to align the reported system, vendor, and boot security patch levels with current Play Integrity requirements.

---

## Installation & Setup

1. Flash the latest `TEESimulator-RS-*.zip` release in Magisk, KernelSU, or APatch.
2. Reboot the device.
3. Place your unrevoked `keybox.xml` file into:
   ```bash
   /data/adb/teesim/keybox.xml
   ```
4. Define your targeted application packages inside:
   ```bash
   /data/adb/teesim/target.txt
   ```
5. Changes are monitored live by the control process without requiring an additional reboot.

---

## Troubleshooting & Common Issues

- **Attestation Returns Software-Only**: If key attestation tools report software-only backing, verify that `/data/adb/teesim/keybox.xml` is present, readable, and contains valid RSA/EC private keys and certificate chains.
- **Daemon Recovery**: If key operations hang due to corrupt profiles, restart the keystore daemon from a root shell (`kill $(pidof keystore2)`).
