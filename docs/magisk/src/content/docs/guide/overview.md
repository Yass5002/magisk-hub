---
title: "Universal Magisk Installation Guide"
description: "Brand-neutral step-by-step Magisk installation guide for Android devices with beginner tips and device-specific paths."
---

Welcome to the universal Magisk installation guide. Any Android device with an unlockable bootloader can be rooted with Magisk by following the universal workflow:

$$\text{Unlock Bootloader} \longrightarrow \text{Patch Partition Image} \longrightarrow \text{Flash Patched Image via Fastboot / Odin}$$

---

## Device Quick Selector

If you prefer a guide tailored specifically to your manufacturer, select your device brand below:

| Device Brand | Firmware / Android Version | Direct Installation Guide |
|---|---|---|
| **Xiaomi / Redmi / POCO** | Android 12 & earlier (`boot.img`) | [Xiaomi boot.img Guide](/magisk/install/xiaomi-boot) |
| **Xiaomi / Redmi / HyperOS** | Android 13+ (`init_boot.img`) | [Xiaomi init_boot Guide](/magisk/install/xiaomi-init-boot) |
| **Google Pixel** | Pixel 6 & earlier (`boot.img`) | [Pixel boot.img Guide](/magisk/install/pixel-boot) |
| **Google Pixel** | Pixel 7, 8, 9+ (`init_boot.img`) | [Pixel init_boot Guide](/magisk/install/pixel-init-boot) |
| **OnePlus** | Android 12 & earlier (`boot.img`) | [OnePlus boot.img Guide](/magisk/install/oneplus-boot) |
| **OnePlus** | OxygenOS 13+ (`init_boot.img`) | [OnePlus init_boot Guide](/magisk/install/oneplus-init-boot) |
| **Realme** | Realme UI 3 & earlier (`boot.img`) | [Realme boot.img Guide](/magisk/install/realme-boot) |
| **Realme** | Realme UI 4+ / Android 13+ (`init_boot.img`) | [Realme init_boot Guide](/magisk/install/realme-init-boot) |
| **Motorola** | Legacy models (`boot.img`) | [Motorola boot.img Guide](/magisk/install/motorola-boot) |
| **Motorola** | Android 13+ (`init_boot.img`) | [Motorola init_boot Guide](/magisk/install/motorola-init-boot) |
| **Samsung Galaxy** | Android 12 & earlier (`boot.img`) | [Samsung boot.img Guide](/magisk/install/samsung-boot) |
| **Samsung Galaxy** | One UI 5+, Android 13+ (`init_boot.img`) | [Samsung init_boot Guide](/magisk/install/samsung-init-boot) |
| **Non-Unlockable Devices** | Any Android device (Root without BL Unlock) | [LightSpeed VM Guide](/magisk/install/virtual-machine) |

---

## Which File Do You Need: `boot.img` or `init_boot.img`?

Starting with Android 13 (Linux Kernel 5.10+ GKI architecture), Google moved the boot ramdisk from `boot.img` into a dedicated `init_boot.img` partition.

To check which partition your device uses:
1. Open **Settings** on your phone.
2. Tap **About Phone** > **Android Version** (or **All Specs**).
3. Look at the **Kernel Version**:
   - **Kernel 5.10, 5.15, 6.1 or newer**: Your phone uses **`init_boot.img`**.
   - **Kernel 4.14, 4.19, or older**: Your phone uses **`boot.img`**.

---

## Universal Step-by-Step Installation

### Step 1: Unlock the Bootloader

:::caution[Important: Back Up Your Data First!]
Unlocking the bootloader **will perform a factory reset and erase all user data** on your device (photos, apps, messages, and settings). Always back up critical data to a computer or cloud storage before proceeding.
:::
Every manufacturer has a dedicated unlock workflow:
- **Xiaomi / Redmi / POCO**: Follow the [Xiaomi Bootloader Unlock Guide](/magisk/unlock/xiaomi).
- **Google Pixel**: Follow the [Google Pixel Bootloader Unlock Guide](/magisk/unlock/pixel).
- **OnePlus**: Follow the [OnePlus Snapdragon Unlock Guide](/magisk/unlock/oneplus-snapdragon) or [OnePlus MediaTek Unlock Guide](/magisk/unlock/oneplus-mediatek).
- **Realme**: Follow the [Realme Snapdragon Unlock Guide](/magisk/unlock/realme-snapdragon) or [Realme MediaTek Unlock Guide](/magisk/unlock/realme-mediatek).
- **Motorola**: Follow the [Motorola Bootloader Unlock Guide](/magisk/unlock/motorola).
- **Samsung**: Follow the [Samsung Bootloader Unlock Guide](/magisk/unlock/samsung).

*(If your carrier or regional device cannot unlock the bootloader, see the [LightSpeed Virtual Machine Guide](/magisk/install/virtual-machine) to run Magisk in a root environment without unlocking).*

---

### Step 2: Acquire Stock `boot.img` or `init_boot.img`

You must obtain the unmodified stock partition image matching your **exact current firmware build**:

- **Devices with `payload.bin` (Pixel, OnePlus, Xiaomi, Realme, Motorola)**:
  - Download official firmware for your phone.
  - Use [payload-dumper-go](/magisk/extract/payload-dumper-boot) to extract `boot.img` or [payload-dumper-go init_boot](/magisk/extract/payload-dumper-init-boot).
  - *Fast extraction without downloading the whole ROM*: Use [Payload-Dumper-Compose Tool](/magisk/extract/payload-dumper-compose).
- **Samsung Galaxy**:
  - Download official firmware using [Frija](/magisk/extract/samsung-frija) or [SamFirm](/magisk/extract/samsung-samfirm).
  - Extract the `AP_...tar.md5` package using [7-Zip](https://www.7-zip.org/) to retrieve `boot.img.lz4` or `init_boot.img.lz4`.
- **Xiaomi / Redmi**:
  - Download matching Recovery or Fastboot package from [Official & Community Archives](/magisk/extract/download-xiaomi-rom).

:::tip[Safety Net Recommendation]
Always keep an unmodified copy of your stock `boot.img` (or `init_boot.img`) on your computer. If anything goes wrong, you can flash it back in seconds to restore normal booting.
:::
---

### Step 3: Copy Partition Image to Your Phone

1. Connect your phone to your PC with a USB cable.
2. Select **File Transfer (MTP)** mode on your phone.
3. Copy the extracted `boot.img` or `init_boot.img` into your phone's **Download** folder.

---

### Step 4: Install the Magisk App

1. Download the latest official Magisk APK from [Official GitHub Releases](https://github.com/topjohnwu/Magisk/releases).
2. Install the APK on your device (allow installation from unknown sources if prompted).

---

### Step 5: Patch the Image in Magisk

1. Launch the **Magisk** app on your phone.
2. In the top Magisk card, tap **Install**.
3. Choose **Select and Patch a File**.
4. Browse to your `Download` folder and select your `boot.img` or `init_boot.img`.
5. Tap **LET'S GO**.
6. Magisk will unpack, patch, and repack the image. When complete, note the output filename (e.g., `magisk_patched-28100_xxxxx.img`) saved in your `Download` directory.

![Patching boot image in Magisk](/images/a1bd2ef6dbcc0ef.jpg)
*Patching partition image in Magisk*

---

### Step 6: Set Up Platform-Tools on Your PC

1. Download the official [Google Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools) for Windows, macOS, or Linux.
2. Extract the archive using [7-Zip](https://www.7-zip.org/) or your system file manager.

:::tip[Beginner Tip: Opening Terminal in Platform-Tools]
On Windows, open the extracted `platform-tools` folder in File Explorer, click directly on the address bar at the top, type `cmd`, and press **Enter**. This opens Command Prompt directly in the correct folder, preventing "command not found" errors.
:::
---

### Step 7: Transfer Patched Image to PC

1. Connect your phone to PC in **File Transfer** mode.
2. Copy `magisk_patched-xxxxx.img` from your phone's `Download` folder into the `platform-tools` folder on your PC.

![Copying patched image to PC](/images/bdb4e2a5c4bfb97.png)
*Patched image inside platform-tools folder*

---

### Step 8: Boot into Fastboot / Bootloader Mode

1. Power off your phone completely.
2. Hold down **Power + Volume Down** simultaneously until the Fastboot screen appears.
3. Connect your phone to the PC via USB.

![Fastboot screen](/images/5617427dce0c230.png)
*Fastboot / Bootloader mode*

---

### Step 9: Flash the Patched Image

In your terminal inside `platform-tools`, verify the connection first:

```bash
fastboot devices
```

If your device serial number appears, flash the patched image:

#### For devices using `boot.img`:
```bash
fastboot flash boot magisk_patched-xxxxx.img
```

#### For devices using `init_boot.img`:
```bash
fastboot flash init_boot magisk_patched-xxxxx.img
```

> **Note:** Replace `magisk_patched-xxxxx.img` with the actual filename generated by Magisk.

---

### Step 10: Reboot and Verify

Reboot your device:

```bash
fastboot reboot
```

![Fastboot flashing terminal output](/images/a39401275d1b300.png)
*Terminal output showing successful flash*

Once the phone boots, open the **Magisk** app. If the **Installed** section displays the Magisk version number, root is successfully activated!

![Magisk root verified](/images/33e75ff09dd601b.jpg)
*Magisk successfully installed*

---

## Safety Net & Troubleshooting

:::tip[How to Recover from a Bootloop]
If your device gets stuck on the boot logo or bootloops after flashing:
1. Put the phone back into Fastboot mode (**Power + Volume Down**).
2. Flash your unmodified stock backup image:
   ```bash
   fastboot flash boot boot.img
   # OR for init_boot devices:
   fastboot flash init_boot init_boot.img
   ```
3. Run `fastboot reboot`. Your phone will boot normally with no data loss.
:::

- **Hanging on "waiting for any device"**: See the [Fastboot Driver Troubleshooting Guide](/magisk/troubleshooting/waiting-for-device).
- **Samsung One UI 5 / 6 boot errors**: See the [Samsung Error -45 Fix](/magisk/troubleshooting/samsung-error-45).
- **Bootloop caused by AVB verification**: See [How to Disable AVB Verification](/magisk/troubleshooting/disable-avb).
- **Lock screen bug after unlocking on Android 15**: See [Android 15 Lock Screen Fix](/magisk/troubleshooting/android-15-lockscreen-bug).
