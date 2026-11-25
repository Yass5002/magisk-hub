---
id: "oosgms-optimiser"
title: "OOSGMS Optimizer：面向 OxygenOS 与 GMS 的隐私及省电优化模块"
sidebarTitle: "OOSGMS Optimizer"
description: "禁用 Google Play 服务（GMS）、氧 OS（OOS）以及主流第三方应用中的后台遥测追踪器、唤醒锁与冗余分析组件。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "OOSGMS-OPTIMISER Magisk 模块"
  - "氧 OS GMS 追踪拦截 Root 模块"
  - "epicmann24 OOSGMS-OPTIMISER 下载"
  - "谷歌服务 GMS 耗电严重修复 Magisk"
  - "一加 OxygenOS 精简追踪组件"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "运行氧 OS（OxygenOS）的一加手机或安装了 Google Play 服务的设备"
conflicts: []
configPaths:
  - "/data/adb/modules/oosgms-optimiser/"
features:
  - "全面屏蔽追踪器：禁用 Google Play 服务（GMS）与氧 OS（OOS）内的遥测接收器及数据分析组件"
  - "第三方应用去追踪：限制高遥测应用的后台追踪行为（涵盖 Instagram、TikTok、Facebook、Reddit、Telegram、Temu 与 X/Twitter）"
  - "降低待机耗电：阻止周期性唤醒锁与后台轮询闹钟持续唤醒 CPU"
  - "无损组件开关控制：通过 Android 包组件管理命令禁用服务，不删除任何关键系统二进制文件"
  - "安全卸载流程：内置专用 Action 恢复脚本（可在 KernelSU 或 MMRL 中执行），一键无损还原被禁用的组件"
faq: []
---

## 概述

Google Play 服务（GMS）与一加氧 OS（OxygenOS / OOS）等厂商系统在后台运行着大量诊断服务、数据上报组件与位置轮询接收器。长期运行下，这些后台任务极易陷入异常重试循环，导致待机功耗飙升，并阻碍设备进入 Linux 内核深度休眠状态。

由 epicmann24 开发的 **OOSGMS-OPTIMISER** 是一款专项优化模块，旨在禁用 Google Play 服务与氧 OS 中侵入式的遥测采集、追踪服务以及非必要的后台唤醒锁。

## 覆盖范围与目标应用

除静默核心 GMS 分析服务外，该模块还对常见存在重度后台遥测行为的第三方应用实施组件级禁用规则：
- **核心 Google 框架**：`com.google.android.gms`、`com.google.ar.core`、`com.google.android.projection.gearhead`（Android Auto）、`com.google.android.play.games`
- **社交与媒体应用**：Instagram（`com.instagram.android`）、TikTok（`com.zhiliaoapp.musically`）、Facebook（`com.facebook.katana`）、Reddit（`com.reddit.frontpage`）、Telegram（`org.telegram.messenger`）以及 X（`com.twitter.android`）
- **购物与其他应用**：Temu（`com.einnovation.temu`）、AliExpress（`com.alibaba.aliexpresshd`）、eBay（`com.ebay.mobile`）以及 Coinbase（`com.coinbase.android`）

## 安装与安全卸载

### 安装方法
1. 从 GitHub Releases 页面下载 `OOSGMS-OPTIMISER.zip`。
2. 通过 **Magisk** 或 **KernelSU** 刷入模块压缩包。
3. 重启设备即可生效。

### 安全卸载流程
由于该模块通过系统包管理器钩子禁用了特定的 Android 组件接收器，卸载前需先将对应组件状态完整还原：
1. 在 **KernelSU**（或 **MMRL** 模块管理器）中点击该模块，触发内置的恢复操作（Action）。
2. 待恢复脚本确认所有组件均已还原后，再按常规流程卸载模块并重启设备。
