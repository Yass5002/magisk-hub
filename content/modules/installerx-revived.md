---
id: "installerx-revived"
title: "InstallerX Revived: Modern Multi-Backend Android Package Installer"
sidebarTitle: "InstallerX Revived"
description: "Community-maintained Android package installer (com.rosan.installer.x.revived) supporting APK, APKS, APKM, XAPK, batch installs, and Root, Shizuku, Dhizuku, and Rootless backends."
category: "system-utilities"
tier: 1
searchQueries:
  - "installerx revived apk download"
  - "installerx revived shizuku root dhizuku"
  - "install apks apkm xapk android"
  - "replace stock android package installer"
  - "com.rosan.installer.x.revived guide"
prerequisites:
  - "Android device running in Rootless mode, or with Shizuku, Dhizuku, or Root (Magisk / KernelSU / APatch) configured"
conflicts:
  - "Original unmaintained iamr0s/InstallerX build if sharing package/installer defaults without switching default handler"
configPaths:
  - "/data/data/com.rosan.installer.x.revived/"
features:
  - "Multi-format package installation: natively parses and installs APK, APKS, APKM, XAPK, APK files inside ZIP archives, and batch APK sets"
  - "Flexible privilege backends: supports **Shizuku**, **Dhizuku** (DeviceOwner/ProfileOwner APIs), **Root** (`app_process`), and **Rootless** system package manager mode"
  - "Multiple install workflows: interactive Material 3 dialog, background notification install, automatic install, silent install, and Android 16+ Live Activity progress"
  - "Smart dialog batch selection: preserves split APK and dex metadata selections per package row when toggling choices during analysis"
  - "Integrated management utilities: `UninstallerActivity`, `UnarchiveActivity`, Quick Settings tile (`SettingsTileService`), and optional `BiometricsAuthenticationActivity`"
faq:
  - question: "Which privilege backend should I choose: Shizuku, Dhizuku, or Root?"
    answer: "Shizuku is usually the fastest and cleanest option because it reuses an already-running shell or root binder service (`rikka.shizuku.ShizukuProvider`). Direct Root works everywhere on rooted devices (`Magisk`, `KernelSU`, `APatch`) but can have slight startup latency due to cold `app_process` spawning. Dhizuku uses DevicePolicy/DeviceOwner privileges where enabled, while Rootless falls back to standard Android installer prompts."
  - question: "What package formats does InstallerX Revived support?"
    answer: "Beyond standard single `.apk` files, InstallerX Revived parses split-APK bundles and archives including `.apks`, `.apkm`, `.xapk`, and `.apk` files nested inside `.zip` archives, plus multi-package batch queues."
  - question: "How is InstallerX Revived related to the original InstallerX?"
    answer: "InstallerX Revived (`wxxsfxyzm/InstallerX-Revived`, package `com.rosan.installer.x.revived`) is the active community-maintained continuation of `iamr0s/InstallerX`, bringing Material 3 UI refinements, Android 16+ Live Activity progress, and ongoing compatibility updates."
---

## Overview

**InstallerX Revived** (`wxxsfxyzm/InstallerX-Revived`, package `com.rosan.installer.x.revived`) is a modern, open-source Android package installer and the active community continuation of the original `iamr0s/InstallerX` project.

Stock OEM package installers often block split-APK bundles (`.apks`, `.apkm`, `.xapk`), inject bloatware/app-store redirects, or omit basic install options like downgrade flags and installer-package spoofing. InstallerX Revived replaces limited stock installers with a clean Material 3 interface, comprehensive archive parsing, and selectable privilege backends spanning **Rootless**, **Shizuku**, **Dhizuku**, and **Root** (**Magisk**, **KernelSU**, **APatch**).

---

## Technical Architecture & Supported Backends

Inspecting `InstallerX-Revived-online-26.11.caccb78.apk` (`26.11.caccb78`) highlights its modular installer architecture:

### Authorizers / Installer Backends
1. **Shizuku (`rikka.shizuku.ShizukuProvider` / `moe.shizuku.manager.permission.API_V23`)**:
   - Obtains ADB-shell or root-level `PackageInstaller` session privileges via Shizuku's persistent binder daemon, delivering fast installs without cold-spawning a new root process per install.
2. **Dhizuku (`com.rosan.dhizuku.permission.API`)**:
   - Leverages Dhizuku's shared DeviceOwner / DevicePolicy APIs for privileged silent installations on non-rooted devices configured with Dhizuku.
3. **Root (`Magisk` / `KernelSU` / `APatch`)**:
   - Executes all privileged `PackageInstaller` operations (`INSTALL_PACKAGES`, `DELETE_PACKAGES`, `UPDATE_PACKAGES_WITHOUT_USER_ACTION`, `INTERACT_ACROSS_USERS_FULL`) via `app_process` with root access.
4. **Rootless / System Mode**:
   - Works out of the box without root or Shizuku using Android's standard `REQUEST_INSTALL_PACKAGES` session confirmation flow.

### Core App Components & Capabilities
- **Activities & Services**: Includes `InstallerService` (special-use foreground service), `InstallerActivity`, `UninstallerActivity`, `UnarchiveActivity` (handling `UNARCHIVE_DIALOG`), `SettingsTileService` (Quick Settings tile), and optional `BiometricsAuthenticationActivity` for installation gating.
- **Format & Batch Handling**: Handles `.apk`, `.apks`, `.apkm`, `.xapk`, `.zip`-wrapped APKs, and batch queues. During dialog batch analysis, toggling a single-version row off and back on restores its prior split-ABI/density and dex metadata selections automatically.
- **Install Flows**: Supports interactive dialog installation, background notification installation, automatic confirmation, silent installation (when authorized), and Android 16+ Live Activity progress notifications (`POST_PROMOTED_NOTIFICATIONS`).

---

## Installation & Setup

1. Download `InstallerX-Revived-online-26.11.caccb78.apk` from `wxxsfxyzm/InstallerX-Revived` releases and install it:
   ```bash
   adb install InstallerX-Revived-online-26.11.caccb78.apk
   ```
2. Open **InstallerX Revived** -> **Settings** (`SettingsActivity`) and select your preferred **Authorizer**:
   - **Shizuku**: Grant permission when Shizuku prompts.
   - **Dhizuku**: Authorize via Dhizuku Manager.
   - **Root**: Grant superuser permission in Magisk, KernelSU, or APatch.
   - **None / System**: Use standard Rootless mode.
3. Optionally set InstallerX Revived as your default handler for `.apk` and archive MIME types (`application/vnd.android.package-archive`), or share files directly to InstallerX Revived via Android's **Share** (`SEND` / `SEND_MULTIPLE`) sheet.

---

## Troubleshooting & Notes

- **Cold startup delay in Root mode**: Direct Root mode launches `app_process` per privileged session, which can feel slower than Shizuku. Switching the authorizer to **Shizuku** (backed by root or ADB) eliminates cold `app_process` overhead.
- **OEM restrictions on replacing the default installer**: Some Chinese OEM ROMs (MIUI/HyperOS, ColorOS) restrict overriding the built-in system installer for `.apk` taps from file managers. Use Android's **Open with / Share** menu or configure an installer-replacement helper when needed.
