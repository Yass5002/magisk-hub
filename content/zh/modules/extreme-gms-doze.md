---
id: "extreme-gms-doze"
title: "Extreme GMS Doze：Google Play 服务熄屏省电优化"
sidebarTitle: "Extreme GMS Doze"
description: "在设备熄屏期间智能挂起 Google Play 服务后台活动与唤醒锁，最大限度延长待机深度休眠时间。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Extreme GMS Doze Magisk 模块"
  - "Skyghost090 Extreme GMS Doze"
  - "熄屏暂停 Google Play 服务 Root"
  - "解决谷歌服务待机耗电 深度休眠"
  - "Extreme Doze 谷歌服务通知屏蔽"
prerequisites:
  - "Android 8.0 及以上系统"
  - "通过 Magisk（建议 v24.0+）、KernelSU 或 APatch 获取 Root 权限"
  - "设备已安装 Google Play 服务"
conflicts: []
configPaths:
  - "/data/adb/modules/extreme-gms-doze/"
features:
  - "亮熄屏同步 GMS 挂起：屏幕关闭后立即暂停非必要的 Google Play 服务后台任务"
  - "待机续航增强：抑制唤醒锁（Wakelock）频繁触发，让处理器在闲置时段稳定进入深度休眠状态"
  - "服务自动恢复：用户点亮或解锁屏幕时即刻恢复 Play 服务接口"
  - "安装即用免维护：全自动后台运行，无需手动配置后台白名单"
faq: []
---

## 概述

在运行谷歌移动服务（GMS）的已 Root Android 设备上，**Google Play 服务**（`com.google.android.gms`）往往是待机耗电的最大元凶。后台位置检测、统计分析上报、签入心跳包以及广告遥测服务会持续申请内核唤醒锁，阻碍 SoC 进入低功耗深度休眠（Deep Sleep）。

由 Skyghost090 开发的 **Extreme GMS Doze** 通过对 Google Play 服务强制施加休眠策略实现激进省电。每当屏幕关闭时，模块便会抑制活跃的 GMS 后台进程与唤醒锁，释放 CPU 集群进入休眠；当屏幕重新点亮时，所有服务功能即刻恢复正常。

## 熄屏拦截工作原理

原厂 Android 电池优化默认将 Google Play 服务排除在完整的 Doze 限制之外，Extreme GMS Doze 改变了这一行为：

1. **熄屏触发器**：后台事件监听器会实时感知屏幕熄灭与锁定状态。
2. **选择性挂起**：暂停非核心的 GMS 后台进程与轮询守护进程，阻断蜂窝网络与 Wi-Fi 下的频繁同步唤醒。
3. **进入深度休眠**：消除唤醒锁后，Linux 内核可顺利进入挂起模式（`suspend-to-RAM`），大幅降低待机掉电。
4. **亮屏瞬时唤醒**：屏幕亮起的瞬间，模块立即解除限制，让待处理的云端消息与后台数据无缝恢复同步。

## 消除 Play 服务异常通知提示

由于 Google Play 服务在熄屏期间会被短暂挂起，系统偶尔可能会弹出“Play 服务不可用”或“正在等待网络”的通知提示。

如需屏蔽此类瞬时提示（不影响正常应用通知）：
1. 打开 **设置** → **应用** → **Google Play 服务**。
2. 点击 **通知** → **通知类别**。
3. 找到 **Play 服务可用性（Play Services availability）** 类别并将其开关设为 **关闭**。

## 安装与配置

1. 下载 `Extreme-Gms-Doze` 的 `.zip` 发布包。
2. 打开 **Magisk Manager**、**KernelSU** 或 **APatch**。
3. 从本地存储刷入该模块并重启手机。
4. 让设备在夜间或闲置时段保持待机，随后可在电池监控工具（如 BetterBatteryStats 或 GSam）中查看显著提升的深度休眠比例。
