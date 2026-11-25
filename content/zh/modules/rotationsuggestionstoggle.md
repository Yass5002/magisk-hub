---
id: "rotationsuggestionstoggle"
title: "Rotation Suggestions Toggle：控制 Android 浮动屏幕旋转建议按钮"
sidebarTitle: "屏幕旋转建议开关"
description: "无系统分区修改配置或屏蔽 Android 导航栏与手势指示条角落出现的浮动“屏幕旋转建议”按钮。"
category: "customization-ui"
tier: 1
searchQueries:
  - "RotationSuggestionsToggle Magisk 模块"
  - "Astoritin RotationSuggestionsToggle"
  - "关闭导航栏屏幕旋转按钮 Root"
  - "隐藏安卓浮动旋转图标"
  - "KernelSU 禁用屏幕旋转建议提示"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/rotationsuggestionstoggle/"
features:
  - "屏蔽干扰提示：永久关闭或切换导航栏角落浮动的屏幕旋转建议按钮"
  - "减少误触烦恼：彻底避免躺卧使用手机时误碰角落旋转图标导致的意外横屏"
  - "全平台 Root 兼容：完美适配 Magisk、KernelSU 与 APatch 各类实现"
  - "无破坏框架配置：通过纯净配置标志位生效，不破坏系统分区完整性"
  - "即时可逆还原：禁用或卸载模块后立即恢复 Android 原生旋转建议行为"
---

## 概述

自 Android 9 Pie 起，系统引入了上下文感知的“屏幕旋转建议”功能：当关闭自动旋转且倾斜手机时，导航栏底角或手势提示条旁会弹出一个小型浮动旋转按钮。尽管这对部分场景有所便利，但对于喜欢躺着看书、横屏玩游戏或单手刷视频的用户而言，该按钮不仅频繁在边缘闪烁干扰视线，还极易因误触导致屏幕突然翻转。

由 Astoritin 开发的 **RotationSuggestionsToggle** 是一款无系统分区修改（Systemless）的 Root 模块，提供了对该特性的精细控制能力，支持在原生 AOSP、Pixel 固件及各类 OEM 定制系统上彻底屏蔽或切换旋转建议图标。

## 为什么选择隐藏屏幕旋转建议？

1. **杜绝误触翻车**：在锁定竖屏时横持手机，旋转建议按钮恰好位于底部导航区或收起键盘按钮附近，极易在操作边缘时误触触发方向切换。
2. **沉浸式全屏体验**：在观看视频信息流或游玩全屏游戏时，消除屏幕底角多余的视觉弹窗干扰。
3. **纯粹无系统分区修改**：通过系统框架覆盖配置标志位实现，而非侵入式修补二进制文件，确保不会影响 Android dm-verity 校验或 Google Play Integrity 认证状态。

## 安装与 Root 支持

- **平台兼容性**：已在 **Magisk**、**KernelSU** 与 **APatch** 上完整测试通过。
- **安装步骤**：
  1. 从 GitHub Releases 下载 `RotationSuggestionsToggle-*.zip`。
  2. 打开你常用的 Root 管理器应用，选择从本地存储安装该 ZIP 包。
  3. 重启设备使新的屏幕旋转配置生效。
