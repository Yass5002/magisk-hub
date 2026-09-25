---
id: "ohmykeymint"
title: "OhMyKeymint: Rust-Based Keystore 2.0 & KeyMint Interceptor"
sidebarTitle: "OhMyKeymint"
description: "Rust-engineered attestation redirection module hooking Android 12+ keystore2 daemons to route cryptographic attestation to custom KeyMint profiles."
category: "root-management"
tier: 1
searchQueries:
  - "ohmykeymint magisk module"
  - "qwq233 ohmykeymint"
  - "keystore2 rust hook android"
  - "ohmykeymint config toml"
  - "keymint attestation spoofer"
prerequisites:
  - "Android 12 or newer (specifically requires keystore2 architecture)"
  - "64-bit architecture (arm64-v8a)"
  - "Magisk, KernelSU, or APatch"
conflicts:
  - "Stated plainly: No documented conflicts with other modules; other active keystore2 injectors (such as TrickyStore or TEESimulator) should not be run concurrently"
configPaths:
  - "/data/adb/ohmykeymint/config.toml"
  - "/data/adb/ohmykeymint/"
features:
  - "Rust-powered injection engine: hooks into keystore2 via ptrace or dlopen with zero runtime GC overhead"
  - "Custom KeyMint routing: intercepts hardware key generation calls and directs them to user-defined KeyMint providers"
  - "TOML-based configuration: declare fine-grained package targets, device identifiers, and attestation policies"
  - "Zero interference with biometrics: non-targeted applications access real device secure enclaves transparently"
  - "Seamless integration: compatible with modern root stacks across Magisk, KernelSU, and APatch"
faq:
  - question: "Why does OhMyKeymint require Android 12 or higher?"
    answer: "OhMyKeymint is specifically architected to hook Android's Keystore 2.0 system daemon (keystore2) and its AIDL KeyMint HAL interfaces. Devices on Android 11 and older use the legacy C++ keystore daemon and HIDL Keymaster HAL, which are not targeted by this engine."
  - question: "How do I configure target applications in OhMyKeymint?"
    answer: "Configuration is managed in /data/adb/ohmykeymint/config.toml, where you can define application package names, spoofed security patch levels, and keybox credential parameters."
---

## Overview

Developed by **qwq233**, **OhMyKeymint** is an advanced attestation interception framework written in Rust for modern Android versions (Android 12+).

As Google transitioned from legacy Keymaster HIDL services to AIDL-based Keystore 2.0 (`keystore2`), the mechanisms used by applications to request hardware-backed key attestations were redesigned. OhMyKeymint hooks directly into the `keystore2` process, allowing users to define flexible, programmatically generated KeyMint profiles that satisfy Play Integrity while preserving device hardware keys for standard biometric authentication.

---

## Technical Architecture & How It Works

### Keystore 2.0 Daemon Hooking

OhMyKeymint operates within the system keystore process address space:

1. **Binder Transaction Interception**: Hooks Android's `android.system.keystore2` AIDL interface within the `keystore2` daemon.
2. **Selective Policy Evaluation**: When a client application calls `generateKey` with attestation parameters, OhMyKeymint consults its TOML configuration to determine whether the calling UID matches a declared target.
3. **KeyMint Simulation**: Intercepted requests are redirected to an authentic software KeyMint instance, signing the resulting certificate chain with configured credentials.

---

## Installation & Setup

1. Verify your device runs **Android 12** or newer on a **64-bit** platform.
2. Download the latest `OhMyKeymint-*.zip` release.
3. Flash the module in your root manager (Magisk, KernelSU, or APatch).
4. Reboot the device.

---

## Configuration & Usage

Configure target packages and profiles in:
```toml
/data/adb/ohmykeymint/config.toml
```
Review the sample configuration in the repository documentation to define package names and security patch levels.

---

## Troubleshooting & Common Issues

- **Keystore Daemon Crashing**: If the keystore daemon restarts repeatedly, verify that your `config.toml` contains valid TOML syntax and that no other keystore hooks are conflicting.
