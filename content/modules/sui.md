---
id: "sui"
title: "Sui: Systemless Super User Interface & Shizuku Provider"
sidebarTitle: "Sui"
description: "Modern root interface integrating Shizuku API directly into system services, allowing apps to invoke privileged Android APIs without spawning full su subshells."
category: "system-utilities"
tier: 1
searchQueries:
  - "sui magisk module"
  - "sui shizuku alternative root"
  - "xiaotong6666 sui"
  - "systemless shizuku server"
  - "sui interactive shell android"
prerequisites:
  - "Android 8.0 or newer"
  - "Magisk, KernelSU, or APatch with Riru or Zygisk injection support"
conflicts:
  - "Standalone Shizuku application running concurrently as a background user-space service (can cause conflicting binder registrations)"
configPaths:
  - "/data/adb/sui/"
  - "/data/adb/modules/sui/"
features:
  - "Native Shizuku API integration: grants authorized apps direct access to privileged Android Framework Java APIs"
  - "Process spawning optimization: eliminates the latency and memory overhead of spawning separate su binary shells for each command"
  - "System Settings management UI: integrates authorization prompts and permission management directly into Android's native Settings app"
  - "Multiple authorization modes: supports interactive confirmation prompts, automatic grant mode, or total restriction"
  - "Built-in interactive root shell & adb root helper: provides high-speed root terminal access directly over binder"
faq:
  - question: "How does Sui differ from the standard Shizuku app?"
    answer: "The standard Shizuku application runs as an external background process started via ADB or a root shell wrapper. Sui is a systemless module that injects directly into system_server and app processes at boot, starting instantly with zero user intervention and operating directly inside the Android Framework."
  - question: "Where do I manage app permissions in Sui?"
    answer: "Sui does not use a standalone launcher app. Instead, it embeds its management panel directly into your phone's native Settings application under System or Developer Options (or triggers an overlay interface when an app requests permission)."
---

## Overview

Developed by **RikkaApps** and maintained by **XiaoTong6666**, **Sui** is a modern Super User Interface (SUI) implementation for Android.

Rather than relying solely on traditional Unix-style `su` subshells—which require starting heavy `/system/bin/sh` processes and parsing fragile text streams—Sui integrates the **Shizuku API** directly into Android's system framework. This enables privileged applications to call hidden and system-level Android Java APIs directly over high-speed IPC with authentic system permissions.

---

## Technical Architecture & How It Works

### Framework Service Injection & Binder IPC

Sui operates from within the Android OS runtime:

1. **System Server Hooking**: During early boot, Sui hooks into `system_server` using Zygisk or Riru. It registers a secure local Binder service that exposes privileged platform capabilities.
2. **Direct Framework Invocation**: Client applications link against the Shizuku API library. When invoking commands (such as package management, permission granting, or display controls), the request passes over Binder IPC directly to the system server without spawning shell processes.
3. **Integrated Security Dialogs**: When an untrusted app requests access, Sui triggers a native framework authorization dialog directly on the user's screen.

---

## Installation & Setup

1. Verify that your root environment (Magisk, KernelSU, or APatch) has an active Zygisk implementation.
2. Download the latest `Sui-v*.zip` from the official repository releases.
3. Flash the module in your root manager and reboot.
4. Launch any Shizuku-compatible app (such as App Ops, Swift Backup, or Shizuku tools); Sui will automatically handle authorization.

---

## Configuration & Usage

- **Management Interface**: Access Sui's permission manager directly through Android Settings or by launching the configuration helper via terminal:
  ```bash
  su -c /data/adb/modules/sui/bin/sui
  ```
- **Permission Modes**: Configure per-application policies (Allow, Deny, Prompt each time) without needing a standalone management APK installed on your home screen.

---

## Troubleshooting & Common Issues

- **Conflicting Shizuku Service**: If an application fails to detect Sui, verify that you have not left the standalone Shizuku app running in the background. Stop and uninstall the standalone Shizuku APK to allow Sui to bind to the default Shizuku IPC endpoint.
- **Root Shell Access**: To start an interactive root shell powered by Sui, execute `sui shell` from a terminal emulator.
