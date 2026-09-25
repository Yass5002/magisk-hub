---
id: "multiuseruienabler"
title: "Multi-User UI Enabler: Unlock Multiple User Profiles on Stripped OEM ROMs"
sidebarTitle: "Multi-User UI Enabler"
description: "Systemlessly injects framework properties to reveal the hidden Android Multiple Users settings interface on restricted OEM ROMs like One UI Core."
category: "system-environment"
tier: 1
searchQueries:
  - "multiuseruienabler magisk"
  - "insertx2k multiuseruienabler"
  - "enable multiple users one ui core"
  - "android multi user settings hidden"
  - "fw show multiuserui magisk"
prerequisites:
  - "Root access via Magisk 20.4+"
  - "Device ROM must support native user management commands (`pm create-user`, `am switch-user`)"
conflicts: []
configPaths:
  - "/data/adb/modules/multiuseruienabler/"
features:
  - "Unlocks native Multi-User settings: reveals the hidden user profile management menu in Settings > Accounts and backup > Users"
  - "Systemless build.prop modification: injects fw.max_users=5 and fw.show_multiuserui=1 without modifying physical partition files"
  - "Zero Zygisk requirement: operates purely through system property overlays without needing Zygisk runtime hooks"
  - "Isolated sandboxes: provides separate application data, storage, and home screens for secondary users or guest accounts"
  - "Proven OEM compatibility: successfully verified on Samsung One UI Core and custom OEM builds"
---

## Overview

Android includes robust native multi-user architecture, allowing multiple independent user profiles—each with its own application instances, settings, and sandboxed storage—to share a single device. However, certain manufacturers (such as Samsung on their budget "One UI Core" devices) intentionally hide the multi-user configuration screen from the Settings app.

Created by InsertX2k, **multiuseruienabler** is a lightweight systemless Magisk module that injects Android framework flags to unhide and restore the multi-user management interface.

## Prerequisites & Verification

Before installing the module, ensure your device's ROM has not had underlying multi-user service binaries completely excised. You can test compatibility via an ADB shell or Termux:

1. **Verify user switching**:
   ```bash
   su -c am get-current-user
   ```
   *(Should return `0` for the primary system user).*
2. **Verify user creation capability**:
   ```bash
   su -c pm create-user TestUser
   ```
   *(If this command completes without errors, your ROM contains the underlying user service).*
3. **Clean up the test profile**:
   ```bash
   su -c pm remove-user 10
   ```
   *(Replace `10` with the user ID returned during creation. Never attempt to remove user `0`).*

## How It Works

The module leverages Magisk's `system.prop` handling to systemlessly inject framework configuration properties during boot:
- `fw.show_multiuserui=1`: Forces the Android Settings application to render the Multiple Users preference controller.
- `fw.max_users=5`: Sets the maximum allowed concurrent user profile slots to five.

## Installation

1. Download `multiuseruienabler.zip` from GitHub releases.
2. Flash the module in **Magisk Manager**.
3. Reboot your device.
4. Navigate to **Settings > Accounts and backup > Users** (or **Settings > System > Multiple users**) to configure secondary accounts and guest profiles.
