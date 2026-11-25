---
id: "alwaysstrong"
title: "AlwaysStrong: All-in-One Strong Play Integrity Module"
sidebarTitle: "AlwaysStrong"
description: "Bundled solution by Evokerr integrating TEESimulator-RS and PlayIntegrityFork into a single module with automated keybox updates and WebUI management."
category: "root-management"
tier: 1
searchQueries:
  - "alwaysstrong magisk module"
  - "evokerr alwaysstrong gitlab"
  - "pass strong integrity all in one"
  - "alwaysstrong webui"
  - "teesimulator-rs playintegrityfork bundle"
prerequisites:
  - "Android 10+ (API 29+) with Magisk, KernelSU (verCode >= 10670), or APatch"
  - "Active standalone Zygisk engine (ZygiskNext, ReZygisk, or NeoZygisk recommended)"
conflicts:
  - "Standalone installations of TrickyStore, TEESimulator-RS, or PlayIntegrityFix/Fork (AlwaysStrong bundles both engines and uses the tricky_store module ID)"
  - "Legacy Universal SafetyNet Fix (automatically marked for removal during setup)"
configPaths:
  - "/data/adb/tricky_store/alwaysstrong/config"
  - "/data/adb/tricky_store/alwaysstrong/state"
  - "/data/adb/tricky_store/alwaysstrong/apps.map"
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/modules/tricky_store/"
features:
  - "Single-flash bundle: combines Rust-based TEESimulator-RS hardware attestation simulation with PlayIntegrityFork fingerprint spoofing"
  - "Unified configuration directory: keeps module settings, internal loop state, and per-app mappings cleanly under /data/adb/tricky_store/alwaysstrong/"
  - "Integrated WebUI: manage auto-refresh intervals, per-app keybox mappings, spoof flags (spoof.conf), and target packages"
  - "Action button automation: trigger immediate keybox rotation, fingerprint fetching, target rebuilding, and GMS cleanup in one tap"
  - "Multi-manager support: runs on Magisk, KernelSU, and APatch with automatic busybox ash re-exec for action.sh"
faq:
  - question: "Why does AlwaysStrong use the module ID 'tricky_store'?"
    answer: "AlwaysStrong uses the tricky_store module ID to maintain drop-in compatibility with existing root tools, WebUI callers, and scripts that expect keybox.xml and target.txt under /data/adb/tricky_store/."
  - question: "Where does AlwaysStrong store its own settings and state?"
    answer: "Since v1.0.5+, AlwaysStrong stores its settings, state, and per-app keybox map under /data/adb/tricky_store/alwaysstrong/{config,state,apps.map} (alongside packages, spoof.conf, imported, and logs/), keeping the root /data/adb/tricky_store/ directory clean for the attestation engine."
  - question: "Should I keep Play Integrity Fix installed when using AlwaysStrong?"
    answer: "No. AlwaysStrong bundles PlayIntegrityFork (reading binary-patched paths inside /data/adb/modules/tricky_store/) together with TEESimulator-RS. Remove standalone PlayIntegrityFix/Fork or TrickyStore modules before flashing."
---

## Overview

Developed by **Evokerr** and hosted on GitLab (**Evokerr/AlwaysStrong**), **AlwaysStrong** (`v1.0.6.1`) is an all-in-one packaging of the integrity bypass stack required to achieve `MEETS_STRONG_INTEGRITY` on rooted Android 10+ (SDK 29+) devices.

Passing Google's highest attestation tiers typically requires flashing, configuring, and updating multiple separate modules—a hardware attestation simulator (TEESimulator-RS) and a build fingerprint spoofer (PlayIntegrityFork). AlwaysStrong unifies both components into a single drop-in package with an integrated WebUI, native fetchers (`asfetch` and `aswatcher`), and one-tap Action maintenance.

---

## Technical Architecture & How It Works

### Unified Stack Orchestration

AlwaysStrong combines framework spoofing and hardware Keystore simulation under a single module directory (`/data/adb/modules/tricky_store/`):

1. **Integrated Core Engines**: Combines the native Rust/C++ attestation simulation of **TEESimulator-RS** (`libTEESimulator.so`, `libinject.so`, `libsupervisor.so`, `libcertgen.so`, `daemon`, `tee_classes.dex`) with the property manipulation rules of **PlayIntegrityFork** (`custom.pif.prop` patched to read directly from the module directory).
2. **Consolidated Storage Layout**: Module-owned files live inside `/data/adb/tricky_store/alwaysstrong/` (`config` for `key=value` toggles like `auto_fp` and `interval_sec`, `state` for internal engine/loop state, `apps.map` for per-app keybox and mode mappings, `packages` for custom targets, `spoof.conf` for Advanced tab overrides, `imported`, `logs/`, and `tmp/`), while keystore engine files (`keybox.xml`, `target.txt`) stay in `/data/adb/tricky_store/`.
3. **Automated Action & Boot Pipeline**: Tapping **Action** (`action.sh`) hops into the root manager's busybox `ash` and executes a progressive pipeline that refreshes active keybox certificates, fetches updated Pixel fingerprints, builds `/data/adb/tricky_store/target.txt`, synchronizes security patch levels, and flushes cached Google Play Services processes.
4. **WebUI Dashboard**: Provides a built-in `webroot/` interface on KernelSU, APatch, and WebUI-enabled Magisk managers to toggle auto-refresh intervals, inspect status, import keyboxes, and manage per-app mappings.

---

## Installation & Setup

1. Uninstall any standalone copies of TrickyStore, TEESimulator, or PlayIntegrityFix/Fork.
2. Ensure an active standalone Zygisk engine is installed (**ZygiskNext**, **ReZygisk**, or **NeoZygisk**; keep Magisk's built-in **Enforce DenyList** turned OFF).
3. Download `AlwaysStrong-v1.0.6.1.zip` from the official GitLab release (`Evokerr/AlwaysStrong`).
4. Flash the module in your root manager (recovery installation is not supported) and reboot.
5. Tap the **Action** button in your root manager to run the initialization and attestation fetch routine.

---

## Configuration & Practical Usage

- **WebUI Interface**: Open the module's WebUI to configure automatic refresh intervals, override spoof flags (`spoof.conf`), import custom keyboxes, and select target applications.
- **Storage Paths**:
  ```text
  /data/adb/tricky_store/keybox.xml
  /data/adb/tricky_store/target.txt
  /data/adb/tricky_store/alwaysstrong/config
  /data/adb/tricky_store/alwaysstrong/state
  /data/adb/tricky_store/alwaysstrong/apps.map
  ```
- **Legacy Migration**: When upgrading from pre-1.0.5 releases, `post-fs-data.sh` automatically runs `as_migrate` to import legacy loose marker files from `/data/adb/tricky_store/` into `/data/adb/tricky_store/alwaysstrong/`.

---

## Troubleshooting & Common Issues

- **Detection Still Failing**: Run the **Action** button again in your root manager to pull the latest keybox/fingerprint bundle and flush cached Play Services attestation tokens, then inspect `/data/adb/tricky_store/alwaysstrong/logs/`.
- **Zygisk Recommendation**: Avoid Magisk's built-in Zygisk and never enable **Enforce DenyList** when using standalone Zygisk loaders, as doing so can break module injection and hiding.
