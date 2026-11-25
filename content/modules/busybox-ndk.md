---
id: "busybox-ndk"
title: "Busybox for Android NDK: Multi-Architecture Static Binary Installer"
sidebarTitle: "Busybox NDK"
description: "Static NDK-compiled BusyBox 1.36.1 installer by osm0sis supporting ARM, ARM64, x86, x86_64, and MIPS with SELinux builds and automated symlink cleanup."
category: "system-utilities"
tier: 1
searchQueries:
  - "busybox ndk magisk module"
  - "osm0sis busybox for android ndk 1.36.1"
  - "busybox kernelsu apatch zip"
  - "busybox ndk selinux nolinks zip name"
  - "android static busybox arm64"
prerequisites:
  - "Magisk, KernelSU, APatch, SuperSU, or custom recovery (TWRP / OrangeFox)"
  - "Supported CPU architecture: ARM, ARM64, x86, x86_64, MIPS, or MIPS64"
conflicts:
  - "Legacy BusyBox installers (e.g., Stericson BusyBox) that place conflicting applets in `/system/bin` or `/system/xbin`"
configPaths:
  - "/data/adb/modules/busybox-ndk/system/xbin/busybox"
  - "/data/adb/modules/busybox-ndk/system/bin/busybox"
features:
  - "Includes 10 static NDK-compiled BusyBox 1.36.1 binaries (`arm`, `arm64`, `x86`, `x86_64`, `mips`, `mips64`, plus `-selinux` variants)"
  - "Diffusion Installer Core (`customize.sh` + `diffusion_config.sh`) supporting both booted root managers and recovery flashing/uninstallation"
  - "ZIP filename option flags (`nolinks`, `noselinux`) allow toggling applet symlink generation and SELinux builds without editing scripts"
  - "Cleans stale `busybox` symlinks from prior installations and avoids clobbering existing `/system/bin` applets when installing to `bin`"
faq:
  - question: "How do I install BusyBox without creating applet symlinks or without SELinux support?"
    answer: "Busybox for Android NDK uses `USE_ZIP_OPTS=true` in `diffusion_config.sh`. Simply rename the ZIP file before flashing: include `nolinks` (case-insensitive) in the filename to skip symlink creation, or `noselinux` to install the non-SELinux binary instead of the default `-selinux` variant."
  - question: "Where is the `busybox` binary installed under Magisk, KernelSU, or APatch?"
    answer: "The installer checks whether `/system/xbin` exists (or `/magisk`/Magisk module paths). When `/system/xbin` is present, it installs systemlessly to `/data/adb/modules/busybox-ndk/system/xbin/busybox`; on modern SAR/Android devices without `/system/xbin`, it falls back to `$MODPATH/system/bin/busybox` and skips symlinking applets that already exist in `/system/bin`."
---

## Overview

**Busybox for Android NDK**, maintained by **osm0sis** (`xda-developers`), provides a clean, statically linked **BusyBox 1.36.1** binary compiled against the Android NDK (originating from the `AIK-mobile` toolchain). Many root scripts, shell utilities, and recovery-compatible modules depend on standard GNU/POSIX tools (`awk`, `sed`, `grep`, `tar`, `unzip`, `nc`, `vi`) with consistent flags rather than Android's stripped-down `toybox` or `mksh` builtins.

This package ships pre-built static binaries for every major Android ABI and automatically handles architecture detection, SELinux capability selection, and safe symlink hygiene.

---

## Technical Architecture & Installer Behavior

Inspecting `UPDATE-Busybox.Installer.v1.36.1-ALL-signed.zip` confirms the **Diffusion Installer Core** architecture (`customize.sh` + `diffusion_config.sh`):

### Bundled Static Binaries
The archive bundles 10 static ELF binaries built from `osm0sis/android-busybox-ndk`:
- **ARM / ARM64**: `busybox-arm`, `busybox-arm-selinux`, `busybox-arm64`, `busybox-arm64-selinux`
- **x86 / x86_64**: `busybox-x86`, `busybox-x86-selinux`, `busybox-x86_64`, `busybox-x86_64-selinux`
- **MIPS / MIPS64**: `busybox-mips`, `busybox-mips64` (non-SELinux; `custom_install` unsets `SELINUX` on `mips*`)

### Installation & Symlink Logic (`diffusion_config.sh`)
1. **ZIP Filename Options (`custom_zip_opts`)**:
   - Default behavior installs the `-selinux` binary (on ARM/x86 families) and creates applet symlinks.
   - Adding `nolinks` (`*nolinks*`, `*NoLinks*`, `*NOLINKS*`) to the ZIP filename sets `NOLINKS=1`, installing only the `busybox` binary.
   - Adding `noselinux` (`*noselinux*`, `*NoSELinux*`, `*NOSELINUX*`) omits the `-selinux` suffix.
2. **Target Directory Resolution**:
   - Under systemless root managers (Magisk, KernelSU, APatch), files are staged inside the module directory (`system/xbin` if `/system/xbin` exists, otherwise `system/bin`).
   - Permissions are set to `0755` with SELinux context `u:object_r:system_file:s0`.
3. **Stale Symlink Cleanup (`custom_cleanup`)**:
   - Scans `$XBIN` (and legacy `/bin/busybox` paths if migrating) for existing symbolic links resolving to `*busybox` and removes them before regenerating symlinks.
4. **Safe Symlink Generation (`custom_postinstall`)**:
   - Queries `$XBIN/busybox --list` and runs `busybox ln -sf busybox $applet`.
   - When installing into `*/bin` instead of `*/xbin`, it compares each applet against `ls /system/bin` so stock Android `/system/bin` commands (like `sh` or `toolbox`/`toybox` binaries) are not accidentally shadowed unless they were already replaced by the module.

---

## Installation & Usage

1. Download `UPDATE-Busybox.Installer.v1.36.1-ALL-signed.zip` (optionally renaming it to include `nolinks` or `noselinux` if desired).
2. Flash the ZIP in **Magisk**, **KernelSU**, or **APatch** (**Modules → Install from storage**), or via custom recovery.
3. Reboot your device.

### Verification Commands

Confirm that the static BusyBox 1.36.1 binary is mounted and check its active path and applet count:

```bash
# Locate mounted busybox binary
which busybox

# Verify version and NDK build info
busybox | head -n 2

# Count available applets
busybox --list | wc -l

# Inspect SELinux context on the installed binary
ls -Z "$(which busybox)"
```

---

## Uninstallation

Removing **Busybox for Android NDK** from your root manager uninstalls the systemless overlay cleanly upon reboot. If flashed directly to `/system` in recovery mode without a systemless manager, renaming the ZIP or re-flashing in recovery triggers `ACTION=uninstall` inside `customize.sh`, invoking `custom_uninstall` and `custom_cleanup` to remove `busybox` and all associated symlinks.
