---
id: "magisk-ad-blocking-module"
title: "Magisk Ad-Blocking Module：Systemless Hosts 广告与追踪拦截器"
sidebarTitle: "Ad-Blocking Module"
description: "零开销的无系统分区修改（Systemless）hosts 替换模块，整合 OISD、1Hosts 与反成人内容过滤规则，全局屏蔽网络广告与追踪域名。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "Magisk Ad Blocking Module pantsufan"
  - "Android Systemless hosts 去广告模块"
  - "OISD 1Hosts Magisk hosts 文件"
  - "Root 免 VPN 全局屏蔽广告"
  - "Magisk 去广告模块下载"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "在 Root 管理器设置中启用 Systemless hosts 支持"
conflicts:
  - "明确说明：暂无与其他模块的已知冲突文档记录；但其他修改 `/system/etc/hosts` 的模块会与本模块相互覆盖"
configPaths:
  - "/system/etc/hosts"
  - "/data/adb/modules/adblocking-module/"
features:
  - "零电池额外开销：通过 hosts 文件由系统底层 DNS 解析直接拦截，无需常驻后台 VPN 服务"
  - "多源合并拦截库：聚合来自 OISD、1Hosts 及精选域名黑名单的过滤规则"
  - "色情与成人追踪过滤：内置成人内容屏蔽规则，适合家庭守护与专注场景使用"
  - "全系统应用覆盖：覆盖网页浏览器、游戏及第三方应用中的广告与遥测域名"
  - "标准模块模板构建：基于稳定的 MMT-Extended 框架打造，支持干净卸载与平滑升级"
faq:
  - question: "该模块如何在不运行后台进程的情况下拦截广告？"
    answer: "模块会将一份完整的 hosts 文件挂载覆盖到 `/system/etc/hosts`。当应用发起针对已知广告和遥测服务器的 DNS 查询时，Android 会在本地直接将该域名解析为 `0.0.0.0`，从而以零 CPU 开销瞬间阻断连接。"
  - question: "可以与常规 VPN 应用同时使用吗？"
    answer: "可以。由于基于 hosts 的广告拦截工作在操作系统的域名解析层，而非占用 Android 的 `VpnService` API，因此你可以自由地同时使用第三方 VPN 或 Tor 连接。"
---

## 概述

由 **pantsufan** 维护的 **Magisk Ad-Blocking Module** 是一款专为 Root Android 设备打造的轻量级 Systemless hosts 内容拦截器。

不同于需要持续运行 VPN 服务（不仅耗电、引入额外处理开销，还会独占 Android 唯一的 VPN 隧道槽位）的移动端去广告应用，本模块以无系统分区修改的方式覆盖 Android 的 `/system/etc/hosts` 文件。当应用试图加载广告横幅或连接追踪服务器时，连接会在操作系统层面被直接丢弃阻断。

---

## 技术架构与工作原理

### Systemless Hosts 解析机制

本模块直接通过 Android 的 POSIX 域名解析栈发挥作用：

1. **Hosts 规则合成**：将来自 **OISD**、**1Hosts** 以及专项追踪器数据库的可靠域名源整合为一份统一格式的 `hosts` 文件。
2. **本地回环重定向**：将数十万计的广告网络域名、遥测探测节点及恶意追踪端点全部指向 `0.0.0.0`。
3. **Magic Mount 叠层挂载**：开机时使用 Systemless 绑定挂载技术将编译好的 hosts 数据库放置于 `/system/etc/hosts`，保持底层 `/system` 分区只读且毫发无损。

---

## 安装与配置

1. 打开你的 Root 管理器（Magisk、KernelSU 或 APatch），确认已**开启** **Systemless hosts** 支持开关。
2. 从官方仓库下载最新发布包。
3. 在 Root 管理器中刷入该模块 zip 压缩包。
4. 重启设备以使新的 hosts 文件生效。

---

## 日常配置与使用

- **维护与更新**：模块安装后即可全自动静默运行。随着上游黑名单规则演进，你只需通过更新模块版本即可获取最新域名拦截库。
- **自定义白名单**：若特定服务或应用需要访问某个被拦截的域名，可直接编辑 `/system/etc/hosts`（或位于 `/data/adb/modules/adblocking-module/system/etc/hosts` 的底层模块文件），删除对应的域名条目即可。

---

## 故障排查与常见问题

- **部分应用中依然显示广告**：部分应用（例如 YouTube 或 Facebook）会从与正片媒体内容相同的域名下发广告。域名级别的 hosts 拦截器无法在不破坏视频正常播放的前提下剥离第一方媒体流中内嵌的广告。
- **规则被其他模块覆盖**：如果你刷入了其他同样修改 hosts 文件的模块（如某些 VPN 辅助或私人 DNS 模块），请确保仅启用一个 hosts 管理模块，避免规则相互覆盖。
