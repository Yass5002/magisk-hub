---
id: "debugassistant"
title: "DebugAssistant：跨多次重启的自动化开机 Logcat 抓取与崩溃诊断工具"
sidebarTitle: "DebugAssistant"
description: "自动化 logcat 日志捕获工具，在系统早期启动阶段开始记录日志，并在三次轮转重启周期内持久保留诊断轨迹，便于崩溃排错。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "DebugAssistant Magisk 模块"
  - "ThePedroo DebugAssistant"
  - "Android Root 开机抓取 logcat"
  - "排查随机重启 卡米 Bootloop 日志"
  - "多周期重启 logcat 日志轮转"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "Android 8.0 及以上系统版本"
conflicts: []
configPaths:
  - "/data/adb/modules/debugassistant/"
features:
  - "开机自动记录：在服务初始化早期阶段即开始录制 logcat 数据流，无需连接电脑或开启 USB ADB 调试"
  - "三周期轮转保留：在 `DebugAssistant.log`、`DebugAssistant-Boot1.log` 与 `DebugAssistant-Boot2.log` 之间循环轮转日志"
  - "崩溃与 Bootloop 诊断：完整保存前几次启动轨迹，确保系统崩溃或意外 Panic 后的关键日志在下次重启后依然可读"
  - "自动脱敏过滤：在将追踪日志写入磁盘前自动过滤常见用户敏感令牌信息"
faq: []
---

## 概述

使用传统桌面端调试工具排查 Android 间歇性 System Server 崩溃（Panic）、随机内核重启或框架早期启动故障往往十分棘手。等开发者在设备重启后重新插上 ADB 数据线时，内存中活跃的 logcat 环形缓冲区早已被清空，导致致命异常的所有现场证据丢失。

由 ThePedroo 开发的 **DebugAssistant** 可将已 Root 的 Android 手机变为具备自记录能力的诊断设备。该模块在 Magisk/KernelSU 初始化的最早阶段便在后台静默运行，将 logcat 输出实时写入持久闪存中，并连续滚动保留最近三个启动周期的日志存档。

## 三次启动轮转保留架构

为确保诊断日志在你有机会查看前不会被覆盖，DebugAssistant 采用循环日志轮转机制：

- **`DebugAssistant-Boot2.log`**：最近一次（即当前）系统启动期间抓取的日志。
- **`DebugAssistant-Boot1.log`**：上一次启动周期期间抓取的日志。
- **`DebugAssistant.log`**：最早保留的两轮启动前的日志文件。

连续启动三次后，系统会自动清理最旧的归档文件。这种设计既能避免诊断记录过度占用闪存空间，又能确保崩溃重启后的现场数据得到妥善保存。

## 常见使用场景

- **随机内核重启排查**：精确定位触发硬件看门狗（Watchdog）重启的系统服务、Vendor HAL 或后台进程。
- **问题模块故障诊断**：排查新刷入的个性化模块时，查看 Zygote 崩溃前一刻究竟是哪个环节出错。
- **离线外场测试**：无需随身携带笔记本电脑，即可在移动场景下实时捕获应用闪退与框架层异常日志。

## 安装与日志提取

1. 下载 `DebugAssistant` 的 `.zip` 压缩包，并通过 **Magisk** 或 **KernelSU** 刷入。
2. 重启设备，日志记录将自动启动。
3. 如需查看或提取已捕获的日志，请使用带 Root 权限的文件管理器或终端进入模块目录：
   ```bash
   su -c ls -l /data/adb/modules/debugassistant/
   ```
4. 直接检索最新一次启动日志中的致命错误：
   ```bash
   su -c cat /data/adb/modules/debugassistant/DebugAssistant-Boot2.log | grep -E "FATAL|AndroidRuntime"
   ```
