---
id: "zygisk-cacerts"
title: "Zygisk CAcerts：现代 AOSP 系统根证书库同步注入模块"
sidebarTitle: "Zygisk CAcerts"
description: "由 vvb2060 开发的无侵入式安全工具模块，使用上游 AOSP 最新 CA 根证书更新 Android 7 至 16 的系统根证书库，全面支持 16KB 内存页。"
category: "security-certificates"
tier: 1
searchQueries:
  - "Zygisk CAcerts vvb2060 下载"
  - "Magisk 更新 Android 系统根证书"
  - "AOSP ca-certificates 更新模块"
  - "Zygisk 16KB 内存页根证书"
  - "修复 Android 老系统根证书过期"
prerequisites:
  - "已获取 Root 权限的 Android 7.0 至 Android 16 设备"
  - "Magisk、KernelSU 或 APatch"
  - "已在 Root 管理器中启用 Zygisk"
conflicts: []
configPaths:
  - "/data/adb/modules/zygisk_cacerts/"
features:
  - "上游 AOSP 根证书同步：使用官方上游 AOSP 证书归档替换老旧或已过期的系统根证书"
  - "完善适配现代硬件架构：全面支持 ARM64、RISC-V（`riscv64`）以及现代 16KB 内核内存页对齐"
  - "SELinux 上下文修复：在旧版 Android（Android 10 以前版本）上自动应用正确的安全上下文标签"
  - "零网络依赖：内置干净且经过校验的完整证书包，无需动态联网下载即可工作"
faq: []
---

## 概述

Zygisk CAcerts 由知名 Android 安全研究者 vvb2060 开发，可将 Android 系统的根证书信任库（`/system/etc/security/cacerts`）更新为来自上游 Android 开源项目（AOSP）代码树的最新官方证书集合。

随着 Android 设备逐渐老化并停止接收厂商提供的官方月度系统更新，设备内预置的根证书颁发机构（CA）证书会陆续过期或被安全联盟吊销（例如旧版 Let's Encrypt 或 Sectigo 交叉签名证书的弃用）。当设备的信任库过时后，访问现代 HTTPS 网站、安全银行 API 以及建立 VPN 连接时便会频繁出现 SSL/TLS 握手失败。Zygisk CAcerts 通过在系统早期启动阶段干净地挂载现代可信根证书库，彻底解决这一难题。

## 前置要求与兼容性

- **Android 版本**：广泛兼容 Android 7.0（Nougat）至 Android 16 系统。
- **Root 框架**：Magisk、KernelSU 或 APatch，且需**启用 Zygisk**。
- **硬件架构**：支持 ARM、ARM64、x86 以及 **RISC-V（`riscv64`）**，同时兼容现代 **16KB 内存页大小（16KB Page Size）**内核。

目前暂无已知的模块冲突。

## 核心架构与特性

### 1. 直连上游证书源同步
模块直接从官方 [AOSP ca-certificates 代码仓库](https://android.googlesource.com/platform/system/ca-certificates/)提取根证书库。每个发布版本均同步包含最新的密码学信任标准，涵盖新增的根证书以及已被吊销的问题 CA 清理。

### 2. 底层挂载与安全上下文修复
- 利用早期启动脚本（`post-fs-data.sh`）将更新后的证书目录挂载覆盖到 `/system/etc/security/cacerts`。
- 自动跨版本强制应用合法的 SELinux 文件标签（`system_file`），避免在 Android 9 及更早版本上触发 AVC 拒绝日志，防止网络守护进程因权限受阻而无法读取证书。

## 安装与验证

1. 从项目仓库的 Releases 页面下载最新的 `zygisk_cacerts-*-release.zip` 安装包。
2. 通过 Magisk、KernelSU 或 APatch 刷入该模块。
3. 重启设备。
4. 激活后的模块资源文件存放于：
   ```bash
   /data/adb/modules/zygisk_cacerts/
   ```

### 通过 Shell 验证生效状态

执行以下命令确认新版证书库已正确挂载且可读：
```bash
su -c "ls -la /system/etc/security/cacerts | head -n 10"
```
输出列表中的证书文件将显示对应当前 AOSP 发布周期的全新时间戳。

## 故障排查

- **未启用 Zygisk 导致不生效**：如果发现模块似乎没有起作用，请进入 Root 管理器设置确认 Zygisk 开关已打开，随后重启设备。
- **自定义用户证书与系统证书的区别**：请注意，本模块仅用于更新**系统**自带的根证书库。如果你需要让系统信任个人调试用的中间人（MITM）抓包证书（如 Charles Proxy 或 Burp Suite），请将你的代理证书存放到 `/data/local/tmp` 或配合专门的用户证书注入模块使用。
