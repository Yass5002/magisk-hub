---
id: "custom-certificates"
title: "Custom Certificates: System Trust Store Injection with Hybrid Mount Stealth"
sidebarTitle: "Custom Certificates"
description: "Injects user-installed CA certificates into Android's system trust store with meta-hybrid_mount support to hide tmpfs mount artifacts from root detectors."
category: "security-certificates"
tier: 1
searchQueries:
  - "custom certificates magisk module"
  - "yujiacheng1996 custom certificates"
  - "meta hybrid mount certificate injection"
  - "hide tmpfs cert mount android root"
  - "adguard cert custom trust store"
prerequisites:
  - "Android 10 through Android 15+"
  - "Root access via Magisk, KernelSU, or APatch"
  - "User CA certificates installed via Android Settings credential storage"
  - "Optional meta-hybrid_mount module to conceal tmpfs mount traces from integrity detectors"
conflicts:
  - "adguardcert (AdGuard Certificate module)"
  - "custom-certificate-authorities (incompatible mount clash; remove before installing)"
configPaths:
  - "/data/adb/modules/custom-certificates/"
features:
  - "Automated trust store promotion: sweeps user credential storage on boot and binds certificates into the system root authority store"
  - "Stealth tmpfs concealment: integrates with meta-hybrid_mount to eliminate detectable tmpfs mount points"
  - "APEX partition compatibility: handles modern Android 14+ updatable Conscrypt APEX trust stores"
  - "Simple two-step workflow: install certificate in Android Settings and reboot to achieve global application trust"
---

## Overview

Modern Android versions strictly isolate user-installed Certificate Authorities (CAs), refusing to trust them for HTTPS inspection in third-party applications. While several modules exist to copy certificates from user storage to the system store, most standard implementations utilize exposed `tmpfs` bind mounts over `/system/etc/security/cacerts` or Conscrypt APEX directories. Sophisticated root detection libraries (such as those found in banking applications and anti-cheat engines) scan `/proc/mounts` for these `tmpfs` overlays and flag the device as tampered.

Developed by YujiaCheng1996, **Custom Certificates** builds upon foundational work from AdGuard Certificate and Custom-Certificate-Authorities, while introducing specialized stealth integration. By partnering with **`meta-hybrid_mount`**, it injects user-installed certificates into the system authority store without leaving exposed `tmpfs` traces in process mount tables.

## Explicit Module Incompatibilities

> [!WARNING]
> **Custom Certificates is strictly incompatible with `adguardcert` and `custom-certificate-authorities`.**

Because all three modules attempt to control and mount the Android system CA certificate paths, flashing this module alongside either predecessor will cause mount collisions and broken certificate stores. You must completely uninstall existing certificate modules before installing Custom Certificates.

## Stealth Integration (`meta-hybrid_mount`)

To prevent root detection suites from spotting certificate mounts:
1. Install **`meta-hybrid_mount`** through your root manager.
2. If using an older revision of `meta-hybrid_mount`, ensure that `apex` is explicitly included in its target partitions list.
3. Install **Custom Certificates**.
4. The module leverages hybrid overlay mounting to present the modified certificate store seamlessly within the stock filesystem namespace.

## Step-by-Step Certificate Installation

1. Uninstall any older certificate promotion modules.
2. Install **Custom Certificates** in Magisk, KernelSU, or APatch.
3. Open Android **Settings** → **Security & Privacy** → **More Security Settings** → **Encryption & credentials** → **Install a certificate** → **CA certificate**.
4. Select your root certificate file (e.g., from Burp Suite, AdGuard, or mitmproxy) and confirm installation.
5. **Reboot your device**.
6. On startup, the module harvests newly added certificates and mounts them into the system trust store.

## Verification

To verify that your certificate is recognized system-wide:

1. Open **Settings** → **Encryption & credentials** → **Trusted credentials** → **System**.
2. Locate your custom certificate authority name in the list.
3. Launch your target app through an interception proxy to confirm transparent HTTPS decryption.
