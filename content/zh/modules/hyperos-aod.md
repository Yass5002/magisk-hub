---
id: "hyperos-aod"
title: "HyperOS AOD：澎湃 OS 增强版息屏显示与锁屏编辑器"
sidebarTitle: "HyperOS AOD"
description: "为所有小米澎湃 OS 设备解锁旗舰级息屏显示（AOD）样式、景深壁纸特效以及完整锁屏编辑器自定义功能。"
category: "customization-ui"
tier: 1
searchQueries:
  - "HyperOS AOD Magisk 模块"
  - "Kashi HyperOS AOD 锁屏编辑器"
  - "澎湃 OS 解锁锁屏个性化"
  - "小米澎湃息屏显示增强模块"
  - "红米解锁完整 AOD 息屏"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "运行小米澎湃 OS（HyperOS）的 Xiaomi、Redmi 或 POCO 设备"
  - "若运行 Android 14+ 国际版或国行 ROM，需先刷入 Core Patch 或 Apk Protection Patch 模块"
conflicts: []
configPaths:
  - "/data/adb/modules/hyperos-aod/"
features:
  - "解锁旗舰级 AOD：在被小米人为限制的中低端机型上解锁完整息屏时钟、环境小部件与主题样式"
  - "景深壁纸锁屏编辑器：启用澎湃 OS 景深人像时钟、字体排版样式与多图层锁屏布局"
  - "丝滑过渡动效：优化 AOD 息屏时钟、锁屏界面与系统桌面之间的视觉衔接动画"
  - "广泛硬件适配：突破旗舰与中端机型的市场分级限制，全面适配各类 AMOLED 屏幕设备"
  - "无损 Systemless 替换：以无侵入方式覆盖原厂 `com.miui.aod` 应用包"
faq: []
---

## 概述

小米澎湃 OS（HyperOS）带来了全新设计的锁屏个性化引擎与动态息屏显示（AOD）特效。然而，小米将这些旗舰特性——例如景深壁纸、突破 10 秒限制的持续息屏控制以及高级艺术排版时钟——人为限定在高端旗舰机型上。

由开发者 Kashi 通过 Mods-Center 维护的 **HyperOS-AOD** 是一款无系统分区修改（Systemless）增强模块，可将系统原厂 `com.miui.aod` 应用替换为完整解锁的增强版本，让任何运行澎湃 OS 的小米、Redmi 或 POCO 手机都能体验旗舰级锁屏编辑与无限制息屏显示功能。

## 已解锁特性

- **景深壁纸引擎**：支持将锁屏时钟字体置于人像主体、风景轮廓与自定义壁纸图层之后，呈现立体遮挡效果。
- **完整锁屏自定义**：解锁此前在入门级硬件上隐藏的全部经典、菱格与杂志锁屏模板。
- **无限制 AOD 息屏时钟**：提供丰富的指针表盘、数字时钟、个性签名及环境状态小组件。
- **细腻亮度与过渡动画**：消除从低亮度 AOD 状态点亮至锁屏界面时的亮度跳变与掉帧卡顿。

## 安装与前置要求

在 Android 14 及更新版本的澎湃 OS ROM 中，小米强制启用了严格的系统包签名校验机制，会阻止加载经过修改的系统 APK：

1. **前置条件**：若你的设备运行 Android 14+（国际版、欧洲版或国行 ROM），请先刷入 **Apk Protection Patch** 模块，或在 LSPosed 中启用 **Core Patch**。
2. 从项目的 GitHub Releases 页面下载最新版 `HyperOS_AOD_V*.zip`。
3. 打开 **Magisk** 或 **KernelSU**，从本地存储安装压缩包并重启设备。
4. 长按锁屏即可进入增强版锁屏编辑器，或前往 **设置 > 息屏与锁屏** 自定义显示效果。
