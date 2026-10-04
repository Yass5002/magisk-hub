---
id: "google-mobile-services-core"
title: "Google Mobile Services (GMS) Core Suite: Systemless Play Services"
sidebarTitle: "GMS Core Suite"
description: "Comprehensive systemless Google Mobile Services and Play Store framework deployment, stripping regional vendor restrictions to enable location history and global Play ecosystem features."
category: "system-environment"
tier: 1
searchQueries:
  - "google mobile services core magisk"
  - "gms china restriction unlock"
  - "google play services systemless magisk"
  - "unlock cn gms location history"
prerequisites:
  - "Android 10, 11, 12, or 13 Chinese or global firmware"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "microG or conflicting microG GmsCore stubs"
configPaths:
  - "/system/priv-app/GmsCore/GmsCore.apk"
  - "/system/priv-app/Phonesky/Phonesky.apk"
  - "/system/priv-app/GoogleServicesFramework/GoogleServicesFramework.apk"
  - "/system/etc/permissions/cn.google.services.xml"
features:
  - "Systemlessly mounts complete Google Mobile Services framework including GmsCore, Phonesky, and GSF"
  - "Strips cn.google.services regional restriction flags to unlock Google Location History and timeline tracking"
  - "Resolves Google Play Store error 404 download failures on domestic Chinese firmware builds"
  - "Restores device visibility in the web-based Google Play Store console"
  - "Maintains proper system signature level permissions without modifying /system partition blocks"
faq:
  - question: "Will this module trigger SafetyNet or Play Integrity issues?"
    answer: "No. The module installs official, unaltered Google binaries into /system/priv-app and removes regional permission locks. To pass Device and Strong Play Integrity, pair this module with Play Integrity Fix."
  - question: "Does this replace microG?"
    answer: "This module installs authentic Google Mobile Services binaries rather than microG. It is intended for devices that lack native GMS or have restricted regional GMS implementations."
---

## Overview

**Google Mobile Services Core Suite** (authored by Shiguang) is a systemless deployment of Google's proprietary mobile services platform, engineered primarily for domestic Chinese firmware builds (Xiaomi MIUI/HyperOS, Oppo ColorOS, Vivo OriginOS, etc.) that lack complete Google Play functionality.

Even when Chinese OEM ROMs offer a basic "Google Services" toggle, regional firmware often includes restrictive system permission overlays that disable Google Location History, hide device registrations from Google Play web management, and cause unexpected error 404 download failures. This suite provides the complete GMS stack while stripping away regional constraints.

---

## Technical Architecture & How It Works

GMS functionality on modern Android relies on coordinated system privileges across several components:

### 1. Core Framework Ingestion

The module binds the required privileged applications into `/system/priv-app/`:

- **GmsCore.apk**: The central runtime for Google Play Services (accounts, maps, push notifications, authentication APIs).
- **Phonesky.apk**: The official Google Play Store client interface and package installer.
- **GoogleServicesFramework.apk**: The underlying token provider and device registration daemon.

### 2. Elimination of Regional Restrictions

Chinese OEM firmware frequently injects a permission file:

```xml
<!-- Restricted permission in stock vendor image -->
<feature name="cn.google.services" />
```

This tag instructs Google Play Services to disable location tracking, contact syncing, and certain account backup pipelines in accordance with local regulations. The module eliminates this restriction systemlessly, restoring full global Google feature parity.

---

## Troubleshooting & Best Practices

- **Grant All Permissions**: After initial installation, open **Settings > Apps > Google Play Services** and ensure location, physical activity, and contacts permissions are granted.
- **Battery Optimization Exemption**: To guarantee uninterrupted push notifications, set Google Play Services and Google Services Framework battery usage to **Unrestricted**.
