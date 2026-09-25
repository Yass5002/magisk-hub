---
id: "treat-wheel-zygisk"
title: "Treat Wheel (Zygisk): High-Performance Traceless Root & ReVanced Unmount Engine"
sidebarTitle: "Treat Wheel"
description: "C99-engineered Zygisk and ReZygisk companion module delivering low-complexity root hiding, dynamic mount isolation, and automated ReVanced overlay unmounting (RVU)."
category: "root-management"
tier: 1
searchQueries:
  - "treat wheel zygisk"
  - "performanc treat-wheel-zygisk"
  - "rezygisk treat wheel"
  - "revanced umount rvu magisk"
  - "treat wheel webui"
prerequisites:
  - "Android 7.1 or higher"
  - "Magisk Official, KernelSU Official (API compliant), or APatch"
  - "ReZygisk build 508 or higher"
conflicts: []
configPaths:
  - "/data/adb/modules/treat_wheel/"
features:
  - "Pure C99 architecture: compiled without heavy C++ runtime overhead for minimal memory footprints and zero trace execution"
  - "ReVanced Umount (RVU): dynamically detects and unmounts ReVanced application mounts using modular `tw_config` descriptors"
  - "Modern WebUI dashboard: rich multilingual settings interface accessible through KernelSU, APatch, or standalone WebUI hosts"
  - "System property virtualization: provides clean, bionic-aligned system property manipulation routines"
---

## Overview

Treat Wheel, developed by ThePedroo under the PerformanC organization, is a lightweight general-purpose Zygisk module engineered in strict C99. Designed to operate hand-in-hand with ReZygisk (version 508 and above), Treat Wheel avoids bloated abstractions to provide high-speed, traceless root hiding and process isolation.

Its standout feature is ReVanced Umount (RVU)—an automated subsystem that parses module configurations across your root environment and cleans up overlay mounts within target application mount namespaces, preventing detection routines from identifying modified APK structures.

## Prerequisites & Compatibility

Treat Wheel enforces strict technical prerequisites to ensure reliability:

- **Android Version**: Android 7.1 (Nougat, API 25) or higher.
- **Root Environment**: Official Magisk, API-compliant KernelSU, or APatch.
- **Zygisk Implementation**: **ReZygisk build 508 or higher** is strictly required. Treat Wheel relies on ReZygisk-specific daemon bindings and memory protection interfaces.

There are no documented module conflicts, provided the ReZygisk version requirement is met.

## Key Capabilities & Architecture

### ReVanced Umount (RVU)

Standard root-based ReVanced integrations mount patched APK binaries directly over stock system or data app installations. While functional, these bind mounts can be enumerated by anti-tamper security routines.

Treat Wheel resolves this via RVU. For any installed ReVanced module that supplies a `tw_config` descriptor:
```properties
module_type=revanced
allow_umount=true
```
Treat Wheel automatically discovers the mount points, counts expected overlays, and detaches them from non-essential application namespaces so that protected applications cannot detect the presence of mounted APK artifacts.

### Traceless Native Core

Treat Wheel contains native C components compiled to minimize ELF symbols and memory artifacts:
- `rz_daemon`: Background coordination between Zygisk hooks and root namespaces.
- `hiding.c`: Memory namespace isolation routines.
- `system_properties`: Internal implementation for managing Android property contexts safely without triggering security alerts.

## WebUI Interface & Configuration

Treat Wheel bundles a full WebUI interface located at:
```bash
/data/adb/modules/treat_wheel/
```
The interface is accessible directly from KernelSU and APatch manager interfaces, or via standalone tools such as KSUWebUIStandalone and MMRL on Magisk. It provides toggleable controls for RVU status, namespace isolation profiles, and multilingual localization support (English, German, Spanish, Polish, Russian, Chinese, Vietnamese, and more).

## Troubleshooting & Common Pitfalls

- **Module Fails to Hook**: Verify that ReZygisk build 508+ is actively installed and running. Treat Wheel cannot function on standard legacy Zygisk implementations without the appropriate daemon interfaces.
- **ReVanced App Detects Mounts**: Ensure the ReVanced module in question includes the valid `tw_config` properties file inside its module directory (`/data/adb/modules/<module_name>/tw_config`). Without this file, Treat Wheel will not register the module for automated unmounting.
