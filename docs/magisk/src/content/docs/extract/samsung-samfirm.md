---
title: "SamFirm (Samsung Firmware Download Tool)"
description: "Download official Samsung firmware directly from Samsung FUS servers using SamFirm."
---

:::note[Requirements]
Requires **.NET Framework 3.5** and **Microsoft Visual C++ Redistributable** installed on Windows.
:::

## Steps

1. **Install Prerequisites:**
   - .NET Framework 3.5

![.NET Framework 3.5 installer](/images/73087fa5c3f51cf.png)
*.NET Framework 3.5 installer*

   - Microsoft Visual C++ Redistributable

![Visual C++ installer](/images/3fde8552ca73be1.jpg)
*Visual C++ installer*

2. **Download SamFirm:** Extract `SamFirm.zip` on your PC.

![SamFirm tool archive](/images/1c7403ae03c5d2e.png)
*SamFirm tool archive*

3. Launch `SamFirm.exe`.

![SamFirm interface](/images/feeca8549d1a687.jpg)
*SamFirm interface*

4. Enter:
   - **Model:** Device model code (e.g. `SM-G9750`)
   - **Region:** CSC code (e.g. `CHC`)
5. Check **Auto** and **Decrypt automatically**.

![Checking update](/images/587b692da192589.png)
*Checking update*

6. Click **Check Update** -> **Download**.
7. When complete, extract the zip file to obtain the AP, BL, CP, and CSC files for Odin flashing.

![Firmware archive ready](/images/29d9cb08eb5792e.png)
*Firmware archive ready*

---

## Next Steps

Once your Samsung firmware finishes downloading:
- [Samsung boot.img Guide](/magisk/install/samsung-boot)
- [Samsung init_boot Guide](/magisk/install/samsung-init-boot)
