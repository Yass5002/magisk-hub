---
id: "hyperos-app-vault"
title: "HyperOS App Vault：解锁旗舰小部件、毛玻璃模糊与高端特性"
sidebarTitle: "HyperOS App Vault"
description: "为所有小米设备开启澎湃 OS 负一屏（App Vault）毛玻璃模糊背景、高端旗舰小部件以及机型特性伪装功能。"
category: "customization-ui"
tier: 1
searchQueries:
  - "HyperOS App Vault Magisk"
  - "Kashi HyperOS 负一屏模块"
  - "解锁澎湃负一屏小部件和模糊"
  - "澎湃 OS 负一屏旗舰功能"
  - "小米智能助理毛玻璃效果"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "运行小米澎湃 OS（HyperOS）的 Xiaomi、Redmi 或 POCO 智能手机"
  - "Android 14+ 国际版或国行固件需先安装 Apk Protection Patch 或 Core Patch"
conflicts: []
configPaths:
  - "/data/adb/modules/hyperos-app-vault/"
features:
  - "毛玻璃模糊背景：为负一屏全套原生小部件卡片开启现代磨砂玻璃背景模糊效果"
  - "高端机型特性伪装：内置开关可让应用识别为顶级旗舰，从而解锁旗舰专属小部件与快捷卡片"
  - "完整系统小部件库：开放全套时钟、天气、电池及效率快捷工具小部件"
  - "丝滑滚动物理曲线：全面优化小部件信息流中的滑动阻尼与帧率稳定性"
  - "整合 Xiaomi.eu 底层优化：融合 Xiaomi.eu 社区版的多语言优化与精简卡片资源"
faq: []
---

## 概述

小米智能助理 / 负一屏（`com.miui.personalassistant`，国际版称为 App Vault）是澎湃 OS 与 MIUI 桌面左滑呼出的辅助信息面板，承载交互式小部件、快捷开关、健康数据与信息卡片。但在中低端机型上，小米通常会削减背景高斯模糊效果（改为纯灰或纯色不透明面板），并隐藏仅面向旗舰机型开放的高级交互组件。

由开发者 Kashi 通过 Mods-Center 修改维护的 **HyperOS-App-Vault** 是一款 Systemless 增强模块，基于优化后的 Xiaomi.eu 版本构建，为你无侵入地安装功能全面解锁的负一屏应用。

## 核心增强功能

- **磨砂毛玻璃模糊**：恢复小部件容器的动态背景模糊渲染，让桌面壁纸色彩柔和透出卡片底层。
- **高端特性开关**：内置开关可将当前设备伪装为小米顶级旗舰型号，一键开启隐藏的小部件样式、复杂数据可视化组件与电池监控磁贴。
- **自定义模糊度**：支持直接在负一屏设置内微调模糊透明度与高斯模糊半径。
- **流畅滑动动效**：消除从默认系统桌面滑入或滑出负一屏界面时的掉帧卡顿现象。

## 安装指南

1. **Android 14+ 前置要求**：若设备运行 Android 14 及以上版本的国际版或国行 ROM，请先刷入 **Apk Protection Patch** 以允许加载修改版系统应用包。
2. 从项目发布页下载 `HyperOS_AppVaultV*.zip`。
3. 打开 **Magisk Manager** 或 **KernelSU**，刷入模块压缩包并重启手机。
4. 在主屏幕向右滑动或双指捏合/长按桌面壁纸，即可体验丰富解锁后的全新小部件集合。
