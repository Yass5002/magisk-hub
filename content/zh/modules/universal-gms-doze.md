---
id: "universal-gms-doze"
title: "Universal GMS Doze：Google Play 服务深度休眠与电池优化"
sidebarTitle: "Universal GMS Doze"
description: "修补 Google Play 服务及其后台组件，使其纳入 Android Doze 电池优化机制，显著降低 Android 6 至 15+ 设备待机耗电。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Universal GMS Doze Magisk 模块"
  - "MarsPatrick Universal GMS Doze 下载"
  - "Google Play 服务电池优化 Root"
  - "强制 GMS 进入深度 Doze 休眠"
  - "KernelSU Universal GMS Doze WebUI"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "Android 6.0（API 23）至 Android 15+ 系统"
conflicts: []
configPaths:
  - "/data/adb/modules/universal-gms-doze/"
features:
  - "解除 Doze 白名单特权：将 Google Play 服务（`com.google.android.gms`）从系统强制电池优化豁免列表中移除"
  - "强制深度休眠：让 GMS 后台同步任务在手机静置息屏时严格遵循系统 Doze 空闲维护窗口"
  - "保留 FCM 推送通知：智能放行高优先级 Firebase Cloud Messaging 推送通道，确保即时通讯消息准时送达"
  - "适配 Android 15+ 新系统：由社区持续维护的现代分支，已针对新版 Android 框架与 KernelSU 做好兼容修补"
  - "内置 WebUI 控制面板：通过直观的网页交互界面随时调整优化规则并查看各后台进程的 Doze 状态"
---

## 概述

自 Android 6.0 Marshmallow 起，Google 引入了 **Doze 休眠模式**，这一系统级省电机制会在设备静置息屏时让后台应用进入休眠，并将网络请求打包合并至周期性维护窗口执行。然而颇具讽刺意味的是，Google 在系统底层将自家的 **Google Play 服务（GMS）** 框架硬编码进了永久电量白名单，导致 GMS 进程可以随时唤醒 CPU、发起网络握手与位置查询，成为许多设备夜间待机掉电严重的主要根源。

由 MarsPatrick 维护（基于 gloeyisk 原作分支并针对现代系统重构）的 **Universal GMS Doze** 是一款无侵入式模块，可将 Google Play 服务从系统强制电池优化豁免名单中剥离，使其能够与其他普通应用一样正常进入深度休眠。

## 工作原理

1. **移除权限白名单**：修改系统电源管理配置文件，撤销 GMS 永久免疫 Doze 休眠的系统级特权。
2. **同步任务合并调度**：将非关键的 Google 遥测上报、分析心跳包与后台位置查询延迟至设备处于亮屏活跃状态或标准 Doze 维护时间窗口期间再执行。
3. **关键通知无损保留**：高优先级的 Firebase Cloud Messaging（FCM）消息推送（例如 WhatsApp 来电或 Telegram 聊天消息）仍可按设计及时唤醒设备，不会漏接重要通知。

## 多 Root 框架与 WebUI 支持

- **广泛的生态兼容**：完美支持 **Magisk**、**KernelSU** 与 **APatch**。
- **交互式 WebUI**：在 KernelSU 与 APatch 中，你可以直接打开模块的 WebUI 面板，查看当前受优化的 GMS 组件列表并单独切换各个服务的豁免状态。

## 安装步骤

1. 从 GitHub Releases 下载最新的 `gms_*.zip` 模块压缩包。
2. 在你的 Root 管理器中刷入该模块。
3. 重启设备。
4. *（效果验证）*：前往**设置 > 应用 > 特殊应用权限 > 电池优化**，查看 Google Play 服务是否已显示为“已优化”或允许手动开启电池优化。
