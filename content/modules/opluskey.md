---
id: "opluskey"
title: "OplusKey: Hardware Alert Slider & Custom Side Button Remapper for OnePlus & OPPO"
sidebarTitle: "OplusKey Remapper"
description: "Customizes the OnePlus tri-state alert slider and OPPO side action keys with single click, double click, and long press shell commands."
category: "customization-ui"
tier: 1
searchQueries:
  - "opluskey magisk"
  - "itoseo opluskey"
  - "remap oneplus alert slider root"
  - "oppo custom side key remap"
  - "three stage key custom action android"
prerequisites:
  - "Root access via Magisk"
  - "OnePlus, OPPO, or Realme smartphone with a three-stage alert slider or dedicated custom physical side button"
conflicts: []
configPaths:
  - "/data/adb/modules/opluskey/"
features:
  - "Alert slider customization: intercepts the physical three-position slider (Ring, Vibrate, Silent) to execute arbitrary root shell scripts"
  - "Multi-gesture side button detection: captures single-click, double-click, triple-click, and long-press button inputs"
  - "Optimized C++ daemon: monitors kernel input device event streams with thread affinity pinned to a single efficiency CPU core"
  - "Stock UI suppression: silences the default system alert banner to prevent intrusive volume overlays"
  - "Flexible automation: trigger hardware shortcuts such as toggling NFC, turning on the flashlight, capturing voice memos, or launching screen recorders"
---

## Overview

The physical three-stage alert slider found on OnePlus devices and modern customizable side keys on OPPO/Realme hardware provide tactile hardware convenience. However, stock ColorOS and OxygenOS restrict these buttons to predefined audio profiles or limited assistant triggers.

Developed by ItosEO, **OplusKey** is a lightweight, high-performance root module written in C++. It intercepts hardware input streams directly from kernel `/dev/input/` event nodes, enabling users to rebind the alert slider and custom physical buttons to any custom shell script or system action.

## Key Capabilities

1. **Classic Three-Stage Slider**:
   - Listens for slider position changes between top, middle, and bottom states.
   - Automatically suppresses stock OEM audio profile switches, allowing you to repurpose the slider for custom modes (such as toggling battery saver, private mode, or orientation lock).
2. **Modern Multi-Action Side Keys**:
   - Detects complex click cadences: single click, double click, triple click, and long press.
3. **Ultra-Low Power C++ Architecture**:
   - The compiled native daemon uses non-blocking stream listening and sets its CPU thread affinity strictly to a single little/efficiency core, keeping battery consumption virtually undetectable.

## Configuration & Usage

The module includes sample shell actions that you can tailor to your preferences:
- **Common Actions**: Toggle flashlight, turn on/off Bluetooth, switch NFC state, initiate background voice recording, or start screen recording.
- For modern customizable side buttons, set the default system setting to **No Action** in ColorOS/OxygenOS settings, allowing OplusKey's native listener to handle all inputs.

## Installation

1. Download the latest `OplusKey-*.zip` release from GitHub.
2. Flash the module in **Magisk Manager**.
3. Reboot your device.
4. Customize your trigger actions in the module's script directory to suit your workflow.
