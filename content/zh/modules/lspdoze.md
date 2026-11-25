---
id: "lspdoze"
title: "LSPDoze：优化待机续航与解锁全屏常亮 AOD (com.op.lspdoze)"
description: "基于 LSPosed 的系统级待机优化模块，可在熄屏瞬间强制进入深度 Doze 模式以降低待机功耗，并支持开启全屏常亮息屏显示（AOD）。"
category: "xposed-runtime-hooks"
author: "ItosEO"
version: "5.4"
updatedAt: "2026-10-04"
compatibility: ["LSPosed"]
sidebarTitle: "LSPDoze 待机省电与全屏 AOD (com.op.lspdoze)"
tier: 1
searchQueries: []
prerequisites: []
conflicts: []
configPaths: []
features: []
faq: []
---

## 概述与系统架构

由知名 Android 系统优化研究者 ItosEO 开发的 **LSPDoze（`com.op.lspdoze`）** 是一款专注于解决 Android 待机掉电痛点并拓展息屏显示（AOD）能力的 LSPosed 模块。

标准 Android Doze 机制要求设备在熄屏后保持完全静止长达 30 至 60 分钟才会逐步进入深度打盹（Deep Doze）状态。在这段漫长的等待窗口期内，后台唤醒锁（Wakelock）、定时网络轮询警报以及传感器事件仍会持续消耗大量电量。LSPDoze 通过 Hook 系统核心服务 `DeviceIdleController` 及厂商电源管理服务（尤其针对 ColorOS、OxygenOS 与 realme UI 框架深度适配），实现在屏幕面板熄灭后立即触发向深度 Doze 状态的无缝切换。

## 安装包技术分析

对 4.4 MB 安装包（`162-5.4.apk`）的结构分析证实了其专用的系统框架 Hook 集成方案：

- **模块包名**：`com.op.lspdoze`
- **Hook 作用域目标**：`android`（系统框架 / Android OS 核心服务）。
- **系统版本支持**：Android 11 至 Android 15。
- **架构增强特性**：除通用的 AOSP Doze 挂钩外，还针对 OPPO / 一加 / 真我设备（OPlus 框架）提供了专项底层优化支持。

## 核心省电与显示增强功能

1. **熄屏瞬时深度 Doze**：跳过 Android 原生静止运动检测超时等待，在屏幕关闭数秒内直接将设备转入 Deep Sleep 深度睡眠状态。
2. **唤醒锁与后台对齐压制**：拦截非关键唤醒警报与后台同步任务，高效合并网络请求批次。
3. **OPlus 深度睡眠强化**：在 ColorOS / OxygenOS / realme UI 设备上强制调度原厂仅在超级省电模式下才启用的低功耗子系统休眠策略。
4. **强制解锁全屏 AOD**：解除厂商软件限制，在支持的 AMOLED 屏幕上开启不受 10 秒超时拘束的自定义全屏常亮息屏显示（Always-On Display）。

## 安装与配置

### 前置要求
- 已通过 Magisk、KernelSU 或 APatch 获取 Root 权限的设备。
- 已在 Zygisk 模式下运行的 **LSPosed 框架**。

### 第一步：安装 APK
下载并安装 `162-5.4.apk`。

### 第二步：在 LSPosed 中激活（系统框架作用域）
1. 打开 **LSPosed 管理器**。
2. 在模块列表中找到并点击 **LSPDoze**。
3. 打开模块启用开关。
4. 确认已在作用域（Scope）列表中勾选 **系统框架（`android`）**。

### 第三步：重启设备
由于 LSPDoze 直接 Hook 系统核心电源管理服务，配置完成后必须重启系统方可生效：
```bash
reboot
```

### 第四步：通过 Shell 验证效果
息屏等待约 20 秒后重新点亮屏幕，执行以下命令检查 DeviceIdle 状态：
```bash
dumpsys deviceidle
# 检查输出中的 mState 是否已处于 IDLE 或 IDLE_MAINTENANCE 状态
```

## 故障排查与白名单规则

- **即时通讯消息延迟**：若微信、Telegram 或 WhatsApp 等关键通讯应用出现后台推送延迟，请前往 **设置 > 应用 > 特殊应用权限 > 电池优化 > 不优化**，将对应应用加入系统电池优化白名单。
