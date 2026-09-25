---
id: "zeromount"
title: "ZeroMount: Mountless VFS Module Loading Engine for Rooted Android"
sidebarTitle: "ZeroMount"
description: "Advanced mount orchestration engine by Enginex0 that intercepts kernel VFS getname() calls to load root modules with zero mount table pollution and integrated SUSFS stealth."
category: "root-management"
tier: 1
searchQueries:
  - "zeromount android root"
  - "enginex0 zeromount"
  - "mountless module loader kernelsu"
  - "vfs getname module redirection"
  - "zeromount susfs integration"
prerequisites:
  - "Android device rooted with KernelSU, APatch, or Magisk"
  - "Linux kernel with VFS redirection capability or SUSFS support (for Tier 1 VFS mountless mode)"
conflicts: []
configPaths:
  - "/data/adb/modules/zeromount/"
features:
  - "Kernel-level VFS redirection: intercepts filesystem path resolution at `getname()`, redirecting file queries to module storage without creating mount table entries"
  - "Three-tier fallback orchestration: automatically chooses between VFS (mountless) → OverlayFS (overlay) → MagicMount (binds) based on kernel features"
  - "Zero mount table traces: leaves `/proc/mounts`, `/proc/self/mountinfo`, and `/proc/self/mountstats` completely pristine and matching stock ROM state"
  - "Comprehensive SUSFS integration: coordinates with SUSFS to provide kstat attribute spoofing, `/proc/maps` sanitization, and path concealment"
  - "Interactive WebUI dashboard: monitor mount engine health, configure per-module loading strategies, and review boot logs in real time"
---

## Overview

ZeroMount, created by Enginex0, represents a paradigm shift in how systemless modules are loaded on rooted Android. Traditional root frameworks—such as Magisk and stock KernelSU—rely heavily on Linux bind mounts or OverlayFS layers. While functional, these mounts leave obvious traces in `/proc/mounts`, `/proc/self/mountinfo`, and `/proc/self/mountstats`. Modern anti-tamper and banking security systems easily detect root by inspecting these mount tables for foreign filesystem overlays.

ZeroMount eliminates mount pollution at the root. Operating through a custom kernel driver paired with a high-performance Rust userspace daemon, ZeroMount intercepts the Linux Virtual File System (VFS) layer at `getname()`. When an application or system process queries a file path, the kernel redirects the read to the module's directory *before* the filesystem even processes the request. Your modules load perfectly, while system mount tables remain 100% stock.

## Prerequisites & Compatibility

- **Root Environment**: KernelSU, APatch, or Magisk. KernelSU environments paired with GKI kernels or SUSFS-patched trees unlock the full power of VFS mountless redirection.
- **Architecture**: ARM64 (aarch64).

There are no documented module conflicts. ZeroMount coordinates with existing root modules and auto-detects companion security layers.

## The Three-Tier Mount Cascade

ZeroMount automatically probes kernel capabilities at boot and selects the optimal loading strategy:

1. **Tier 1: VFS Redirection (Primary)**:
   - Module files are redirected at the kernel VFS layer.
   - Zero entries appear in mount tables.
   - Directory entry injection ensures `readdir()` and `ls` show overlaid files as native system files.
   - SELinux security contexts are dynamically aligned without causing AVC denials.
2. **Tier 2: OverlayFS (Automatic Fallback)**:
   - Used when the kernel lacks custom VFS redirection hooks.
   - Leverages overlay filesystems while applying SUSFS stealth layers to hide overlay mount points.
3. **Tier 3: MagicMount (Last Resort)**:
   - Traditional individual bind-mount cascade applied when OverlayFS is unavailable.

Users can also define per-module overrides in the WebUI to force specific loading strategies for idiosyncratic modules.

## Installation & Configuration

1. Download the latest `ZeroMount-*.zip` release from the repository.
2. Flash the module through KernelSU, APatch, or Magisk.
3. Reboot your device.
4. Launch the **ZeroMount WebUI** from your manager:
   - Review active mount strategies across all installed modules.
   - Configure SUSFS stealth features (kstat spoofing, `/proc/maps` hiding).
   - Inspect the boot pipeline health checks to confirm zero mount leakage.
5. Module binaries and configuration state reside in:
   ```bash
   /data/adb/modules/zeromount/
   ```

## Troubleshooting & Verification

- **Verify Clean Mount Tables**: Run the following command from an unprivileged shell terminal to verify that no module mount points are exposed:
  ```bash
  cat /proc/self/mountinfo | grep -E "adb|modules"
  # Should return zero results under VFS redirection mode
  ```
- **Fallback Triggered**: If the WebUI reports that ZeroMount fell back to OverlayFS or MagicMount, your kernel lacks the required VFS hooks. Flash a compatible custom kernel or enable SUSFS patches to utilize Tier 1 mountless redirection.
