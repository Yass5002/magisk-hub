---
id: "dirtysepolicy-bypass"
title: "DirtySepolicy Bypass: Neutralize App-Zygote SELinux Probing & Policy Tamper Detection"
sidebarTitle: "DirtySepolicy Bypass"
description: "Zygisk module intercepting App-Zygote SELinux filesystem queries to defeat DirtySepolicy detection methods across /sys/fs/selinux/ and policy sequence counters."
category: "root-management"
tier: 1
searchQueries:
  - "dirtysepolicy bypass magisk module"
  - "flipphoneguy dirtysepolicy bypass"
  - "defeat dirtysepolicy v2.2 zygisk"
  - "app zygote selinux probe bypass"
  - "spoof sys fs selinux access android"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "Active Zygisk runtime enabled in root manager"
  - "Android 10 through Android 15+"
conflicts: []
configPaths:
  - "/data/adb/modules/dirtysepolicy-bypass/"
features:
  - "Complete DirtySepolicy mitigation: defeats all four probe techniques utilized by LSPosed/DirtySepolicy up to v2.2"
  - "Virtual SELinux filesystem virtualization: intercepts direct open/read/write calls to /sys/fs/selinux/access and context nodes"
  - "Sequence counter spoofing: masks policy load counter changes in /sys/fs/selinux/status to conceal runtime sepolicy mutations"
  - "App-Zygote sandbox isolation: prevents isolated service processes from enumerating custom framework injection types"
---

## Overview

Modern anti-root detection suites (such as the detection routines in LSPosed/DirtySepolicy, Momo, and advanced financial security SDKs) no longer rely merely on searching for `su` binaries or checking `which` paths. Instead, they spawn an unprivileged **App-Zygote** child process and query the kernel's SELinux virtual filesystem (`/sys/fs/selinux/`) directly.

Because root frameworks (such as Magisk, KernelSU, and APatch) inject custom domain rules into the live kernel sepolicy to allow superuser daemons to run, an App-Zygote can probe whether non-stock contexts exist or verify whether policy reload sequence counters (`seqno`) have incremented. If any anomalies are found, the app classifies the device as compromised.

Developed by flipphoneguy, **DirtySepolicy Bypass** is a specialized Zygisk module engineered to blindfold these SELinux probing techniques at the native libc system call boundary.

## Probing Vectors Defeated

DirtySepolicy Bypass systematically neutralizes all four core detection vectors implemented by DirtySepolicy v2.2 and derivative detectors:

### 1. `contextExists()` Probes
Detectors write arbitrary security contexts to `/sys/fs/selinux/context` or query `/proc/self/attr/current` to see if root-injected types (like `magisk`, `kernelsu`, or `su`) exist in the active policy dictionary. The module intercepts these writes and returns `EINVAL` (invalid argument), mimicking standard stock behavior.

### 2. Direct Kernel `checkSELinuxAccess()`
Advanced detectors resolve class and permission identifiers directly from `/sys/fs/selinux/class/` and submit binary permission queries to `/sys/fs/selinux/access`, intentionally bypassing user-space `libselinux.so`. DirtySepolicy Bypass hooks raw `openat`, `read`, and `write` syscalls to intercept these low-level queries and return strictly stock policy verdicts.

### 3. Policy Reload & Sequence Counter Monitoring (`readStatus()`)
When Magisk or KernelSU injects rules at boot, the kernel increments its internal `policyload` counter in `/sys/fs/selinux/status`. Detectors compare this counter against expected stock baseline values. The module presents a virtualized, static status structure that masks all runtime policy mutations.

### 4. Indirect Stock-Context Probes
Detectors test allow rules between stock Android contexts (such as `rootfs → tmpfs:associate`) that only exist because a root framework modified the rule graph. DirtySepolicy Bypass intercepts these indirect queries, returning stock denials.

## Installation & Setup

1. Verify that **Zygisk** is enabled in Magisk or KernelSU.
2. Download the `DirtySepolicy_Bypass` `.zip` from GitHub.
3. Flash the module in your root manager.
4. Reboot the smartphone.
5. Launch your detection test suite (such as DirtySepolicy test apps or Momo); all SELinux probe checks will pass cleanly.
