---
title: "OnePlus In-Depth Test Unlock App"
description: "Download and usage instructions for the official OnePlus Deep Testing unlock application."
---

:::note[Application Overview]
Newer OnePlus devices running modern ColorOS / OxygenOS builds require applying for unlocking qualification through the official **In-Depth Testing (Deep Testing)** application before `fastboot flashing unlock` will be accepted.
:::

## Steps

1. **Download App:** Download the version of the In-Depth Test APK matching your device model and regional firmware build.

![OnePlus In-Depth Test App](/images/2652d98c5ebe964.jpg)
*OnePlus In-Depth Test App*

2. **Submit Application:** Open the app on your phone, tap **Apply for In-Depth Test**, agree to the disclaimer, and submit your request.
3. **Query Review Status:** The approval process typically takes between a few hours to several business days.
4. **Enter Fastboot:** Once approved, open the app, tap **Start In-Depth Test**, and the device will automatically reboot into Fastboot mode.
5. **Unlock:** Connect to PC and run:
   ```bash
   fastboot flashing unlock
   ```

---

## Next Steps

Once your application is approved and you run the unlock command:
- Install Magisk (boot.img): [OnePlus boot.img Guide](/magisk/install/oneplus-boot)
- Install Magisk (init_boot.img): [OnePlus init_boot Guide](/magisk/install/oneplus-init-boot)
