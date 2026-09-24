---
id: "trickystore"
title: "TrickyStore: Hardware Keystore Attestation & Keybox Spoofer"
sidebarTitle: "TrickyStore"
description: "Advanced Keystore HAL interception module enabling devices with unlocked bootloaders to satisfy MEETS_STRONG_INTEGRITY via custom keybox injection."
category: "root-management"
tier: 1
searchQueries:
  - "trickystore magisk module"
  - "how to pass meets strong integrity"
  - "tricky store keybox xml setup"
  - "key attestation bypass android 14"
  - "trickystore target txt guide"
prerequisites:
  - "Magisk, KernelSU, or APatch with Zygisk support"
  - "Valid, non-revoked AOSP or OEM `keybox.xml` certificate bundle"
conflicts:
  - "Other Keymaster/Keystore HAL hijacking modules"
configPaths:
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/modules/trickystore/"
features:
  - "Hooks into Android Keystore 2.0 and Keymaster HAL daemons"
  - "Injects custom certificate chains and EC/RSA private keys into hardware attestation requests"
  - "Granular target selection: specify exact packages that should receive spoofed certificate chains"
  - "Achieves MEETS_STRONG_INTEGRITY on rooted hardware with unlocked bootloaders"
faq:
  - question: "Where do I obtain a valid keybox.xml?"
    answer: "A keybox is an OEM cryptographic credential containing an ECDSA/RSA private key and a matching attestation certificate chain signed by Google. Keyboxes cannot be generated locally; they must be dumped from factory test builds, OEM recovery firmware, or leaked engineering devices."
  - question: "Will TrickyStore work without a keybox.xml?"
    answer: "No. Without a valid keybox.xml, TrickyStore cannot forge the cryptographic signature required by Google's attestation servers for MEETS_STRONG_INTEGRITY. If you only have a standard device fingerprint, use PlayIntegrityFork to achieve MEETS_DEVICE_INTEGRITY instead."
---

## Overview

Developed by **5ec1cff**, **TrickyStore** is an advanced low-level module that operates at the Android Keystore HAL (Hardware Abstraction Layer) boundary. 

Starting with Android 8.0 and strictly enforced in modern versions, Google Play Integrity utilizes **Hardware-Backed Key Attestation**. When a banking or payment application demands strong assurance, Android's Keystore delegates key generation to the device's physical Trusted Execution Environment (TEE) or StrongBox chip. The TEE creates an asymmetric key pair and signs an attestation certificate chain containing a root of trust flag (`bootloader: UNLOCKED`).

TrickyStore intercepts these attestation requests inside Keystore daemons, substituting the hardware response with an attestation certificate chain signed by a legitimate, unrevoked OEM keybox, successfully convincing Google that the device has a locked bootloader and verified boot state.

---

## Technical Architecture & How It Works

### Keystore 2.0 / Keymaster HAL Interception

1. **Service Hooking**: On Android 12+, Android manages keys via the `android.system.keystore2` binder service. TrickyStore injects native hooks into the Keystore 2 daemon (`keystore2`).
2. **Attestation Interception**: When a target process (like Google Play Services or an enterprise security app) requests `generateKey` with attestation challenges, TrickyStore intercepts the call before it is processed by the hardware Keystore HAL.
3. **Keybox Substitution**: TrickyStore uses the cryptographic keys and certificate chains provided in `/data/adb/tricky_store/keybox.xml` to construct a valid X.509 certificate chain.
4. **Root of Trust Forgery**: The generated certificate includes an ASN.1 attestation extension where `verifiedBootState` is marked as `Verified` and `deviceLocked` is set to `true`.
5. **Target Filtering**: Through `/data/adb/tricky_store/target.txt`, TrickyStore only intercepts attestation for explicitly declared applications, allowing biometric unlock and DRM keys (Widevine L1) to continue utilizing hardware Keystore without corruption.

---

## Installation & Configuration

### Step 1: Install TrickyStore
1. Flash `TrickyStore-vX.zip` in your root manager (Magisk, KernelSU, or APatch).
2. Reboot your device.

### Step 2: Configure keybox.xml
Place your valid keybox file into `/data/adb/tricky_store/keybox.xml`:
```xml
<?xml version="1.0"?>
<AndroidAttestation>
    <NumberOfKeyboxes>1</NumberOfKeyboxes>
    <Keybox DeviceID="...">
        <Key algorithm="ecdsa">
            <PrivateKey format="pem">
-----BEGIN EC PRIVATE KEY-----
...
-----END EC PRIVATE KEY-----
            </PrivateKey>
            <Certificate format="pem">
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
            </Certificate>
        </Key>
    </Keybox>
</AndroidAttestation>
```

### Step 3: Configure target.txt
Define the packages that require spoofed attestation in `/data/adb/tricky_store/target.txt`:
```text
com.google.android.gms
com.google.android.gms.unstable
com.android.vending
```
*(Append any specific banking or enterprise app package names that perform direct Key Attestation).*

---

## Common Issues & Troubleshooting

- **Revoked Keybox**: If Google discovers a leaked keybox, they add its certificate serial number to the Android CRL (Certificate Revocation List). When this happens, attestation immediately fails with `REVOKED` or falls back to `NO_INTEGRITY`. You must replace the keybox in `/data/adb/tricky_store/keybox.xml` with an unrevoked one.
- **Biometric Unlock / FIDO Breakage**: If biometric app locks stop working, check `/data/adb/tricky_store/target.txt` and ensure system biometric framework packages (`com.android.settings`, `android`) are **NOT** included in the file.
