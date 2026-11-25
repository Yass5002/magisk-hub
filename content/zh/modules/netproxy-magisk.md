---
id: "netproxy-magisk"
title: "NetProxy：全功能 Sing-Box 透明代理与 WebUI 管理套件"
sidebarTitle: "NetProxy"
description: "内置交互式本地 WebUI 仪表盘、自动订阅更新及智能规则分流的 Sing-box 透明代理引擎。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "NetProxy Magisk 模块下载"
  - "Android Root sing-box WebUI"
  - "Magisk WebUI 透明代理模块"
  - "Fanju6 NetProxy 下载配置"
  - "Android sing-box 控制面板"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "可用的 Sing-box 订阅链接或兼容的 JSON 配置文件"
conflicts:
  - "不可与其他透明代理模块（如 Box for Magisk、Clash for Magisk）同时启用"
configPaths:
  - "/data/adb/modules/netproxy-magisk/"
  - "/data/adb/netproxy/"
features:
  - "内置轻量级 WebUI 仪表盘，通过手机浏览器访问 `http://127.0.0.1:9090` 即可管理"
  - "高性能原生 Sing-box 核心，全面支持 Shadowsocks、VLESS、VMess、Trojan 与 Hysteria2 协议"
  - "支持按计划周期自动更新远程代理订阅"
  - "智能规则分流：自动划分国内直连流量与境外代理流量"
faq:
  - question: "如何打开 NetProxy 的 WebUI 管理面板？"
    answer: "刷入并启动模块后，打开手机浏览器（如 Chrome 或 Firefox）访问 `http://127.0.0.1:9090`（如果所使用的 KernelSU 或 Magisk 版本支持 WebUI 快捷入口，也可直接点击打开）。"
  - question: "支持 Hysteria2 和 TUIC 协议吗？"
    answer: "支持。NetProxy 打包了最新版多协议 Sing-box 二进制内核，完整支持 UDP/QUIC 协议并已开启 TPROXY 透明代理路由。"
---

## 概述

由 **Fanju6** 开发的 **NetProxy-Magisk** 是一款功能前沿的代理工具套件，将 **Sing-box** 的高速与灵活特性引入已 Root 的 Android 设备，并配备了精致的内置 WebUI 管理仪表盘。

在手机上直接操作命令行代理模块往往较为繁琐，NetProxy 通过内置本地网页控制台解决了这一痛点。用户无需打开终端，即可直接在手机浏览器中导入远程订阅链接、切换节点、查看实时流量图表以及检查活跃的 TCP/UDP 连接。

---

## 技术架构与工作原理

### 高性能 Sing-box TPROXY 网关

1. **内核路由初始化**：NetProxy 在开机时自动配置 Linux `ip rule` 及 `iptables` / `nftables` 路由规则表。
2. **Sing-box 引擎**：作为受监控的 Root 后台守护进程拉起编译好的 Sing-box 二进制程序。
3. **TPROXY 入站拦截**：利用 Linux 内核 TPROXY（透明代理）机制拦截设备出站流量，完整保留原始源 IP 与目标 IP 地址。
4. **本地 WebUI 仪表盘**：在本地回环地址（`127.0.0.1:9090`）提供响应式 Web 管理界面，支持节点选择、延迟测速、分流规则管理及实时连接日志查看。

---

## 安装与快速上手

1. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入 `NetProxy-vX.zip`。
2. 重启设备。
3. 打开手机浏览器并访问：
   `http://127.0.0.1:9090`
4. 在 **Subscription**（订阅）标签页中粘贴你的 Sing-box 订阅链接并点击 **Update**（更新）。
5. 选定需要使用的代理节点，并将 **Proxy Status**（代理状态）开关切换为开启即可。
