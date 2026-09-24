---
id: "alwaystrustusercerts"
title: "AlwaysTrustUserCerts: System-Wide SSL/TLS Certificate Injection"
sidebarTitle: "AlwaysTrustUserCerts"
description: "Security analysis module by NVISO that automatically elevates user-installed CA certificates into the system trust store for seamless HTTPS traffic inspection."
category: "security-certificates"
tier: 1
searchQueries:
  - "alwaystrustusercerts magisk module"
  - "install burp suite cert system android"
  - "mitmproxy system ca cert android 14"
  - "how to trust user certs as system certs"
  - "nvisosecurity alwaystrustusercerts"
prerequisites:
  - "Android 7.0 through Android 13 (for Android 14+, see MoveCertificate)"
  - "Magisk, KernelSU, or APatch"
conflicts:
  - "MoveCertificate (choose one based on Android OS version)"
configPaths:
  - "/system/etc/security/cacerts/"
  - "/data/misc/user/0/cacerts-added/"
features:
  - "Automated user-to-system CA certificate promotion during boot"
  - "Magic Mount overlay onto `/system/etc/security/cacerts/` without modifying read-only system partitions"
  - "Essential utility for penetration testing, mobile security auditing, and API reverse engineering"
  - "Allows Burp Suite, Charles Proxy, and mitmproxy to decrypt HTTPS traffic from all applications"
faq:
  - question: "Why doesn't Android trust user-installed CA certificates by default?"
    answer: "Starting in Android 7.0 (Nougat), Google updated the default Network Security Configuration to ignore user-installed CA certificates for application traffic. Apps only trust certificates stored in the read-only /system/etc/security/cacerts/ directory. This module bridges that gap by mounting user certificates directly into the system trust store."
  - question: "Why does this module fail on Android 14?"
    answer: "In Android 14+, Google moved root CA certificates out of /system/etc/security/cacerts/ and into an immutable, updatable APEX container (com.android.conscrypt). Standard systemless overlay mounts cannot modify the Conscrypt APEX. On Android 14 and newer, use the MoveCertificate module instead."
---

## Overview

Developed by **NVISO Security**, **AlwaysTrustUserCerts** is the de-facto standard mobile penetration testing tool for intercepting SSL/TLS encrypted traffic on rooted Android devices.

When security researchers or developers need to inspect mobile API traffic using proxy tools like **Burp Suite**, **OWASP ZAP**, or **mitmproxy**, they install custom root CA certificates on the device. However, modern Android versions strictly isolate user CAs from application network stacks. AlwaysTrustUserCerts automatically monitors user certificate installations and elevates them into the authoritative system trust store at boot.

---

## Technical Architecture & How It Works

### The Systemless Certificate Overlay

1. **User Certificate Detection**: When a user installs a certificate via Android Settings $\rightarrow$ Security $\rightarrow$ Encryption & Credentials, Android places the `.0` hashed certificate file into `/data/misc/user/0/cacerts-added/`.
2. **Early Boot Synchronization**: During the `post-fs-data` stage, AlwaysTrustUserCerts scans `/data/misc/user/0/cacerts-added/` for new certificates.
3. **Magic Mount Integration**: The module copies the detected certificates into `/data/adb/modules/alwaystrustusercerts/system/etc/security/cacerts/` and fixes permissions (`chmod 644`, `chown root:root`).
4. **Trust Store Overlay**: Magisk / KernelSU mounts this directory over `/system/etc/security/cacerts/`. When any application initiates a TLS handshake, Android's Bionic cryptographic libraries treat the proxy certificate as a pre-installed, trusted root authority.

---

## Installation & Usage (Penetration Testing Workflow)

### Step 1: Install the Module
1. Download `AlwaysTrustUserCerts.zip` and flash it in **Magisk** or **KernelSU**.
2. Reboot your device.

### Step 2: Install Your Proxy CA Certificate
1. Export the CA certificate from your proxy tool (e.g., `cacert.der` from Burp Suite).
2. Rename the extension to `.crt` and transfer it to your device's internal storage.
3. On your Android device, go to **Settings** $\rightarrow$ **Security** $\rightarrow$ **Install a certificate** $\rightarrow$ **CA certificate** $\rightarrow$ select the file.
4. Name the certificate (e.g., "BurpCA") and confirm.

### Step 3: Reboot to Promote
Reboot your phone. The certificate will now appear under **Trusted Credentials** $\rightarrow$ **System**, and your proxy will successfully decrypt HTTPS API requests.
