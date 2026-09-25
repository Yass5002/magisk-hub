---
id: "tree"
title: "Tree for Android: Bash-Based Recursive Directory Tree Visualizer"
sidebarTitle: "Tree Visualizer"
description: "Provides a pure bash implementation of the classic Linux tree command for Android root shells, generating recursive ASCII directory hierarchies."
category: "system-utilities"
tier: 1
searchQueries:
  - "tree command android root"
  - "tree magisk module"
  - "bash tree command android terminal"
  - "recursive directory listing android adb"
  - "magisk system utilities tree"
prerequisites:
  - "Root access via Magisk"
  - "Bash interpreter present on the device"
conflicts: []
configPaths:
  - "/data/adb/modules/tree/"
features:
  - "Recursive directory graphing: renders hierarchical tree diagrams of file systems and directories directly in terminal"
  - "Core flag compatibility: supports standard options including -a (all files), -d (directories only), -L (depth limit), -n (no color), and -i (ASCII mode)"
  - "Pure Bash architecture: functions without requiring heavy compiled glibc dependencies or full chroot containers"
  - "Systemless integration: exposes the tree command across ADB shells and root terminal sessions"
  - "Lightweight utility: negligible storage footprint and zero background memory consumption"
---

## Overview

The standard GNU/Linux `tree` command is an indispensable terminal utility for inspecting directory structures, examining package layouts, and debugging complex filesystem permissions. Because Android's default Toybox and Toolbox suites omit the `tree` binary, developers and system administrators are typically forced to use unwieldy `find` or `ls -R` pipelines.

**Tree for Android** provides a systemless Magisk package containing a pure Bash implementation designed to mimic the classic Linux `tree` command inside Android root shells.

## Supported Flags & Options

The command accepts familiar standard parameters:

```bash
tree [OPTIONS] [DIRECTORY]
```

- **`-a`**: Show all files (including hidden dotfiles).
- **`-d`**: List directories only; omit individual files.
- **`-L <depth>`**: Limit maximum display depth to specified number of directory levels (e.g., `tree -L 2 /sdcard/`).
- **`-n`**: Turn off terminal ANSI color formatting.
- **`-i`**: Force pure ASCII tree lines instead of extended Unicode box-drawing characters.

## Example Usage

Inspect a root module directory:

```bash
su
tree -L 2 /data/adb/modules/tree
```

Outputs:
```text
/data/adb/modules/tree
├── META-INF
│   └── com
├── module.prop
└── system
    └── bin
        └── tree
```

## Installation

1. Download `tree-main.zip` from GitHub releases.
2. Flash the module in **Magisk Manager**.
3. Reboot your device to access `tree` in your terminal shell.
