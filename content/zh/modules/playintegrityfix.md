---
id: "playintegrityfix"
title: "PlayIntegrityFix (PIF)：原生 Zygisk 设备完整性认证修复模块"
sidebarTitle: "PlayIntegrityFix"
description: "社区主流维护的 PlayIntegrityFix 分支，在现代 Android 上通过 GMS 属性伪装恢复 Play Integrity 设备认证通过状态。"
category: "root-management"
tier: 1
searchQueries:
  - "PlayIntegrityFix 官方下载"
  - "playintegrityfix kowx712 配置"
  - "Magisk 修复 MEETS_DEVICE_INTEGRITY"
  - "Play Integrity 过检测模块 2026"
prerequisites:
  - "Magisk 26.0+（需开启 Zygisk），或 KernelSU / APatch 搭配 Zygisk Next"
  - "设备具备有效网络连接，用于首次与 GMS 进行密钥协商"
conflicts:
  - "osm0sis/PlayIntegrityFork（二选一使用，严禁同时安装两个版本）"
  - "过时的旧版 SafetyNet Fix 模块（请务必卸载）"
configPaths:
  - "/data/adb/pif.json"
  - "/data/adb/modules/playintegrityfix/"
features:
  - "通过 Zygisk 自动向 GMS DroidGuard 认证服务进程注入伪装逻辑"
  - "内置经过验证且尚未被吊销的认证设备指纹配置"
  - "兼容 playcurlNEXT 等自动化脚本，支持一键更新设备指纹"
  - "纯轻量级原生二进制实现，无后台常驻 CPU 或电量开销"
faq:
  - question: "PlayIntegrityFix 和 PlayIntegrityFork 有什么区别？"
    answer: "PlayIntegrityFix 侧重开箱即用的标准化体验，内置调校好的设备指纹配置并经过广泛社区测试；而 osm0sis 维护的 PlayIntegrityFork 为进阶用户提供了更细粒度的 `pif.json` 多字段手动覆盖能力。"
  - question: "使用此模块时，需要把 Google Play 服务加入 Magisk 排除列表吗？"
    answer: "当 Magisk 开启了“遵守排除列表（Enforce DenyList）”时，绝对不要把 `com.google.android.gms` 加入排除列表。一旦 Magisk 将 GMS 与 Root 完全隔离，Zygisk 就无法把本模块的钩子注入到 `com.google.android.gms.unstable` 进程中。"
---

## 概述

由 **KOWX712** 在上游项目归档后接手维护的 **PlayIntegrityFix**（简称 **PIF**），是目前在 Magisk、KernelSU 与 APatch Root 环境中修复 `MEETS_DEVICE_INTEGRITY` 认证最主流的社区标准模块。

Google Play Integrity API 是银行类应用、生物识别安全令牌、移动支付工具（Google Wallet）以及 DRM 加密游戏用来检测系统完整性的核心门禁。解锁 Bootloader 后，硬件加密校验会暴露设备未锁定状态；PlayIntegrityFix 通过引导 DroidGuard 回退至软件验证模式，并将关键系统属性伪装为已认证的 OEM 出厂参数，从而绕过检测。

---

## 技术架构与工作原理

### 完整性认证拦截流程

1. **Zygote 进程孵化识别**：每当应用请求 Play Integrity 校验时，Google Play 服务会拉起专门的检测子进程 `com.google.android.gms.unstable`。
2. **`libc` 系统属性 Hook**：PlayIntegrityFix 挂钩 Android 原生属性读取接口（`__system_property_get` 与 `__system_property_read_callback`）。
3. **精准按需伪装**：仅当 DroidGuard 引擎查询以下属性时，模块才会在内存中拦截并返回合规的认证设备参数：
   - `ro.product.model`
   - `ro.product.brand`
   - `ro.build.fingerprint`
   - `ro.build.version.security_patch`
   设备上的其他常规应用仍读取真实的机型信息，因此不会对相机算法、屏幕色彩校准或原厂桌面产生任何副作用。

---

## 安装与配置步骤

1. 打开你的 Root 管理器（**Magisk App**、**KernelSU App** 或 **APatch**）。
2. 确认 Zygisk 运行环境已就绪：
   - **Magisk**：在设置中启用 **Zygisk**。
   - **KernelSU / APatch**：确保模块列表中已安装并启用 **Zygisk Next**。
3. 刷入 `PlayIntegrityFix_vX.zip` 安装包并重启手机。
4. 从 Google Play 商店下载完整性检测工具（例如 *Play Integrity API Checker*）。
5. 点击 **Check Integrity**，若配置正常，**MEETS_BASIC_INTEGRITY** 与 **MEETS_DEVICE_INTEGRITY** 均会显示绿色通过。

---

## 维护有效的设备指纹

Google 会定期拉黑并吊销公开模块中广泛流传的开源设备指纹。

当发生指纹封禁导致认证降级时，可按以下方式更新：
1. 从未 Root 的官方认证设备提取（或借助 `playcurlNEXT` 等工具获取）一份干净可用的设备指纹。
2. 将属性内容写入 `/data/adb/pif.json`。
3. 终止 Google Play 服务检测进程使新配置立即生效：
   ```bash
   su -c "killall com.google.android.gms.unstable"
   ```
4. 重新检测 Play Integrity 认证状态。
