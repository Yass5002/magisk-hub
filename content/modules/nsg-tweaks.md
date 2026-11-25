---
id: "nsg-tweaks"
title: "NSG Tweaks: Network Signal Guru LSPosed Extension"
sidebarTitle: "NSG Tweaks"
description: "MIT-licensed LSPosed module (com.nsgmod.band) that extends Network Signal Guru (com.qtrun.QuickTest v4.8.14) with 16-cell tables, ARFCN/bandwidth columns, signaling search, and log-replay controls."
category: "xposed-runtime-hooks"
tier: 1
searchQueries:
  - "nsg tweaks lsposed module"
  - "network signal guru mod apk"
  - "com.nsgmod.band com.qtrun.QuickTest"
  - "nsg 16 cell table arfcn bandwidth"
  - "network signal guru signaling search replay"
prerequisites:
  - "Android 6.0+ (`minSdkVersion 23`)"
  - "LSPosed with Xposed API 102 support (`minApiVersion=102`)"
  - "Network Signal Guru (`com.qtrun.QuickTest`) **qtrun v4.8.14** build exclusively"
conflicts:
  - "Any Network Signal Guru build other than qtrun v4.8.14 (including Google Play `gplay` flavor or v4.8.12 and earlier)"
  - "Other Xposed modules hooking `com.qtrun.QuickTest` UI tables or signaling adapters"
configPaths:
  - "/data/adb/lspd/"
  - "/data/data/com.qtrun.QuickTest/shared_prefs/"
features:
  - "Expands NR-NSA and LTE serving/neighbor cell tables up to 16 rows while injecting `Band` (ARFCN) and `BW` (DL bandwidth in MHz) columns and compacting row height"
  - "Highlights same-site NR neighbors (`CellIdMatchHook`) and optionally displays NR-NSA gNB-ID, NR-SA Pathloss column, NR PDSCH SINR, and CellID instead of PCI"
  - "Adds signaling log navigation, search, and sharing tools (`SignalingNavHook`, `SignalingSearchHook`, `SignalingShareHook`) plus `RT-Play` button and granular replay seek controls"
  - "Provides 11 dedicated runtime toggles inside **NSG → Settings → Experiments** (`SettingsToggleHook`)"
faq:
  - question: "Why does NSG Tweaks v12.0 fail on the Google Play version or older Network Signal Guru APKs?"
    answer: "Starting in v12.0, NSG Tweaks dropped runtime flavor detection and support for both the Google Play (`gplay`) build and older qtrun releases (v4.8.12 and earlier). It targets obfuscated class and method names using a single verified symbol table built strictly for **qtrun v4.8.14** of `com.qtrun.QuickTest`."
  - question: "Where do I configure individual NSG Tweaks features after enabling it in LSPosed?"
    answer: "After enabling `com.nsgmod.band` in LSPosed with scope set to `com.qtrun.QuickTest` and force-stopping NSG, open **NSG → Settings → Experiments**. Eleven `NSGMod:` toggles appear at the bottom of that screen to turn individual table, highlight, refresh, and replay hooks on or off."
---

## Overview

**NSG Tweaks** (`com.nsgmod.band`), developed by **henrik**, is an open-source (MIT) LSPosed module designed for cellular RF engineers and enthusiasts using **Network Signal Guru (`com.qtrun.QuickTest`)**. Because NSG's stock interface truncates neighbor cell tables at 8 entries, hides ARFCN and channel bandwidth inline, and lacks granular log-replay scrubbing, NSG Tweaks hooks directly into NSG's UI and data models at runtime to surface dense radio-layer telemetry.

In **v12.0**, the module enforces `staticScope=true` targeting `com.qtrun.QuickTest` and requires **LSPosed API 102** (`minApiVersion=102`, `targetApiVersion=102`) on **qtrun v4.8.14** specifically.

---

## Technical Architecture & Hook Catalog

Inspecting `nsg_tweaks_lsposed_v12-0.apk` reveals `META-INF/xposed/java_init.list` pointing to `com.nsgmod.band.MainHook` and `scope.list` pinned to `com.qtrun.QuickTest`. The DEX payload implements modular hook classes across four subsystems:

### 1. Cell Table & RF Metric Extensions
- **NR-NSA & LTE 16-Cell Tables (`NrNsaExtCellsHook`, `CellRowHeightHook`, `CellTableRowDispatcher`)**: Removes the redundant sub-row beneath each cell entry (reclaiming ~22 dp per row, reducing top row height from 28 dp to 22 dp and child rows from 26 dp to 21 dp in NR-SA) and expands table capacity from 8 to 16 cells.
- **Inline ARFCN & Bandwidth (`BandColumnHook`, `NrNsaBandwidthColumnHook`, `LteBandwidthColumnHook`, `NrSaCellColumnsHook`)**: Injects **Band** (ARFCN) and **BW** (downlink channel bandwidth in MHz) columns into NR-NSA (`Serving | Band | BW | PCI | Beam | RSRP | RSRQ | SINR`) and NR-SA cell tables.
- **NR-SA & CA Matrix Hooks**: Adds `NrSaHeaderPathlossHook` (Pathloss column), `NrSaCsiSnrRowHook` (NR PDSCH SINR row), `NrNsaGnbIdHeaderHook` (gNB-ID in header), `NrSaBwpIdHook` (`BWP-ID`), `BwpUlBwDedicatedModeHook`, `CaMatrixDlHook`, `SACAMatrixDLHook`, `LteCaMatrixUlInNsaHook`, `LteCaMatrixUlQpskHook`, `NrSaMimoFormatHook`, `NrSaModUsageRowHook`, `NrSaPucchTxRowHook`, `NrSaThputPerPrbHook`, and `RenamePuschTxLabelHook`.

### 2. Visual Matching & Refresh Rate
- **Same-Site Highlighting (`CellIdMatchHook`, `NrSaCellColorHook`, `LteCellColorHook`, `MapDotColorHook`)**: Highlights NR neighbor rows whose PCI and ARFCN match the serving cell.
- **Fast Refresh & Identity Display (`RefreshIntervalHook`, `PerSimFormatHook`, `PlmnOperatorToastHook`)**: Accelerates UI refresh cadence and allows switching cell identifiers from PCI to CellID.

### 3. Signaling & Log Replay Tools
- **Signaling Utilities (`SignalingNavHook`, `SignalingSearchHook`, `SignalingShareHook`)**: Adds search, quick navigation, and export/share capabilities to signaling message views.
- **Replay Controls (`RtPlayHook`, `ReplayStatusBarHook`, `GranularSeekBarHook`, `PageDotJumpHook`, `ScrollBarHook`)**: Adds an `RT-Play` button and finer-grained seekbar scrubbing during recorded `.nsg` log playback.

### 4. In-App Experiments Toggles (`SettingsToggleHook`)
Inside **NSG → Settings → Experiments**, NSG Tweaks injects 11 feature toggles:
- `NSGMod: Cell table mods`
- `NSGMod: NR-NSA 16-cell table`
- `NSGMod: LTE 16-cell table`
- `NSGMod: Collapse empty cell rows`
- `NSGMod: Highlight same-site NR neighbours`
- `NSGMod: NR-NSA gNB-ID in header`
- `NSGMod: NR-SA Pathloss column`
- `NSGMod: Show NR PDSCH SINR`
- `NSGMod: Use CellID instead of PCI`
- `NSGMod: Fast refresh`
- `NSGMod: RT-Play button`

---

## Installation & Verification

1. Ensure **Network Signal Guru qtrun v4.8.14** (`com.qtrun.QuickTest`) is installed.
2. Install `nsg_tweaks_lsposed_v12-0.apk`.
3. Open **LSPosed Manager → Modules → NSG Tweaks**, enable the module, and verify `com.qtrun.QuickTest` is checked in the scope list.
4. Force-stop and relaunch Network Signal Guru:
```bash
su -c "am force-stop com.qtrun.QuickTest"
```
5. Open **NSG → Settings → Experiments** and scroll to the bottom to verify the **NSGMod:** toggles and `TweaksVersionFooterHook` version footer are present.

---

## Troubleshooting

- **Missing Columns or Crashes on Launch**: Verify your installed NSG APK version is exactly **qtrun v4.8.14** (`dumpsys package com.qtrun.QuickTest | grep versionName`). Google Play builds and v4.8.12 or older are incompatible with NSG Tweaks v12.0.
- **Hooks Not Applying**: Confirm your LSPosed framework supports **Xposed API 102** (`minApiVersion=102`) and check LSPosed logs for `MainHook` or `BWHook` messages.
