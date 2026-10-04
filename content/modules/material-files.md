---
id: "material-files"
title: "Material Files: Open-Source Root & Shizuku File Manager for Android"
sidebarTitle: "Material Files"
description: "Clean, privacy-focused Material Design file manager by zhanghai built upon direct Linux syscalls, supporting root su access, Shizuku SAF bypass, and network storage."
category: "system-utilities"
tier: 1
searchQueries:
  - "material files apk download"
  - "material files root file manager"
  - "material files shizuku android data"
  - "zhanghai material files github"
  - "open source android root explorer"
prerequisites:
  - "Android 5.0 (Lollipop) or newer"
  - "Root access via Magisk/KernelSU/APatch OR Shizuku service for privileged storage access"
conflicts:
  - "Restricted Scoped Storage access on Android 11+ without Shizuku or Root"
configPaths:
  - "/data/data/me.zhanghai.android.files/"
features:
  - "Native Linux syscall backend: bypasses unreliable ls shell parsing to inspect permissions, symlinks, and SELinux contexts accurately"
  - "Root & Shizuku integration: edit root partition files (/system, /data/adb) or browse restricted /sdcard/Android/data folders"
  - "Full archive management: view, compress, and extract ZIP, 7Z, TAR, GZ, and XZ formats natively"
  - "Network protocols: connect to SMB (Windows Share), SFTP, FTP, and WebDAV servers without third-party plugins"
faq:
  - question: "How do I access `/sdcard/Android/data` and `/sdcard/Android/obb` on Android 11+?"
    answer: "Android 11 and newer block document providers from accessing `Android/data`. In Material Files, tap the side navigation menu -> Add storage -> select 'Shizuku'. Grant permission when prompted; you will immediately obtain uninhibited read and write access to all app data and obb directories."
  - question: "Why is Material Files safer than closed-source root file explorers?"
    answer: "Granting root access to closed-source file managers allows proprietary binaries to execute arbitrary shell scripts with UID 0 across your entire private data partition. Material Files is 100% open-source under GPL-3.0, verified by reproducible builds, and contains zero trackers or remote analytics."
  - question: "How do I change file permissions (chmod) and ownership (chown) in Material Files?"
    answer: "Navigate to the file in root mode, tap the three dots icon -> select 'Properties' -> 'Permissions'. You can toggle Read, Write, and Execute bits for Owner, Group, and Others, or manually input numeric octal values (e.g. 0644 or 0755)."
---

## Overview

A robust, trustworthy file manager is an essential foundation for any rooted Android device. Power users frequently need to inspect module configurations, modify system properties in `/data/adb/`, adjust file permissions (`chmod`), create symbolic links, and access Scoped Storage directories (`/sdcard/Android/data/`) restricted by modern Android versions.

However, most legacy root file managers (such as Root Explorer or Solid Explorer) are proprietary, closed-source applications. Granting superuser (`su`) privileges to closed-source software exposes your device's most sensitive data to untrusted binaries. Furthermore, many open-source file managers rely on parsing text output from command-line utilities like `ls`—a notoriously brittle design that breaks across different Android toybox/toolbox versions and mangles non-UTF8 filenames.

**Material Files**, created by developer Hai Zhang (zhanghai), solves both challenges: it is a 100% open-source, beautifully designed file manager built strictly according to Material Design principles and powered by **native Linux system calls**.

---

## Technical Architecture: Linux Syscalls vs `ls` Parsing

Most Android file managers interact with root by executing shell commands:
```bash
su -c "ls -la /data/adb"
```
The application then runs string parsing and regular expressions across the returned text to extract file names, permissions, and sizes. This legacy architecture suffers from severe flaws:
1. **Filename Corruption**: Filenames containing spaces, escape characters, or localized characters cause parser crashes.
2. **Missing Metadata**: Standard `ls` parsers struggle with symbolic link targets, hard links, and SELinux contexts.
3. **High Latency**: Executing and parsing shell commands incurs substantial CPU latency.

Material Files implements the **Java NIO2 File API** and binds directly to native Linux syscalls (`stat`, `openat`, `readdir`, `readlink`, `chmod`, `chown`). This ensures instantaneous directory navigation, atomic file operations, and zero parsing errors.

---

## Root & Shizuku Capabilities

Material Files supports multiple elevation backends:

- **Local Storage Provider**: High-performance local file operations via Java NIO2 filesystem APIs.
- **Root Superuser Provider**: Direct read/write access to protected partitions (`/system`, `/data/adb`, `/data/data`) via Magisk / KernelSU / APatch `su`.
- **Shizuku Provider**: Bypasses Android Scoped Storage restrictions for non-root access to `/Android/data` and `/Android/obb`.
- **Network Storage Providers**: Native client implementations for SMB (v1/v2/v3), SFTP, FTP, and WebDAV protocols.

### 1. Root Mode (Magisk / KernelSU / APatch)
- Open Material Files -> Tap **Root directory** (`/`) from the drawer.
- Grant Superuser permission in Magisk, KernelSU, or APatch.
- You can freely browse, edit, and modify system partitions, inspect Magisk module directories (`/data/adb/modules/`), and edit configuration scripts.

### 2. Shizuku Storage Provider (Rootless Scoped Storage Access)
Android 11 through Android 15 block standard file managers from accessing `/sdcard/Android/data` and `/sdcard/Android/obb`.
- Start **Shizuku**.
- In Material Files, open the left drawer -> tap **Add storage** -> choose **Shizuku**.
- Browse into `/sdcard/Android/data` with full copy, move, and edit permissions without needing full root.

---

## Network Storage & Archive Management

### Remote Storage Client
Material Files includes built-in network clients supporting:
- **SMB / CIFS**: Connect directly to Windows network shares, TrueNAS, or local routers.
- **SFTP / SSH**: Securely browse remote Linux servers over encrypted SSH tunnels.
- **FTP / FTPS**: Legacy server connections.
- **WebDAV**: Connect to Nextcloud, ownCloud, or remote cloud storage.

### High-Performance Archive Support
The application natively browses and creates archives without extracting them to disk first:
- View and edit files inside `.zip`, `.tar`, `.tar.gz`, `.tar.bz2`, `.tar.xz`, and `.7z`.
- Extract split archives and password-protected ZIP/7Z files with AES-256 encryption.

---

## Safety & Permission Verification

When editing system scripts or module manifests in `/data/adb/modules/`, ensuring correct Linux permissions is vital to prevent bootloops:

```bash
# Verify permissions directly in Material Files Properties or terminal:
chmod 0755 /data/adb/modules/<module_id>/post-fs-data.sh
chmod 0755 /data/adb/modules/<module_id>/service.sh
```
Material Files visually confirms file mode bits (`rwxr-xr-x`) and SELinux file contexts (`u:object_r:system_file:s0`) in the Properties sheet.
