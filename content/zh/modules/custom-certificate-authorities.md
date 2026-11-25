---
id: "custom-certificate-authorities"
title: "Custom Certificate Authorities：支持 DER 转 PEM 与 APEX 的系统证书挂载模块"
sidebarTitle: "Custom Certificate Authorities"
description: "自动将用户安装的 CA 根证书提升至 Android 系统信任区，内置 DER 转 PEM 转换并支持现代 APEX Conscrypt 与 BoringSSL 双路径绑定挂载。"
category: "security-certificates"
tier: 1
searchQueries:
  - "custom certificate authorities magisk 模块"
  - "whalehub custom certificate authorities 下载"
  - "android 14 root 系统 ca 证书"
  - "android 自动 der 转 pem 根证书"
  - "flutter boringssl 自定义系统证书抓包"
prerequisites:
  - "Android 11 及以上版本（最高支持 Android 15+）"
  - "Magisk v24.1 及以上版本"
  - "已通过标准 Android 系统“设置”用户凭据存储安装 CA 证书"
conflicts: []
configPaths:
  - "/data/adb/modules/Custom-Certificate-Authorities/"
  - "/data/local/tmp/customcert.log"
features:
  - "零配置导入：直接从 Android 用户凭据目录读取证书，无需手动执行 `openssl` 计算哈希"
  - "自动 DER 转 PEM：自动识别二进制 DER 编码证书并在开机时实时转换为 PEM 格式"
  - "全面兼容 BoringSSL 与 Flutter：同步注入传统系统证书路径，满足非 Conscrypt TLS 引擎需求"
  - "适配现代 APEX Conscrypt：通过绑定挂载应对 Android 14 及以上版本的可更新 Conscrypt APEX 信任库"
  - "多用户配置支持：递归扫描并整合辅助用户及工作资料空间内配置的用户证书"
faq: []
---

## 概述

自 Android 7.0（Nougat）起，Google 修改了平台网络安全策略：应用网络栈默认仅信任系统预置的 CA 根证书，忽略用户手动安装的证书。对于使用网络抓包代理（如 Burp Suite、Charles 或 mitmproxy）的安全研究人员、逆向工程师和企业开发者而言，拦截 HTTPS 流量必须先将代理根证书移入系统信任区。

到了 Android 14，这一操作变得更加棘手：Google 将系统根证书迁入了只读、可独立更新的 Conscrypt APEX 模块（`/apex/com.android.conscrypt/cacerts`），导致过去只挂载 `/system/etc/security/cacerts` 的旧版 Magisk 模块全面失效。此外，基于 Flutter / Dart 等现代框架编译的应用内置静态链接的 BoringSSL 库，它们会绕过 Conscrypt，且如果证书是二进制 DER 格式而非 PEM 格式则会直接解析失败。

由 whalehub 与 Loukious 开发的 **Custom Certificate Authorities** 通过一套全自动开机脚本一次性解决了上述所有架构难题。

## 核心特性与架构

### 1. APEX 与传统路径双路挂载
在 Android 14 及更高版本上，系统的证书信任存储处于分离状态：
- **系统 Conscrypt 信任区**：位于 `/apex/com.android.conscrypt/cacerts/`
- **传统框架与 BoringSSL 信任区**：位于 `/system/etc/security/cacerts/`

Custom Certificate Authorities 会扫描用户安装的证书，并同时对**上述两个路径**执行动态绑定挂载（Bind Mount）。这确保了标准 Java `HttpsURLConnection` 请求、Chromium WebView、OkHttp 客户端以及原生 BoringSSL 网络栈都能正确识别你的抓包代理 CA。

### 2. 自动 DER 转 PEM 格式转换
许多抓包代理或企业内网门户下发的根证书采用二进制 DER 编码（`.crt` 或 `.cer`）。而 BoringSSL 严格拒收系统信任目录中的 DER 证书，强制要求 Base64 编码的 PEM 格式（`.0` 哈希文件）。本模块会在开机阶段自动探测证书编码格式，实时将 DER 转换为 PEM，无需在电脑端提前手动转换。

### 3. 多用户与工作资料支持
在多用户配置环境（如启用了工作资料、Island 或 Shelter 的设备）中，用户证书被隔离存放在以用户 ID 编号的凭据目录中（`/data/misc/user/<userid>/cacerts-added`）。模块会递归遍历所有活跃用户空间，将全部 CA 证书统一归集至系统根目录。

## 如何添加证书

无需手动重命名文件或计算 Subject Name 哈希值：

1. 在 Magisk 中刷入并安装 **Custom Certificate Authorities**，随后重启手机。
2. 将抓包代理的 CA 证书（如 `cacert.der`、`charles-ssl-proxying-certificate.pem`）传至手机存储。
3. 打开 Android **设置** → **安全与隐私** → **更多安全设置** → **加密与凭据** → **安装证书** → **CA 证书**。
4. 选中你的证书文件并确认安装。
5. **重启设备**。
6. 开机引导过程中，模块会自动读取新安装的用户证书，按需转换格式并绑定挂载至两套系统证书信任库中。

## 验证与诊断

按以下步骤确认证书已成功提升至系统信任区：

1. 打开 Android **设置** → **加密与凭据** → **受信任的凭据** → **系统**。
2. 向下滚动查找你的代理 CA 证书；此时它应出现在“系统”列表而非“用户”列表中。
3. 在 ADB 或 Root 终端中查看模块运行日志：
   ```bash
   su -c cat /data/local/tmp/customcert.log
   ```
   日志会详细记录文件扫描、格式转换结果以及 Conscrypt 与传统目录的挂载状态。
