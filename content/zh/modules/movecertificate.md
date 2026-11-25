---
id: "movecertificate"
title: "MoveCertificate：Android 14+ Conscrypt APEX 证书移动模块"
sidebarTitle: "MoveCertificate"
description: "专为 Android 14 与 15 打造的证书注入安全模块，可将用户安装的 CA 根证书直接绑定挂载至 Conscrypt APEX 系统信任库。"
category: "security-certificates"
tier: 1
searchQueries:
  - "MoveCertificate Magisk 模块下载"
  - "Android 14 安装 Burp 抓包证书"
  - "Android 14 系统 CA 证书 APEX 注入"
  - "ys1231 MoveCertificate"
  - "Android 15 信任用户根证书模块"
prerequisites:
  - "Android 14 或 Android 15 系统"
  - "Magisk、KernelSU 或 APatch"
conflicts:
  - "旧版 AlwaysTrustUserCerts 模块（仅适用于 Android 13 及更早版本）"
configPaths:
  - "/apex/com.android.conscrypt/cacerts/"
  - "/data/misc/user/0/cacerts-added/"
features:
  - "全面兼容 Android 14+ 可更新 APEX Conscrypt 安全架构"
  - "利用挂载命名空间覆盖机制将证书注入 `/apex/com.android.conscrypt/cacerts/`"
  - "每次开机自动扫描用户证书、重新计算哈希并修正文件权限"
  - "在 Android 14/15 上恢复 Burp Suite、Charles 与 mitmproxy 的完整 HTTPS 解密抓包能力"
faq:
  - question: "为什么传统移动证书模块在 Android 14 上全部失效了？"
    answer: "从 Android 14 开始，Google 将 Conscrypt 安全加密提供程序重构为可独立更新的 APEX 组件。系统 CA 根证书库也从原本的 `/system/etc/security/cacerts/` 迁移至位于 `/apex/com.android.conscrypt/cacerts/` 的只读 APEX 回环挂载目录中。常规挂载到 `/system` 分区的 Magisk 模块已无法影响 TLS 校验行为。MoveCertificate 通过专门针对 Conscrypt APEX 挂载命名空间创建覆盖挂载来解决这一问题。"
  - question: "可以在 Android 13 或更低版本上使用 MoveCertificate 吗？"
    answer: "不可以。在 Android 13 及更早版本中，系统证书目录仍位于 `/system/etc/security/cacerts/`。若设备为 Android 7 至 13，请改用 AlwaysTrustUserCerts 模块。"
---

## 概述

由 **ys1231** 开发的 **MoveCertificate** 专为解决 **Android 14** 在系统根证书信任机制上的破坏性架构变更而设计。

在 Android 14 中，Google 完成了核心系统安全组件向 Mainline APEX 模块的迁移，系统 CA 根证书目录被永久迁出 `/system/etc/security/cacerts/`，转而存放在 `com.android.conscrypt` APEX 的只读挂载文件系统中。受此影响，过去仅靠挂载 `/system` 目录生效的传统 Magisk 移动证书模块在 Android 14 上彻底失效。MoveCertificate 通过精细的挂载命名空间注入技术，重新打通了全局 SSL/TLS 流量抓取与代理信任链路。

---

## 技术架构与工作原理

### APEX 挂载命名空间注入

1. **证书扫描**：在系统早期启动阶段，MoveCertificate 会扫描存放于 `/data/misc/user/0/cacerts-added/` 目录下的用户已安装证书。
2. **构建临时合并目录**：模块创建一个临时目录，同时汇总系统原生 Conscrypt CA 证书以及用户新增的证书文件。
3. **APEX 命名空间覆盖挂载**：由于 APEX 挂载运行在各自独立的 Linux 挂载命名空间中，模块会在根命名空间内执行原生挂载指令：
   ```bash
   mount --bind /data/local/tmp/cacerts_merged /apex/com.android.conscrypt/cacerts
   ```
4. **Bionic 信任链传播**：当 Android 应用初始化 TLS 会话时，Bionic Conscrypt 加密引擎会直接从 APEX 挂载目录读取合并后的证书列表，从而在全局范围内信任代理 CA 根证书。

---

## 安装与使用步骤

1. 打开你的 Root 管理器（**Magisk**、**KernelSU** 或 **APatch**）。
2. 下载并刷入 `MoveCertificate-vX.zip` 模块压缩包。
3. 重启设备。
4. 通过系统常规路径安装代理 CA 根证书（如 Burp Suite、mitmproxy、Charles）：**设置（Settings）** → **安全（Security）** → **从存储设备安装（Install from storage）** → **CA 证书（CA Certificate）**。
5. 再次重启设备使开机脚本完成合并挂载。
6. 前往 **设置（Settings）** → **受信任的凭据（Trusted Credentials）** → **系统（System）** 选项卡验证：若你的代理证书已出现在系统证书列表中，即表示配置成功。
