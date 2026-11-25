---
id: "google-mobile-services-core"
title: "Google Mobile Services (GMS) 核心套件：无侵入式 Play 服务部署方案"
sidebarTitle: "GMS 核心套件"
description: "通过无系统分区修改（Systemless）方式完整部署 Google 移动服务与 Play 商店框架，消除国行固件区域限制，恢复定位历史记录与完整全球生态功能。"
category: "system-environment"
tier: 1
searchQueries:
  - "GMS 核心套件 Magisk 模块"
  - "国行手机解除 GMS 区域限制"
  - "Google Play 服务无侵入安装 Magisk"
  - "解锁国行谷歌位置记录"
prerequisites:
  - "Android 10、11、12 或 13 国行或国际版固件"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "microG 或存在冲突的 microG GmsCore 存根实现"
configPaths:
  - "/system/priv-app/GmsCore/GmsCore.apk"
  - "/system/priv-app/Phonesky/Phonesky.apk"
  - "/system/priv-app/GoogleServicesFramework/GoogleServicesFramework.apk"
  - "/system/etc/permissions/cn.google.services.xml"
features:
  - "无侵入式挂载完整 Google 移动服务框架，涵盖 GmsCore、Phonesky 与 GSF"
  - "移除 `cn.google.services` 区域限制标记，解锁谷歌位置记录与时间轴功能"
  - "解决国行固件下 Google Play 商店下载应用报 404 错误的问题"
  - "恢复设备在网页端 Google Play 商店控制台中的可见状态"
  - "在不修改 `/system` 分区块的前提下保留完整的系统签名级权限"
faq:
  - question: "该模块会导致 SafetyNet 或 Play Integrity 认证失败吗？"
    answer: "不会。该模块将官方未修改的 Google 二进制应用安装至 `/system/priv-app`，并移除区域权限锁。如需通过 Device 与 Strong 级别 Play Integrity 认证，请配合 Play Integrity Fix 模块使用。"
  - question: "该模块是否用于替代 microG？"
    answer: "本模块安装的是官方原版 Google 移动服务组件，而非 microG，适用于缺少原生 GMS 或预装受限区域版 GMS 的设备。"
---

## 概述

**Google Mobile Services Core Suite**（由 Shiguang 制作）是一套采用无系统分区修改（Systemless）方式部署的 Google 专有移动服务平台，主要针对缺少完整 Google Play 功能的国行固件（如小米 MIUI / HyperOS、OPPO ColorOS、vivo OriginOS 等）而打造。

即便部分国行 OEM ROM 在系统中内置了基础的“谷歌基础服务”开关，区域固件往往仍会注入限制性系统权限覆盖配置，导致谷歌位置记录无法启用、设备无法在 Google Play 网页端管理界面显示，并在下载应用时意外触发 404 错误。本套件在提供完整 GMS 组件栈的同时彻底剥离此类区域限制。

---

## 技术架构与工作原理

现代 Android 系统的 GMS 功能依赖多个组件之间协同运作的系统特权：

### 1. 核心框架注入

该模块将必需的特权系统应用绑定挂载至 `/system/priv-app/`：

- **GmsCore.apk**：Google Play 服务的核心运行时（负责账号体系、地图服务、推送通知与身份认证 API）。
- **Phonesky.apk**：官方 Google Play 商店客户端界面与应用安装器。
- **GoogleServicesFramework.apk**：底层令牌提供程序与设备注册守护进程。

### 2. 消除区域功能限制

国行 OEM 固件通常会内置如下权限声明文件：

```xml
<!-- Restricted permission in stock vendor image -->
<feature name="cn.google.services" />
```

该标记会指示 Google Play 服务依据本地监管策略关闭定位追踪、联系人同步以及部分账号备份链路。本模块通过无侵入方式消除该限制，从而恢复完整的全球版 Google 功能体验。

---

## 故障排查与最佳实践

- **授予全部权限**：首次安装完成后，前往 **设置 > 应用 > Google Play 服务**，确保已授予位置信息、健身运动与通讯录权限。
- **关闭电池优化**：为确保推送通知稳定送达，请将 Google Play 服务与 Google 服务框架的耗电策略设为 **无限制**。
