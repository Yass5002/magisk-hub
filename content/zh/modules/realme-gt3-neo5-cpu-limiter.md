---
id: "realme-gt3-neo5-cpu-limiter"
title: "Realme GT3 与 GT Neo 5 CPU 限频器：骁龙 8+ Gen 1 功耗调优"
sidebarTitle: "真我 CPU 限频器"
description: "在真我 GT3 与 GT Neo 5 上自定义骁龙 8+ Gen 1 的 CPU 频率上限、节能调度器（Governor）与核心离线策略，显著延长日常续航时间。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "真我 GT3 CPU 限频 Magisk 模块"
  - "Realme GT Neo 5 降频省电"
  - "Quantom2 真我 CPU 限频器"
  - "骁龙 8+ Gen 1 降频锁频 Root"
  - "Android 关闭 CPU 核心省电"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "真我 GT3 或真我 GT Neo 5（高通骁龙 8+ Gen 1 芯片）"
conflicts:
  - "其他修改相同 sysfs 节点的内核锁频模块或 CPU 调优工具"
configPaths:
  - "/data/adb/modules/Realme-GT3-neo5-CPU-limiter/"
features:
  - "CPU 频率封顶：限制 Cortex-X2 超大核、Cortex-A710 大核与 Cortex-A510 小核集群的最高运行频率"
  - "节能调度策略：将当前 CPU 频率调节器切换为 Conservative 或 Powersave 省电模式"
  - "选择性核心离线：最多可彻底关闭 4 颗 CPU 核心，大幅降低轻度使用场景下的基础功耗"
  - "息屏核心休眠：在屏幕关闭时自动下线选定的高功耗大核，有效减少待机耗电"
  - "配置持久化：模块重新刷入或系统 OTA 升级后依然保留用户的自定义频率与核心配置"
---

## 概述

搭载在真我（Realme）GT3 与 GT Neo 5 上的高通骁龙 8+ Gen 1（SM8475）拥有极其强劲的运算性能。然而在网页浏览、聊天社交、音乐播放等日常轻负载场景下，其激进的升频机制与全核心调度往往会消耗远超实际需求的电量，造成机身发热增加并缩短亮屏续航时间（SOT）。

由 Quantom2 开发的 **Realme-GT3-neo5-CPU-limiter** 是一款面向 Magisk 与 KernelSU 的专用性能与功耗优化模块，允许真我 GT3 和 GT Neo 5 用户按需降频、切换节能调度器（Governor）以及关闭部分 CPU 核心。

## 核心调优机制

1. **频率封顶（Frequency Clamping）**：通过 `/sys/devices/system/cpu/cpufreq/` 节点，为 Cortex-X2 超大核与 Cortex-A710 性能核心集群设定硬性最高频率上限。
2. **调度器调整（Governor Adjustments）**：将默认的 interactive/schedutil 调度器切换为经过调校的 Conservative 或 Powersave 策略，避免后台微小负载波动就触发 CPU 飙升至峰值频率。
3. **核心离线（Core Offlining）**：以无侵入式（Systemless）方式停用最多 4 颗 CPU 核心，将八核处理器转化为高能效的四核或六核模式，实现日常重度续航保护。
4. **息屏休眠状态**：监听屏幕亮灭状态事件，在息屏瞬间自动将高功耗核心集群下线，几乎彻底消除待机期间的后台漏电功耗。

## 安装与配置

1. 从 GitHub Releases 下载最新的 `Realme-GT3-neo5-CPU-limiter_*.zip` 压缩包。
2. 在 **Magisk** 或 **KernelSU** 中刷入该模块。
3. 按照终端安装向导的交互提示，选择并配置你期望的最高频率与核心启用方案。
4. 重启设备以使节能限制生效。
