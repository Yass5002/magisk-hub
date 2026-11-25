---
id: "reqable"
title: "Reqable：全功能 Android HTTP/HTTPS MITM 抓包与 API 调试客户端"
sidebarTitle: "Reqable"
description: "高性能跨平台网络调试与 API 测试客户端（com.reqable.android），在安卓端同时支持免 Root 本地 VPN 抓包以及 Root/Magisk 系统 CA 根证书与透明代理模式。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "Reqable 安卓版下载"
  - "Reqable Magisk 系统证书安装"
  - "Android 14 HTTPS 抓包工具 Root"
  - "Reqable APEX Conscrypt 证书"
  - "com.reqable.android"
prerequisites:
  - "64 位 ARM（`arm64-v8a`）架构 Android 设备"
  - "免 Root 本地 VPN 模式开箱即用；若需拦截不信任用户证书的应用或使用透明代理，需配合 Magisk、KernelSU 或 APatch 获取 Root 权限"
conflicts:
  - "启用免 Root VPN 模式时，与其他占用 Android `VpnService` 的科学上网/广告过滤应用互斥"
  - "开启严格证书锁定（SSL Pinning）且未注入解绑 Hook 的目标应用"
configPaths:
  - "/data/data/com.reqable.android/"
  - "/system/etc/security/cacerts/"
  - "/apex/com.android.conscrypt/cacerts/"
features:
  - "双抓包模式自由切换：支持免 Root 的 `NetbareVpnService` 本地回环抓包，以及配合 Root 环境的系统 CA 根证书与透明代理工作流"
  - "原生高性能网络栈（`libreqable_netbare.so`、`libreqable_cronet.so`、`libtun2proxy.so`），完整支持 HTTP/1.1、HTTP/2、HTTP/3、WebSocket 与 SSE"
  - "全能 MITM 调试工具链：实时断点拦截、请求/响应重写、重放测试、HAR 导入导出与自定义脚本处理"
  - "内置 API 测试客户端，支持接口集合管理、多作用域环境变量、扫码互联桌面端及 MCP 协议集成"
faq:
  - question: "为什么在 Android 上推荐搭配 Magisk / Root 环境使用 Reqable？"
    answer: "自 Android 7.0 起，面向 API 24+ 编译的应用默认仅信任系统预置的 CA 根证书，会忽略用户手动安装的证书。在免 Root VPN 模式下，Reqable 虽可通过 `NetbareVpnService` 捕获流量，但无法解密此类应用的 HTTPS 载荷。借助 Magisk、KernelSU 或 APatch，可将 Reqable CA 根证书部署至系统证书目录（含 Android 14+ 的 `/apex/com.android.conscrypt/cacerts`），从而顺畅解密常规应用的 HTTPS 通信。"
  - question: "Reqable 是开源软件吗？"
    answer: "不是。官方仓库 `Reqable/reqable-app` 明确说明 Reqable 属于闭源商业（Proprietary）软件，GitHub 仓库主要用于问题追踪、文档发布与正式版安装包分发。个人开发者常用的绝大多数抓包与 API 测试功能在免费社区版中均可无期限使用。"
  - question: "安装了系统级 CA 根证书后，为什么部分应用依然无法抓包？"
    answer: "系统 CA 证书仅能通过操作系统标准的 `TrustManager` 校验。如果目标应用在代码层硬编码了证书锁定（SSL Pinning，如 OkHttp `CertificatePinner`、Flutter 内置 BoringSSL 或自定义原生库校验），仍会主动断开 MITM 连接。此时需搭配 LSPosed（如 TrustMeAlready）或 Frida 脚本解除证书绑定。"
---

## 概述

**Reqable**（包名 `com.reqable.android`）是一款集 **MITM 流量抓包分析**（类比 Charles / Fiddler）与 **API 接口调试测试**（类比 Postman）于一体的现代网络开发利器。Android 客户端提供原生 `arm64-v8a` 完整体验，既可在手机端独立完成抓包与断点调试，也支持通过局域网扫码与桌面端无缝协同。

---

## 技术架构与抓包工作模式

`reqable-app-android-arm64.apk` 采用 Flutter 界面框架搭配自研高性能原生底层库，包括 `libnetbare-jni.so`、`libreqable_netbare.so`、`libtun2proxy.so`、`libreqable_cronet.so`、`libreqable_http.so`、`libreqable_protobuf.so`、`libreqable_brotli.so`、`libreqable_zstd.so` 以及用于高速本地存储的 `libobjectbox-jni.so`。

### 1. 免 Root 本地 VPN 模式（`NetbareVpnService`）

- 通过 Android 原生 `android.net.VpnService`（`com.reqable.android.NetbareVpnService`）建立本地虚拟网卡，将选定应用的网络流量环回至 Reqable MITM 引擎，无需对设备进行 Root。
- **适用边界**：适合调试自有开发版应用（已在 `network_security_config.xml` 中信任用户证书）或未启用严格校验的流量；但对于忽略用户 CA 或检测 `TRANSPORT_VPN` 的应用，单纯依靠 VPN 模式会受限。

### 2. Root / Magisk / KernelSU 增强模式

- **系统 CA 根证书部署**：在 Root 环境下（Android 14+ 需同步覆盖位于 `/apex/com.android.conscrypt/cacerts/` 的 APEX 证书目录），将 Reqable 根证书提升为系统级信任证书，解除 Android 7+ 对普通应用 HTTPS 抓包的信任限制。
- **透明代理与桌面协同**：避免应用因检测到 VPN 激活而拒绝联网，支持结合代理转发或桌面端联动进行深度报文解析。

---

## 安装与配置指南

1. 下载 `reqable-app-android-arm64.apk` 并安装至 `arm64-v8a` 架构的 Android 设备。
2. **免 Root 使用场景**：启动 Reqable，按照内置引导将 CA 证书安装至“用户凭据”，并授权开启本地 VPN 抓包服务。
3. **Root 设备（Android 7–13）**：在证书安装向导中导出或通过 Root 方式将哈希命名的 `.0` 证书放入 `/system/etc/security/cacerts/`（可通过系统证书类 Magisk 模块无系统修改挂载）。
4. **Root 设备（Android 14–16+ APEX Conscrypt）**：先将 Reqable 证书安装为用户证书，再启用支持 APEX Conscrypt 的系统证书同步模块（如 MoveCert / MagiskTrustUserCerts 衍生模块），使 `/apex/com.android.conscrypt/cacerts/` 同步生效。
5. 根据需要在调试界面配置应用过滤白名单、重写规则、断点或脚本。

---

## 常见问题与排查

- **抓包记录显示 TLS 握手失败或证书未知**：目标应用面向 Android 7+ 编译且未信任用户证书，请确认已将 Reqable CA 迁移至系统证书目录（Android 14+ 需检查 `/apex/com.android.conscrypt/cacerts/` 挂载是否生效）。
- **无法与其他 VPN 工具同时运行**：Android 系统同一时刻仅允许存在一个活跃的 `VpnService`。使用本地 VPN 模式前需暂停其他代理或广告拦截 VPN，或在 Root 环境下改用代理/透明转发方式。
- **特定 App 在抓包时断网**：说明目标应用启用了 SSL Pinning 校验。若无需分析该应用，请将其移出 Reqable 的捕获应用列表；若确需调试，请配合 LSPosed 或 Frida 绕过证书锁定。
