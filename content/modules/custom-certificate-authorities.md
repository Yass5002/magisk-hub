---
id: "custom-certificate-authorities"
title: "Custom Certificate Authorities: System Trust Store Promotion with DER-to-PEM & APEX Support"
sidebarTitle: "Custom Certificate Authorities"
description: "Promotes user-installed CA certificates into the Android system trust store with automatic DER-to-PEM conversion and dual bind mounts for modern APEX Conscrypt and BoringSSL."
category: "security-certificates"
tier: 1
searchQueries:
  - "custom certificate authorities magisk module"
  - "whalehub custom certificate authorities"
  - "android 14 system ca cert root"
  - "der to pem automatic ca convert android"
  - "flutter boringssl custom ca trust store"
prerequisites:
  - "Android 11 or newer (up to Android 15+)"
  - "Magisk v24.1 or newer"
  - "CA certificates installed via standard Android Settings user credential storage"
conflicts: []
configPaths:
  - "/data/adb/modules/Custom-Certificate-Authorities/"
  - "/data/local/tmp/customcert.log"
features:
  - "Zero-configuration ingestion: imports certificates directly from Android's user credential storage without manual openssl command hashing"
  - "Automatic DER-to-PEM conversion: detects binary DER-encoded certificates and converts them to PEM format on the fly"
  - "Full BoringSSL & Flutter compatibility: injects certificates into legacy system paths required by non-Conscrypt TLS engines"
  - "Modern APEX Conscrypt support: handles Android 14+ updatable Conscrypt APEX trust stores via bind mounting"
  - "Multi-user profile support: sweeps and integrates certificates configured across secondary user and work profiles"
---

## Overview

Starting in Android 7.0 (Nougat), Google updated the platform network security policy so that application network stacks trust only system-installed Certificate Authorities (CAs) by default, disregarding user-installed certs. For security researchers, reverse engineers, and enterprise developers using network interception proxies (such as Burp Suite, Charles, or mitmproxy), inspecting HTTPS traffic requires moving the interception root certificate into the system trust store.

In Android 14, this process became even more challenging: Google relocated system certificates into the read-only, updatable Conscrypt APEX module (`/apex/com.android.conscrypt/cacerts`), breaking older Magisk modules that merely placed certificate files into `/system/etc/security/cacerts`. Furthermore, apps compiled with modern frameworks like Flutter/Dart utilize statically linked BoringSSL libraries that ignore Conscrypt and fail if certificates are provided in binary DER format instead of PEM.

Developed by whalehub and Loukious, **Custom Certificate Authorities** addresses all of these architectural complexities in a single, automated boot script.

## Core Features & Architecture

### 1. Dual-Path APEX & Legacy Mounting
On Android 14 and newer, network trust is bifurcated:
- **System Conscrypt Store**: Located at `/apex/com.android.conscrypt/cacerts/`
- **Legacy Framework & BoringSSL Store**: Located at `/system/etc/security/cacerts/`

Custom Certificate Authorities scans user-installed certificates and performs dynamic bind mounts targeting **both** locations simultaneously. This guarantees that standard Java `HttpsURLConnection` calls, Chromium WebViews, OkHttp clients, and native BoringSSL stacks all recognize your proxy CA.

### 2. Automated DER-to-PEM Transformation
Many network proxies or corporate portals distribute root certificates in binary DER format (`.crt` or `.cer`). BoringSSL strictly rejects DER certificates in system trust directories, requiring Base64-encoded PEM formatting (`.0` hash files). The module automatically detects incoming certificate encoding and converts DER to PEM format during boot without requiring external desktop conversion scripts.

### 3. Multi-User & Work Profile Harvesting
In multi-user setups (such as devices utilizing work profiles, Island, or Shelter), user certificates are isolated in numbered credential directories (`/data/misc/user/<userid>/cacerts-added`). The module recursively traverses all active user profile namespaces to consolidate CA certificates into the system root.

## How to Add Certificates

You do not need to rename files or calculate Subject Name hashes manually:

1. Flash and install **Custom Certificate Authorities** in Magisk, then reboot.
2. Transfer your proxy's CA certificate (e.g., `cacert.der`, `charles-ssl-proxying-certificate.pem`) to your smartphone's storage.
3. Open Android **Settings** → **Security & Privacy** → **More Security Settings** → **Encryption & credentials** → **Install a certificate** → **CA certificate**.
4. Select your certificate file and confirm installation.
5. **Reboot your device**.
6. During the boot sequence, the module reads the newly installed user certificate, converts it if necessary, and bind-mounts it into both system certificate stores.

## Verification & Diagnostics

To verify that your certificate was successfully promoted:

1. Open Android **Settings** → **Encryption & credentials** → **Trusted credentials** → **System**.
2. Scroll to locate your proxy certificate authority; it should now appear in the System list rather than the User list.
3. Review the module execution log in an ADB or root terminal:
   ```bash
   su -c cat /data/local/tmp/customcert.log
   ```
   The log confirms file discovery, conversion results, and mount states for both Conscrypt and legacy directories.
