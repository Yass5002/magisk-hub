---
id: "zygisk-cacerts"
title: "Zygisk CAcerts: Modern AOSP Root Certificate Store Injection"
sidebarTitle: "Zygisk CAcerts"
description: "Systemless security utility by vvb2060 that updates Android's root certificate store with upstream AOSP CA certificates across Android 7 through 16 with 16k page size support."
category: "security-certificates"
tier: 1
searchQueries:
  - "zygisk cacerts vvb2060"
  - "update root certificates android magisk"
  - "aosp ca-certificates module"
  - "zygisk 16k page size cacerts"
  - "fix expired root certificates android"
prerequisites:
  - "Rooted Android device running Android 7.0 through Android 16"
  - "Magisk, KernelSU, or APatch"
  - "Zygisk enabled in your root manager"
conflicts: []
configPaths:
  - "/data/adb/modules/zygisk_cacerts/"
features:
  - "Upstream AOSP certificate store: replaces legacy or outdated root certificates with official upstream AOSP certificate archives"
  - "Modern architecture ready: fully supports ARM64, RISC-V (riscv64), and modern 16KB kernel memory page alignment"
  - "SELinux context remediation: automatically applies correct security contexts across older Android releases (pre-Android 10)"
  - "Zero network dependencies: embeds clean, verified certificate bundles directly in the module without requiring dynamic internet queries"
---

## Overview

Zygisk CAcerts, developed by recognized Android security researcher vvb2060, updates Android's system root certificate store (`/system/etc/security/cacerts`) with the latest official certificates from the upstream Android Open Source Project (AOSP) tree.

As Android devices age and stop receiving official monthly operating system updates from device manufacturers, their embedded root certificate authorities (CAs) gradually expire or get revoked by security consortiums (such as the deprecation of older Let's Encrypt or Sectigo cross-signatures). When a device's trust store falls out of date, modern HTTPS websites, secure banking APIs, and VPN connections begin throwing SSL/TLS handshake failures. Zygisk CAcerts resolves this by mounting modern trusted certificates cleanly at early boot.

## Prerequisites & Compatibility

- **Android Version**: Broad compatibility spanning Android 7.0 (Nougat) up through Android 16.
- **Root Framework**: Magisk, KernelSU, or APatch with **Zygisk enabled**.
- **Hardware Architecture**: Supports ARM, ARM64, x86, and **RISC-V (`riscv64`)**, alongside compatibility with modern **16KB memory page size** kernels.

There are no documented module conflicts.

## Key Architecture & Features

### 1. Direct Upstream Synchronization
The module sources its root certificate store directly from the official [AOSP ca-certificates repository](https://android.googlesource.com/platform/system/ca-certificates/). Each release incorporates the newest cryptographic standards, including root certificate additions and revoking compromised CAs.

### 2. Low-Level Mount & Context Fixing
- Uses early boot scripts (`post-fs-data.sh`) to mount the updated certificate store over `/system/etc/security/cacerts`.
- Automatically enforces valid SELinux labeling (`system_file`) across Android versions, preventing AVC audit denials on Android 9 and older versions that could prevent network daemons from reading certificates.

## Installation & Verification

1. Download the latest `zygisk_cacerts-*-release.zip` package from the repository releases.
2. Flash the module through Magisk, KernelSU, or APatch.
3. Reboot the device.
4. Active module assets reside in:
   ```bash
   /data/adb/modules/zygisk_cacerts/
   ```

### Verification via Shell

To verify that the updated certificate store is mounted and readable:
```bash
su -c "ls -la /system/etc/security/cacerts | head -n 10"
```
The listed files will display modern timestamps corresponding to the current AOSP release.

## Troubleshooting

- **Zygisk Disabled Warning**: If the module does not appear to take effect, ensure that Zygisk is toggled ON in your root manager's settings and reboot.
- **Custom User Certificates vs System Certificates**: Note that this module updates the *system* root store. If you need to trust personal MITM proxy certificates (such as Charles Proxy or Burp Suite), ensure your proxy certificates are placed in `/data/local/tmp` or configured with a dedicated user-certificate injection module.
