---
id: "zapret-pocket"
title: "zapret Pocket: Standalone DPI Censorship Circumvention Engine"
sidebarTitle: "zapret Pocket"
description: "Rooted Android port of bolvan's zapret DPI bypass utility by sevcator, enabling packet desynchronization, SNI splitting, and fake TLS ClientHellos without external VPN tunnels."
category: "networking-proxies"
tier: 1
searchQueries:
  - "zapret pocket magisk"
  - "sevcator zapret-pocket"
  - "bypass dpi youtube discord android root"
  - "nfqws android magisk"
  - "zapret android config strategies"
prerequisites:
  - "Rooted Android device with Magisk, KernelSU, or APatch"
  - "Kernel support for `iptables` or `nftables` packet filtering and queueing (`nfqueue`)"
conflicts: []
configPaths:
  - "/data/adb/modules/zapret/"
  - "/data/adb/modules/zapret/zapret/"
features:
  - "Multi-strategy DPI evasion: implements TCP segment splitting, SNI fragmentation, fake TLS ClientHellos, bad checksums, and hop-limit TTL tricks"
  - "Zero external server necessity: modifies packet flows directly on-device without routing data through third-party proxy nodes or VPN servers"
  - "Vast preset library: features curated profiles optimized for regional telecom filters and specific platforms (YouTube, Discord voice, gaming)"
  - "Transparent operation: intercepts network traffic at the netfilter layer, keeping Android's system VPN slot free for other applications"
---

## Overview

zapret Pocket, ported and maintained by sevcator, brings the renowned `zapret` Deep Packet Inspection (DPI) circumvention software to rooted Android devices. In jurisdictions where internet service providers (ISPs) and state regulatory bodies employ middleboxes to throttle or block protocols (such as YouTube 4K streams, Discord voice gateways, and social networks), DPI engines inspect the initial TLS ClientHello and SNI (Server Name Indication) fields to drop or delay packets.

zapret Pocket circumvents these middleboxes without requiring a remote VPN or proxy server. Operating entirely on-device via `nfqws` (Netfilter Queue Web Surrogate) and kernel packet filtering, it desynchronizes packets—sending out-of-order segments, invalid checksums that the destination server drops while confusing the middlebox, and split TLS handshakes that prevent inspection appliances from recognizing prohibited domain names.

## Prerequisites & Compatibility

- **Root Environment**: Compatible with Magisk, KernelSU, and APatch.
- **Kernel Requirements**: Requires Linux kernel support for Netfilter packet queueing (`CONFIG_NETFILTER_NETLINK_QUEUE` / `iptables` `NFQUEUE`). Almost all modern Android stock and custom kernels support these standard networking features out of the box.

There are no documented module conflicts. However, running a system VPN app with a killswitch simultaneously will route traffic through that VPN tunnel before zapret can process outbound packets on raw interfaces.

## Packet Desynchronization Mechanics

zapret Pocket deploys `nfqws` alongside pre-configured desynchronization scripts:

- **Fake TLS ClientHello**: Precedes the genuine TLS handshake with a crafted fake TLS ClientHello packet. Middleboxes lock onto the dummy domain while the destination server rejects the fake packet and accepts the real connection.
- **SNI Splitting (`splitsniext`)**: Fragments the TLS ClientHello right at the Server Name Indication boundary across multiple TCP segments. Middleboxes looking for whole hostnames fail to assemble the stream.
- **TTL / Hop-Limit Tricks (`ttlpadencap`)**: Sets packet Time-To-Live parameters so that fake packets survive just long enough to fool the inspection middlebox, but expire before reaching the actual destination server.
- **QUIC / HTTP3 Handshake Manipulation**: Modifies UDP QUIC initial headers to unblock YouTube and modern browser connections using HTTP/3.

## Configuration & Usage

1. Download the latest `zapret` module zip from the project repository.
2. Install via Magisk, KernelSU, or APatch.
3. Reboot your device.
4. The module automatically selects a default general bypass strategy.
5. To test or switch strategies, explore the curated scripts in:
   ```bash
   /data/adb/modules/zapret/zapret/
   ```
   Presets include platform-tailored scripts like `discordfake.sh`, `discord_voice_badseq.sh`, `general_alt*.sh`, and regional ISP templates.
6. Execution state and binaries reside in:
   ```bash
   /data/adb/modules/zapret/
   ```

## Troubleshooting & Verification

- **DPI Still Blocks Connection**: DPI equipment configurations vary significantly across different ISPs and cellular carriers. If the default preset fails to unblock services, switch strategies by selecting an alternative configuration script (e.g. testing `fake-i.sh`, `splitsniext.sh`, or `faketlsalt_*.sh`) inside the module directory.
- **DNS Blocking**: zapret desynchronizes TCP and UDP data streams, but does not circumvent DNS poisoning. Ensure you use an encrypted DNS provider (such as DNS-over-HTTPS or DNS-over-TLS) alongside zapret to prevent DNS-level redirection.
