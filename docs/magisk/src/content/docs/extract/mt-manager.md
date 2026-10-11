---
title: "MT Manager: Unpack payload.bin & Extract boot.img"
description: "How to extract boot.img directly on Android using MT Manager without a PC."
---

:::note[Standalone Android Extraction]
If you do not have a computer readily available, you can extract `boot.img` directly on your phone using the popular file manager **MT Manager**.
:::


![MT Manager Payload Extraction Interface](/images/0bb07d8cb009e35.jpg)
*MT Manager Payload Extraction Interface*


## Steps

1. **Download Full Recovery ROM:** Download the recovery zip package onto your phone storage.
2. **Install MT Manager:** Install MT Manager APK.
3. **Open System Archive:** Navigate to the ROM zip file and tap on it to view contents.
4. **Open payload.bin:** Tap on `payload.bin`. MT Manager has built-in payload parser support.
5. **Extract boot.img:** Long-press `boot.img` (or `init_boot.img`), select **Extract**, and confirm.
6. The partition image is now extracted to your local phone storage and ready for Magisk to patch!
