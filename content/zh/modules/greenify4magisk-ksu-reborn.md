---
id: "greenify4magisk-ksu-reborn"
title: "Greenify4Magisk/KSU Reborn：系统特权应用集成与 Boost 模式解锁"
sidebarTitle: "Greenify Reborn"
description: "无侵入式将绿色守护（Greenify）挂载至 /system/priv-app/，跨 Magisk、KernelSU 与 APatch 解锁 Boost 模式与特权级后台应用休眠。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "greenify4magisk-ksu-reborn"
  - "Drsexo 绿色守护重生版下载"
  - "开启绿色守护 Boost 模式 Root"
  - "绿色守护系统特权化 Magisk 模块"
  - "KernelSU 自动后台休眠应用"
prerequisites:
  - "Android 8.0 至 Android 14+ 系统"
  - "通过 KernelSU、Magisk 或 APatch 获取 Root 权限"
  - "设备已安装 Greenify（绿色守护）应用"
conflicts: []
configPaths:
  - "/data/adb/modules/greenify4magisk-ksu-reborn/"
features:
  - "无侵入式特权应用挂载：将 Greenify 绑定挂载至 /system/priv-app/，直接赋予核心系统级进程控制权限"
  - "激活 Boost Mode™：无需安装传统 Xposed 框架即可开启特权休眠 Hook 能力"
  - "后台应用自动冻结：熄屏后平稳将非活跃应用转入休眠状态，减少后台唤醒"
  - "全平台 Root 引擎兼容：针对 Magisk、KernelSU 与 APatch 完成适配验证并持续维护"
faq: []
---

## 概述

多年来，**Greenify（绿色守护）** 一直是 Android 电池优化与后台应用管理的标杆工具。然而随着现代 Android 权限收紧，普通用户安装的应用若不每次恢复出厂后繁琐地通过 ADB 手动授权，便无法强力冻结后台任务或监听进程生命周期事件；同时，绿色守护标志性的“Boost 模式”在早期也高度依赖 Xposed 框架。

由 Drsexo 开发的 **Greenify4Magisk/KSU Reborn** 让绿色守护重新融入现代 Root 生态。该模块通过无系统分区修改（Systemless）方式将应用挂载至 Android 系统特权目录（`/system/priv-app/`），自动为绿色守护授予完整系统平台特权权限，在 **KernelSU**、**Magisk** 与 **APatch** 上无缝解锁 Boost 模式与自动化后台休眠。

## 系统特权架构优势

当作为系统特权应用挂载后，绿色守护将获得以下 Android 内部系统权限：
- **`android.permission.DUMP`**：允许绿色守护直接从 `ActivityManager` 读取电池统计与进程实时状态。
- **`android.permission.PACKAGE_USAGE_STATS`**：零轮询延迟感知应用何时退入后台。
- **`android.permission.WRITE_SECURE_SETTINGS`**：修改设备空闲参数，使休眠动作与熄屏状态精准同步。
- **解锁 Boost Mode™**：通过底层系统服务直接执行休眠控制，彻底摆脱模拟无障碍点击屏幕的繁琐流程。

## 安装与配置

1. 在设备中安装官方版 Greenify（绿色守护）应用。
2. 从 GitHub 发布页下载 `Greenify4Magisk-KSU-Reborn` 的 `.zip` 安装包。
3. 在 **KernelSU**、**Magisk** 或 **APatch** 中刷入该模块。
4. 重启手机。
5. 打开绿色守护，应用将自动识别其系统特权身份并激活 Boost 模式。
6. 按需勾选需要管理的应用（社交软件、游戏、购物应用等），即可开启自动化后台休眠。
