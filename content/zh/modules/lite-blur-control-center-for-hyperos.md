---
id: "lite-blur-control-center-for-hyperos"
title: "Lite Blur Control Center for HyperOS：兼顾毛玻璃美感与流畅度"
sidebarTitle: "HyperOS 轻量模糊控制中心"
description: "为小米 HyperOS 控制中心与电源菜单恢复毛玻璃模糊效果，同时禁用高开销的实时着色器管线，防止中低端机型卡顿掉帧。"
category: "customization-ui"
tier: 1
searchQueries:
  - "HyperOS 控制中心模糊 Magisk 模块"
  - "fakerieh lite blur hyperos 下载"
  - "小米 HyperOS 控制中心灰底修复"
  - "红米 POCO 通知栏开启模糊不卡顿"
  - "HyperOS 轻量级高斯模糊模块"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "运行小米 HyperOS 的 Xiaomi、Redmi 或 POCO 智能手机"
conflicts:
  - "其他控制中心模糊模块或完整重度模糊补丁"
configPaths:
  - "/data/adb/modules/Lite-Blur-Control-Center-for-HyperOS/"
features:
  - "性能优先的模糊引擎：在不大量消耗 GPU 算力的情况下，将扁平灰底矩形替换为美观的半透明磨砂玻璃效果"
  - "跟手即达的滑动响应：移除拖沓的展开延迟与沉重的下拉动画，实现控制中心瞬时呼出"
  - "磨砂电源菜单：在 HyperOS 重启与关机菜单背后渲染顺滑的背景模糊效果"
  - "专为中低端芯片优化：针对入门及中端 Helio、天玑（Dimensity）与骁龙（Snapdragon）芯片深度调优"
  - "无系统分区修改（Systemless）叠加：通过运行时资源叠加（RRO）生效，不破坏系统分区完整性"
faq: []
---

## 概述

在运行 HyperOS 的中低端智能手机上，小米会自动精简控制中心与通知栏的毛玻璃模糊效果。与旗舰机型精致的半透明视觉体验不同，这类设备默认只能看到呆板单调的纯灰背景。虽然常规的强开模糊模块可以强制恢复完整的旗舰级模糊，但往往会带来严重掉帧、界面卡顿以及触摸响应延迟。

由 fakerieh 开发的 **Lite-Blur-Control-Center-for-HyperOS** 正是为解决这一痛点而打造的轻量优化修改模块。它在恢复磨砂背景玻璃质感的同时，刻意禁用了高负载的实时着色器计算，从而在性能有限的硬件上依然提供稳定流畅的 60/120 FPS 体验。

## 核心优化

- **无实时着色器（No Real-Time Shaders）**：模块不再对底层壁纸逐帧执行连续多通道高斯模糊，而是采用经过优化的静态或轻量渲染技巧来模拟景深质感。
- **手势更迅捷**：精简展开动画流程，确保下滑手势触发后通知栏与快捷开关面板能够瞬时呈现。
- **克制均衡的界面覆盖**：为电源菜单与控制中心面板启用模糊，同时保持音量条界面简洁高效、响应迅速。
- **极低的内存与 CPU 占用**：避免 `com.android.systemui` 出现后台内存膨胀，减少触发系统激进低内存杀手（LMK）机制的风险。

## 安装步骤

1. 从 GitHub Releases 下载最新的 `Lite.Blur.HyperOS.*.zip` 安装包。
2. 打开 **Magisk 管理器** 或 **KernelSU 管理器**。
3. 进入 **模块 > 从本地安装**，选择该 zip 压缩包并刷入。
4. 重启设备以应用全新的界面样式。
