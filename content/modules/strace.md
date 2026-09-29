---
id: "strace"
title: "Strace: System-Call Tracing on Rooted Android"
sidebarTitle: "Strace"
description: "Install the strace diagnostic utility systemlessly through Magisk."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "strace magisk android"
  - "evdenis strace module"
  - "system call tracing rooted android"
  - "strace v6.19 android"
prerequisites:
  - "A rooted Android device with Magisk"
  - "A shell or terminal with permission to execute the installed binary"
  - "One of the ARM64, ARM, x86_64, or x86 architectures supported by the release"
conflicts:
  - "No known module conflict is documented upstream; tracing still adds overhead to the traced process."
configPaths:
  - "/system/bin/strace"
features:
  - "Installs strace v6.19 through a systemless Magisk overlay"
  - "Includes binaries for ARM64, ARM, x86_64, and x86"
  - "Selects the device architecture during module installation"
faq:
  - question: "What does this module install?"
    answer: "The upstream release packages a statically linked, stripped strace v6.19 binary and places the matching architecture under /system/bin/strace through Magisk's systemless mount."
  - question: "Why did installation abort with an unsupported architecture?"
    answer: "The release contains ARM64, ARM, x86_64, and x86 directories only. Its installer aborts when Magisk reports an architecture without a matching binary."
  - question: "Does the module trace applications automatically?"
    answer: "No. It only installs the command. You choose the process and tracing options from a root-capable shell; tracing can produce substantial output and runtime overhead."
  - question: "How do I remove it?"
    answer: "Disable or remove Strace from Magisk's module manager, then reboot if Magisk requests it."
---

## Overview

Strace is a diagnostic utility that records the system calls and signals made by a process. The `evdenis/strace` project packages strace v6.19 as a Magisk module rather than modifying the read-only Android system partition.

The release ZIP includes separate precompiled binaries for `arm64`, `arm`, `x86_64`, and `x86`. Its `customize.sh` selects the directory reported by Magisk and aborts if no matching binary exists.

## Installation and verification

1. Download the current `strace-v2.zip` from the upstream release.
2. In Magisk, open **Modules**, choose **Install from storage**, and select the ZIP.
3. Reboot when Magisk requests it.
4. From a root-capable shell, verify the installed command:

   ```sh
   su -c 'command -v strace && strace -V'
   ```

The upstream module installs the command at `/system/bin/strace` using Magisk's systemless overlay. It does not claim KernelSU or APatch support, so this guide lists Magisk only.

## Using the tool safely

Trace a short-lived command first and redirect output to a writable location:

```sh
su -c 'strace -f -o /data/local/tmp/trace.log -- ls /data'
```

Tracing a long-running or noisy process can generate large logs and affect timing. Avoid treating a trace as proof that a process is safe or malicious; interpret calls in the context of the application and Android permissions.

## Limitations and recovery

The module is a binary packaging project, not a full Android tracing tutorial. The upstream README points to the strace project and an XDA discussion for broader usage. No Android-version matrix is asserted by the upstream module.

If the module causes a boot or manager problem, use Magisk's safe-mode recovery path or remove the module directory from a compatible recovery environment. The module itself only provides the executable and has no documented persistent service.

## Sources

- [Upstream README](https://github.com/evdenis/strace)
- [Upstream release](https://github.com/evdenis/strace/releases/tag/v2)
- [Upstream source](https://github.com/evdenis/strace)
