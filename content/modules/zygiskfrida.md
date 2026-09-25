---
id: "zygiskfrida"
title: "ZygiskFrida: Stealth Frida Gadget Injection Framework"
sidebarTitle: "ZygiskFrida"
description: "Dynamic instrumentation module injecting the Frida gadget into Android applications via Zygisk to evade ptrace and anti-tamper detection."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "zygiskfrida magisk module"
  - "frida gadget zygisk injection"
  - "bypass ptrace frida android"
  - "lico-n zygisk frida"
  - "stealth frida instrumentation root"
prerequisites:
  - "Rooted device or emulator with Zygisk enabled (or Riru for legacy environments)"
  - "Frida CLI tools (frida-tools) installed on the host development machine"
conflicts:
  - "Standalone frida-server (e.g. MagiskFrida) running simultaneously on the default port 27042 unless the gadget is configured to use a different port"
configPaths:
  - "/data/local/tmp/re.zyg.fri/config.json"
  - "/data/local/tmp/re.zyg.fri/config.json.example"
  - "/data/local/tmp/re.zyg.fri/libgadget.so"
  - "/data/adb/modules/zygisk_frida/"
features:
  - "Non-intrusive gadget injection: injects Frida gadget without modifying target APK files, preserving signature and APK integrity checks"
  - "No ptrace debugger attachment: evades common anti-debugging and ptrace detection routines used by protected applications"
  - "Startup delay control: configure start_up_delay_ms to allow application security routines to complete before gadget initialization"
  - "Child gating support: pause and instrument spawned child processes in freeze mode with dedicated child gadget libraries"
  - "Arbitrary library injection: load custom native shared libraries (.so) alongside Frida directly into the target process memory space"
faq:
  - question: "Why use ZygiskFrida instead of running a standard frida-server daemon?"
    answer: "Standard frida-server attaches to the target application from the outside using Linux's ptrace system call, which is immediately detected and blocked by modern banking and anti-cheat SDKs. Additionally, repackaging APKs with frida-gadget breaks cryptographic signature checks. ZygiskFrida injects the gadget from within the process during Zygote initialization, bypassing both ptrace and signature checks."
  - question: "Why does the target app pause immediately upon launching?"
    answer: "By default, the injected Frida gadget runs in 'listen' mode, pausing application execution at startup until a Frida client (e.g. frida -U -N <package>) attaches to its listening socket. You can configure execution behavior inside /data/local/tmp/re.zyg.fri/config.json."
---

## Overview

Developed by **lico-n**, **ZygiskFrida** is a stealth dynamic instrumentation framework designed for Android reverse engineers and security researchers.

Traditional mobile dynamic analysis requires either attaching to an app using `frida-server` (which uses Linux's `ptrace` system call and is easily detected by anti-tamper SDKs) or repackaging the APK to embed `libgadget.so` (which trips APK signature and checksum verification). ZygiskFrida solves both challenges by injecting the Frida gadget into the application process during Zygote specialization, leaving the original APK completely unmodified and avoiding external debugger attachment.

---

## Technical Architecture & How It Works

### In-Process Gadget Loading & Specialization Hooks

ZygiskFrida hooks into the Android process creation lifecycle:

1. **Zygote Companion Hook**: When an application process is forked by Zygote, ZygiskFrida intercepts `postAppSpecialize`. It checks the process package name against the target rules defined in `/data/local/tmp/re.zyg.fri/config.json`.
2. **Native Gadget Injection**: If the process matches an enabled target, the module uses dynamic linker primitives (such as `dlopen` via `xdl`) to map `libgadget.so` directly into process memory.
3. **Execution Delay & Anti-Tamper Avoidance**: Many protected applications perform aggressive integrity scans only within the first few hundred milliseconds of process startup. Through `start_up_delay_ms`, researchers can configure an intentional delay, allowing initial security checks to complete before the gadget initializes.
4. **Child Gating**: Supports instrumenting multi-process applications by intercepting secondary process forks and loading child gadgets in `freeze` mode until explicitly released.

---

## Installation & Setup

### 1. Flash the Module
1. Download the latest `ZygiskFrida-v*.zip` from the project's official releases.
2. Flash the module in your root manager (Magisk, KernelSU, or APatch) with Zygisk enabled.
3. Reboot your device.

### 2. Configure Your Target Application
Copy the example configuration file and specify your target package name:
```bash
adb shell 'su -c cp /data/local/tmp/re.zyg.fri/config.json.example /data/local/tmp/re.zyg.fri/config.json'
adb shell "su -c sed -i 's/com.example.package/com.target.application/' /data/local/tmp/re.zyg.fri/config.json"
```

### 3. Attach with Frida
Launch the application on your Android device. The app will hold at startup:
```bash
frida -U -N com.target.application
# Or attach by gadget name:
frida -U -n Gadget
```

---

## Configuration & Practical Usage

Fine-tuning is handled in `/data/local/tmp/re.zyg.fri/config.json`:
```json
{
  "targets": [
    {
      "app_name": "com.target.application",
      "enabled": true,
      "start_up_delay_ms": 500,
      "injected_libraries": [
        {
          "path": "/data/local/tmp/re.zyg.fri/libgadget.so"
        }
      ],
      "child_gating": {
        "enabled": false,
        "mode": "freeze",
        "injected_libraries": [
          {
            "path": "/data/local/tmp/re.zyg.fri/libgadget-child.so"
          }
        ]
      }
    }
  ]
}
```

---

## Troubleshooting & Common Issues

- **Port Conflict with frida-server**: If you also run a standalone `frida-server` (e.g. via MagiskFrida), both tools will compete for TCP port `27042`. Configure a custom listening port or unix domain socket for the gadget, or disable `frida-server` while using ZygiskFrida.
- **Emulator Native Hooks**: On Android emulators running binary translation (e.g. ARM-on-x86), the gadget initializes within the native translation realm. You can hook Java classes and methods, but hooks on native C/C++ routines may require matching host architecture builds.
