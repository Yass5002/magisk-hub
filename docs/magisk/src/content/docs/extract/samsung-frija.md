---
title: "Frija (Samsung Firmware Download Tool)"
description: "How to use Frija to download official high-speed Samsung Galaxy firmware."
---

:::note[Requirements]
Requires **.NET Core 3.1 Desktop Runtime** installed on Windows to run.
:::

## Steps

1. **Install Runtime:** Install [.NET Core 3.1 Desktop Runtime](https://dotnet.microsoft.com/download/dotnet/3.1/runtime) (required).

![Installing .NET Core Runtime](/images/8382be42efdcd41.png)
*Installing .NET Core Runtime*

2. **Download Frija:**
   - Official [GitHub Frija Releases](https://github.com/SlackingVeteran/frija/releases) (free, open source)

![Frija tool files](/images/a2e402940f28b20.jpg)
*Frija tool files*

3. Extract archive and launch `Frija.exe`.

![Frija user interface](/images/4ed787a46662d00.png)
*Frija user interface*

4. Fill in device parameters:
   - **Model:** Enter your phone model (e.g., `SM-S9280`, check in Settings – About Phone).
   - **CSC:** Enter region CSC (e.g., `CHC` for Open China, `TGY` for Hong Kong, `XAA` for USA unlocked).

![Entering model and CSC](/images/ac2f8c46f786f8e.png)
*Entering model and CSC*

5. Click **Check Update**.
6. When firmware information appears, click **Download**.

![Downloading firmware in Frija](/images/2ffe0d26ab37d3a.png)
*Downloading firmware in Frija*

7. Once downloaded, Frija automatically decrypts the package into the standard Samsung Odin 4-part / 5-part zip archive.

![Firmware decrypted and extracted](/images/59dfdc130dba74e.png)
*Firmware decrypted and extracted*

---

## Next Steps

Once the firmware package (`.zip`) finishes downloading:
1. Extract it using [7-Zip](https://www.7-zip.org/) to obtain `AP_...tar.md5`.
2. Open `AP` to extract `boot.img.lz4` or `init_boot.img.lz4`.
3. Follow the installation guide:
   - [Samsung boot.img Guide](/magisk/install/samsung-boot) (Android 12 and older)
   - [Samsung init_boot Guide](/magisk/install/samsung-init-boot) (Android 13+ / One UI 5+)
