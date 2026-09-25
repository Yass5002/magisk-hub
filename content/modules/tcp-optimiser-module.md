---
id: "tcp-optimiser-module"
title: "TCP Optimiser Module: Dynamic Network Congestion & Queuing Manager"
sidebarTitle: "TCP Optimiser"
description: "Network optimization module by fatalcoder524 that dynamically switches TCP congestion algorithms (BBR, Cubic) and queuing disciplines based on active Wi-Fi and Cellular interfaces."
category: "networking-proxies"
tier: 1
searchQueries:
  - "tcp optimiser module magisk"
  - "fatalcoder524 tcp_optimiser_module"
  - "switch bbr wifi cubic cellular android"
  - "android tcp congestion algorithm webui"
  - "initcwnd initrwnd magisk module"
prerequisites:
  - "Rooted Android device running Magisk, KernelSU, or APatch"
  - "Kernel supporting targeted TCP algorithms (e.g. BBR compiled in kernel config)"
conflicts: []
configPaths:
  - "/data/adb/modules/tcp_optimiser/"
  - "/data/adb/modules/tcp_optimiser/service.log"
features:
  - "Interface-aware congestion switching: automatically applies optimized algorithms when switching between Wi-Fi (`wlan0`) and mobile data (`rmnet_data0`)"
  - "BBR on Wi-Fi, Cubic on Cellular: maximizes unthrottled throughput over Wi-Fi using BBR while preventing packet drop penalties on cellular links"
  - "Configurable queuing disciplines (qdisc): enables per-interface configuration of `fq`, `fq_codel`, or `pfifo_fast` packet schedulers"
  - "TCP window maximization: optional configuration to maximize initial congestion (`initcwnd`) and receive (`initrwnd`) window sizes"
  - "Dual interface control: manage settings using simple filesystem naming conventions or an interactive module WebUI"
---

## Overview

TCP Optimiser Module, developed by fatalcoder524, optimizes Android networking by dynamically switching TCP congestion control algorithms and queuing disciplines (qdisc) according to the device's currently active network interface.

Modern mobile kernels often include Google's BBR (Bottleneck Bandwidth and RTT) algorithm. While BBR delivers massive throughput gains (often 50–60 Mbps higher upload speeds) over stable Wi-Fi connections compared to traditional Cubic, BBR can struggle on cellular networks where radio signal fluctuations and transient packet drops cause unexpected latency penalties. TCP Optimiser solves this by monitoring network interface transitions, automatically applying BBR to Wi-Fi and Cubic to mobile data.

## Prerequisites & Compatibility

- **Root Solution**: Compatible with Magisk, KernelSU, and APatch.
- **Kernel Requirements**: The device kernel must have the desired TCP congestion algorithms compiled in (`CONFIG_TCP_CONG_BBR`, `CONFIG_TCP_CONG_CUBIC`, etc.). If an algorithm is not compiled in your kernel, the module falls back gracefully to system defaults.

There are no documented module conflicts.

## Configuration & Tuning

TCP Optimiser can be controlled via its dedicated WebUI or directly via file descriptors in:
```bash
/data/adb/modules/tcp_optimiser/
```

### Tuning via File Descriptors

The module generates two interface template files in its directory:
- `wlan_{algo}_{qdisc}`: Governs Wi-Fi interfaces.
- `rmnet_data_{algo}_{qdisc}`: Governs cellular interfaces.

To modify the active configuration:
1. **Change Algorithm**: Rename the `{algo}` section (e.g., change `wlan_cubic_fq` to `wlan_bbr_fq`). Supported values include `bbr`, `cubic`, `westwood`, `reno`, and any algorithm listed in `/proc/sys/net/ipv4/tcp_available_congestion_control`.
2. **Change Queuing Discipline**: Rename the `{qdisc}` section to your preferred packet queue (e.g., `fq`, `fq_codel`, `pfifo_fast`).
3. **Maximize Initial Windows**: Create an empty file named `initcwnd_initrwnd` in the module directory to set initial congestion and receive windows to maximum values.
4. **Immediate Application**: Create an empty file named `force_apply` to apply adjustments immediately without a reboot.
5. **Connection Reset (Caution)**: Create an empty file named `kill_connections` if you want existing TCP sockets terminated during interface handover. (Disabled by default to avoid interrupting background downloads).

### Tuning via WebUI

For a graphical experience:
- Open the WebUI via KernelSU or APatch manager, or using KSUWebUIStandalone on Magisk.
- Adjust sliders and dropdown menus for cellular and Wi-Fi profiles.

## Troubleshooting & Verification

- **Verify Active Algorithm**: Check which algorithm is currently active for your network:
  ```bash
  su -c sysctl net.ipv4.tcp_congestion_control
  ```
- **Inspect Module Execution Logs**:
  ```bash
  cat /data/adb/modules/tcp_optimiser/service.log
  ```
- **Requested Algorithm Not Applying**: If an algorithm fails to engage, inspect `/proc/sys/net/ipv4/tcp_available_congestion_control` to verify whether your current kernel actually compiled that specific module.
