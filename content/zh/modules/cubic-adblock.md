---
id: "cubic-adblock"
title: "Cubic AdBlock：精简防误杀的无侵入式 Hosts 广告与遥测拦截模块"
sidebarTitle: "Cubic AdBlock"
description: "通过无侵入式挂载精选 /etc/hosts 过滤规则屏蔽全系统广告与隐私遥测，同时完整保留企业服务、社交账号登录及厂商云功能。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "cubic adblock magisk 模块"
  - "vaz15k cubic adblock 下载"
  - "安卓 root systemless hosts 去广告"
  - "etc hosts 安卓屏蔽广告"
  - "不误杀谷歌微软登录的去广告模块"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "已在 Root 管理器设置中启用 Systemless hosts 支持"
conflicts: []
configPaths:
  - "/data/adb/modules/cubic-adblock/"
  - "/system/etc/hosts"
features:
  - "零后台资源占用：依托操作系统原生 /etc/hosts 文件过滤域名解析，无任何常驻内存开销"
  - "核心服务高兼容性：精细保留 Google 服务、微软账号、Facebook 登录及三星云功能所需的 API 域名"
  - "全系统生效覆盖：同时屏蔽网页浏览器及第三方原生应用内的横幅广告、追踪脚本与插屏视频广告"
  - "自动化规则维护：上游 hosts 规则列表通过自动化 CI 工作流持续维护更新"
faq: []
---

## 概述

基于 VPN 的去广告工具（如 AdGuard 或本机 DNS 过滤应用）虽然规则灵活，但必须常驻一个活动的 Android `VpnService` 会话。这不仅导致用户无法同时使用真正的 VPN 连接，还会造成状态栏通知常驻，并因持续逐包检查而加速电量消耗。

由 Vaz15k 开发的 **Cubic AdBlock** 依托 Android 原生域名解析表提供轻量、透明的广告拦截能力。通过将一份经过精心筛选与优化的 `hosts` 文件无侵入式挂载覆盖至 `/system/etc/hosts`，所有指向广告交易平台、用户遥测收集器及恶意域名的查询都会立即被重定向至本地回环地址（`0.0.0.0`），全程实现零内存占用。

## 精选白名单理念

过于激进的社区 hosts 规则常会意外破坏基础账号登录框架、消息推送网关以及云同步服务。Cubic AdBlock 在整理拦截列表时特别做好了白名单防护，确保以下核心体验不受影响：

- **单点登录（SSO）**：完整保留 Google Identity、Facebook Login 与 Microsoft Live 服务的认证链路。
- **厂商云生态**：确保三星、小米与 Google Pixel 设备的云同步及查找手机等功能正常运转。
- **应用功能完整性**：在屏蔽广告资源加载的同时，避免触发购物与银行类敏感应用的「网络连接失败」异常锁定。

## 工作原理

1. 系统启动期间，Magisk 或 KernelSU 将模块内置的精选 `hosts` 表绑定挂载覆盖至 `/system/etc/hosts`。
2. 每当应用发起 HTTP/HTTPS 连接时，Android Bionic C 库解析器会优先查询 `/etc/hosts`，再决定是否向外部 DNS 服务器发起请求。
3. 若目标域名命中广告网络条目，解析过程将直接返回 `0.0.0.0`。
4. 广告请求在微秒级时间内于本地快速失败，从而显著加快页面加载速度并节省移动流量。

## 安装与配置

1. 若使用 Magisk，请先进入 **Magisk 设置** 并确认已开启 **Systemless hosts**。
2. 从 GitHub 仓库下载最新的 `Cubic-AdBlock` `.zip` 安装包。
3. 通过 **Magisk**、**KernelSU** 或 **APatch** 刷入该压缩包。
4. 重启设备以使更新后的 hosts 映射表生效。

## 生效验证

可通过以下命令验证系统级无侵入式 hosts 文件是否已激活：

```bash
su -c ping -c 1 pagead2.googlesyndication.com
```
命令应立即返回指向 `0.0.0.0` 的响应或提示无法解析，这即表明广告与追踪域名已在系统底层被成功拦截。
