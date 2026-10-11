---
title: "Xiaomi / Redmi Unlock Bootloader"
description: "Official tutorial for unlocking Bootloader on Xiaomi, Redmi, MIUI, and HyperOS devices."
---

:::caution[Critical Notice]
- Unlocking the Bootloader will **wipe all phone data**. Back up all critical personal data before proceeding!
- Universal guide for Xiaomi, Redmi, HyperOS, and MIUI.
:::

## Unlock Steps

### 1. Enable Developer Options
Go to **Settings – My Device – All Specs**, and continuously tap **OS Version** (or **MIUI Version**) until it says "You are now a developer!".

![Enabling Developer Options](/images/1b6949f5780c2dc.jpg)
*Enabling Developer Options*


### 2. Developer Options
Go to **Settings – Additional Settings – Developer Options**.

![Developer Options](/images/4e11161b68c8bef.jpg)
*Developer Options*


### 3. Bind Account and Device
1. In Developer Options, tap **Mi Unlock Status** (Device unlock status).
2. Tap **Add account and device**. *(Ensure your SIM card is inserted with active cellular mobile data).*

![Binding account in Mi Unlock Status](/images/17215f175694cbb.png)
*Binding account in Mi Unlock Status*


### 4. Download Official Mi Unlock Tool on PC
Download the official tool from the [Official Xiaomi Mi Unlock Portal](https://en.miui.com/unlock/download_en.html) (or [Mi Community Archive](https://miuirom.org/updates/mi-flash-unlock)).
Extract the archive with [7-Zip](https://www.7-zip.org/), open the folder, and run `MiUsbDriver.exe` to install drivers.

![Extracting Mi Unlock tool](/images/c2208be4a44763d.png)
*Extracting Mi Unlock tool*


### 5. Sign In to Mi Unlock
Open `miflash_unlock.exe`, and log in with the **same Xiaomi Account** bound to your phone in Step 3.

![Signing in to Mi Unlock on PC](/images/499345506fcab05.png)
*Signing in to Mi Unlock on PC*


### 6. Enter Fastboot Mode
Power off phone, hold **Power + Volume Down** simultaneously until the Fastboot logo appears, then connect to PC via USB.

![Xiaomi Fastboot mode](/images/5617427dce0c230.png)
*Xiaomi Fastboot mode*


### 7. Perform Unlock
In the Mi Unlock software, click **Unlock**. A warning will confirm data wipe. Confirm to proceed.

![Clicking Unlock in Mi Unlock](/images/246d22c17e1df4a.jpg)
*Clicking Unlock in Mi Unlock*


### 8. Unlock Complete
Once the tool reports **Unlocked successfully**, the phone will reboot automatically.

![Unlocked successfully](/images/4cea67955004d45.png)
*Unlocked successfully*


---

## Frequently Asked Questions

<details>
<summary>Q: Tool prompts "Account and device bound mismatch"?</summary>

**A:** The account logged into the PC tool does not match the account bound on the phone. Make sure both use the exact same Mi Account ID and mobile number.
</details>

<details>
<summary>Q: Tool prompts "Please unlock after 168 hours"?</summary>

**A:** Xiaomi imposes a standard security waiting period (usually 168 hours / 7 days). Keep your SIM card in the phone, do not unbind or log out of the account, and run the unlock tool again once the timer expires.
</details>

---

## Next Steps

Now that your bootloader is unlocked, proceed to install Magisk:
- For devices on Android 12 or earlier: [Xiaomi boot.img Guide](/magisk/install/xiaomi-boot)
- For devices on HyperOS / Android 13+: [Xiaomi init_boot Guide](/magisk/install/xiaomi-init-boot)
