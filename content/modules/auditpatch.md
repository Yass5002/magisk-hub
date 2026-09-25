---
id: "auditpatch"
title: "AuditPatch: Kernel Audit Log Context Redaction via Native PLT Injection"
sidebarTitle: "AuditPatch"
description: "Redacts sensitive security contexts and permission denial messages inside Android audit logs using Rust linjector and PLT hooks without restarting logd."
category: "root-management"
tier: 1
searchQueries:
  - "auditpatch magisk module"
  - "silvzr auditpatch"
  - "redact audit log android root"
  - "linjector-rs logd injection"
  - "plt hook audit log mask selinux"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
  - "Android 10 through Android 15+"
  - "Compatible with systems generating kernel audit log entries"
conflicts: []
configPaths:
  - "/data/adb/modules/auditpatch/"
features:
  - "Native runtime injection: utilizes linjector-rs to attach hooks during post-fs-data without requiring Zygisk or restarting logd"
  - "Procedure Linkage Table (PLT) interception: leverages PerformanC PLTI to intercept formatting functions before log records hit buffers"
  - "SELinux context sanitization: scrubs revealing root signatures, package names, and proprietary domain names from system audit traces"
  - "Anti-detection defense: prevents anti-cheat and banking applications from scraping SELinux audit logs to identify root modifications"
---

## Overview

Anti-tamper engines and banking integrity checkers frequently inspect Android's kernel audit buffer (`/dev/log/audit` or logcat audit tags). Whenever a rooted tool or custom su binary interacts with system services, the kernel's SELinux subsystem evaluates permissions. Even if the action succeeds under permissive rules or custom policy injections, an audit record detailing the subject context (`scontext`), target context (`tcontext`), and denied access vectors is broadcast directly into the system log.

Developed by silvzr (building on research by brunoanc), **AuditPatch** addresses these log leaks at their native source. By attaching directly to Android's logging daemon (`logd`), AuditPatch sanitizes audit log payloads before they are serialized and committed to memory buffers.

## Technical Architecture

### 1. Zero-Restart Linjector Pipeline
Traditional logging hooks either require Zygisk runtime assistance or force a restart of `logd` during early boot, which can break system services that hold active Unix socket file descriptors to the logging subsystem. AuditPatch instead employs **`linjector-rs`**, a Rust-based native process injector, to inject its shared library directly into `logd` during the `post-fs-data` boot stage without interrupting log service continuity.

### 2. PLT (Procedure Linkage Table) Hooking
Using PerformanC's lightweight **PLTI** library, AuditPatch patches internal function calls responsible for assembling and dispatching audit log lines:
- Scans outbound log records for sensitive domains and known root process signatures.
- Modifies context descriptors in place to match standard, benign Android system services.
- Eliminates log traces that would otherwise confirm the presence of Magisk, KernelSU, or custom SELinux policy rules.

## Installation & Deployment

1. Download the `AuditPatch` release `.zip` from GitHub.
2. Install the archive in **Magisk**, **KernelSU**, or **APatch**.
3. Reboot your device to allow `post-fs-data` injection into `logd`.
4. Monitor system audit logs via terminal to verify redaction:
   ```bash
   su -c logcat -d -b events -s auditd
   ```

## Compatibility & Constraints

- Operates independently of Zygisk; does not conflict with active Zygisk injection engines.
- Compatible across Android 10 through Android 15+ on 64-bit ARM architectures.
