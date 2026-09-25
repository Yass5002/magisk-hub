---
id: "teesimulator"
title: "TEESimulator: In-Process KeyMint Software Attestation Engine"
sidebarTitle: "TEESimulator"
description: "Software simulation framework embedding AOSP's reference KeyMint trusted application inside Android keystore daemons to satisfy hardware key attestation."
category: "root-management"
tier: 1
searchQueries:
  - "teesimulator magisk module"
  - "teesimulator jingmatrix"
  - "in-process keymint hardware attestation"
  - "teesimulator keybox xml setup"
  - "pass strong integrity teesimulator"
prerequisites:
  - "Android 10 or newer"
  - "64-bit architecture (arm64-v8a or x86_64)"
  - "Magisk, KernelSU, or APatch"
  - "Valid hardware-backed keybox.xml certificate bundle"
conflicts:
  - "Stated plainly: No documented conflicts with other modules; remains an inert no-op if no valid keybox is configured"
configPaths:
  - "/data/adb/teesim/config.json"
  - "/data/adb/teesim/keybox.xml"
  - "/data/adb/modules/teesim/"
features:
  - "Embedded reference KeyMint TA: runs AOSP's native kmr-ta trusted application directly inside Android keystore daemons"
  - "Granular profile architecture: bundles keybox credentials, patch levels, and device identifiers mapped per application"
  - "Dynamic hot-reloading: configuration edits made in config.json apply immediately without requiring a system reboot"
  - "Immutable root-of-trust stability: freezes device root-of-trust values across boots to ensure KeyMint key-encryption-keys remain decipherable"
  - "Selective routing: intercepts attestation transactions only for targeted apps while real hardware keys pass directly to device TEE"
faq:
  - question: "How does TEESimulator differ from TrickyStore?"
    answer: "While TrickyStore intercepts and modifies attestation certificates after generation, TEESimulator embeds AOSP's official reference KeyMint trusted application (kmr-ta) directly inside the keystore daemon. Keys and certificate chains are signed and generated identically to a real TEE, providing internal mathematical consistency by construction."
  - question: "Why does the module only support 64-bit devices?"
    answer: "On Android 10+, Android keystore daemons (keystore and keystore2) are compiled as 64-bit binaries (arm64-v8a and x86_64). Because TEESimulator injects its native hooking library directly into these daemon address spaces, it requires matching 64-bit architecture."
---

## Overview

Created by **JingMatrix**, **TEESimulator** satisfies Android hardware-backed Key Attestation challenges by running an authentic software KeyMint trusted application directly inside the operating system's keystore service.

Instead of modifying existing attestation certificates or tampering with ASN.1 extensions on the fly, TEESimulator embeds AOSP's native reference Rust KeyMint implementation (`kmr-ta`). By simulating genuine hardware cryptographic operations using a user-supplied `keybox.xml`, attestation certificates are created with the exact same sequence of operations performed by an authentic hardware Trusted Execution Environment (TEE).

---

## Technical Architecture & How It Works

### Daemon Injection & Binder Routing

TEESimulator divides its responsibilities between a privileged control daemon and an in-process native interception library:

1. **Boot Initialization & Harvesting**: At boot, the control daemon generates a throwaway hardware key to inspect the physical device's genuine root of trust (verified boot state, OS version, patch level). These parameters are frozen into an immutable hardware profile to ensure stored keys remain decryptable across reboots.
2. **Daemon-Specific Interception**:
   - **Android 12+ (`keystore2`)**: The module injects into the `keystore2` daemon and performs PLT hooks on `AIBinder_transact`. When an attestation request from a targeted application arrives, it redirects the transaction to an in-process `IKeyMintDevice` handling the embedded `kmr-ta` engine. Unlisted applications pass through to the real physical TEE untouched.
   - **Android 10–11 (`keystore`)**: The module hooks `ioctl` on `libbinder` inside the legacy `keystore` daemon, routing callers to a local stub that signs attestations with the software KeyMint engine.
3. **Live Configuration Push**: The daemon listens on a local UNIX domain socket. Whenever `/data/adb/teesim/config.json` is modified, the new settings are pushed directly to the injected interceptor without requiring a system reboot or daemon kill.

---

## Installation & Setup

### 1. Flash the Module
1. Download the latest `TEESimulator-v*.zip` from the project's official releases.
2. Flash the module in Magisk, KernelSU, or APatch and reboot the device.

### 2. Supply Keybox Credentials
Place your valid, unrevoked hardware `keybox.xml` file into the configuration directory:
```bash
/data/adb/teesim/keybox.xml
```

### 3. Assign Target Applications
Configure your target packages in `/data/adb/teesim/config.json`:
```json
{
  "version": 1,
  "profiles": {
    "default": {
      "keybox": "keybox.xml",
      "patchLevel": {
        "system": "today",
        "vendor": "YYYY-MM-05",
        "boot": "YYYY-MM-05"
      },
      "osVersion": "",
      "apps": [
        "com.google.android.gms",
        "com.android.vending"
      ]
    }
  }
}
```
Saving this file immediately notifies the running daemon to update its active target filters.

---

## Configuration & Practical Usage

Inside `/data/adb/teesim/config.json`:
- **Dynamic Date Syntax**: `today` dynamically resolves to the current month, and `YYYY-MM-05` maps to the 5th day of the current calendar month to match standard Android monthly security bulletin conventions.
- **Device Identity Emulation**: Fields such as `brand`, `model`, `serial`, and `imei` can be specified within a profile to satisfy ID attestation checks, or left blank to automatically inherit the physical device's real hardware identifiers.

---

## Troubleshooting & Common Issues

- **Recovery / Clean State**: If a bad configuration or experimental profile causes issues with key creation, restart the keystore daemon from a root shell:
  ```bash
  # Android 12+
  su -c 'kill $(pidof keystore2)'
  # Android 10-11
  su -c 'kill $(pidof keystore)'
  ```
  The keystore daemon will restart cleanly, running un-intercepted until the TEESimulator control daemon re-injects the configuration.
