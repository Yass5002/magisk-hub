---
id: "surfing"
title: "Surfing：多内核透明代理与 Clash 网关模块"
sidebarTitle: "Surfing"
description: "全能型 Systemless 透明代理模块，支持编排 Clash/mihomo、sing-box、Xray 与 Hysteria 内核，并支持 REDIRECT、TPROXY 及 TUN 路由模式。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "Surfing Magisk 模块下载"
  - "Android Root Clash 透明代理"
  - "KernelSU mihomo TPROXY 模块"
  - "Surfing box_bll config.yaml 配置"
  - "SurfingTile 代理管理软件"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "已向 SurfingTile 桌面配套 APK 授予 Root 权限"
  - "已更新至较新版本的 Android System WebView (`com.google.android.webview`) 以正常渲染网页控制台"
conflicts:
  - "当 `proxy_method` 设为 `TUN` 时，`box.config` 中的 `bypass_via_iptables='true'` 会产生冲突"
  - "`enable_ssid_filter` 与 `enable_mac_filter` 为互斥选项（同时开启时优先以 SSID 过滤为准）"
configPaths:
  - "/data/adb/box_bll/clash/config.yaml"
  - "/data/adb/box_bll/scripts/box.config"
  - "/data/adb/box_bll/run/"
  - "/data/adb/modules/Surfing/"
features:
  - "多内核路由引擎：支持 Clash/mihomo、sing-box、v2ray、Xray 与 Hysteria 后端内核"
  - "灵活的拦截模式：提供 REDIRECT（仅 TCP）、TPROXY（TCP+UDP）、TUN 虚拟网卡及混合路由模式"
  - "网络接口精细过滤：支持基于 Wi-Fi SSID、MAC 地址、蜂窝网络状态以及热插拔绕过的策略规则"
  - "SurfingTile 管理应用：提供本地控制面板，用于管理订阅、手动切换节点与查看路由日志"
  - "应用与用户黑白名单：可直接通过 `box.config` 绕过特定 Android 应用或系统多用户配置文件"
faq:
  - question: "为什么在 SurfingTile 中管理面板无法正常显示？"
    answer: "管理面板依赖现代 Chromium 内核特性。如果面板无法渲染或出现白屏，请通过 Google Play 商店等渠道更新 `com.google.android.webview` 组件。"
  - question: "可以同时启用 Wi-Fi SSID 过滤与 MAC 地址过滤吗？"
    answer: "不可以。根据 `box.config` 配置说明，SSID 过滤与 MAC 地址过滤互不兼容。当两者同时开启时，系统将优先执行 SSID 过滤规则并忽略 MAC 过滤。"
---

## 概述

由 **GitMetaio** 开发的 **Surfing** 是一款进阶网络重定向模块，能够将已 Root 的 Android 设备改造为功能完备的透明路由网关。

Surfing 不采用容易耗电且会独占 Android 唯一 `VpnService` 槽位的常规 VPN 接口，而是直接工作在 Linux 内核防火墙层。它利用原生的 iptables 与 nftables 规则链，在网络协议栈拦截套接字流量并导向高性能核心守护进程，支持的后端包括 **Clash.Meta (mihomo)**、**sing-box**、**Xray** 或 **Hysteria**。

---

## 技术架构与工作原理

### 内核防火墙拦截与核心转发

Surfing 将其配置文件、运行时二进制文件与路由规则统一隔离存放在 `/data/adb/box_bll/` 目录中：

1. **代理模式**：
   - **TPROXY（默认）**：利用 `iptables -t mangle -A PREROUTING -p tcp/udp -j TPROXY` 将 TCP 与 UDP 流量透明重定向至本地 `1536` 端口，无需篡改应用层数据包头部。
   - **REDIRECT**：备选的仅限 TCP 的重定向模式，将流量转发至本地 `7891` 端口。
   - **TUN**：创建名为 `Meta` 的虚拟网卡设备，用于兼容不支持套接字拼接（socket splicing）的协议。
2. **网络状态自动化**：辅助守护进程会持续监听网络接口切换事件（如 Wi-Fi 与蜂窝移动数据切换、不同 Wi-Fi SSID 间漫游），并依据 `box.config` 中的黑白名单定义动态开启或暂停代理规则链。
3. **应用隔离与 UID 排除**：通过 Linux cgroups 与 `net_admin` GID 机制，豁免核心代理二进制进程及指定 Android 应用包名，防止代理流量发生回环。

---

## 安装与配置

### 1. 刷入模块
1. 从项目官方发布页下载 `Surfing-v*.zip`。
2. 通过 Magisk、KernelSU 或 APatch 刷入该模块。
3. 重启设备。

### 2. 配置订阅
在网络重定向正式生效前，必须先提供有效的代理订阅配置：
1. 在桌面打开 **SurfingTile** 应用并授予其超级用户（Root）权限。
2. 在 **Menu > Config Override** 中粘贴你的机场订阅链接并触发更新。
3. 或者，也可以直接将原始配置文件写入以下路径：
   ```bash
   /data/adb/box_bll/clash/config.yaml
   ```
4. 重启服务或重启手机即可使路由配置生效。

---

## 配置与实战用法

进阶参数微调可直接在 `/data/adb/box_bll/scripts/box.config` 中完成：

- **选择代理模式**：
  ```bash
  proxy_method="TPROXY" # Options: REDIRECT, TPROXY, TUN, or MIXED
  ```
- **应用绕过列表**：
  从代理拦截中排除特定应用 UID 及用户空间：
  ```bash
  user_packages_list=("0:com.android.captiveportallogin" "0:com.google.android.gms")
  ```
- **Wi-Fi 网络过滤**：
  连接受信任的家庭或办公网络时自动停用代理：
  ```bash
  enable_ssid_filter="true"
  use_wifi_list_mode="blacklist"
  blacklist_wifi_ssids="Home_Network,Office_5G"
  ```

---

## 故障排查与常见问题

- **开机后无网络连接**：检查 `/data/adb/box_bll/run/clash.pid` 确认核心二进制进程是否已成功启动。若订阅因远程服务端校验严格而拉取失败，可尝试在配置文件中调整 User-Agent 设置（`Ua`）。
- **热插拔绕过冲突**：当使用 `proxy_method="TUN"` 模式时，请务必确保 `box.config` 中的 `bypass_via_iptables` 设为 `"false"`，以免 TUN 接口与 iptables mangle 链之间发生路由环路冲突。
