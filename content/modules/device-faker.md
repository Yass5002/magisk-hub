---
id: "device-faker"
title: "Device Faker: Granular Per-App Device Model & Identity Masking"
sidebarTitle: "Device Faker"
description: "High-performance Rust-based Zygisk module for granular per-application device model spoofing and identity cloaking with modern WebUI support."
category: "security-certificates"
tier: 1
searchQueries:
  - "device faker magisk module"
  - "seyud device faker guide"
  - "zygisk device model spoofer"
  - "per app device spoofing android"
  - "device faker config toml"
prerequisites:
  - "Magisk (v24+) with Zygisk enabled, KernelSU (v0.7+) with ZygiskNext, or APatch with ZygiskNext"
conflicts:
  - "Other Zygisk-based device spoofing modules modifying the same property namespaces"
configPaths:
  - "/data/adb/modules/device_faker/"
  - "/data/adb/device_faker/config/config.toml"
features:
  - "Written in Rust using native Zygisk APIs for minimal overhead and zero resident footprint"
  - "Granular per-application targeting: spoof device properties for specific apps without affecting system stability"
  - "Copy-On-Write (COW) property engine: leverages mmap COW memory mapping for process-isolated system properties"
  - "Integrated modern WebUI for template management, application toggling, and real-time configuration"
  - "Immediate configuration reload: changes take effect upon restarting the target app without rebooting"
faq:
  - question: "Does Device Faker permanently modify my system properties globally?"
    answer: "No. Device Faker utilizes an in-memory Copy-On-Write (COW) property spoofing engine. System properties (such as ro.product.model or ro.product.brand) are modified strictly inside the target application's isolated memory space, leaving the global Android system and untouched applications completely stock."
  - question: "Do I need to reboot every time I change a device model template?"
    answer: "No reboot is required. Once you update your configuration in the WebUI or edit config.toml, simply force stop and relaunch the target application to apply the new device profile immediately."
---

## Overview

Developed by **Seyud**, **Device Faker** is an open-source, high-performance **Zygisk module written in Rust** designed for granular per-application device model and hardware identity spoofing.

Many specialized applications (such as high-refresh-rate mobile games, OEM camera suites, streaming platforms, and diagnostic tools) gate graphics presets, HDR playback, or exclusive capabilities behind specific device whitelists (e.g. demanding a Galaxy S24 Ultra, iPad Pro, or ROG Phone model string). Rather than modifying system-wide `build.prop` values—which can cause global stability issues or break vendor services—Device Faker allows you to assign custom hardware profiles to individual target packages.

---

## Technical Architecture & How It Works

- **Zygisk Injection**: Injects into application processes at fork time via the native Zygisk API (`zygisk-api-rs`) before application initialization occurs.
- **Copy-On-Write (COW) Property Spoofing**: Rather than relying on fragile userspace hooks, Device Faker creates a private `mmap` Copy-On-Write clone of the system property area for the target process. When the app reads system properties (`__system_property_get` / `__system_property_read`), it receives the spoofed values while the rest of the OS remains untouched.
- **Unified Execution Flow**: Automatically coordinates JNI field cloaking (`android.os.Build` fields), COW system properties, and companion daemon services without requiring manual mode selection.
- **TOML Configuration Engine**: All settings and device model definitions are stored in clean TOML format at `/data/adb/device_faker/config/config.toml`.

---

## WebUI Management

Device Faker includes an integrated modern WebUI supporting multilingual interfaces (English, Simplified Chinese, Turkish):

- **Template Management**: Create, edit, and maintain hardware profile templates (e.g., Pixel 9 Pro XL, Xiaomi 14 Ultra, ASUS ROG Phone 8) and assign them across multiple packages with a single tap.
- **Application Management**: Displays all installed packages (including multi-user and work profile apps) and lets you toggle spoofing profiles individually.
- **Config Editor**: Direct visual and raw editor for configuring advanced parameters.

---

## Installation & Setup

1. Verify that your root environment has active Zygisk support:
   - **Magisk**: Enable **Zygisk** in Magisk app settings.
   - **KernelSU / APatch**: Install and activate the **ZygiskNext** module.
2. Download the latest `device_faker.zip` release from the official repository.
3. Flash the zip in your root manager (Magisk, KernelSU, or APatch) and reboot your device.
4. Access the **WebUI** via the KernelSU/APatch WebUI manager, or manage the configuration directly via `/data/adb/device_faker/config/config.toml`.
5. Assign your desired device template to your target applications and restart the target apps to apply changes.
