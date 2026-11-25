---
id: "hyperos-accessibility-fix"
title: "HyperOS Accessibility Fix：防止澎湃 OS 自动关闭无障碍服务"
sidebarTitle: "HyperOS Accessibility Fix"
description: "持续监听 logcat 系统事件，防止小米澎湃 OS 因激进后台省电策略强行停止应用而剥夺无障碍服务权限。"
category: "system-environment"
tier: 1
searchQueries:
  - "hyperos-accessibility-fix Magisk 模块"
  - "澎湃 OS 自动关闭无障碍服务"
  - "chkndrp hyperos-accessibility-fix"
  - "HyperOS 无障碍权限自动失效"
  - "小米澎湃 OS 无障碍保活模块"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "运行小米澎湃 OS（HyperOS）的小米、Redmi 或 POCO 设备"
conflicts: []
configPaths:
  - "/data/adb/modules/hyperos-accessibility-fix/"
  - "/data/adb/modules/hyperos-accessibility-fix/a11y_watchlist.txt"
features:
  - "自动保活权限：在后台应用被强行停止时阻止 Android 框架移除已授予的无障碍服务权限"
  - "动态监控列表同步：开机时将已启用的无障碍服务写入 `a11y_watchlist.txt`，并同步追踪用户在系统设置中的变更"
  - "轻量级 logcat 监听：以极低的 CPU 与电量开销实时捕获系统 `AccessibilityManagerService` 生命周期事件"
  - "超级省电模式防护：对抗小米 `LockScreenClean` 清理例程对无障碍权限的粗暴撤销"
  - "零配置开箱即用：自动维护状态并在重启后持续生效"
faq: []
---

## 概述

对于使用小米、Redmi 与 POCO 手机并运行澎湃 OS（HyperOS）的用户而言，系统频繁自动撤销无障碍服务权限是一大长期痛点。重度依赖自动化工具（如 Tasker、MacroDroid）、密码管理器（Bitwarden、1Password）或无障碍悬浮工具的用户，往往会发现后台无障碍服务在不知不觉中被系统关闭。

由 chkndrp 开发的 **hyperos-accessibility-fix** 直击澎湃 OS 导致该问题的底层机制，以无侵入式（Systemless）方案确保已配置的无障碍服务持续保持开启状态。

## 根因分析：`AccessibilityManagerService` 行为机制

在标准 Android 框架中，当托管无障碍服务的应用通过 `ActivityManager` 被强行停止（Force-stop）时，系统内部的 `AccessibilityManagerService` 会将该组件从 `Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES` 中移除。

原生 Android 在常规后台管理中极少触发彻底强行停止，但小米澎湃 OS 固件会在激进省电策略（尤其是 `LockScreenClean` 锁屏清理与开启超级省电模式）执行时触发硬性查杀：

```text
I ActivityManager: Force stopping com.urbandroid.lux appid=10415 user=0: LockScreenClean
D ActivityManager: Force removing proc 8855:com.urbandroid.lux:background/u0a415
```

由于澎湃 OS 强行将该组件从安全设置存储区中剥离，用户不得不反复进入系统设置手动重新开启授权。

## 模块解决方案

本模块在后台部署了一个轻量级监控守护进程：

1. **开机初始化**：系统启动时，服务通过 `settings get secure enabled_accessibility_services` 查询当前启用的无障碍服务，并将其记录至 `/data/adb/modules/hyperos-accessibility-fix/a11y_watchlist.txt`。
2. **事件监测**：守护进程实时监听系统框架的 logcat 事件。若用户手动在设置中变更无障碍开关，列表会同步更新；若服务因后台强行停止或省电清理事件被系统剥离，守护进程会立即捕获这次非预期移除。
3. **自动恢复**：模块随即把对应组件标识重新写入 `Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES`，确保无障碍服务无缝恢复运行。

## 安装与配置

1. 从 GitHub Releases 页面下载最新版 `hyperos-accessibility-fix.zip`。
2. 通过 **Magisk** 或 **KernelSU** 刷入该压缩包。
3. 重启设备。
4. 在 Android 系统设置中开启一次所需的无障碍服务，模块会自动将其加入 `/data/adb/modules/hyperos-accessibility-fix/a11y_watchlist.txt` 并实现持久化保活。
