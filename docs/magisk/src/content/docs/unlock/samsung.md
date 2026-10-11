---
title: "Samsung Unlock Bootloader"
description: "Official tutorial for unlocking Bootloader on Samsung Galaxy devices."
---

:::caution[Notice]
- Applicable only to **Exynos and non-carrier-locked Snapdragon** models (US/Canada carrier versions like AT&T, Verizon cannot be bootloader-unlocked).
- Unlocking Knox will permanently trip Knox to 0x1, which disables Samsung Knox features (Samsung Pay, Secure Folder).
:::

## Unlock Steps

### 1. Enable OEM Unlocking
1. Go to **Settings – About Phone – Software Information**, and tap **Build Number** 7 times.
2. Go to **Settings – Developer Options**.
3. Toggle on **OEM Unlocking**. *(If OEM Unlocking is missing, connect to Wi-Fi and wait for system date sync).*

### 2. Boot into Download Mode (Device Unlock Mode)
1. Power off the phone completely.
2. Unplug USB cable from PC.
3. Press and hold **Volume Up + Volume Down** simultaneously, then insert the USB cable connected to PC.
4. The teal/blue Warning screen appears.

### 3. Unlock Bootloader
1. Long-press **Volume Up** for several seconds to enter **Device Unlock Mode**.
2. Press **Volume Up** once more to confirm: "Unlock bootloader? (This will wipe all data)".
3. The phone will format internal storage and reboot automatically.

---

## Next Steps

Now that your Samsung device is unlocked, install Magisk:
- For Samsung models on Android 12 or earlier: [Samsung boot.img Guide](/magisk/install/samsung-boot)
- For Samsung models on One UI 5 / 6+ (Android 13+): [Samsung init_boot Guide](/magisk/install/samsung-init-boot)
