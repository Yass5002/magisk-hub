---
id: "joyctl-android"
title: "JoyCtl Android: On-Device Xiaomi & HyperOS Joyose Cloud Control Editor"
sidebarTitle: "JoyCtl Android"
description: "MIT-licensed native Android su utility (com.hexwander.joyctl) that reads and modifies Xiaomi/HyperOS Joyose teg_config.db locally for thermal PID thresholds, frame rate locks, and migt tuning."
category: "performance-kernel"
tier: 1
searchQueries:
  - "joyctl android apk"
  - "xiaomi joyose teg_config.db editor"
  - "hyperos remove thermal throttling fps lock"
  - "com.hexwander.joyctl"
  - "persist.sys.sc_allow_conn joyose"
prerequisites:
  - "Xiaomi, Redmi, or POCO device running MIUI or HyperOS with `com.xiaomi.joyose` installed"
  - "Root access via Magisk, KernelSU, or APatch allowing third-party apps to invoke `su`"
conflicts:
  - "Xposed modules or Magisk modules that simultaneously overwrite `teg_config.db` or hook `com.xiaomi.joyose` cloud configs"
configPaths:
  - "/data/data/com.xiaomi.joyose/databases/teg_config.db"
  - "/data/user/0/com.xiaomi.joyose/databases/teg_config.db"
  - "/data/user_de/0/com.xiaomi.joyose/databases/teg_config.db"
  - "/data_mirror/data_ce/null/0/com.xiaomi.joyose/databases/teg_config.db"
features:
  - "Reads and writes Xiaomi Joyose's local SQLite database (`teg_config.db`) directly on-device via `su` with automatic `.joyctl.bak` backup and post-push read-back verification"
  - "Fetches unmodified upstream cloud configurations matching the local Joyose version (or device model fallback) into `teg_config_baseline.db` to detect MCC cloud overwrites"
  - "Provides card-based rule templates supporting multi-game selection to relax Joyose PID thermal thresholds (e.g., `47` → `47:48`), disable frame-rate locks (`dynamic_fps`), and tune `migt` big-core baselines"
  - "Toggles Joyose MCC cloud sync (`persist.sys.sc_allow_conn=0/1`) and includes an official Joyose reset routine if cloud config state becomes corrupted"
faq:
  - question: "What happens if `teg_config.db` does not exist yet on my Xiaomi/HyperOS device?"
    answer: "Joyose generates `teg_config.db` after initial cloud sync or Game Turbo usage. Open Xiaomi Game Turbo (游戏工具箱) or launch a game so Joyose initializes its database under `/data/data/com.xiaomi.joyose/databases/`, then pull again in JoyCtl Android."
  - question: "How do I prevent Xiaomi's cloud service from reverting my modified `teg_config.db` rules?"
    answer: "Use the Freeze Cloud Control action on JoyCtl Android's Device page, which sets `persist.sys.sc_allow_conn=0` and stops the `com.xiaomi.joyose` process so MCC cloud updates cannot overwrite local rules. You can still compare your active DB against the baseline on the Cloud/Device tabs anytime."
---

## Overview

**JoyCtl Android** (`com.hexwander.joyctl`) is a native Kotlin Android port of **hexwander/joyctl**. While the original desktop JoyCtl tool required connecting a rooted Xiaomi smartphone to a PC over ADB to pull, patch, and push Joyose's cloud database, JoyCtl Android performs the entire workflow directly on the phone using `su` privileges.

On MIUI and HyperOS devices, `com.xiaomi.joyose` governs per-app frame-rate caps (`dynamic_fps`), thermal PID throttling (`thermal`), and scheduler hints (`migt`) stored inside `teg_config.db`. JoyCtl Android lets rooted users inspect, back up, edit, and freeze these rules safely from a mobile UI.

---

## Technical Architecture & Database Workflow

Inspecting `JoyCtl-Android-v1.0.17.apk` (`com.hexwander.joyctl`) confirms the following on-device mechanisms:

### 1. Multi-Path Database Discovery (`JoyoseDb`)
Because MIUI/HyperOS builds store Joyose data across different Android storage mounts depending on encryption and OS version, JoyCtl locates `teg_config.db` across:
- `/data/data/com.xiaomi.joyose/databases/teg_config.db`
- `/data/user/0/com.xiaomi.joyose/databases/teg_config.db`
- `/data/user_de/0/com.xiaomi.joyose/databases/teg_config.db`
- `/data_mirror/data_ce/null/0/com.xiaomi.joyose/databases/teg_config.db`
- `/data_mirror/data_de/null/0/com.xiaomi.joyose/databases/teg_config.db`

### 2. Pull, Baseline Comparison & Safe Push
- **Cloud Baseline Fetch**: Queries cloud rule baselines matching the device's local Joyose version first (falling back to device model probing via `ro.product.device` / `ro.product.marketname`), loading active `booster_config` and `common_config` rules (`status=1`).
- **Diff Detection (`CompareResult`)**: Compares the pulled device database against `teg_config_baseline.db` to flag whether MCC cloud sync has overwritten local changes, without altering the baseline when saving edits.
- **Backup & Read-Back Verification**: Before pushing modified SQLite data back to `com.xiaomi.joyose`, JoyCtl writes a `.joyctl.bak` backup and performs a post-write read-back check (`teg_config_device_verify.db`) to ensure integrity.

### 3. Rule Templates & Feature Recognition
- **Thermal Threshold Relaxation**: Supports custom temperature thresholds and multi-game selection, converting integer values into Joyose's PID format (e.g., `47` → `47:48`) across existing PID policy groups.
- **Frame-Rate & Scheduler Rules**: Recognizes and modifies `dynamic_fps` / `dynamic_fps_M` / `dynamic_fps_m` FPS locks, `migt` big-core frequency baselines, and package mappings inside existing `booster_config` / `common_config` entries.
- **Freeze & Official Recovery**: Freezes or restores Joyose MCC cloud connectivity via `persist.sys.sc_allow_conn=0/1`, and provides a one-tap recovery option that clears Joyose data, re-enables `CloudServerReceiver` and `JoyoseBroadCastReceiver`, and sends a boot broadcast.

---

## Usage Guide & Verification

1. Install `JoyCtl-Android-v1.0.17.apk` on a rooted Xiaomi, Redmi, or POCO device.
2. Grant superuser access (`su`) when prompted in **Magisk**, **KernelSU**, or **APatch**.
3. On the **Device** tab, tap **Pull** to load `teg_config.db` (and auto-fetch the matching cloud baseline).
4. Switch to the **Rules** tab to select target games, adjust thermal PID thresholds or FPS locks, tap **Modify**, and return to **Device → Push**.
5. Optionally tap **Freeze** to set `persist.sys.sc_allow_conn=0` and stop Joyose from overwriting your rules.

### Shell Verification Commands

```bash
# Verify cloud control freeze property
getprop persist.sys.sc_allow_conn

# Confirm teg_config.db and JoyCtl backup presence
su -c "ls -la /data/data/com.xiaomi.joyose/databases/"
```

> **Caution**: Relaxing thermal thresholds or removing Joyose FPS caps increases device heat output and battery drain during gaming. Always monitor skin/SoC temperatures and keep `.joyctl.bak` intact.
