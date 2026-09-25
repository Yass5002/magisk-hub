---
id: "supl-replacer"
title: "SUPL Replacer: Secure A-GPS Privacy Protection via GrapheneOS Proxy"
sidebarTitle: "SUPL Replacer"
description: "Replaces default Google SUPL (Secure User-Plane Location) A-GPS servers in gps.conf with privacy-respecting GrapheneOS proxies to stop IMSI tracking."
category: "system-utilities"
tier: 1
searchQueries:
  - "supl replacer magisk"
  - "replace google supl server root"
  - "gps conf privacy grapheneos supl"
  - "prevent imsi leak agps android"
  - "private assisted gps android magisk"
prerequisites:
  - "Root access via Magisk"
conflicts: []
configPaths:
  - "/data/adb/modules/supl-replacer/"
features:
  - "A-GPS privacy enforcement: replaces hardcoded Google SUPL servers (supl.google.com) with privacy-respecting GrapheneOS SUPL proxies"
  - "IMSI leak prevention: prevents mobile carriers and Google from harvesting your unique SIM IMSI and cell tower identifiers during GPS fixes"
  - "Instant satellite lock: preserves fast Assisted GPS Time to First Fix (TTFF) ephemeris downloads"
  - "Dual partition overlay: systemlessly overrides both /system/etc/gps.conf and /vendor/etc/gps.conf"
  - "Universal chipset support: compatible with Qualcomm, MediaTek, and Samsung Exynos GNSS hardware stacks"
---

## Overview

When your smartphone acquires a satellite location fix, Android uses **Assisted GPS (A-GPS)** via the **Secure User-Plane Location (SUPL)** protocol to quickly download satellite orbital predictions (ephemeris data), reducing the Time to First Fix (TTFF) from minutes to mere seconds.

However, standard Android implementations default to `supl.google.com`. Every time an app requests a GPS fix, Android sends an unencrypted or minimally protected packet containing your SIM card's unique **IMSI** (International Mobile Subscriber Identity) alongside the cell tower IDs currently within range. This creates a persistent, unprompted location and identity telemetry leak directly to Google.

**supl-replacer** is a systemless privacy module that modifies `gps.conf` to redirect all SUPL requests to privacy-focused proxies hosted by the **GrapheneOS** project.

## How It Protects Your Privacy

1. **GrapheneOS Proxy Integration**: Replaces `SUPL_HOST=supl.google.com` with GrapheneOS's secure proxy server (`supl.grapheneos.org`).
2. **IMSI Stripping**: The GrapheneOS proxy strips out your SIM card's IMSI and local cell identifiers before relaying the ephemeris query upstream, returning fresh satellite almanac data without logging personal hardware identifiers.
3. **Preserved Fix Speeds**: You retain instantaneous, sub-second GPS locks in navigation applications (Google Maps, OsmAnd, Waze) without transmitting unneeded telemetry.

## Installation

1. Download the latest `supl-replacer-v*.zip` archive from GitHub releases.
2. Install the module in **Magisk Manager**.
3. Reboot your device.
4. Launch any GPS test application (such as GPSTest) to verify that A-GPS satellite fixes resolve promptly.
