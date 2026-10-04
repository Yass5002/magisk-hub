---
id: "shizuku"
title: "Shizuku: Direct System API & Binder IPC Broker for Android"
sidebarTitle: "Shizuku"
description: "Privileged userland service by Rikka that exposes system service binder tokens to third-party applications via ADB wireless debugging or root su without process-fork overhead."
category: "root-management"
tier: 1
searchQueries:
  - "shizuku apk download"
  - "shizuku wireless debugging pairing guide"
  - "start shizuku adb shell command"
  - "shizuku root setup"
  - "shizuku binder ipc android"
prerequisites:
  - "Android 6.0 (Marshmallow) or newer (Wireless debugging requires Android 11+)"
  - "Root privileges via Magisk, KernelSU, or APatch OR an active ADB bridge (Computer or Wireless Debugging)"
conflicts:
  - "Aggressive OEM battery optimizations (Xiaomi HyperOS / MIUI Battery Saver killing background starter processes)"
  - "Restricted USB debugging permission toggles on ColorOS, OxygenOS, and HyperOS"
configPaths:
  - "/sdcard/Android/data/moe.shizuku.privileged.api/start.sh"
  - "/data/user_de/0/moe.shizuku.privileged.api/"
features:
  - "High-performance Binder IPC: proxies direct AIDL system service calls instead of spawning slow su shell subprocesses"
  - "Rootless operation: leverages Android 11+ Wireless Debugging pairing to grant ADB-level capabilities without unlocking the bootloader"
  - "Fine-grained security tokens: ensures client apps only access system APIs through cryptographic token verification managed by the user"
  - "Rish terminal environment: provides an interactive privileged shell using Shizuku's existing Binder token"
faq:
  - question: "Why does Shizuku stop running whenever I turn off my screen on HyperOS or MIUI?"
    answer: "HyperOS and MIUI enforce aggressive background process reclamation. To keep the Shizuku daemon alive, navigate to Settings -> Apps -> Shizuku -> Battery Saver and select 'No restrictions'. Furthermore, ensure 'USB debugging (Security settings)' remains enabled under Developer Options."
  - question: "Do I have to re-pair Wireless Debugging every time I reboot?"
    answer: "No. Pairing is a one-time cryptographic handshake. However, Android randomizes the wireless debugging port upon every reboot and Wi-Fi reconnection. You only need to toggle Wireless Debugging off and on, open Shizuku, and tap 'Start' to re-bind to the new dynamic port."
  - question: "What is the manual ADB command to start Shizuku from a computer?"
    answer: "Connect your device via USB with USB debugging enabled, then execute: `adb shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh`. The Shizuku daemon will spawn and bind immediately."
---

## Overview

Developed by Rikka and open-sourced under the Apache-2.0 license, **Shizuku** represents a fundamental architectural breakthrough in how Android applications interact with privileged operating system internals.

Traditionally, root applications requiring elevated privileges—such as package managers, app freezers, and file browsers—rely on spawning interactive superuser shell processes (`su`). Every operation translates into executing terminal commands (e.g. `pm disable-user <package>` or `dumpsys activity`). This pattern suffers from severe engineering drawbacks:
1. **High Latency**: Spawning shell processes repeatedly incurs significant CPU and fork/exec overhead.
2. **Fragile Text Parsing**: Command outputs must be serialized to string text and deserialized via regex, creating vulnerability to OEM output formatting changes.
3. **Restricted Scope**: Applications are limited strictly to CLI tools compiled into the OS image.

Shizuku eliminates the shell intermediary entirely by establishing an inter-process communication (IPC) broker directly across Android's native Binder framework.

---

## Technical Architecture & How Shizuku Works

Android's system architecture organizes core OS capabilities into system services running inside `system_server` (e.g., `PackageManagerService`, `ActivityManagerService`, `AppOpsService`). User applications interact with these services by obtaining `IBinder` handles:

```
┌─────────────────┐       IPC Binder Token        ┌──────────────────────┐
│   Client App    ├──────────────────────────────►│    Shizuku Server    │
│  (e.g., Canta)  │◄──────────────────────────────┤ (app_process / Java) │
└─────────────────┘                               └──────────┬───────────┘
                                                             │ Direct AIDL
                                                             ▼ Call
                                                  ┌──────────────────────┐
                                                  │    system_server     │
                                                  │ (PackageManager, etc)│
                                                  └──────────────────────┘
```

1. **Daemon Spawning**: Shizuku launches a standalone Java process using Android's native `app_process` binary running under either the `shell` UID (`2000` via ADB) or the `root` UID (`0` via su).
2. **Binder Delegation**: Once the daemon is active, it obtains privileged Binder interfaces from the system server.
3. **IPC Brokerage**: When an authorized client application (such as Hail, Canta, or Material Files) connects, Shizuku verifies the client's UID against the user-approved permission list and returns a proxied Binder wrapper (`ShizukuBinderWrapper`).
4. **Direct Method Invocation**: The client app invokes native AIDL methods directly in Java/Kotlin with near-zero latency and type safety.

---

## Activation Methods

Shizuku supports three distinct operational modes depending on whether your device is rooted or stock:

### 1. Root Mode (Magisk / KernelSU / APatch)
If your device has root access, Shizuku requires zero manual ADB commands:
1. Sideload and install `shizuku-v*.apk`.
2. Open the Shizuku application.
3. Locate the **Start via Root** card and tap **Start**.
4. When prompted by your root manager (Magisk, KernelSU, or APatch), grant Superuser permissions permanently.
5. Shizuku will spawn the background daemon and display `Shizuku is running (root)`.

### 2. Wireless Debugging Mode (Android 11+ Rootless)
On unrooted Android devices running Android 11 or newer:
1. Connect your device to a local Wi-Fi network.
2. Enable **Developer Options** by tapping *Build Number* seven times in *Settings -> About Phone*.
3. In Developer Options, enable **Wireless debugging**.
4. Open Shizuku and tap **Pairing** under *Start via Wireless Debugging*.
5. Split-screen or open Developer Options in a floating window, navigate to *Wireless debugging -> Pair device with pairing code*.
6. Enter the 6-digit pairing code shown on screen into Shizuku's notification prompt.
7. Return to the Shizuku app and tap **Start**. Shizuku will automatically connect to the internal wireless port and initialize the server.

### 3. Cable ADB Mode (Computer)
For stock devices on Android 10 or older, or when Wi-Fi is unavailable:
1. Connect your phone to your computer via USB with **USB debugging** turned on.
2. Open a terminal on your computer and execute:
   ```bash
   adb shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh
   ```
3. The terminal will output confirmation of `app_process` execution, and Shizuku will display `Shizuku is running (adb)`.

---

## Using Rish (Root/Shell Interactive Shell)

Shizuku includes `rish` (Rikka Shell), a tool that converts Shizuku's Binder token into an interactive root or ADB terminal session on your Android device without needing a computer:

1. In Shizuku, tap **Use Shizuku in terminal apps**.
2. Tap **Export files** to save `rish` and `rish_dex.jar` to a local directory.
3. In Termux or your preferred Android terminal emulator, invoke:
   ```bash
   chmod +x ./rish
   ./rish
   ```
4. You will immediately obtain a shell with UID 2000 (`shell`) or UID 0 (`root`), ready for automation scripts.

---

## OEM Quirks & Troubleshooting

### Xiaomi HyperOS / MIUI
- **Issue**: Shizuku closes or permissions time out immediately.
- **Fix**: Open Developer Options and enable both:
  - **USB debugging (Security settings)** *(Requires SIM card verification)*
  - **Disable permission monitoring** *(Prevents MIUI from intercepting runtime Binder checks)*
- Navigate to *Settings -> Battery -> Background app management*, locate Shizuku, and select **No restrictions**.

### Samsung OneUI
- **Issue**: Shizuku stops working after Wi-Fi disconnect.
- **Fix**: Samsung Knox automatically disables Wireless Debugging upon disconnecting from known Wi-Fi networks. Whenever reconnecting, re-toggle *Wireless debugging* in Developer Options.

---

## Emergency Recovery & Stopping Daemon

If a malfunctioning client app consumes excessive resources or if you wish to terminate the Shizuku daemon:

```bash
# Terminate the Shizuku daemon from root shell or ADB:
pkill -f moe.shizuku.privileged.api

# Verify process termination:
ps -ef | grep shizuku
```
