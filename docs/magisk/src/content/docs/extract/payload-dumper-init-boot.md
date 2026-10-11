---
title: "payload-dumper-go: Extract init_boot.img"
description: "How to extract init_boot.img from official Android firmware payload.bin using payload-dumper-go."
---

:::note[Supported Devices]
For devices launching with Android 13+ (Linux kernel 5.15+), the ramdisk is in `init_boot.img` rather than `boot.img`.
:::

## Steps

### 1. Download Firmware & Unpack payload.bin
Download your device's exact firmware package and unpack `payload.bin`.

![Firmware payload.bin file](/images/321c3cf486ed509.png)
*Firmware payload.bin file*


### 2. Download payload-dumper-go
Download `payload-dumper-go` from official [payload-dumper-go GitHub Releases](https://github.com/ssut/payload-dumper-go/releases) and extract it using [7-Zip](https://www.7-zip.org/).

![Extracting payload-dumper-go](/images/2efa273a75fd6b7.jpg)
*Extracting payload-dumper-go*


### 3. Copy payload.bin into Tool Directory
Place `payload.bin` directly inside the `payload-dumper-go` folder.

![Copying payload.bin to tool folder](/images/35beee9e1b2e940.jpg)
*Copying payload.bin to tool folder*


### 4. Run Extraction for init_boot
1. Open a command terminal in the folder (or double-click `打开CMD命令行.bat`).
2. Enter `i` (or run `payload-dumper-go -p init_boot payload.bin`).
3. Press Enter to extract `init_boot.img`.

![Extracting init_boot partition in terminal](/images/a7f97dc973de186.jpg)
*Extracting init_boot partition in terminal*


### 5. Locate Extracted File
Open the `img` folder to find your freshly extracted `init_boot.img`, ready for Magisk patching.

![Extracted init_boot.img file](/images/29273620873e738.jpg)
*Extracted init_boot.img file*

---

## Next Steps

Now that you have extracted `init_boot.img`, copy it to your phone and follow the init_boot installation guide for your device:
- [Xiaomi / Redmi / HyperOS](/magisk/install/xiaomi-init-boot)
- [Google Pixel 7, 8, 9+](/magisk/install/pixel-init-boot)
- [OnePlus OxygenOS 13+](/magisk/install/oneplus-init-boot)
- [Realme UI 4+ / Android 13+](/magisk/install/realme-init-boot)
- [Motorola Android 13+](/magisk/install/motorola-init-boot)
