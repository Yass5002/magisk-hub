---
id: "net-switch"
title: "Net Switch：基于 iptables 的单应用联网隔离防火墙"
sidebarTitle: "Net Switch"
description: "基于 iptables 的独立网络防火墙模块，无需运行耗电的本地 VPN 服务即可精准阻断任意应用的互联网访问。"
category: "security-certificates"
tier: 1
searchQueries:
  - "Net Switch Magisk 模块"
  - "Rem01Gaming Net Switch"
  - "Root iptables 单应用防火墙"
  - "免 VPN 禁止应用联网模块"
  - "Net Switch WebUI MMRL"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "用于管理界面的 WebUI 宿主（KernelSU/APatch 原生支持，Magisk 需搭配 KsuWebUI 或 MMRL）"
conflicts:
  - "无已知冲突：不占用 Android VpnService 接口，可与各类 VPN 客户端完美共存"
configPaths:
  - "/data/adb/modules/net-switch/"
features:
  - "单应用断网隔离：可针对每个已安装应用独立开启或关闭网络访问权限"
  - "零 VPN 架构：完全通过 Linux iptables 数据包过滤工作，无额外后台耗电"
  - "配置文件方案管理：支持保存与还原多组隔离应用清单，便于快速切换网络策略"
  - "内置备份管理：支持安全导出与导入断网规则，方便跨设备迁移配置"
  - "现代响应式 WebUI：流畅直观的交互界面，规则切换即时生效且无需重启"
faq:
  - question: "为什么 Net Switch 比 AFWall+ 等基于 VPN 的防火墙更优秀？"
    answer: "许多传统防火墙应用需要长期维持一个本地 VPN 服务或后台守护进程，不仅持续消耗电量、增加网络转发开销，还会抢占系统 VPN 通道导致无法同时使用真正的 VPN。Net Switch 直接针对应用 UID 下发原生 Linux iptables 丢包规则，几乎没有任何电量或性能损耗。"
  - question: "如何在 Magisk 环境下打开 Net Switch 控制面板？"
    answer: "由于官方版 Magisk 管理器未内置 WebUI 查看器，你可以在 Magisk 环境下配合 MMRL 或 KsuWebUIStandalone 等独立 WebUI 宿主应用来打开 Net Switch 的管理界面。"
---

## 概述

由 **Rem01Gaming** 开发的 **Net Switch** 是一款无系统分区修改（Systemless）的防火墙工具模块，旨在精准隔离单个 Android 应用对移动数据和 Wi-Fi 网络的访问。

大量 Android 应用即便在未处于前台使用时，仍会在后台静默上传遥测数据、分析日志并拉取广告。传统防火墙通常依赖 Android 的 `VpnService` 接口拦截流量——这既会带来额外的电量消耗与网络延迟，又会阻断用户连接常规 VPN；而 Net Switch 直接在内核网络边界层应用原生 Linux `iptables` 丢包策略链。

---

## 技术架构与工作原理

### 基于 UID 的 iptables 过滤机制

Net Switch 直接运行在 Linux 数据包过滤层：

1. **UID 组解析**：每个 Android 应用在安装时都会被分配唯一的 Linux 用户 ID（UID）。Net Switch 会将目标软件包名映射至其对应的系统 UID。
2. **iptables 规则链注入**：创建自定义过滤规则链（`OUTPUT -m owner --uid-owner <UID> -j DROP`），在内核层直接丢弃来自被隔离应用的所有出站 Socket 请求。
3. **规则即时生效**：在 WebUI 中切换应用开关后，规则会立即写入内核网络栈，无需重启设备即可生效。

---

## 安装与配置指南

1. 下载最新版本的 `Net-Switch-*.zip` 发布包。
2. 在 Magisk、KernelSU 或 APatch 中刷入该模块。
3. 重启设备。
4. 启动 WebUI 控制面板（在 KernelSU / APatch 管理器中直接打开，Magisk 用户请通过 MMRL 等宿主打开）。

---

## 使用说明

在 Net Switch 的 WebUI 界面中，你可以进行以下操作：
- **应用联网开关**：点击任意已安装应用即可实时切换其互联网连通性。
- **配置方案（Profiles）**：将应用分组保存为不同策略方案（例如“工作模式”、“离线单机游戏”），实现一键批量切换防火墙规则。
- **备份与恢复**：将隔离规则导出为 JSON 文件，在重刷 ROM 或更换设备后快速恢复。

---

## 故障排查与常见问题

- **被隔离的应用仍能联网**：请检查是否同时选中了该应用关联的辅助组件包（例如独立的媒体下载器或后台同步守护进程），部分应用会通过跨进程调用附属包发起网络请求。
