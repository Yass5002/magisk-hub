---
id: "vpnhide"
title: "VPN Hide：多层级活跃 VPN 状态隐藏框架"
sidebarTitle: "VPN Hide"
description: "多层级 VPN 隐藏框架，跨 Java API、原生 C/C++ 运行时库与内核 netlink 接口屏蔽活跃 VPN 连接状态。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "vpnhide Magisk 模块"
  - "okhsunrog vpnhide 下载"
  - "Android Root 隐藏活跃 VPN"
  - "银行应用绕过 VPN 检测"
  - "NoVPNDetect 替代模块 vpnhide"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "用于 Level 1 Java API 挂钩的 LSPosed 或 Vector"
  - "可选内核补丁（KPM 或内置内核驱动），用于原生 netlink/ioctl 隐藏"
conflicts:
  - "需卸载单层级 VPN 隐藏模块（如早期 NoVPNDetect），以免 Hook 逻辑冲突"
configPaths:
  - "/data/adb/modules/vpnhide_builtin/"
  - "/data/adb/modules/vpnhide_zygisk/"
  - "/data/adb/modules/vpnhide_kmod/"
features:
  - "多层级规避检测：同步在 Java 框架层、原生 C/C++ 运行时与 Linux 内核接口层隐藏 VPN 状态"
  - "抗防篡改检测：检测到反作弊或加固 SDK 时，自动规避进程内内存 Hook"
  - "原生 ioctl 与 netlink 隐藏：拦截排查 `tun`/`tap` 虚拟网卡的 `getifaddrs` 及网络接口枚举调用"
  - "状态栏图标伪装：针对目标应用隐藏系统状态栏中的钥匙或 VPN 图标"
  - "按应用精细配置：可单独勾选需要返回无 VPN 干净网络状态的银行、流媒体或支付应用"
faq:
  - question: "为什么传统的 Xposed VPN 隐藏模块在银行应用上经常失效？"
    answer: "早期模块（如 NoVPNDetect）仅在目标进程内挂钩高层 Java API（例如 `ConnectivityManager`）。现代银行应用普遍集成了可识别 Xposed 内存注入的防篡改 SDK，并通过原生 C/C++ 代码直接读取 `/proc/net/dev` 或发起 `ioctl` 调用，从而完全绕过 Java 层 Hook。"
  - question: "vpnhide 是如何解决原生层 VPN 检测的？"
    answer: "vpnhide 采用多层协同架构，结合 `system_server` 挂钩、Zygisk 动态库过滤以及可选内核驱动，从操作系统系统调用层面直接过滤 `tun`/`tap` 虚拟网络接口。"
---

## 概述

由 **okhsunrog** 开发的 **VPN Hide** 是一款专为 Android 设备打造的高级反检测解决方案，用于在系统层面彻底隐藏处于活跃状态的 VPN 隧道。

许多地区性银行、网约车与流媒体应用会出于风控与反欺诈策略，在检测到 VPN 连接时直接拒绝运行。虽然简单的 Xposed 模块可以伪造 Android 的 Java 层 `NetworkCapabilities`，但现代应用越来越多地通过原生代码（C/C++、Flutter、React Native）直接查询 Linux 网络套接字（`getifaddrs`、`ioctl` 与 `/proc/net/*`）。VPN Hide 通过同步的多层级架构同时封堵这两类检测途径。

---

## 技术架构与工作原理

### 三层隐藏引擎

VPN Hide 在整个 Android 软件栈中逐层实施防护：

1. **Level 1（Java API / LSPosed）**：尽可能优先挂钩 `system_server`，而非直接注入目标应用的私有地址空间，在网络状态分发给应用前剔除 `NetworkCapabilities` 中的 `TRANSPORT_VPN` 标志位。
2. **Level 2（原生运行时 / Zygisk）**：拦截原生 C 标准库调用（`getifaddrs`、`socket`、`ioctl`），过滤掉虚拟网卡名称（例如 `tun0`、`ppp0`、`wg0`）。
3. **Level 3（内核子系统 / 内置驱动）**：在支持内核级集成（KPM 或已打补丁的内核）的环境中，直接于内核空间过滤网络接口列表，使虚拟隧道对底层系统调用完全不可见。

---

## 安装与配置

1. 确认你的 Root 管理器（Magisk、KernelSU 或 APatch）已启用 **Zygisk** 环境。
2. 安装 **LSPosed** 或 **Vector** 以启用 Java 层拦截。
3. 从项目仓库下载最新的 `vpnhide-*.zip` 发布包。
4. 在 Root 管理器中刷入模块并重启设备。
5. 打开 LSPosed 启用 VPN Hide 模块，并勾选需要隐藏 VPN 的目标应用。

---

## 参数配置与实用指南

- **目标应用勾选**：在 LSPosed 中打开 VPN Hide 配置界面，勾选需要伪装为直连 Wi-Fi 或移动数据（无 VPN 状态）的应用。
- **内核级集成**：如果你的内核支持 Kernel Patch Module（KPM），可额外刷入配套的 `vpnhide_kmod` 组件以开启底层硬件/内核级接口屏蔽。

---

## 故障排查与常见问题

- **应用检测到内存 Hook 并闪退**：若目标应用因防篡改检测机制崩溃，请将模块切换至仅挂钩 `system_server` 的拦截模式，避免向受保护的应用进程直接注入代码。
