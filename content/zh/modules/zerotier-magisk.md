---
id: "zerotier-magisk"
title: "ZeroTier for Magisk：无侵入式 Mesh VPN 守护进程与控制端"
sidebarTitle: "ZeroTier for Magisk"
description: "由 eventlOwOp 开发的 Magisk 无侵入式 ZeroTier One 后台守护进程，无需占用 Android 系统 VPN 通道即可建立加密 P2P 虚拟局域网。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "zerotier Magisk 模块"
  - "eventlowop zerotier-magisk 下载"
  - "Android 不占 VPN 槽位 ZeroTier"
  - "自建 ZeroTier Planet Android Root"
  - "zerotier-one 安卓后台守护进程"
prerequisites:
  - "Android 9.0（API 28）及以上系统"
  - "ARMv7-A 或 ARMv8-A（AArch64）处理器架构"
  - "已通过 Magisk 获取 Root 权限的 Android 设备"
  - "安装配套的 Controller APK（用于图形界面管理）"
conflicts: []
configPaths:
  - "/data/adb/zerotier/"
  - "/data/adb/zerotier/home/planet"
  - "/data/adb/modules/zerotier-magisk/"
features:
  - "守护进程级组网：开机直接将原生 `zerotier-one` 二进制程序作为 Linux 系统守护进程拉起"
  - "不独占 VPN 通道：在不调用系统 `VpnService` 的前提下创建虚拟网卡，支持与常规 VPN 应用同时运行"
  - "自定义 Moon 与 Planet：通过替换本地 `planet` 定义文件轻松接入私有自建根服务器"
  - "免 Root 权限控制端：通过无特权的配套应用即可输入 16 位 Network ID 并实时查看连接状态"
faq: []
---

## 概述

由 eventlOwOp 开发的 ZeroTier for Magisk 将企业级点对点（P2P）Mesh 组网守护进程 `zerotier-one` 直接移植到了已 Root 的 Android 设备。普通用户态的 Android ZeroTier 客户端依赖系统的 `VpnService` API，这会导致 Android 将 ZeroTier 视为常规 VPN，从而独占系统唯一可用的 VPN 卡槽，使用户无法同时运行隐私 VPN、WireGuard 或基于本地 VPN 的 DNS 去广告工具。

该 Magisk 模块在 Linux 内核与网络协议栈层直接启动 `zerotier-one`。它在系统启动时初始化持久化的虚拟以太网接口，让 Android 手机能够跨移动网络与 Wi-Fi 直接加入加密私有局域网，同时完全不占用系统 VPN 卡槽。

## 前置要求与兼容性

- **Android 版本**：Android 9.0（Pie，API 28）及以上。
- **CPU 架构**：
  - `arm64-v8a`（AArch64）
  - `armeabi-v7a`（32 位 ARM）
- **Root 方案**：Magisk（稳定版或 Canary 版）。

目前无已知的模块冲突，可与第三方 VPN 客户端及防火墙管理工具稳定共存。

## 核心架构与特性

- **后台守护进程**：原生守护进程在开机后期阶段（`service.sh`）启动，并与远程节点（笔记本电脑、家庭 NAS、云服务器）维持轻量的 P2P UDP 打洞直连。
- **私有根服务器（Planets 与 Moons）**：对于搭建私有 ZeroTier 控制器的用户（如 ztncui 或自定义 Planet 拓扑），可将自定义网络拓扑文件直接部署到 `/data/adb/zerotier/home/planet`。
- **SSO 单点登录集成**：AArch64 GCC 构建版本内置单点登录认证支持（`zeroidc`），可用于企业身份验证场景。

## 安装与配置

1. 从 GitHub Releases 页面下载 `zerotier-magisk.zip` 模块包以及配套的 `controller.apk`。
2. 在 Magisk 中刷入模块包，并按普通应用方式安装 Controller APK。
3. 重启设备以初始化网络守护进程。
4. 打开 **ZeroTier Controller** 应用：
   - 输入你的 16 位 ZeroTier Network ID。
   - 点击 **Join**。
5. 登录你的 ZeroTier 网络管理控制台（例如 `my.zerotier.com`），批准新加入的 Android 节点。
6. Android 设备将获得私有内网 IP 地址，并可立即跨 Mesh 网络互通互访。
7. 运行时守护状态、密钥与 Planet 配置文件保存在：
   ```bash
   /data/adb/zerotier/
   ```

## 故障排查与验证

- **节点未出现在 ZeroTier 控制台中**：
  - 通过 ADB Root Shell 检查守护进程是否正常在线：
    ```bash
    su -c zerotier-cli status
    # 正常应返回：200 info <node_id> <version> ONLINE
    ```
- **自定义 Planet 未生效**：如果使用私有根服务器，请将编译好的 `planet` 二进制文件放入 `/data/adb/zerotier/home/planet`，重启守护进程（`su -c killall zerotier-one`），随后使用 `zerotier-cli peers` 验证节点连接状态。
