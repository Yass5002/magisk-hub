---
id: "hid-gadget-module"
title: "USB HID Gadget Module: Turn Android into a Keyboard, Mouse & DuckyScript Injector"
sidebarTitle: "HID Gadget Module"
description: "Enables USB Human Interface Device (HID) gadget emulation on Android, providing an interactive terminal TUI keyboard/mouse and DuckyScript 3.0 automation."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "hid gadget module magisk"
  - "kelexine hid gadget module"
  - "android usb keyboard mouse emulator root"
  - "duckyscript 3.0 badusb android magisk"
  - "hid-tui terminal keyboard android"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "Kernel compiled with USB ConfigFS and HID gadget drivers (CONFIG_USB_CONFIGFS_F_HID)"
  - "USB-C or micro-USB data cable connected to a host computer"
conflicts: []
configPaths:
  - "/data/adb/modules/hid-gadget-module/"
features:
  - "Full hardware HID emulation: presents Android to connected PCs/Macs as a native physical USB keyboard, optical mouse, and media remote"
  - "Static musl compilation: zero shared library dependencies, supporting ARM, ARM64, x86, and x86_64 environments"
  - "Interactive Terminal TUI (hid-tui): renders an interactive 75% keyboard layout and trackpad navigation inside Termux"
  - "DuckyScript 3.0 execution engine: injects automated keystroke payloads for rapid system administration, recovery scripts, and penetration testing"
  - "Automated driver self-healing: automatically resets and rebinds the Linux ConfigFS gadget subsystem if a host USB reset occurs"
---

## Overview

Whether you are recovering a headless home server with a broken keyboard, managing field equipment without carrying extra peripherals, or conducting penetration tests, having a physical USB Human Interface Device (HID) in your pocket is invaluable.

Developed by kelexine, the **USB HID Gadget Module & Terminal Controller** transforms a rooted Android smartphone into a USB keyboard, mouse, and multimedia remote control. Built with a statically linked `musl` toolchain and backed by an interactive terminal graphical interface (`hid-tui`), the module initializes the Linux kernel's ConfigFS gadget framework, allowing your phone to transmit low-level USB scancodes to any connected PC, Mac, or game console without requiring Bluetooth or companion software on the target machine.

## Key Capabilities

### 1. Interactive Terminal TUI (`hid-tui`)
The module includes a full-featured console application that runs directly inside Termux:
- **75% Laptop Keyboard Layout**: Send function keys, alphanumeric characters, navigation arrows, and modifiers (`Ctrl`, `Alt`, `Super/Win`) from your smartphone screen.
- **Mouse & Trackpad Emulation**: Transmit discrete cursor movements, mouse clicks, and scroll wheel commands over USB.
- **Media Remote**: Control volume, media playback, and brightness controls on target systems.

### 2. DuckyScript 3.0 Payload Execution
For system administrators and penetration testers, the module includes an interpreter compliant with **DuckyScript 3.0**. You can load script files (`.ducky`) and inject complex keystroke payloads into target computers in seconds.

### 3. Native ConfigFS Gadget Management
Operating at the kernel USB layer (`/dev/hidg0`, `/dev/hidg1`), the module configures USB descriptors during early boot. If the host PC resets the USB bus, an intelligent watchdog routine automatically rebinds the gadget driver via `su` to ensure uninterrupted connectivity.

## Launching the TUI Controller

1. Connect your Android phone to the target computer using a standard USB data cable.
2. Open Termux on your phone, acquire root privileges, and launch the interface:
   ```bash
   su -c hid-tui
   ```
3. Use the touchscreen navigation keys to type and control the target computer's cursor directly.

## Installation & Requirements

- Download the latest `hid-gadget-module` `.zip` from GitHub releases.
- Flash the package in **Magisk** or **KernelSU**.
- Reboot your device.
- *Note*: Your device kernel must support USB ConfigFS and HID endpoint functions (`CONFIG_USB_CONFIGFS_F_HID`). Most modern custom kernels and stock AOSP kernels include this support by default.
