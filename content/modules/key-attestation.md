---
id: "key-attestation"
title: "Key Attestation: Cryptographic Hardware Keystore & KeyMint Diagnostic Tool"
sidebarTitle: "Key Attestation"
description: "Authoritative, network-isolated diagnostic security tool by vvb2060 for generating, analyzing, and validating Android Hardware Keystore, StrongBox, and KeyMint certificate chains."
category: "security-certificates"
softwareType: "standalone-app"
tier: 1
searchQueries:
  - "key attestation apk vvb2060"
  - "android hardware keystore attestation test"
  - "keymint strongbox verify android"
  - "verifiedbootstate locked check"
  - "tricky store key attestation"
prerequisites:
  - "Android 7.0 (Nougat / API 24) or newer (Keymaster 2.0+ support)"
  - "Works fully rootless (no root required)"
conflicts:
  - "None (operates purely as an offline analysis utility)"
configPaths:
  - "vvb2060.org.web.application.keyattestation"
features:
  - "Zero network permissions: contains no INTERNET permission, ensuring complete data privacy and tamper-free offline analysis"
  - "KeyMint & StrongBox verification: inspects security levels across Trusted Execution Environments (TEE) and dedicated Secure Elements (SE)"
  - "ASN.1 attestation parser: decodes verified boot state, OS patch levels, unlock status, and root-of-trust public key hashes"
  - "Exportable certificate chains: exports raw PEM/DER certificate chains for external verification on independent workstations"
faq:
  - question: "Why does Key Attestation intentionally lack internet access?"
    answer: "Security verifications must be deterministic and trust-minimized. By omitting the `android.permission.INTERNET` permission entirely, the app guarantees that private keys and attestation payloads cannot be exfiltrated. Furthermore, it embeds certificate revocation lists directly inside the APK, preventing MITM attacks during network requests."
  - question: "What does 'Software' vs 'TrustedEnvironment' vs 'StrongBox' mean in the report?"
    answer: "`Software` indicates keys are stored in standard Android OS memory, vulnerable to root compromise. `TrustedEnvironment` (TEE) indicates the private key is physically isolated inside a secure processor enclave (ARM TrustZone). `StrongBox` represents a dedicated discrete hardware security chip (such as Google Titan M2, Apple Secure Enclave, or Samsung Knox Vault) with tamper-resistant packaging and independent power lines."
  - question: "How is Key Attestation used alongside Tricky Store or TEESimulator?"
    answer: "Modders and developers use Key Attestation as the definitive ground truth test. If Tricky Store is configured to target Key Attestation, the app will generate an attestation request and display whether your spoofed hardware certificate is properly delivered with a simulated 'Verified' bootloader status."
---

## Overview

**Key Attestation**, created by renowned Android system researcher vvb2060, is the canonical open-source utility for inspecting the integrity and cryptographic capabilities of Android's hardware-backed keystore subsystem.

Beginning with Android 7.0 (Nougat), Google introduced **Key and ID Attestation** to enable security-sensitive services (such as Google Pay, mobile banking, and MDM solutions) to cryptographically verify that cryptographic keys are physically generated and locked inside hardware enclaves—and that the device's bootloader is securely locked.

Key Attestation generates an asymmetric key pair inside your device's hardware keystore (`KeyStore2` / `KeyMint`) and displays the full X.509 certificate chain, parsing every authorization extension down to individual ASN.1 bitflags.

---

## Technical Mechanics & ASN.1 Attestation Records

When Key Attestation prompts KeyStore to generate an attested key pair, the hardware security module signs a leaf certificate using its factory-provisioned private key. The leaf certificate contains a custom X.509 extension (OID `1.3.6.1.4.1.11129.2.1.17`):

```
┌────────────────────────────────────────────────────────┐
│                   Key Attestation App                  │
│       Generates EC/RSA key with Attestation Challenge  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                  KeyMint / Hardware TEE                │
│  - Generates key pair inside secure hardware enclave   │
│  - Signs certificate chain using batch attestation key │
│  - Embeds immutable security parameters into ASN.1     │
└───────────────────────────┬────────────────────────────┘
                            │ returns X.509 Certificate Chain
┌───────────────────────────▼────────────────────────────┐
│              Parsed Security Attestation               │
│  • Security Level: TrustedEnvironment / StrongBox      │
│  • Verified Boot State: Verified / SelfSigned / Locked │
│  • OS Version & Security Patch Level: YYYY-MM          │
│  • Verified Boot Key (SHA-256): [OEM Root Hash]        │
└────────────────────────────────────────────────────────┘
```

### Critical Authorization Tags

Key Attestation parses and displays the exact security properties attested by the hardware:
- **`attestationSecurityLevel`**: Confirms whether the attestation was executed by software or genuine hardware.
- **`verifiedBootState`**:
  - `Verified` (0): Device booted with official OEM locked bootloader and verified boot chain.
  - `SelfSigned` (1): Bootloader locked with a user-provided custom root of trust key.
  - `Unverified` (2): Bootloader is completely unlocked (triggers Play Integrity failures).
  - `Failed` (3): Boot verification failed.
- **`verifiedBootKey`**: The SHA-256 fingerprint of the public key burned into hardware fuses that validated your current boot image.

---

## Independent Offline Verification

Because an active root environment with zygote hooks can theoretically tamper with local display rendering, Key Attestation supports full offline export:
1. Tap the **Share / Save** icon in Key Attestation to save the certificate chain as a file.
2. Transfer the exported file to a secure, unrooted workstation or second phone.
3. Open Key Attestation on the second device and choose **Load Certificate Chain**, or verify using OpenSSL:
   ```bash
   openssl x509 -in cert.pem -text -noout
   ```
4. This guarantees that your hardware attestation results are completely authentic and unaffected by runtime display hooks.
