---
id: "bootloader-spoofer"
title: "Bootloader Spoofer: Bypass Local Hardware KeyStore Attestation"
sidebarTitle: "Bootloader Spoofer"
description: "Targeted Xposed hook by chiteroman that patches KeyStore ASN.1 certificate extensions in memory to conceal unlocked bootloader states from local integrity verifiers."
category: "xposed-runtime-hooks"
tier: 1
searchQueries:
  - "bootloader spoofer lsposed"
  - "chiteroman bootloader spoofer apk"
  - "spoof locked bootloader android"
  - "bypass local key attestation root"
  - "xposed hide unlocked bootloader"
prerequisites:
  - "Android 8.0 (Oreo) or newer"
  - "LSPosed framework running with active Zygisk injection"
conflicts:
  - "Selecting Google Play Services, Play Store, or System Framework in the LSPosed scope (will invalidate Google server-side Play Integrity checks)"
  - "Global un-scoped Xposed hooks targeting KeyStore certificate parsers"
configPaths:
  - "/data/system/users/0/lspd/"
features:
  - "ASN.1 Certificate Extension Patching: dynamically alters RootOfTrust and verifiedBootState fields in client memory"
  - "Targeted per-app scoping: only runs inside selected financial, enterprise, or banking applications"
  - "Zero system modifications: leaves hardware TEE/SE keystore keys intact while modifying return certificates in userspace"
  - "Local attestation bypass: tricks apps that parse X.509 certificate chains locally into reporting locked bootloader"
faq:
  - question: "Why does Bootloader Spoofer only work for 'local' attestations?"
    answer: "Android hardware attestation signs an X.509 certificate chain inside the hardware TEE (Trusted Execution Environment) or StrongBox chip using Google-issued root keys. If an application sends this certificate chain to its remote backend servers for verification, the server checks the cryptographic signature; modifying the certificate locally invalidates the signature, causing verification to fail. However, many banking and enterprise apps inspect the certificate attributes locally on the device—which Bootloader Spoofer intercepts and patches cleanly."
  - question: "Why should I NEVER select Google Play Services or System Framework in the scope?"
    answer: "Google Play Services (`com.google.android.gms`) generates Play Integrity verdicts by sending certificate data directly to Google cloud verification endpoints. Hooking KeyStore inside Play Services invalidates the hardware signature, causing MEETS_STRONG_INTEGRITY and MEETS_DEVICE_INTEGRITY to fail immediately. Only select the specific third-party banking/work apps that complain about an unlocked bootloader."
  - question: "How do I configure Bootloader Spoofer in LSPosed?"
    answer: "1. Install `app-release.apk`. 2. Open LSPosed Manager -> Modules tab -> tap Bootloader Spoofer. 3. Toggle the module ON. 4. In the Scope list, select ONLY the specific banking or enterprise application that blocks execution. 5. Force close the target app and reopen it."
---

## Overview

When an Android device's bootloader is unlocked (a necessary step for flashing custom recovery images, KernelSU, or Magisk), the hardware Trusted Execution Environment (TEE) updates its internal hardware flags:
- `deviceLocked` is set to `false`.
- `verifiedBootState` changes from `Verified` to `Unverified` or `Orange`.

Modern financial applications, enterprise MDM agents (like Microsoft Intune, MobileIron), and DRM-protected streaming apps increasingly inspect hardware-backed keystores via **Android KeyStore Key Attestation**. They generate an asymmetric key pair and query the certificate chain (`getCertificateChain()`). Embedded within the certificate's ASN.1 extension data (OID `1.3.6.1.4.1.11129.2.1.17`) are explicit data structures indicating that the bootloader has been unlocked.

Even if an application cannot detect `su` binaries or Magisk packages due to Zygisk denylist or Shamiko, reading this certificate chain locally allows it to detect an unlocked bootloader and terminate execution.

**Bootloader Spoofer**, developed by security researcher chiteroman (creator of PlayIntegrityFix), hooks these local certificate queries in userland application memory.

---

## Technical Hooking Architecture

Android applications perform local key attestation by invoking `java.security.KeyStore.getCertificateChain(alias)`. The operating system returns an array of `Certificate` objects containing an ASN.1 encoded byte sequence representing the `RootOfTrust`:

```
┌────────────────────────────────────────────────────────┐
│             Target Banking / Enterprise App            │
│  - Calls KeyStore.getCertificateChain("my_key")        │
└───────────────────────────┬────────────────────────────┘
                            │ Intercepted in memory
┌───────────────────────────▼────────────────────────────┐
│               Bootloader Spoofer Hook                  │
│  - Intercepts return value of getCertificateChain()    │
│  - Parses ASN.1 sequence:                              │
│    * Replaces verifiedBootState: Orange -> Verified    │
│    * Replaces deviceLocked: false -> true              │
│  - Re-encodes modified X.509 Certificate               │
└───────────────────────────┬────────────────────────────┘
                            │ Returns spoofed certificate
┌───────────────────────────▼────────────────────────────┐
│               Target App Verification Logic            │
│  - Reads: deviceLocked = true                          │
│  - Concludes: Bootloader is LOCKED                     │
│  - App launches successfully                           │
└────────────────────────────────────────────────────────┘
```

Because the modification happens in userspace RAM immediately before the application's local verification routines parse the certificate, the app observes a clean, locked device state.

---

## Strict Scope Configuration Rules

Because Bootloader Spoofer alters certificate bytes in memory, **the cryptographic signature of the certificate is altered**:

> [!WARNING]
> **Strict Rule**: NEVER add `com.google.android.gms` (Google Play Services), `com.android.vending` (Google Play Store), or `android` (System Framework) to the LSPosed scope for Bootloader Spoofer. Doing so will break remote Google Play Integrity checks.

### Safe Configuration Steps:
1. Sideload and install `app-release.apk` from the official Bootloader Spoofer release.
2. Launch **LSPosed Manager** and tap the **Modules** icon.
3. Locate **Bootloader Spoofer** and toggle it **ON**.
4. In the application list, check **ONLY** the specific third-party applications (e.g., your banking app, enterprise portal, or KeyAttestation test app).
5. Swipe the target app out of Recent Apps to terminate its process.
6. Launch the target app; it will now pass local bootloader security checks without error.

---

## Limitations: Local vs Remote Attestation

It is critical to distinguish between local and remote attestation:

- **Local Attestation (Supported)**: The application code inspects the certificate directly on your phone using bundled Java/Kotlin logic. Bootloader Spoofer successfully bypasses 100% of these checks.
- **Remote / Server-Side Attestation (Unsupported)**: The application uploads the raw DER-encoded certificate chain to its backend cloud servers, where the server verifies the cryptographic signature against Google's Root CA public key. In this scenario, any local modification destroys signature mathematical validity, and the server rejects the device. For server-side checks, use `PlayIntegrityFix` and `TrickyStore`.
