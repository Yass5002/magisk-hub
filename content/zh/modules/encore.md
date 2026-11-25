---
id: "encore"
title: "Encore Tweaks：动态游戏性能与电池调度优化器"
sidebarTitle: "Encore Tweaks"
description: "智能性能管理引擎，可在游戏时动态释放极限帧率，并在日常使用中精细控电以延长电池续航。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Encore Tweaks Magisk 模块"
  - "Rem01Gaming Encore 下载"
  - "安卓游戏调度优化模块"
  - "Encore WebUI MMRL 配置"
  - "Encore Tweaks KernelSU 教程"
prerequisites:
  - "Android 8.0 及以上系统"
  - "Magisk、KernelSU 或 APatch"
  - "兼容独立 WebUI 管理器：KsuWebUI、WebUI-X 与 MMRL"
conflicts:
  - "可能与第三方 CPU/GPU 锁频模块或激进后台查杀类模块存在冲突"
configPaths:
  - "/data/adb/modules/encore/"
  - "/data/adb/modules/encore/config/"
features:
  - "动态负载缩放：游戏场景无缝拉升硬件频率，阅读等静态场景自动降频省电"
  - "现代化 WebUI 面板：通过 KsuWebUI 或 MMRL 自定义调度模式并微调温控缓解策略"
  - "设备缓解引擎：内置分机型温控缓解规则，防止持续高负载下出现热失控与严重过热"
  - "低待机功耗：精细优化深度休眠唤醒与 cpufreq 调度器响应策略"
  - "Action 按钮集成：支持直接从 Root 管理器界面快速切换模式与查看状态诊断"
faq:
  - question: "Encore Tweaks 需要刷入第三方自定义内核吗？"
    answer: "不需要。Encore Tweaks 基于标准 Linux 内核 sysfs 接口与 Android Power HAL 接口运行，在原厂内核与自定义内核上均能带来明显的性能与续航改善。"
  - question: "在 Magisk 下如何打开 Encore Tweaks 的控制面板？"
    answer: "由于官方版 Magisk 不提供原生 WebUI 环境，Magisk 用户可以借助 MMRL 或 WebUI-X 等独立 WebUI 宿主应用来管理和配置 Encore Tweaks。"
---

## 概述

由 **Rem01Gaming** 开发的 **Encore Tweaks** 是一款兼顾游戏流畅度与日常续航效率的动态 Android 性能优化模块。

Encore Tweaks 不会像传统方案那样一味强制硬件长期高频锁频（导致电量飞速消耗并引发温控降频），而是根据当前前台应用的实际需求持续动态调整 CPU、GPU 与内存总线参数。在游戏过程中，它确保帧率输出稳定连贯；在浏览社交软件或电子书阅读时，则优先保障低功耗与续航表现。

---

## 技术架构与工作原理

### 自适应能效调度与硬件 Governor

Encore Tweaks 协同工作于 Linux 内核调度器（Governor）与 Android 运行时框架之间：

1. **前台场景识别**：自动识别游戏包名及高负载应用，触发优化后的交互式调度器参数并适当提高最低频率下限。
2. **设备缓解引擎**：依托 `/data/adb/modules/encore/config/device_mitigation.json` 平滑调节持续功耗上限，避免触及激进的硬件温控降频阈值。
3. **Cpuset 与内存管理**：优化低内存查杀（LMK）阈值与虚拟内存缓存参数，减少应用切换时的卡顿掉帧。

---

## 安装与配置

1. 下载最新版的 `Encore-Tweaks-*.zip` 发布包。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入模块。
3. 重启设备。
4. 打开 Root 管理器的 WebUI（或在 Magisk 下打开 **MMRL**）完成初始性能配置。

---

## 配置与日常使用

- **性能模式**：可在省电（Battery Saver）、均衡（Balanced）与游戏（Gaming）三种配置模式间自由切换。
- **WebUI 高级微调**：通过内置 WebUI 控制面板精细调整 GPU 调度器、CPU 簇升频速率与内存管理参数。

---

## 故障排查与常见问题

- **异常高耗电**：若发现耗电异常升高，请检查是否同时启用了其他性能增强模块或竞争性的温控移除模块。
