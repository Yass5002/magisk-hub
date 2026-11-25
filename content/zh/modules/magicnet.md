---
id: "magicnet"
title: "MagicNet：支持 TUN 与 eBPF 的 Root 级 Sing-Box 透明代理引擎"
sidebarTitle: "MagicNet"
description: "基于定制版 sing-box 分支的高性能透明代理引擎，通过 TUN 或 eBPF 路由 Android 设备流量，无需占用系统 VPN 槽位。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "MagicNet Magisk 模块下载"
  - "LIghtJUNction MagicNet sing-box"
  - "Android Root eBPF 透明代理"
  - "不占用 VPN 槽位的 sing-box 代理"
  - "MagicNet CLI 命令行管理"
prerequisites:
  - "已获取 Root 权限的 Android 设备（运行 Magisk、KernelSU 或 APatch）"
  - "必须将 Android 的“私人 DNS”设为关闭（不可设为自动）"
  - "可用的代理订阅（HTTPS 链接、Clash YAML 或 sing-box JSON）"
conflicts: []
configPaths:
  - "/data/adb/modules/MagicNet/"
  - "/data/adb/modules/MagicNet/cli"
features:
  - "无 VPN 透明代理：通过定制版 sing-box 核心路由设备网络流量，不占用 Android 系统的 VpnService 槽位"
  - "双流量引擎：支持在 TUN 模式（`magicnet0`）与内核级 eBPF 数据包重定向之间显式切换，并具备失败自动回滚机制"
  - "通用订阅接入：支持最多 5 个订阅源同时生效，兼容远程 HTTPS 链接、Clash/Mihomo YAML、sing-box JSON 与 base64 字符串"
  - "分应用策略路由：将指定应用分配至代理、直连或绕过分组，并支持热点共享流量代理"
  - "丰富管理工具：提供功能完善的多语言 WebUI、全功能终端命令行工具（`cli`）以及经认证的 MCP 服务集成"
faq: []
---

## 概述

由 LIghtJUNction 开发的 **MagicNet** 是一套面向 Root Android 设备的强大透明代理与流量管理套件。MagicNet 构建于开源 `sing-box` 网络核心的定制分支之上，直接在 Linux 内核层面拦截并路由网络流量。

与需要占用 Android 唯一系统 VPN 槽位（导致无法同时运行本地去广告工具、WireGuard 或企业 VPN 客户端）的用户态 VPN 应用不同，MagicNet 在后台无感运行。它借助虚拟 TUN 接口或 Linux 扩展伯克利数据包过滤器（eBPF）透明捕获并转发数据包，将系统 VPN 槽位完全留给其他应用使用。

## 前置要求与关键设置规范

1. **Root 管理器**：兼容 Magisk、KernelSU 与 APatch。
2. **强制系统设置**：前往 **设置 > 网络和互联网 > 私人 DNS**，将其设为**关闭**。若保留“自动”模式，Android 的 DNS 解析器会尝试绕过本地透明代理端口，从而导致 DNS 泄露与路由黑洞。
3. **代理节点资源**：MagicNet 为代理客户端引擎，用户需自行准备合规可用的代理节点或订阅链接。

目前暂无已知的模块冲突记录。

## 技术架构：TUN 与 eBPF 模式对比

MagicNet 允许用户在两种路由机制之间按需切换：

- **TUN 模式（默认）**：创建名为 `magicnet0` 的虚拟网络适配器，通过策略路由将入站与出站数据包转发至 sing-box 核心。推荐在追求通用兼容性的各类设备与内核上使用。
- **eBPF 模式**：利用现代 Linux 内核的 eBPF cgroup 与流量控制（TC）过滤器，直接在 Socket 层拦截套接字连接。在兼容的内核上，eBPF 模式可减少数据包拷贝开销并降低功耗。若 eBPF 初始化失败，MagicNet 会自动回滚至 TUN 模式。

## 安装与配置

1. 从官方仓库下载最新发布包，并在 Root 管理器中刷入。
2. 确认 Android **私人 DNS 已关闭**。
3. 重启设备。
4. 在 Root 管理器界面打开 MagicNet WebUI（Magisk 用户可通过 WebUI X 或 MMRL 打开）。
5. 在 **Subscriptions**（订阅）标签页添加你的订阅链接，或导入本地 Clash/Mihomo YAML 配置文件。
6. 保存并启动服务。
7. 运行中的模块资源与二进制工具位于：
   ```bash
   /data/adb/modules/MagicNet/
   ```

## CLI 命令行管理与诊断

MagicNet 提供了可通过 `su` 调用的完善命令行工具：

- **检查服务健康状态与网络接口**：
  ```bash
  su -c /data/adb/modules/MagicNet/cli health
  ```
- **查看透明代理运行状态**：
  ```bash
  su -c /data/adb/modules/MagicNet/cli transparent status
  ```
- **无头模式快速初始化配置**：
  ```bash
  su -c '/data/adb/modules/MagicNet/cli setup "https://your-subscription-url"'
  ```
- **更新订阅与内核**：
  ```bash
  su -c /data/adb/modules/MagicNet/cli sub update sing-box
  ```

## 故障排查与验证

- **开启后无法访问互联网**：
  - 确认 Android 设置中的 **私人 DNS** 已设为**关闭**。
  - 执行健康检查命令：`su -c /data/adb/modules/MagicNet/cli health`。若 sing-box 启动失败，请检查订阅文件中是否包含有效的节点配置。
- **热点共享设备未走代理**：在 WebUI 的热点设置中开启下游代理共享，使连接的笔记本电脑或备用手机流量能够通过 MagicNet 的当前代理规则转发。
