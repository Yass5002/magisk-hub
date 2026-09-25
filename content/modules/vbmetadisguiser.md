---
id: "vbmetadisguiser"
title: "VBMeta Disguiser: Android Verified Boot (AVB), Boot Hash & Security Property Masker"
sidebarTitle: "VBMeta Disguiser"
description: "Disguises Android Verified Boot properties, VBMeta partition parameters, and bootloader status flags to evade hardware attestation detectors and root scanners."
category: "system-environment"
tier: 1
searchQueries:
  - "vbmeta disguiser magisk module"
  - "astoritin vbmetadisguiser"
  - "spoof vbmeta boot hash android"
  - "avb 2.0 bootloader property mask"
  - "native detector vbmeta bypass"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
  - "Device Boot Hash copied from Key Attestation or Native Detector"
  - "Root file explorer or text editor to configure /data/adb/vbmeta_disguiser/vbmeta.conf"
conflicts: []
configPaths:
  - "/data/adb/vbmeta_disguiser/vbmeta.conf"
  - "/data/adb/vbmeta_disguiser/slain_prop.prop"
  - "/data/adb/modules/vbmetadisguiser/"
features:
  - "Verified boot parameter masking: spoof AVB version (2.0) and VBMeta partition sizing (4096) to match factory stock images"
  - "Cryptographic boot hash substitution: allows users to bind verified release boot hashes into ro.boot.vbmeta.* properties"
  - "Property slayer (props_slay): permanently removes ordered system properties that betray unlocked bootloader states"
  - "Security patch alignment: coordinates system patch dates with Tricky Store TEE configurations"
  - "Bootloader & build type spoofing: masks bootloader state as locked and spoofs user/release-keys build types"
---

## Overview

Modern anti-tamper detection applications (such as Native Detector, Momo, and specialized banking clients) do not rely solely on SafetyNet or Play Integrity verdicts. To catch unlocked bootloaders, they inspect the system property table for Android Verified Boot (AVB) flags—specifically looking at `ro.boot.vbmeta.device_state`, `ro.boot.vbmeta.avb_version`, partition sizes, and cryptographic boot hashes. On an unlocked handset, these flags explicitly report unverified states.

Developed by Astoritin, **VBMeta Disguiser** is a comprehensive system property masking engine. Operating across Magisk, KernelSU, and APatch, it allows users to align their device's exposed AVB properties with genuine, locked production devices without modifying physical flash partitions.

> [!NOTE]
> VBMeta Disguiser targets the **property layer** (`resetprop` / userspace reflection). It is designed to work in synergy with modules like **Tricky Store**, which handles TEE-level cryptographic attestation responses.

## Key Configuration Directives (`vbmeta.conf`)

Configuration is managed via `/data/adb/vbmeta_disguiser/vbmeta.conf`. Edit this file with superuser permissions to activate specific features:

### 1. Boot Hash & Partition Verification
```ini
# Android Verified Boot version (defaults to 2.0)
avb_version=2.0

# VBMeta partition byte size (defaults to 4096)
vbmeta_size=4096

# Paste your genuine Boot Hash copied from Native Detector / Key Attestation
boot_hash=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

### 2. Encryption State & Bootloader Spoofing
```ini
# Force Data partition state: encrypted, unencrypted, or unsupported
crypto_state=encrypted

# Spoof bootloader properties as locked (ro.boot.flash.locked=1, etc.)
bootloader_props_spoof=true

# Spoof ROM build type to production user/release-keys
build_type_spoof=true
```

### 3. Property Stripping (`props_slay`)
Detectors often identify root environments by scanning for stale debug properties left behind by custom ROMs or earlier root modules.
```ini
# Enable property removal
props_slay=true

# Space-separated list of properties to purge on boot
props_list="persist.sys.phh.no_magisk ro.debuggable persist.service.adb.enable"
```
*Note*: Slain properties are backed up to `/data/adb/vbmeta_disguiser/slain_prop.prop`. If `props_slay` is set back to `false`, original values are restored.

### 4. Security Patch Date Synchronization
If running alongside **Tricky Store**, VBMeta Disguiser automatically defers to Tricky Store's configuration (`/data/adb/tricky_store/security_patch.txt`). If configured independently:
```ini
security_patch_disguise=true
all=20260705
```

## Step-by-Step Installation

1. Flash the **VBMeta Disguiser** `.zip` via Magisk, KernelSU, or APatch.
2. Open **Key Attestation** or **Native Detector** on your device and copy your target device's valid Boot Hash.
3. Open `/data/adb/vbmeta_disguiser/vbmeta.conf` using a root text editor.
4. Paste your Boot Hash into `boot_hash=` and enable required spoofing flags.
5. Reboot your device to allow the property masking routines to execute during early boot.

## Troubleshooting

- **Native Detector Shows Property Modified (10)**: This is expected on the initial boot after configuring `props_slay`. Due to how `resetprop` binds to the Android property service, a second reboot is often required to normalize property tree nodes.
- **Build Type Bootloop**: Enabling `build_type_spoof=true` on certain vendor-modified ROMs with strict internal integrity checks can cause framework crashes. If you encounter boot issues, boot into Safe Mode or remove the module to revert changes.
