---
id: "aurora"
title: "Aurora：面向 Sing-Box 与 Mihomo 的全局透明代理启动器"
sidebarTitle: "Aurora 透明代理"
description: "无系统分区修改（Systemless）部署高性能代理核心（sing-box、mihomo），通过 TProxy 与 TUN 网络接口建立全局透明路由。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "aurora magisk 透明代理模块"
  - "tkocean aurora 代理"
  - "sing-box 安卓 root 透明代理"
  - "mihomo tproxy kernelsu 配置"
  - "magisk 全局代理路由"
prerequisites:
  - "Android 12 或更高版本"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "内核需支持 iptables/nftables 以及 TProxy / TUN 套接字选项"
conflicts: []
configPaths:
  - "/data/adb/modules/aurora/"
  - "/data/adb/aurora/"
features:
  - "双核心代理调度：内置集成 sing-box 与 mihomo 二进制核心，满足现代多协议代理路由需求"
  - "高阶网络接管模式：支持高吞吐量的 TProxy（TCP + UDP）与 TUN 虚拟网卡路由"
  - "自动化防火墙规则管理：在服务启动与停止阶段动态下发及清理 iptables 路由表"
  - "模块化目录结构：用户自定义配置文件独立存放于 /data/adb/aurora/，模块更新时不受影响"
faq: []
---

## 概述

在 Android 上实现全局透明代理通常需要借助第三方 VPN 应用，这类应用往往会在通知栏常驻前台通知，因 Android `VpnService` 抽象层带来额外电量消耗，并在切换网络时频繁出现断连。

由 Tkocean 开发的 **Aurora** 能够将 Android 设备直接转变为原生路由网关。通过 Magisk、KernelSU 或 APatch 直接介入 Linux 网络协议栈，Aurora 可调度 **sing-box** 与 **mihomo** 等现代代理核心，借助内核级 TProxy 与 TUN 套接字路由表接管全部系统出入站数据包。

## 网络路由模式

Aurora 绕过耗电较高的 Android `VpnService` API，以无侵入式方案路由网络流量：

- **TProxy（TCP + UDP）**：在内核 Netfilter 阶段直接拦截数据包并重定向至本地代理端口，同时完整保留原始数据包头与目标 IP 地址。
- **TUN 虚拟适配器**：分配由代理核心直接接管的虚拟网络接口，为绕过常规套接字路由表的应用提供全协议栈覆盖。

## 目录结构与配置

核心二进制文件、运行脚本及运行时文件隔离存放于模块目录中，而持久化用户配置则保存在 `/data/adb/aurora/`：

- **`/data/adb/aurora/config/`**：存放自定义 `sing-box`（`config.json`）或 `mihomo`（`config.yaml`）配置文件的目录。
- **`/data/adb/aurora/scripts/`**：负责处理 iptables 规则、策略路由数据库（`ip rule`）以及接口生命周期的网络初始化脚本。

## 安装与配置

1. 确认设备运行 **Android 12** 或更高版本，并已安装兼容的 Root 管理器。
2. 下载并刷入 **Aurora** `.zip` 安装包。
3. 将你的代理配置文件（sing-box JSON 或 mihomo YAML）放入 `/data/adb/aurora/`。
4. 重启设备。后台守护进程将自动启动并下发内核路由表。

## 故障排查

- **重启后无法联网**：若网络流量无法正常解析或连通，请核对代理配置文件中的服务器节点信息是否有效，并确认上游 DNS 无需经过代理即可直连解析。
- **内核不支持 TProxy**：若 logcat 日志中出现 iptables 报错（如 `No chain/target/match by that name`），说明当前设备内核缺少 `xt_TPROXY` 模块支持；请在模块配置中将路由模式切换为 TUN。
