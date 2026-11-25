---
id: "antisafetycore"
title: "AntiSafetyCore：阻止 Google 静默安装 SafetyCore 与 Key Verifier"
sidebarTitle: "AntiSafetyCore"
description: "通过部署签名不匹配的占位 APK，阻止 Google Play 服务在后台静默安装 Android System SafetyCore 与 Key Verifier 遥测组件。"
category: "security-certificates"
tier: 1
searchQueries:
  - "antisafetycore magisk 模块"
  - "astoritin antisafetycore 下载"
  - "root 阻止谷歌安装 safetycore"
  - "magisk 禁用 android system key verifier"
  - "禁止 play 服务静默安装 apk"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "保持标准 Android 应用签名校验机制完好的 ROM"
  - "在 KernelSU（内核版本 ≥ 22098）或 APatch（内核版本 ≥ 11170）上使用 `systemize` 模式时，需配合 Metamodule"
conflicts:
  - "核心破解（Core Patch）、幸运破解器（Lucky Patcher）或任何禁用 Android APK 签名校验的模块（会导致 Play 服务直接覆盖占位应用）"
configPaths:
  - "/data/adb/anti_safetycore/"
  - "/data/adb/anti_safetycore/keep_running"
  - "/data/adb/anti_safetycore/systemize"
  - "/data/adb/modules/anti_safetycore/"
features:
  - "签名冲突屏障：安装与目标包名相同但使用任意私钥签名的空白占位 APK，从而拒绝静默安装更新"
  - "精准组件压制：定向拦截 Android System SafetyCore 与 Android System Key Verifier"
  - "后台常驻守护进程（`keep_running`）：持续监控包状态，一旦发现 Play 服务尝试清理占位包即刻重新注入"
  - "无系统分区修改系统化（`systemize`）：将占位包挂载至系统分区路径，防止用户态权限将其卸载"
faq: []
---

## 概述

在近期的 Android 版本中，Google Play 服务开始在未经通知或用户同意的情况下，在后台静默下载并安装专有系统组件。其中最受关注的是 **Android System SafetyCore**（`com.google.android.safetycore`）与 **Android System Key Verifier**（`com.google.android.contactkeys`）。尽管它们的命名酷似操作系统基础核心组件，但这些后台二进制程序实则用于执行持续遥测、端侧内容扫描与身份核验。

由 Astoritin 开发的 **AntiSafetyCore** 专门用于彻底阻断这一静默安装行为。它巧妙利用了 Android 操作系统的一项底层安全铁律：如果新安装包与已安装应用包名相同但加密签名不一致，包管理器将严厉拒绝安装或覆盖更新。

## 工作原理

1. **占位包注入**：初始化阶段，AntiSafetyCore 会安装对应 Google 目标包名的良性空白占位 APK。这些占位包均使用模块内置的自定义私钥进行签名，与 Google 官方签名完全不同。
2. **安装拦截锁定**：当 Google Play 服务试图在后台自动安装官方版 SafetyCore 或 Key Verifier APK 时，Android 的 `PackageManagerService` 会检测到签名不匹配，并立即以 `INSTALL_FAILED_UPDATE_INCOMPATIBLE` 错误中止安装。
3. **遥测机制失效**：由于占位包已抢占了目标包名命名空间，任何 Google 专有后台服务或工作线程均无法被拉起运行。

## 严重冲突警告：禁用签名校验模块

> [!WARNING]
> **AntiSafetyCore 与核心破解（Core Patch）、幸运破解器（Lucky Patcher）或任何关闭 Android 签名校验的 Xposed 模块从根本上互不兼容。**

如果设备关闭了应用签名校验，Android 包管理器就会放行 Google Play 服务用官方 APK 直接覆盖掉占位应用，导致本模块的防护机制完全失效。

## 配置标志位

从 1.3.0 版本起，AntiSafetyCore 支持模块化运行模式。你可以在配置目录 `/data/adb/anti_safetycore/` 中创建无扩展名的空触发文件来切换运行行为：

### 1. `keep_running`（守护进程哨兵模式）
默认情况下，模块仅在开机时执行一次检查。如果 Google Play 服务在系统运行期间设法强制卸载了用户态占位包，防护可能会在下次重启前出现空窗期。
- 创建文件 `/data/adb/anti_safetycore/keep_running` 可指示模块拉起轻量级后台监控守护进程。
- 守护进程会定期轮询应用包状态，一旦检测到占位包被移除或校验异常，立即重新安装占位包。

### 2. `systemize`（系统级挂载模式）
- 创建 `/data/adb/anti_safetycore/systemize` 后，模块会将占位 APK 直接挂载到系统分区路径，而非作为普通用户应用安装。
- 当以无系统分区修改（Systemless）方式作为系统应用挂载时，Google Play 服务将不具备卸载或替换它们的权限。
- **KernelSU 与 APatch 特别说明**：如果运行环境为 KernelSU（内核版本 ≥ 22098）或 APatch（内核版本 ≥ 11170），必须安装官方 **Metamodule** 才能启用系统级挂载功能。若未安装 Metamodule，占位包将自动回退为标准用户应用安装模式。

## 安装与验证

1. 确认设备中未启用任何绕过签名校验的模块。
2. 在 Magisk、KernelSU 或 APatch 中刷入 AntiSafetyCore `.zip` 压缩包。
3. 重启设备。
4. 在 ADB 或 Root 终端中验证防护状态：
   ```bash
   su -c pm list packages -f | grep safetycore
   ```
   输出中应显示占位 APK 的安装路径。
5. *（可选）* 开启守护进程持续监控：
   ```bash
   su -c touch /data/adb/anti_safetycore/keep_running
   ```
