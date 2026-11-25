---
id: "magisk-tailscaled"
title: "Magisk Tailscaled：在 Root Android 上运行 Tailscale 用户态组网"
sidebarTitle: "Magisk Tailscaled"
description: "通过 Magisk 或 KernelSU 模块在已 Root 的 Android 设备上以用户态网络模式运行 Tailscale 守护进程。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "Magisk Tailscaled Android 下载"
  - "anasfanani Magisk-Tailscaled"
  - "Android Root Tailscale 用户态组网"
  - "Tailscale 与 Android VPN 共存"
  - "tailscaled Magisk KernelSU 模块"
prerequisites:
  - "搭载 Magisk 或 KernelSU 的已 Root Android 设备"
  - "按文档安装流程需具备 ARM 或 ARM64 架构"
  - "用于首次登录 Tailscale 的终端访问权限"
  - "当安装包需要拉取匹配依赖时，安装过程需保持网络连接"
conflicts:
  - "与本模块的用户态隧道及路由脚本存在冲突的网络配置或 VPN"
configPaths:
  - "/data/adb/tailscale/"
  - "/data/adb/tailscale/tmp/tailscaled.state"
  - "/data/adb/tailscale/run/tailscaled.log"
  - "/data/adb/tailscale/scripts/"
features:
  - "通过模块服务在设备开机后自动启动 `tailscaled`"
  - "采用 Tailscale 用户态网络模式（userspace networking），而非内核 TUN 接口"
  - "提供 `tailscale`、`tailscaled`、`tailscaled.service` 与 `tailscaled.tun` 命令"
  - "根据上游项目文档说明，可与 Android 系统 VPN 共存使用"
  - "内置基于 SOCKS5 隧道的变通方案，用于访问 tailnet 内的其他设备"
faq:
  - question: "该模块提供的网络模式与官方 Linux 版 Tailscale 客户端相同吗？"
    answer: "不同。上游文档明确指出本模块使用 `-tun=userspace-networking` 参数启动 `tailscaled`，因此其 `tailscale0` 接口和路由行为与常规 Linux TUN 模式存在差异。"
  - question: "为什么无法直接连通 tailnet 内的其他设备？"
    answer: "上游排查说明要求 `tailscaled.service` 和 `tailscaled.tun` 均处于运行状态，并使用监听在 `1099` 端口的本地 SOCKS5 代理。请检查 `/data/adb/tailscale/run/tailscaled.log` 模块日志，并使用 `tailscale ping` 及文档提供的 `curl` 代理测试连通性。"
  - question: "该模块是否支持 MagicDNS 和子网路由（Subnet Routes）？"
    answer: "上游 README 明确表示 MagicDNS 目前无法正常工作。子网路由则需要在 `tailscaled.tun.up` 与 `tailscaled.tun.down` 中手动定义路由规则，无法做到开箱即用。"
  - question: "为什么在 Root 管理器之外的环境中安装失败？"
    answer: "发布版的安装脚本明确要求在 Magisk Manager 或 KernelSU Manager 环境下运行，若未启用 `BOOTMODE` 会直接中止安装。该安装脚本不支持通过 Recovery 卡刷。"
---

## 概述

**Magisk Tailscaled** 将 Tailscale 打包为适用于已 Root Android 设备的模块。上游 README 将其描述为一个第三方模块，可在开机后启动 `tailscaled` 守护进程，从而让 Root Android 设备接入 Tailscale 虚拟组网。

请注意，它并非官方的 Tailscale Android 客户端应用。该项目明确采用了用户态网络模式，并说明该模块可与 Android 系统 VPN 同时使用。实际网络表现仍取决于设备的 ROM、Root 管理器以及本地路由配置。

## 兼容性与局限性

上游文档列明需使用 Magisk，并确认支持 KernelSU。安装脚本会自动识别 `arm` 与 `arm64` 架构；除非用户手动提供兼容的二进制文件，否则其他架构将被安装脚本拒绝。

以下文档记录的局限性尤为重要：

- 守护进程以 `-tun=userspace-networking` 参数运行。
- MagicDNS 在文档中标注为当前不可用。
- 子网路由需要在隧道脚本中手动编写 iptables/路由规则。
- 在 Android/Linux 混合环境下，部分 Tailscale 功能可能无法正常工作。
- 本模块与 Tailscale 官方项目无隶属关系。

由于上游文档未提供明确说明，此处不对 Android 系统版本范围作额外断言。

## 安装步骤

1. 从上游发布页下载最新的 ZIP 安装包。
2. 通过 Magisk Manager 或 KernelSU Manager 刷入模块。
3. 重启设备。
4. 打开 Root 终端并执行登录授权：

   ```sh
   su -c tailscale login
   ```

5. 在浏览器中打开 Tailscale 输出的授权链接完成认证。
6. 若 Android 的 DNS 处理机制干扰配置，上游快速入门建议执行：

   ```sh
   su -c tailscale set --accept-dns=false
   ```

安装脚本会自动选择 `arm` 或 `arm64` 组件。如果所下载的发布包未内置所需的二进制文件，安装器会从上游项目下载匹配的 Tailscale 与 `jq` 依赖，因此安装过程中需要保持网络连接。

## 运行目录布局与常用命令

模块将其工作数据存放在 `/data/adb/tailscale/` 目录下。状态文件路径如下：

```text
/data/adb/tailscale/tmp/tailscaled.state
```

运行日志写入路径：

```text
/data/adb/tailscale/run/tailscaled.log
```

发布版提供以下命令行工具：

- `tailscale`：主客户端 CLI 工具
- `tailscaled`：后台守护进程
- `tailscaled.service`：用于启动、停止、重启及检查守护进程状态
- `tailscaled.tun`：用于管理用户态隧道辅助脚本

查看本机节点分配的 IP 地址：

```sh
su -c tailscale ip
```

检查守护进程运行状态：

```sh
su -c tailscaled.service status
```

## 故障排查

若设备无法访问 tailnet 中的其他节点：

1. 确认两个核心服务均在运行：

   ```sh
   su -c tailscaled.service status
   su -c tailscaled.tun status
   ```

2. 测试 Tailscale 节点链路连通性：

   ```sh
   su -c "tailscale ping YOUR_TAILNET_IP"
   ```

3. 检查 `/data/adb/tailscale/run/tailscaled.log` 日志输出。
4. 在修改任何路由规则之前，先测试文档所述的 `1099` 端口本地 SOCKS5 代理是否畅通。

如需配置子网路由，请仔细查阅上游的 `tailscaled.tun.up` 与 `tailscaled.tun.down` 脚本，仅添加适用于当前本地网络的路由规则，切勿假设在某款 ROM 或网卡接口上生效的规则可以直接照搬到其他设备上。

## 参考来源

- [上游 README](https://github.com/anasfanani/Magisk-Tailscaled)
- [上游发布页 (Releases)](https://github.com/anasfanani/Magisk-Tailscaled/releases)
- [上游源码仓库](https://github.com/anasfanani/Magisk-Tailscaled)
