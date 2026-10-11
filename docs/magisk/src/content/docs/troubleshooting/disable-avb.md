---
title: "Disable Android Verified Boot (AVB)"
description: "How to disable AVB (Android Verified Boot) signature verification using vbmeta.img."
---

:::note[Note]
Modern official Magisk releases patch vbmeta headers automatically for most MediaTek and Qualcomm devices. Disabling AVB manually is only required if your device specifically bootloops on custom partitions or dm-verity checks.
:::

## Steps

### 1. Extract `vbmeta.img`
Extract `vbmeta.img` from your device's official firmware package, and copy it into your PC's `platform-tools` directory.

### 2. Flash with Verification Disabled Flags
Put your phone into Fastboot mode, open command prompt, and run:

```bash
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
```

### 3. Verification Complete
The terminal will output `OKAY`, confirming AVB and dm-verity have been disabled.

### How to Restore
If you ever need to restore original AVB verification, flash stock `vbmeta.img` without the flags:

```bash
fastboot flash vbmeta vbmeta.img
```
