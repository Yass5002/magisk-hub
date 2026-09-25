---
id: "antisafetycore"
title: "AntiSafetyCore: Block Silent Installation of Google SafetyCore & Key Verifier"
sidebarTitle: "AntiSafetyCore"
description: "Prevents Google Play Services from silently installing Android System SafetyCore and Key Verifier telemetry packages by deploying signature-mismatched placeholder APKs."
category: "security-certificates"
tier: 1
searchQueries:
  - "antisafetycore magisk module"
  - "astoritin antisafetycore"
  - "block google safetycore installation root"
  - "android system key verifier disable magisk"
  - "stop play services silent apk installs"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
  - "Android ROM with standard Android package signature verification intact"
  - "Metamodule required on KernelSU (kernel ≥ 22098) or APatch (kernel ≥ 11170) if using the systemize toggle"
conflicts:
  - "Core Patch, Lucky Patcher, or any module that disables Android APK signature verification (allows Play Services to overwrite placeholders)"
configPaths:
  - "/data/adb/anti_safetycore/"
  - "/data/adb/anti_safetycore/keep_running"
  - "/data/adb/anti_safetycore/systemize"
  - "/data/adb/modules/anti_safetycore/"
features:
  - "Signature conflict barrier: installs dummy placeholder APKs matching target package names with arbitrary signatures to reject silent updates"
  - "Targeted component suppression: blocks Android System SafetyCore and Android System Key Verifier"
  - "Persistent background daemon (keep_running): continuously monitors package states and re-injects placeholders if Play Services attempts a purge"
  - "Systemless systemization (systemize): mounts placeholders into system partitions to prevent user-space deletion attempts"
---

## Overview

In recent Android releases, Google Play Services has begun silently downloading and installing proprietary background packages onto user devices without notification or consent. The most prominent among these are **Android System SafetyCore** (`com.google.android.safetycore`) and **Android System Key Verifier** (`com.google.android.contactkeys`). While named similarly to essential OS components, these background binaries facilitate continuous telemetry, on-device content scanning, and identity verification.

Developed by Astoritin, **AntiSafetyCore** halts this silent installation mechanism. It leverages a fundamental security invariant of the Android operating system: the package manager strictly refuses to install or overwrite an application if the new package shares the same package name as an installed app but carries a conflicting cryptographic signature.

## How AntiSafetyCore Works

1. **Placeholder Injection**: During initialization, AntiSafetyCore installs benign placeholder APKs corresponding to the targeted Google package names. These dummy packages are signed with a custom, mismatched private key.
2. **Installation Lockout**: When Google Play Services attempts its automated background installation of the official SafetyCore or Key Verifier APKs, Android's `PackageManagerService` detects the signature mismatch and immediately aborts the installation with `INSTALL_FAILED_UPDATE_INCOMPATIBLE`.
3. **Telemetry Nullification**: Because the dummy package occupies the namespace, no proprietary Google background services or background workers for these components can run.

## Critical Incompatibility: Signature Verification Disablers

> [!WARNING]
> **AntiSafetyCore is fundamentally incompatible with Core Patch, Lucky Patcher, or any XPosed module that disables Android signature verification.**

If your device has disabled signature verification, the Android Package Manager will happily permit Google Play Services to overwrite the placeholder APK with the official Google package, defeating the entire protection mechanism of this module.

## Configuration Flags

Since version 1.3.0, AntiSafetyCore supports modular operational modes. You can configure behavior by placing empty, extensionless trigger files inside the configuration directory `/data/adb/anti_safetycore/`:

### 1. `keep_running` (Daemon Sentinel Mode)
By default, the module runs once at boot. If Google Play Services manages to force-uninstall the user-space placeholder during active runtime, the protection could lapse until the next reboot.
- Creating the file `/data/adb/anti_safetycore/keep_running` instructs the module to spawn a lightweight background monitor.
- The daemon checks package statuses periodically and immediately re-installs the placeholder if a removal or mismatch is detected.

### 2. `systemize` (System-Level Mounting)
- Creating `/data/adb/anti_safetycore/systemize` causes the module to mount the placeholder APKs directly into system partition paths rather than installing them as user apps.
- When mounted systemlessly as system apps, Google Play Services lacks the permission to uninstall or replace them.
- **KernelSU & APatch Requirement**: If running KernelSU (kernel version ≥ 22098) or APatch (kernel version ≥ 11170), you must install the official **Metamodule** to enable systemized mounting. Without the Metamodule, the placeholders fall back to standard user-app installation.

## Installation & Verification

1. Ensure no signature-verification bypass modules are active.
2. Flash the AntiSafetyCore `.zip` in Magisk, KernelSU, or APatch.
3. Reboot your device.
4. Verify protection in an ADB or root terminal:
   ```bash
   su -c pm list packages -f | grep safetycore
   ```
   The output should show the placeholder APK path.
5. *(Optional)* Enable daemon monitoring:
   ```bash
   su -c touch /data/adb/anti_safetycore/keep_running
   ```
