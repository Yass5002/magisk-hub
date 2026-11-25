---
id: "unlock-cn-gms"
title: "Unlock CN GMS: Remove China-ROM Google Services XML Restrictions"
sidebarTitle: "Unlock CN GMS"
description: "Systemless module by fei-ke that detects and patches cn.google.services and services_updater XML permission files across OEM partitions so Google Location History and Maps Timeline work on China-ROM phones."
category: "system-environment"
tier: 1
searchQueries:
  - "unlock cn gms magisk module"
  - "enable google location history china rom"
  - "google maps timeline cn.google.services"
  - "fei-ke unlock-cn-gms"
  - "oppo xiaomi cn_google xml fix"
prerequisites:
  - "Magisk, KernelSU, or APatch on a device running a Chinese OEM ROM with built-in GMS"
  - "Target ROM must contain at least one `cn.google.services` XML permission or sysconfig file"
conflicts:
  - "Other modules replacing the exact same `/etc/permissions/` or `/etc/sysconfig/` XML files"
  - "Global/EEA ROMs (no restriction XML present; installer intentionally aborts)"
configPaths:
  - "/data/adb/modules/com.fei_ke.unlockcngms/"
  - "/system/etc/permissions/services.cn.google.xml"
  - "/product/etc/permissions/cn.google.services.xml"
  - "/odm/etc/permissions/com.gnss.bds_preference.xml"
  - "/my_bigball/etc/permissions/oplus_google_cn_gms_features.xml"
  - "/my_product/etc/permissions/oplus_google_cn_gms_features.xml"
features:
  - "Scans 11+ known permission and sysconfig XML paths across `/system`, `/vendor`, `/product`, `/odm`, `/my_bigball`, `/my_product`, and `/my_heytap`"
  - "Dynamically strips `<feature name=\"cn.google.services\" />` and `<feature name=\"com.google.android.feature.services_updater\" />` directly from the device's own XMLs"
  - "Generates `post-fs-data.sh` `mount -o ro,bind` rules automatically for standalone OEM partitions (`/odm`, `/my_bigball`, `/my_product`, `/my_heytap`)"
  - "Restores Google Location History, Google Maps Timeline, and Web Google Play device visibility"
faq:
  - question: "Why does `customize.sh` generate `post-fs-data.sh` with `mount -o ro,bind` on OPPO, OnePlus, or Xiaomi devices?"
    answer: "Standard Magisk/KernelSU module overlays reliably mount paths under `/system`, `/vendor`, and `/product`, whereas OEMs such as OPlus (ColorOS/Realme UI) and Xiaomi place restriction XMLs on separately mounted partitions like `/my_bigball`, `/my_product`, `/my_heytap`, and `/odm`. For those partitions, `customize.sh` writes `mount -o ro,bind` commands into `post-fs-data.sh` so the patched XML overlays the read-only partition early at boot."
  - question: "Why did flashing fail with `No suitable permission file found!`?"
    answer: "If none of the 11 scanned XML files exist on your firmware, your ROM either does not ship with `cn.google.services` restrictions (typical on Global/EEA/AOSP ROMs) or places them under an unlisted vendor path. In that case, the module aborts cleanly without creating empty files."
  - question: "I flashed Unlock CN GMS, why is Google Location History still unavailable?"
    answer: "Removing `cn.google.services` unlocks the ROM-level system feature restriction, but Google Play Services may also check SIM MCC/MNC carrier codes or regional flags. As noted by the author, pairing this module with an Xposed module such as `LocationReportEnabler` (`GhostFlying/LocationReportEnabler`) may be required depending on your region and carrier."
---

## Overview

Many Chinese-market Android smartphones (Xiaomi HyperOS/MIUI, OPPO/OnePlus ColorOS, realme UI, vivo OriginOS) include Google Mobile Services (GMS) frameworks out of the box, yet restrict key Google capabilities via system feature XML declarations—most notably `cn.google.services`.

When this feature flag is advertised to Android's `PackageManager`, Google apps and Play Services enforce China-specific limitations: **Google Location History** cannot be turned on, **Google Maps Timeline** remains disabled, and the device often fails to appear in the web **Google Play** device selector. **Unlock CN GMS** (`fei-ke/unlock-cn-gms`, module ID `com.fei_ke.unlockcngms`) eliminates these declarations systemlessly without editing read-only partitions.

---

## Technical Architecture & Payload Internals

Rather than shipping hardcoded static XML files that could break OEM-specific features on mismatched ROMs, `unlock-cn-gms-v3.9.zip` inspects your live device filesystem inside `customize.sh` and patches only the exact XML files present on your firmware.

### Scanned Partition Paths

`customize.sh` iterates over the following locations:

- `/system/etc/permissions/services.cn.google.xml`
- `/system/etc/permissions/com.oppo.features.cn_google.xml`
- `/vendor/etc/permissions/services.cn.google.xml`
- `/vendor/etc/permissions/cn.google.services.xml`
- `/product/etc/permissions/services.cn.google.xml`
- `/product/etc/permissions/cn.google.services.xml`
- `/product/etc/sysconfig/cn_feature.xml`
- `/odm/etc/permissions/com.gnss.bds_preference.xml` *(e.g., Xiaomi 8e5 and multi-partition builds)*
- `/my_bigball/etc/permissions/oplus_google_cn_gms_features.xml`
- `/my_product/etc/permissions/oplus_google_cn_gms_features.xml`
- `/my_heytap/etc/permissions/my_heytap_cn_gms_features.xml` *(plus `/my_heytap/etc/permissions/my_heytap_cn_features.xml` when present)*

### Patching & Dual Mounting Strategy

For every matching file found, `customize.sh` copies the original XML and removes only the two restriction lines via `sed`:

```xml
<feature name="cn.google.services" />
<feature name="com.google.android.feature.services_updater" />
```

1. **System/Vendor/Product Partitions**: Copied into `$MODPATH/system/...` (or `$MODPATH$origin` when already under `/system`) so Magisk Magic Mount or KernelSU/APatch OverlayFS handles the replacement cleanly.
2. **Standalone OEM Partitions (`/odm`, `/my_bigball`, `/my_product`, `/my_heytap`)**: Because these mount points sit outside `/system`, `customize.sh` dynamically constructs `$MODPATH/post-fs-data.sh` containing `mount -o ro,bind ${0%/*}/<file> <origin_path>` commands so every matching partition is covered simultaneously.

---

## Installation & Configuration

1. Verify that Google Play Services / GMS is enabled on your China-ROM device.
2. Flash `unlock-cn-gms-v3.9.zip` via **Magisk**, **KernelSU**, or **APatch**.
3. Inspect the flash log to confirm each `modify <path>` line corresponding to your ROM's partitions.
4. Reboot your device.
5. Clear cache or force-stop **Google Play Services** (`com.google.android.gms`) and **Google Maps** (`com.google.android.apps.maps`) if the Timeline/Location History state was cached prior to flashing.

---

## Common Issues & Troubleshooting

- **Multi-Partition Devices (e.g., Xiaomi 8e5 / OPlus)**: Some ROMs declare `cn.google.services` in two or more partitions simultaneously (such as `/odm` and `/product`, or `/my_bigball` and `/my_product`). Do not delete `post-fs-data.sh`, as both the standard module overlay and the generated bind mounts are needed together.
- **After a ROM OTA Update**: Because `customize.sh` copies your device's XMLs at flash time, re-flash `unlock-cn-gms` after major system OTA updates so any newly introduced permissions in OEM XML files stay synchronized.
- **Location History Still Blocked**: If `pm list features | grep cn.google.services` returns nothing after rebooting yet Location History remains greyed out, combine Unlock CN GMS with **LocationReportEnabler** via LSPosed to address SIM/MCC checks.
