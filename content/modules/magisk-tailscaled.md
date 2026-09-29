---
id: "magisk-tailscaled"
title: "Magisk Tailscaled: Tailscale Userspace Networking on Rooted Android"
sidebarTitle: "Magisk Tailscaled"
description: "Run Tailscale's daemon on rooted Android through a Magisk or KernelSU module using userspace networking."
category: "networking-proxies"
tier: 1
searchQueries:
  - "magisk tailscaled android"
  - "anasfanani magisk tailscaled"
  - "tailscale userspace networking root android"
  - "tailscale alongside android vpn"
  - "tailscaled magisk kernelSU"
prerequisites:
  - "Rooted Android device with Magisk or KernelSU"
  - "ARM or ARM64 architecture for the documented installation path"
  - "Terminal access for the initial Tailscale login"
  - "Network access during installation when the package needs to fetch matching dependencies"
conflicts:
  - "Network configurations or VPNs that conflict with the module's userspace tunnel and routing scripts"
configPaths:
  - "/data/adb/tailscale/"
  - "/data/adb/tailscale/tmp/tailscaled.state"
  - "/data/adb/tailscale/run/tailscaled.log"
  - "/data/adb/tailscale/scripts/"
features:
  - "Runs tailscaled automatically after boot through the module service"
  - "Uses Tailscale userspace networking rather than a kernel TUN interface"
  - "Provides tailscale, tailscaled, tailscaled.service, and tailscaled.tun commands"
  - "Can coexist with an Android VPN according to the upstream project documentation"
  - "Includes a SOCKS5-tunnel-based workaround for reaching tailnet devices"
faq:
  - question: "Does this module provide the same networking mode as the official Linux Tailscale client?"
    answer: "No. The upstream documentation says this module runs tailscaled with -tun=userspace-networking. Its tailscale0 interface and routing behavior therefore differ from the normal Linux TUN setup."
  - question: "Why can I not reach another tailnet device directly?"
    answer: "The upstream troubleshooting notes require tailscaled.service and tailscaled.tun to be running and use a local SOCKS5 proxy on port 1099. Check the module log at /data/adb/tailscale/run/tailscaled.log and test connectivity with tailscale ping and the documented curl proxy checks."
  - question: "Does the module support MagicDNS and subnet routes?"
    answer: "The upstream README states that MagicDNS is currently not working. Subnet routes require manually defining routes in tailscaled.tun.up and tailscaled.tun.down, so they are not plug-and-play."
  - question: "Why did installation fail outside a root manager?"
    answer: "The release installer explicitly requires Magisk Manager or KernelSU Manager and aborts when BOOTMODE is not enabled. Recovery installation is not supported by the installer."
---

## Overview

**Magisk Tailscaled** packages Tailscale for rooted Android devices. The upstream README describes it as a third-party module that starts `tailscaled` after boot and lets a rooted Android device join a Tailscale network.

This is not the official Tailscale Android application. The project specifically documents userspace networking and says the module can be used alongside an Android VPN. Network behavior remains dependent on the device ROM, root manager, and local routing configuration.

## Compatibility and limitations

The upstream documentation lists Magisk as a requirement and confirms KernelSU support. The installer handles `arm` and `arm64`; other architectures are rejected by the installer unless a user supplies compatible binaries manually.

The documented limitations are important:

- The daemon runs with `-tun=userspace-networking`.
- MagicDNS is documented as not working.
- Subnet routes require manual iptables/routing edits in the tunnel scripts.
- Some Tailscale features may not work correctly in the Android/Linux environment.
- The module is not affiliated with the official Tailscale project.

No Android version range is asserted here because the upstream documentation does not provide one.

## Installation

1. Download the current ZIP from the upstream release page.
2. Flash it through Magisk Manager or KernelSU Manager.
3. Reboot the device.
4. Open a root terminal and authenticate:

   ```sh
   su -c tailscale login
   ```

5. Open the authorization URL shown by Tailscale.
6. If Android DNS handling interferes with the setup, the upstream quick start suggests:

   ```sh
   su -c tailscale set --accept-dns=false
   ```

The installer selects `arm` or `arm64` content. If the release package does not already contain the required binaries, its installer downloads matching Tailscale and `jq` dependencies from the upstream projects, so installation needs network access.

## Runtime layout and commands

The module stores its working data below `/data/adb/tailscale/`. The state file is documented at:

```text
/data/adb/tailscale/tmp/tailscaled.state
```

Logs are written to:

```text
/data/adb/tailscale/run/tailscaled.log
```

The release provides these command roles:

- `tailscale`: the main client CLI
- `tailscaled`: the daemon
- `tailscaled.service`: start, stop, restart, and inspect the daemon
- `tailscaled.tun`: manage the userspace tunnel helper

Check the node address with:

```sh
su -c tailscale ip
```

Check daemon state with:

```sh
su -c tailscaled.service status
```

## Troubleshooting

If the device cannot reach another tailnet node:

1. Confirm both services are running:

   ```sh
   su -c tailscaled.service status
   su -c tailscaled.tun status
   ```

2. Test the Tailscale path:

   ```sh
   su -c "tailscale ping YOUR_TAILNET_IP"
   ```

3. Inspect `/data/adb/tailscale/run/tailscaled.log`.
4. Test the documented local SOCKS5 proxy on port `1099` before changing routing rules.

For subnet routes, review the upstream `tailscaled.tun.up` and `tailscaled.tun.down` scripts and add only routes appropriate for the local network. Do not assume that a route working on one ROM or interface will work on another.

## Sources

- [Upstream README](https://github.com/anasfanani/Magisk-Tailscaled)
- [Upstream releases](https://github.com/anasfanani/Magisk-Tailscaled/releases)
- [Upstream source](https://github.com/anasfanani/Magisk-Tailscaled)
