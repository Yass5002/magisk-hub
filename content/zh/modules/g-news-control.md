---
id: "g-news-control"
title: "G-News Control：通过 Action 按钮与命令行开关 Google Discover 负一屏"
sidebarTitle: "G-News Control"
description: "在不禁用 Google 应用或破坏语音助手功能的前提下，有选择地启用或关闭主屏幕最左侧的 Google Discover 信息流。"
category: "customization-ui"
tier: 1
searchQueries:
  - "G-News Control Magisk 模块"
  - "mango0oo G-News Control 下载"
  - "Root 关闭 Google Discover 负一屏"
  - "gnc switch 命令 Android"
  - "KernelSU Action 按钮开关谷歌新闻"
prerequisites:
  - "Android 8.0 及以上系统"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "集成了 Google Discover 信息流的设备桌面启动器"
conflicts: []
configPaths:
  - "/data/adb/modules/g-news-control/"
features:
  - "一键 Action 按钮切换：直接在 Root 管理器模块卡片中点击即可开关 Google Discover，无需重启"
  - "终端 CLI 命令：使用 `gnc` 与 `gnc switch` 查看当前状态或切换开关"
  - "完整保留 Google 应用功能：仅关闭负一屏信息流，Google 搜索、智慧镜头（Lens）与语音助手均 100% 正常工作"
  - "状态持久化记忆：系统重启后自动保持你偏好的负一屏显示状态"
faq: []
---

## 概述

在许多原生 Android 及 OEM 桌面启动器（如 Pixel Launcher、Motorola、Nothing OS 与 Sony Xperia）中，在主屏幕向右滑动会唤出 **Google Discover**（Google 新闻）负一屏信息流。虽然部分用户觉得实用，但也有大量用户认为该信息流容易分散注意力、存在隐私顾虑且增加后台耗电。然而，许多厂商桌面并未提供原生关闭开关——这往往迫使用户要么停用整个 Google 应用（从而破坏语音助手与语音搜索），要么更换第三方桌面。

由 mango0oo 开发的 **G-News Control** 为 Google Discover 负一屏提供了无缝且无损的控制方案。用户可通过 Root 管理器的交互式 Action 按钮或快捷终端命令按需随时启用或关闭该信息流，全程无需修改 Google 应用权限，也不会删除任何安装包组件。

## 如何开关负一屏信息流

G-News Control 在首次安装后默认会关闭 Google 新闻负一屏。你可以随时通过以下两种方式来回切换状态：

### 1. Root 管理器 Action 按钮
适用于运行 **KernelSU**、**APatch** 或 **MMRL** 的设备：
- 进入**模块**标签页。
- 找到 **G-News Control** 模块卡片。
- 点击 **Action**（操作）按钮即可立即切换负一屏状态。

### 2. 终端命令（`gnc`）
打开 Termux 或 ADB Root 终端：
```bash
# Query the current Google News feed state
su -c gnc

# Toggle between enabled and disabled
su -c gnc switch
```

## 无损架构设计

不同于粗暴执行 `pm disable com.google.android.googlequicksearchbox` 的精简脚本：
- G-News Control 仅切换内部框架覆盖层（Overlay）与信息流提供者组件。
- Google 搜索、Google 语音助手、语音转写、即圈即搜（Circle to Search）与 Google 智慧镜头完全不受影响，仍可正常使用。

## 安装与配置

1. 从 GitHub Releases 页面下载 `G-News Control` 的 `.zip` 压缩包。
2. 在 **Magisk** 或 **KernelSU** 中刷入该模块。
3. 重启设备。
4. 在主屏幕向右滑动，即可确认 Google Discover 负一屏已隐藏。
