---
id: "freezeit-background-optimizer"
title: "FreezeIt Background App Optimizer: Kernel-Level Process Suspension"
sidebarTitle: "FreezeIt Freezer"
description: "Intelligent background application suspension daemon utilizing Linux kernel cgroups and process freezer subsystems to eliminate standby battery drain and background wakelocks."
category: "battery-power-charging"
tier: 1
searchQueries:
  - "freezeit magisk module"
  - "background app freezer root"
  - "linux cgroups freezer android"
  - "stop battery drain background apps root"
prerequisites:
  - "Kernel with cgroups and freezer subsystem support (Android 8+)"
  - "Magisk 20.4+, KernelSU, or APatch"
conflicts:
  - "Conflicting aggressive background slayers executing overlapping SIGSTOP commands"
configPaths:
  - "/data/adb/modules/freezeit/freezeit.conf"
  - "/data/adb/modules/freezeit/whitelist.txt"
  - "/sys/fs/cgroup/freezer/"
features:
  - "Leverages Linux cgroup freezer subsystem to pause processes without terminating them"
  - "Preserves app memory state for instantaneous zero-lag resumption upon user focus"
  - "Aggressively neutralizes background wakelocks, timer alarms, and battery drain"
  - "Automated whitelist protects messaging apps, download managers, and root daemons"
faq:
  - question: "How does freezing differ from killing background apps?"
    answer: "Killing an app clears its memory, forcing a heavy CPU cold start when reopened. Freezing pauses the process in RAM via kernel cgroups (FROZEN state). It consumes zero CPU cycles or battery in standby, yet restores instantly when tapped."
  - question: "Will I miss instant push notifications from chat apps?"
    answer: "Core messaging services (WhatsApp, Telegram, WeChat) are pre-whitelisted by default. You can also append any package name to /data/adb/modules/freezeit/whitelist.txt to exempt it."
---

## Overview

**FreezeIt Background App Optimizer** (authored by JARK006) is a high-performance systemless battery optimization daemon designed to solve modern Android standby battery drain.

Modern mobile applications often spawn numerous background services, push monitors, analytics daemons, and tracking loops that keep the CPU in active awake states (wakelocks). Standard Android Doze helps, but is often bypassed by apps registering high-priority job schedulers. FreezeIt addresses this at the kernel level by placing non-essential processes into the Linux `freezer` cgroup.

---

## Technical Architecture & How It Works

FreezeIt utilizes the Linux control group (`cgroups`) freezer subsystem (`CONFIG_CGROUP_FREEZER`):

### 1. Process State Management

When an application moves out of the foreground:

```text
Foreground Activity -> App Minimized -> Grace Period (e.g. 30s) -> Kernel Freeze
```

The daemon writes the application's process IDs (PIDs) into the cgroup freezer control file:

```bash
echo $PID > /sys/fs/cgroup/freezer/freezeit/cgroup.procs
echo "FROZEN" > /sys/fs/cgroup/freezer/freezeit/freezer.state
```

In the `FROZEN` state:
- The Linux kernel scheduler skips all threads belonging to the task.
- Zero CPU instructions are executed.
- Memory remains locked in RAM, preventing cold-launch disk I/O when the user returns.

### 2. Resumption & Focus Handshake

When the user switches back to the application or a high-priority system broadcast arrives:

```bash
echo "THAWED" > /sys/fs/cgroup/freezer/freezeit/freezer.state
```

The threads resume execution immediately at their exact previous CPU instruction pointer with zero delay.

---

## Configuration & Whitelist Management

Customize behavior via the local configuration files:

```bash
# Whitelist path
/data/adb/modules/freezeit/whitelist.txt
```

Add application package names (one per line) to keep them running continuously:

```text
com.whatsapp
org.telegram.messenger
com.google.android.gms
```
