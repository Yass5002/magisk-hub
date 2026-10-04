---
id: "miui-perfect-icons"
title: "MIUI Perfect Icons HD Suite: 2K Uniform Vector Icons"
sidebarTitle: "MIUI Perfect Icons"
description: "Comprehensive icon harmonization suite for Xiaomi MIUI Launcher replacing irregular, low-resolution third-party application icons with crisp 2K vector squircles and stripping ad badges."
category: "customization-ui"
tier: 1
searchQueries:
  - "miui perfect icons magisk"
  - "xiaomi launcher 2k icon pack module"
  - "miui uniform squircle icons root"
  - "remove ad badge miui icons magisk"
prerequisites:
  - "Xiaomi, Redmi, or POCO device running MIUI 12+ or HyperOS"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Other modules that overwrite /system/media/theme/default/icons"
configPaths:
  - "/system/media/theme/default/icons"
features:
  - "High-definition 2K texture rendering prevents icon blurriness on WQHD+ and 120Hz displays"
  - "Enforces consistent squircle geometry across both system apps and third-party packages"
  - "Strips intrusive promotional badges and ad ribbons from commercial app icons"
  - "Systemlessly overlays the default launcher icon cache without modifying /system partitions"
faq:
  - question: "How do I refresh the icons if they do not change immediately after reboot?"
    answer: "Go to Settings -> Apps -> Manage Apps -> System Launcher, force stop the launcher, and clear launcher cache. Alternatively, toggle your system theme once in Theme Manager."
  - question: "Does this icon pack support newly installed Play Store apps?"
    answer: "Yes, the suite includes automatic background masking rules that dynamically frame unsupported third-party application icons into matching squircle containers."
---

## Overview

**MIUI Perfect Icons HD Suite** (curated and authored by Move.p) is a systemless visual enhancement module designed to solve the visual inconsistency common on Xiaomi MIUI and HyperOS desktops.

While Xiaomi provides clean stock icons for first-party system apps, third-party apps installed via Google Play or domestic app stores often render with mismatched borders, lower-resolution bitmaps, or intrusive ad banners. Perfect Icons overlays a curated library of high-resolution 2K vector assets and dynamic masking filters, delivering a polished, uniform desktop aesthetic.

---

## Technical Architecture & How It Works

Xiaomi's System Launcher resolves application icon assets through the system theme engine:

### 1. Theme Asset Binding

The module systemlessly bind-mounts a unified icon archive over:

```bash
/system/media/theme/default/icons
```

When the launcher initializes or when `ThemeManager` compiles desktop caches, it reads vector drawables and pre-rendered 2K bitmaps directly from this path.

### 2. Geometric Masking & Ad Stripping

- **Adaptive Squircle Masking**: For applications lacking direct vector replacements, the internal `transform_config.xml` applies a calibrated squircle mask and drop shadow, harmonizing the icon with Xiaomi's official icon geometry.
- **Badge Removal**: Commercial apps often include hardcoded promotional ribbons (such as holiday sales or anniversary badges). The module replaces these with clean, unaltered brand logos.

---

## Troubleshooting & Verification

- **Clearing Icon Caches**: If an icon appears cached in low resolution, restart the launcher:
  ```bash
  killall com.miui.home
  ```
- **Reverting to Factory Icons**: Disable the module in your root manager and reboot the device to instantly restore standard MIUI stock icons.
