---
id: "hide-navbar"
title: "NavTweaks：全面屏手势与导航栏定制模块"
sidebarTitle: "NavTweaks"
description: "定制 Android 导航栏外观，通过隐藏手势小白条与移除键盘底部空白间距，实现真正的全屏手势导航体验。"
category: "customization-ui"
tier: 1
searchQueries:
  - "Hide Navbar Magisk 模块"
  - "NavTweaks 全面屏手势 Android"
  - "Android 14 15 隐藏手势小白条"
  - "DanGLVK NavTweaks 下载"
  - "Magisk 移除输入法底部空白"
prerequisites:
  - "Android 10 至 Android 15"
  - "Magisk 20+，或 KernelSU / APatch"
  - "KernelSU 用户需确保 SystemUI 位于应用列表中且已关闭“卸载模块（unmount modules）”"
conflicts:
  - "GSI 类 ROM（GSI 系统的 Overlay 挂载行为存在不一致）"
  - "在 Android 11 及以上版本中，不保证导航栏动态明暗配色自适应正常生效"
configPaths:
  - "/data/adb/modules/HideNavBar/"
features:
  - "真正沉浸式全屏手势：移除底部手势小白条，释放额外屏幕显示空间"
  - "消除键盘底部留白：移除输入法弹出时键盘下方的多余空白区域"
  - "音量键交互式安装：刷入过程中通过实体音量键自选手势条高度、灵敏度与 Overlay 模式"
  - "Systemless Overlay 挂载：无需修改磁盘上的框架 APK 即可应用界面尺寸调整"
  - "广泛的系统兼容：全面支持 Android 10（Q）至 Android 15（V）"
faq:
  - question: "为什么在 KernelSU 上会导致 SystemUI 崩溃或样式不生效？"
    answer: "KernelSU 会利用挂载命名空间隔离应用。为确保 NavTweaks 的 Overlay 能够正常作用于 SystemUI，请务必将 SystemUI 软件包加入 KernelSU 的配置列表，并关闭其“卸载模块（unmount modules）”选项。"
  - question: "安装后还可以更改手势条选项吗？"
    answer: "可以。无需卸载模块，直接在 Root 管理器中重新刷入一次即可，音量键选择界面会重新提示你挑选偏好的导航栏高度与间距配置。"
---

## 概述

由 **DanGLVK** 开发的 **NavTweaks**（原名 *Fullscreen/Immersive Gestures*）是一款面向 Android 10 至 Android 15 的无系统分区修改（Systemless）界面模块，专注于定制导航栏与底部手势指示条。

尽管 Android 原生全面屏手势已提供全屏滑动操作，但屏幕底部仍会残留一条常驻的视觉导航指示条（“小白条”），并在输入法键盘下方留下人工空白间距。NavTweaks 通过注入定向框架资源覆盖（Overlay）消除手势小白条，还原真正的无边框全屏显示面积。

---

## 技术架构与工作原理

### 运行时资源覆盖（RRO）定制

NavTweaks 基于 Android 原生的运行时资源覆盖（Runtime Resource Overlay）机制运行：

1. **音量键交互式安装器**：刷入时通过 `customize.sh` 监听实体音量键输入，供用户自由选择覆盖参数（例如完全隐藏小白条、超窄手势条、移除键盘留白或平板布局）。
2. **框架 Overlay 注入**：生成并将定制的 `android.overlay` 安装包挂载至 `/system/overlay/` 或 `/product/overlay/`。
3. **尺寸指标覆盖**：将 Android 框架中的尺寸整型参数（`navigation_bar_height`、`navigation_bar_frame_height`、`navigation_bar_gesture_height`）重定义为零或自定义数值，动态重算界面布局边界。

---

## 安装与配置

1. 从官方发布渠道下载最新版 `NavTweaks-*.zip`。
2. 在 Magisk、KernelSU 或 APatch 中刷入该模块。
3. 在终端安装过程中，按设备**音量加**（选择）与**音量减**（确认）键挑选所需视觉样式。
4. 重启设备以使框架 Overlay 生效。

---

## 配置与使用

- **KernelSU 专项要求**：在 KernelSU 管理器中，确认应用列表已包含 `com.android.systemui`，且已关闭其 `Umount modules`（卸载模块）开关。
- **重新配置参数**：若后续需要更改手势条高度、键盘底部间距或圆角曲率，只需再次刷入模块压缩包并在安装向导中选择新选项即可。

---

## 故障排查与常见问题

- **GSI ROM 兼容问题**：通用系统镜像（GSI）通常采用非标准的 Overlay 优先级排序，可能导致导航栏修改被系统忽略。
- **导航栏着色不一致**：在 Android 11 及更高版本上，受不同 OEM 桌面主题机制影响，导航栏明暗自适应着色可能出现显示异常。
