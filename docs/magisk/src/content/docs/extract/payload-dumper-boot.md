---
title: "payload-dumper-go: Extract boot.img"
description: "How to extract boot.img from official Android firmware payload.bin using payload-dumper-go."
---

:::note[Supported Devices]
Works for all ROMs containing a `payload.bin` file, including Xiaomi, Redmi, OnePlus, Realme, and Google Pixel.
:::

## Steps

### 1. Download Official Firmware
Download the official firmware package that matches your phone\'s **exact current build version** (e.g. from [Xiaomi ROMs](/magisk/extract/download-xiaomi-rom), [Google Pixel Factory Images](https://developers.google.com/android/images), or your manufacturer\'s firmware repository).
*(Alternatively, extract directly from URL without downloading the full archive using [Payload-Dumper-Compose](/magisk/extract/payload-dumper-compose)).*

Extract the downloaded ROM archive using [7-Zip](https://www.7-zip.org/). You only need the `payload.bin` file.

### 2. Download payload-dumper-go
Download the extraction tool from official [payload-dumper-go GitHub Releases](https://github.com/ssut/payload-dumper-go/releases).
Extract the downloaded archive using [7-Zip](https://www.7-zip.org/) to a folder on your PC.

![Extracting payload-dumper-go](/images/2efa273a75fd6b7.jpg)
*Extracting payload-dumper-go*


### 3. Move payload.bin to Tool Folder
Copy your extracted `payload.bin` file into the `payload-dumper-go` folder.

![Placing payload.bin in the extraction folder](/images/35beee9e1b2e940.jpg)
*Placing payload.bin in the extraction folder*


### 4. Run Extraction
1. Open a command terminal in the folder (or double-click `打开CMD命令行.bat`).
2. Follow the prompt and enter `b` (or run `payload-dumper-go -p boot payload.bin`).
3. Press Enter to extract `boot.img`.

![Extracting boot partition in terminal](/images/1bc49334127f327.jpg)
*Extracting boot partition in terminal*


### 5. Access Extracted Image
Open the newly created `extracted_...` or `img` folder. You will find your extracted `boot.img` ready to be patched by Magisk!

![Extracted boot.img file](/images/c3362e52caa3aab.jpg)
*Extracted boot.img file*

---

## Next Steps

Now that you have extracted `boot.img`, copy it to your phone and follow the installation guide for your device:
- [Xiaomi / Redmi / POCO](/magisk/install/xiaomi-boot)
- [Google Pixel](/magisk/install/pixel-boot)
- [OnePlus](/magisk/install/oneplus-boot)
- [Realme](/magisk/install/realme-boot)
- [Motorola](/magisk/install/motorola-boot)
