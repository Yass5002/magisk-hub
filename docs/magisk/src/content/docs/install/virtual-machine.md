---
title: "LightSpeed Virtual Machine Magisk Installation"
description: "Install Magisk and get root inside LightSpeed Virtual Machine on Android without unlocking Bootloader."
---

:::note[No Bootloader Unlock Required]
If your physical phone cannot unlock its Bootloader, you can run a virtual Android environment (VM) on your phone and install Magisk inside the VM to enjoy root permissions and modules.
:::

## Steps

### 1. Download & Install Android Virtual Machine
Download and install **LightSpeed Virtual Machine (GuangSu VM)** or an equivalent Android container (such as **VMOS**) on your Android device:
- **VMOS Official Website**: [VMOS](https://www.vmos.com/)
- **LightSpeed VM Official**: [GuangSu VM](https://www.gsxnj.cn/)

### 2. Create Android 10 Virtual Machine
Inside the app, create an **Android 10** virtual machine instance. *(Many modern Magisk modules do not support Android 7; Android 10 or newer is recommended).*

![Creating Android 10 VM in LightSpeed VM](/images/f897b91030ebee7.jpg)
*Creating Android 10 VM in LightSpeed VM*


### 3. Configure VM Settings
Open VM **Settings**:
1. Enable **Superuser (Root)**
2. Enable **Magisk Support**
3. Enable **Vulkan Rendering**
4. Restart the Virtual Machine.

![Enabling Superuser and Magisk support](/images/17d04c434eb6c85.jpg)
*Enabling Superuser and Magisk support*


### 4. Install Magisk App inside VM
Open the built-in browser inside the VM, download and install the latest Magisk Manager app: [Download Magisk](/magisk/guide/download).

![Downloading Magisk inside VM](/images/b8514cade8667c7.jpg)
*Downloading Magisk inside VM*


### 5. Direct Install Magisk
Open Magisk inside the VM:
1. Tap **Install**
2. Choose **Direct Install (Recommended)**
3. Tap **LET'S GO**
4. When finished, tap **Reboot** to restart the VM.

![Direct Install inside VM](/images/8a57862569185c4.jpg)
*Direct Install inside VM*


### 6. Disable Built-in Superuser
After rebooting:
1. Go to VM **Settings – Superuser Settings**
2. Turn off the VM's built-in **Superuser** toggle
3. Restart the VM.

![Disabling built-in Superuser to let Magisk manage root](/images/ac908c0db2c6025.jpg)
*Disabling built-in Superuser to let Magisk manage root*


Magisk installation inside LightSpeed VM is now complete! You can now install Zygisk, LSPosed, and modules inside the virtual environment.
