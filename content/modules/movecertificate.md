---
id: "movecertificate"
title: "MoveCertificate: Android 14+ Conscrypt APEX Certificate Mover"
sidebarTitle: "MoveCertificate"
description: "Specialized security module designed for Android 14 and 15 that binds user-installed CA certificates directly into the Conscrypt APEX trust store."
category: "security-certificates"
tier: 1
searchQueries:
  - "movecertificate magisk module"
  - "install burp certificate android 14"
  - "android 14 system ca cert apex"
  - "ys1231 movecertificate"
  - "trust user cert android 15"
prerequisites:
  - "Android 14 or Android 15"
  - "Magisk, KernelSU, or APatch"
conflicts:
  - "Legacy AlwaysTrustUserCerts (which only works on Android 13 and older)"
configPaths:
  - "/apex/com.android.conscrypt/cacerts/"
  - "/data/misc/user/0/cacerts-added/"
features:
  - "Full compatibility with Android 14+ Updatable APEX Conscrypt security architecture"
  - "Uses mount namespace overlays to inject certificates into `/apex/com.android.conscrypt/cacerts/`"
  - "Automatically monitors, rehashes, and permissions user certificates on every boot"
  - "Restores full HTTPS decryption support for Burp Suite, Charles, and mitmproxy on Android 14/15"
faq:
  - question: "Why did certificate modules stop working on Android 14?"
    answer: "In Android 14, Google converted the Conscrypt security provider into an Updatable APEX package. The CA certificate store was migrated from /system/etc/security/cacerts/ to an immutable APEX loop mount at /apex/com.android.conscrypt/cacerts/. Standard Magisk modules mounting to /system no longer affect TLS verification. MoveCertificate creates an overlay specifically targeting the Conscrypt APEX mount namespace."
  - question: "Can I use MoveCertificate on Android 13 or older?"
    answer: "No. On Android 13 and older, the system certificate directory is located at /system/etc/security/cacerts/. Use AlwaysTrustUserCerts for Android 7 through 13."
---

## Overview

Developed by **ys1231**, **MoveCertificate** was engineered specifically to solve the architectural breaking changes introduced in **Android 14** regarding system certificate trust.

In Android 14, Google completed the migration of core operating system security components into Mainline APEX modules. The root CA certificate directory was permanently relocated from `/system/etc/security/cacerts/` into the read-only, mounted filesystem of the `com.android.conscrypt` APEX. Because of this, traditional Magisk modules that mounted certificates into `/system` ceased functioning completely on Android 14. MoveCertificate implements advanced mount namespace injection to restore full SSL/TLS traffic interception.

---

## Technical Architecture & How It Works

### APEX Mount Namespace Injection

1. **Certificate Scanning**: During early boot, MoveCertificate scans user-installed certificates stored in `/data/misc/user/0/cacerts-added/`.
2. **Temporary Overlay Creation**: It constructs a temporary directory containing both stock Conscrypt CA certificates and your newly added user certificates.
3. **APEX Namespace Overlay**: Because APEX mounts exist in their own private Linux mount namespaces, the module runs a native script inside the root namespace:
   ```bash
   mount --bind /data/local/tmp/cacerts_merged /apex/com.android.conscrypt/cacerts
   ```
4. **Bionic Trust Propagation**: When Android apps initialize TLS sessions, the Bionic Conscrypt crypto engine reads the merged certificates directly from the APEX mount, trusting proxy CA certificates globally.

---

## Installation & Usage

1. Open your root manager (**Magisk**, **KernelSU**, or **APatch**).
2. Download and flash `MoveCertificate-vX.zip`.
3. Reboot your device.
4. Install your proxy CA certificate (e.g. Burp Suite, mitmproxy, Charles) via Android's standard **Settings** $\rightarrow$ **Security** $\rightarrow$ **Install from storage** $\rightarrow$ **CA Certificate**.
5. Reboot your device one more time.
6. Verify under **Settings** $\rightarrow$ **Trusted Credentials** $\rightarrow$ **System**: your proxy certificate is now listed as a valid system authority.
