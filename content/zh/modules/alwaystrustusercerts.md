---
id: "alwaystrustusercerts"
title: "AlwaysTrustUserCerts：系统级 SSL/TLS 根证书自动注入工具"
sidebarTitle: "AlwaysTrustUserCerts"
description: "由 NVISO 打造的安全测试模块，开机自动将用户安装的 CA 根证书提升至系统信任区，实现无阻的 HTTPS 流量抓包与审计。"
category: "security-certificates"
tier: 1
searchQueries:
  - "alwaystrustusercerts magisk 模块"
  - "android 安装 burp suite 系统证书"
  - "mitmproxy 系统 ca 证书 android 14"
  - "用户证书提升为系统信任证书"
  - "nvisosecurity alwaystrustusercerts"
prerequisites:
  - "Android 7.0 至 Android 13（Android 14 及以上请改用 MoveCertificate）"
  - "Magisk、KernelSU 或 APatch"
conflicts:
  - "MoveCertificate（请根据 Android 系统版本二选一）"
configPaths:
  - "/system/etc/security/cacerts/"
  - "/data/misc/user/0/cacerts-added/"
features:
  - "开机自动将用户级 CA 根证书提升至系统级信任列表"
  - "通过 Magic Mount 覆盖挂载至 `/system/etc/security/cacerts/`，无需改动只读系统分区"
  - "移动渗透测试、应用安全审计与 API 逆向工程必备工具"
  - "支持 Burp Suite、Charles Proxy 与 mitmproxy 解密全部应用的 HTTPS 通信流量"
faq:
  - question: "为什么 Android 默认不信任用户自行安装的 CA 证书？"
    answer: "自 Android 7.0（Nougat）起，Google 调整了默认网络安全配置（Network Security Configuration），应用网络请求会忽略用户安装的 CA 证书。应用默认仅信任存放在只读目录 `/system/etc/security/cacerts/` 中的系统级证书。本模块正是通过将用户证书直接挂载进系统信任目录来打通这一限制。"
  - question: "为什么该模块在 Android 14 上无法生效？"
    answer: "在 Android 14 及更高版本中，Google 将系统根 CA 证书从 `/system/etc/security/cacerts/` 迁移到了不可变且可独立更新的 APEX 容器（`com.android.conscrypt`）中。传统的无系统分区修改覆盖挂载无法直接作用于 Conscrypt APEX。在 Android 14 及更新系统上，请改用 [MoveCertificate](/modules/movecertificate/) 模块。"
---

## 概述

由 **NVISO Security** 开发的 **AlwaysTrustUserCerts** 是移动安全渗透测试领域公认的标准工具，用于在已 Root 的 Android 设备上拦截并解析 SSL/TLS 加密流量。

当安全研究人员或开发者需要借助 **Burp Suite**、**OWASP ZAP** 或 **mitmproxy** 等代理工具分析移动端 API 请求时，通常需要在设备上安装自定义根 CA 证书。然而现代 Android 版本严格隔离了用户证书与应用网络栈。AlwaysTrustUserCerts 会在每次开机时自动扫描用户安装的证书，并将其提升至系统权威信任库中。

---

## 技术架构与工作原理

### 无系统分区修改的证书覆盖层

1. **用户证书识别**：当用户通过 Android“设置”→“安全”→“加密与凭据”安装证书后，系统会将带有 `.0` 哈希后缀的证书文件保存在 `/data/misc/user/0/cacerts-added/`。
2. **早期启动同步**：在系统启动的 `post-fs-data` 阶段，AlwaysTrustUserCerts 会扫描 `/data/misc/user/0/cacerts-added/` 中新增的证书文件。
3. **Magic Mount 集成**：模块将检测到的证书复制至 `/data/adb/modules/alwaystrustusercerts/system/etc/security/cacerts/`，并修正文件权限（`chmod 644`、`chown root:root`）。
4. **信任库挂载覆盖**：Magisk / KernelSU 会将该目录覆盖挂载到 `/system/etc/security/cacerts/`。当任何应用发起 TLS 握手时，Android 的 Bionic 加密库都会把抓包代理证书识别为预装受信任的系统根证书。

---

## 安装与使用（渗透测试工作流）

### 第一步：安装模块
1. 下载 `AlwaysTrustUserCerts.zip` 并在 **Magisk** 或 **KernelSU** 中刷入。
2. 重启设备。

### 第二步：安装代理软件的 CA 证书
1. 从你的代理工具中导出 CA 证书（例如从 Burp Suite 导出的 `cacert.der`）。
2. 将文件扩展名重命名为 `.crt` 并传输至手机内部存储空间。
3. 在 Android 设备上前往 **设置** → **安全** → **安装证书** → **CA 证书** → 选择该证书文件。
4. 为证书命名（例如“BurpCA”）并确认安装。

### 第三步：重启完成提升
重启手机。此时该证书会出现在 **受信任的凭据** → **系统** 选项卡中，代理工具即可成功解密应用的 HTTPS API 请求。
