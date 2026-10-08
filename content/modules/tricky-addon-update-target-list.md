---
id: "tricky-addon-update-target-list"
title: "Tricky Addon - Update Target List: WebUI Manager for Tricky Store and TEESimulator"
sidebarTitle: "Tricky Addon"
description: "Comprehensive WebUI configuration companion by KOWX712 for managing Tricky Store, TEESimulator, and OhMyKeymint target.txt package spoofing rules with one-tap toggles."
category: "security-certificates"
softwareType: "flashable-module"
tier: 1
searchQueries:
  - "tricky addon update target list"
  - "tricky store target.txt webui"
  - "tricky store exclamation mark leaf"
  - "tricky addon ksu module"
  - "teesimulator webui configure"
prerequisites:
  - "Root access via KernelSU, APatch, or Magisk"
  - "One active key attestation module: Tricky Store, TEESimulator, or OhMyKeymint"
  - "KernelSU / APatch built-in WebUI support or KSUWebUIStandalone for Magisk"
conflicts:
  - "None directly (operates purely as an interface configuration addon)"
configPaths:
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/modules/TA_utl/"
features:
  - "Native WebUI integration: embeds cleanly into KernelSU and APatch module management screens"
  - "One-tap package selection: search, filter, and toggle target spoofing across all installed user and system apps"
  - "Advanced target syntax support: effortlessly toggle the trailing exclamation mark (!) to switch between leaf cert and chain generation modes"
  - "Automated backup & sync: prevents accidental corruption of target lists and supports cloud/local export"
faq:
  - question: "What is the difference between listing a package as 'com.example.app' versus 'com.example.app!'?"
    answer: "In Tricky Store and TEESimulator, appending an exclamation mark (`!`) instructs the keystore hook to spoof only the leaf certificate rather than generating a complete synthetic hardware certificate chain. This is critical for certain banking apps and security verifiers that cross-check intermediate CA fingerprints against known root stores."
  - question: "Does this module work on Magisk?"
    answer: "Yes. In Magisk environments, Tricky Addon automatically provisions KSUWebUIStandalone or WebUI X, exposing an action trigger button in the Magisk app to launch the configuration interface in your browser."
  - question: "Does uninstalling this module erase my configured targets?"
    answer: "No. The actual targets file is stored independently at `/data/adb/tricky_store/target.txt`. Removing or updating the Tricky Addon module leaves your configured target list and keystore certificates untouched."
---

## Overview

**Tricky Addon - Update Target List**, developed by KOWX712, is an essential companion utility for modern Android keystore spoofing frameworks, including **Tricky Store**, **TEESimulator**, and **OhMyKeymint**.

Modern anti-abuse solutions, Play Integrity, and mobile banking applications increasingly query Android's Hardware Keystore (`KeyStore2` / `KeyMint`) through cryptographic attestation to verify that the bootloader is locked and the device is untampered. Frameworks like Tricky Store intercept these attestation calls in `keystore2` and inject valid hardware-backed leaf certificates.

However, Tricky Store relies on a plain-text configuration file located at `/data/adb/tricky_store/target.txt` to determine which specific packages should receive spoofed attestations. Manually editing this file through root text editors on a touchscreen is error-prone. Tricky Addon provides a responsive, native WebUI to search apps, toggle attestation rules, and inspect keystore routing in real time.

---

## Technical Mechanics & Keystore Interception

- **Target Application**: Requests KeyGen or hardware attestation (e.g., Google Play Services, Google Wallet, or banking apps).
- **Android Keystore 2.0 (`keystore2`)**: Intercepted at the HAL binder layer by Tricky Store.
- **Tricky Store Target Evaluation**:
  - **Match** (package listed in `target.txt`): Injects valid hardware attestation certificate chain and keybox credentials.
  - **No Match** (package not in `target.txt`): Passes request directly to stock device TEE / KeyMint hardware.

Tricky Addon interfaces directly with `/data/adb/tricky_store/target.txt`:

```
com.google.android.gms
com.google.android.apps.walletnfcrel
com.target.bank.app!
```

- When you check an application in the WebUI, Tricky Addon safely writes its package name to `target.txt`.
- When you toggle **Leaf Mode**, Tricky Addon appends the trailing `!` flag.
- Atomic file writes ensure that `keystore2` never reads a partially written target list during app initialization.

---

## WebUI Compatibility Matrix

| Root Solution | UI Delivery Method | Action Required |
| :--- | :--- | :--- |
| **KernelSU** | Native WebUI tab inside KernelSU app | Zero setup; open KernelSU -> Modules -> Tricky Addon -> WebUI |
| **APatch** | Native WebUI tab inside APatch app | Zero setup; tap WebUI button on module card |
| **Magisk** | KSUWebUIStandalone / WebUI X Portable | Automatically installs portable standalone host or opens via Action button |

---

## Best Practices for Target Configuration

1. **Avoid Universal Wildcards**: Never add every installed package to `target.txt`. Blanket spoofing can cause unexpected certificate mismatches in standard messaging apps and cloud services.
2. **Standard Targets**:
   - `com.google.android.gms` (Google Play Services, essential for MEETS_DEVICE_INTEGRITY / MEETS_STRONG_INTEGRITY)
   - `com.android.vending` (Google Play Store)
   - Specific financial, banking, or enterprise apps requiring hardware attestation
3. **Use Leaf Mode (`!`) When Necessary**: If a banking app crashes or reports an invalid certificate authority after adding to `target.txt`, enable the trailing `!` flag in Tricky Addon to restrict spoofing strictly to the leaf certificate.
