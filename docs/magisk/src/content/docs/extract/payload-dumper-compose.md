---
title: "Payload-Dumper-Compose Tool"
description: "Web & Docker-based extraction tool to unpack partitions directly from official ROM URLs."
---

:::note[Feature Highlight]
Applicable to Xiaomi, Redmi, OnePlus, Realme, Google Pixel, or any firmware containing `payload.bin`. If you have the direct download URL of a ROM, this tool can stream and extract partitions without downloading the entire 6GB+ package!
:::


![Payload-Dumper-Compose User Interface](/images/7101d8f5f324faa.jpg)
*Payload-Dumper-Compose User Interface*


## Steps

1. **Install App / Service:**
   - Official repository: [GitHub ssut/payload-dumper-go](https://github.com/ssut/payload-dumper-go/releases)
2. **Copy ROM Link:** Copy the direct `.zip` download link of your device's exact firmware.
3. **Parse Link:** Paste the link into the URL field and click **Parse**.
4. **Download Target Partition:** Select `boot.img` or `init_boot.img` and download only the partition you need into your `Download` directory.
