---
id: "box-for-magisk"
title: "Box for Magisk：全能透明代理平台（Sing-box / Xray / Clash）"
sidebarTitle: "Box for Magisk"
description: "无侵入式代理套件，借助原生 iptables 路由将已 Root 的 Android 设备打造为透明代理网关，支持 Sing-box、Xray、V2Ray 与 Clash。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "box for magisk 配置教程"
  - "安卓 root 透明代理"
  - "sing box magisk 模块"
  - "clash for magisk 透明代理"
  - "taamarin box for magisk 下载"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "Linux 内核需启用 iptables、tproxy 及 cgroup 套接字匹配支持"
conflicts:
  - "同时运行的其他透明代理模块（如 clash-for-magisk、NetProxy）"
configPaths:
  - "/data/adb/box/"
  - "/data/adb/box/scripts/box.config"
features:
  - "多核心兼容架构：支持 Sing-box、Xray-core、V2Ray-core 与 Clash.Meta（Mihomo）"
  - "真·无侵入透明代理：基于内核 `TPROXY` 与 `REDIRECT` iptables/nftables 规则实现"
  - "基于 Android UID 过滤与 cgroup 匹配的精细化分应用代理"
  - "零依赖 Android VpnService API：释放系统 VPN 槽位，状态栏不显示钥匙图标或连接通知"
faq:
  - question: "透明代理与普通 VPN 客户端应用有什么区别？"
    answer: "常规 Android VPN 应用基于 VpnService 框架，需要在用户态创建虚拟 tun 网卡，不仅会在状态栏常驻钥匙图标，也容易被部分具备代理检测机制的应用拦截。Box for Magisk 直接工作在 Linux 内核数据包路由层（iptables/nftables），在系统无感知的情况下将出站 TCP/UDP 数据包透明转发至代理核心。"
  - question: "代理订阅或配置文件应该放在哪里？"
    answer: "若使用 Clash/Mihomo，请将配置文件放在 /data/adb/box/clash/config.yaml；若使用 Sing-box，请放在 /data/adb/box/sing-box/config.json。你可以直接在 Termux 或任意支持 Root 的文件管理器中进行编辑。"
---

## 概述

由 **taamarin** 维护的 **Box for Magisk** 是一款面向已 Root Android 设备的一体化透明代理基础设施。

与依赖 Android `VpnService` 接口的常规代理客户端不同，Box for Magisk 直接利用原生 Linux 网络工具栈（**iptables**、**nftables**、**ip route** 与 **cgroups**），将网络流量无缝引导至高性能代理核心：**Sing-box**、**Xray**、**V2Ray** 或 **Mihomo（Clash.Meta）**。这不仅能提供极低延迟的代理转发、绕过常规 VPN 状态检测，还能为你保留设备唯一的系统 VPN 槽位，用于连接公司内网或运行本地过滤工具。

---

## 技术架构与工作原理

### 内核级 TPROXY 与 Cgroup 重定向

1. **流量拦截**：开机或通过 `service.sh` 启动服务时，Box for Magisk 会自动配置 iptables/nftables 的 PREROUTING 与 OUTPUT 链。
2. **基于 UID 的分流规则**：通过识别 Android 应用的 UID 实现灵活控制，支持三种工作模式：
   - 全局模式（Global）：所有应用流量均走代理。
   - 白名单模式（Whitelist）：仅指定应用（如浏览器、社交软件、即时通讯）走代理。
   - 黑名单模式（Blacklist）：对国内银行或游戏应用绕过代理，以获得最低网络延迟。
3. **防回环机制**：借助 Linux `cgroup` 标记，由代理核心自身发出的数据包会被打标并豁免重定向，彻底避免无限路由死循环。
4. **防 DNS 泄露**：自动拦截 53 端口（UDP/TCP）DNS 流量，将其导入代理核心内部配置的 fake-ip 或加密 DNS（DoH/DoT）解析器。

---

## 安装与配置

1. 打开你的 Root 管理器（**Magisk**、**KernelSU** 或 **APatch**）。
2. 下载并刷入最新的 `box4magisk-vX.zip`。
3. 重启设备。
4. 放置对应核心的配置文件：
   - Sing-box：`/data/adb/box/sing-box/config.json`
   - Clash：`/data/adb/box/clash/config.yaml`
5. 编辑 `/data/adb/box/scripts/box.config` 指定当前启用的核心与模式：
   ```bash
   bin_name="sing-box" # 或 "clash"、"xray"
   network_mode="tproxy" # 或 "redirect"
   proxy_mode="whitelist" # 或 "blacklist"、"global"
   ```

---

## 命令行控制（CLI）

可在 **Termux** 或任意 Root 终端中管理代理服务：
```bash
# 启动代理服务
su -c "/data/adb/box/scripts/box.service start"

# 停止代理服务
su -c "/data/adb/box/scripts/box.service stop"

# 重启代理服务
su -c "/data/adb/box/scripts/box.service restart"

# 查看实时连接日志
su -c "tail -f /data/adb/box/run/box.log"
```
