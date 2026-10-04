---
id: "qishui-music-svip-unlocker"
title: "Soda Music SVIP & AdBlock (me.bingyue.fuckqishui)"
description: "LSPosed Xposed module for Soda Music (汽水音乐 / Luna Music) that unlocks SVIP privileges, removes in-app advertisements, and enables lossless audio streaming."
category: "xposed-runtime-hooks"
author: "bingqiu456"
version: "3.0"
updatedAt: "2026-10-04"
compatibility: ["LSPosed"]
---

## Overview & System Architecture

**Soda Music SVIP & AdBlock** (`me.bingyue.fuckqishui`), authored by developer bingqiu456, is an Xposed/LSPosed runtime hooking module created for ByteDance's music streaming platform **Soda Music** (汽水音乐 / international counterpart *Luna Music*).

Operating within the target application's ART process runtime via LSPosed hooks, the module dynamically intercepts account authorization routines, feature flag verifications, and advertising SDK dispatchers. Because modifications take place in volatile process memory, no APK re-signing or application patching is required, preserving original package signature integrity and auto-update compatibility.

## Technical Package Analysis

Inspecting the distributed APK package (`_3.0.apk`) confirms modern Xposed implementation:

- **Target Package Name**: `me.bingyue.fuckqishui`
- **Hooking Architecture**: Utilizes DexKit native hooking library (`lib/arm64-v8a/libdexkit.so`, `lib/armeabi-v7a/libdexkit.so`, `lib/x86_64/libdexkit.so`) for robust symbol resolution across obfuscated code releases.
- **Entry Hook Point**: Standard Xposed initialization registered in `assets/xposed_init`.

## Key Capabilities

1. **SVIP Privilege Emulation**: Hooks user profile verification methods to spoof premium subscription status, unlocking VIP-only audio tracks and exclusive album streams.
2. **Audio Bitrate Unlock**: Unlocks lossless audio streaming (FLAC / High-Bitrate AAC) without requiring an active monthly VIP subscription.
3. **Comprehensive Ad Elimination**: Suppresses cold-start splash advertisements, feed recommendation audio promos, and banner advertisements.
4. **Download Restrictions Bypass**: Allows saving cached audio files for offline listening without VIP download quota limits.

## Installation & Configuration

### Prerequisites
- Android 9.0–14 device rooted via Magisk, KernelSU, or APatch.
- **LSPosed Framework** (Zygisk or Riru release) installed and active.

### Step 1: Install Module APK
Install `_3.0.apk` using your favorite package installer or via ADB:
```bash
adb install _3.0.apk
```

### Step 2: Activate Scope in LSPosed Manager
1. Open the **LSPosed Manager** notification or application.
2. Navigate to the **Modules** tab and locate **汽水音乐Svip+去除广告**.
3. Toggle the module **ON**.
4. Check the scope checkbox for **汽水音乐** (`com.luna.music` / `com.ss.android.ugc.aweme.music`).

### Step 3: Restart Target Application
Force stop and relaunch the music app to load hooks:
```bash
am force-stop com.luna.music
```

## Security & Operational Notes

- **Xposed Scope Isolation**: Keep LSPosed scope restricted strictly to Soda Music. Do not enable system-wide scope.
- **Account Safety**: While this module operates locally by bypassing UI and playback checks, streaming heavily restricted server-authenticated licensed tracks may depend on server-side token validation.
