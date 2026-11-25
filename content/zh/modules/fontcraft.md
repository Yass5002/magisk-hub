---
id: "fontcraft"
title: "FontCraft：基于拟态 WebUI 的无侵入式字体与 Emoji 注入引擎"
sidebarTitle: "FontCraft"
description: "功能全面的字体与 Emoji 管理引擎，内置深色交互式 WebUI、本地离线 TTF 文件浏览器以及双槽位混合构建队列。"
category: "customization-ui"
tier: 1
searchQueries:
  - "FontCraft Magisk 模块"
  - "RipperHybrid FontCraft 下载"
  - "KernelSU WebUI 刷入 TTF 字体"
  - "安卓 Root 离线安装 Emoji 模块"
  - "FontCraft WebUI APatch Magisk"
prerequisites:
  - "Android 8.0 及以上系统"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "支持 WebUI 的 Root 管理器或浏览器界面"
conflicts: []
configPaths:
  - "/data/adb/modules/FontCraft/"
features:
  - "交互式本地 WebUI：现代深色新拟态设计界面，可直接在 Root 管理器内打开使用"
  - "离线本地文件浏览器：无需联网即可浏览、挑选并测试设备存储中的自定义 .ttf 文件"
  - "混合构建队列：支持同时将自定义系统字体与 Apple/Google Emoji 打包入列并一并编译安装"
  - "实时终端遥测：直观展示刷入日志、XML 解析状态与字体替换诊断信息"
faq: []
---

## 概述

在 Android 设备上更换字体和 Emoji 集合，以往往往意味着需要到处寻找针对特定字体的预编译 Magisk 模块，或者在电脑上折腾复杂的字体打包脚本。如果用户想测试一款自定义字体，或是将小众字体与心仪的 Emoji 组合使用，就不得不手动修改 `fonts.xml` 声明并手工打包 ZIP 模块。

由 RipperHybrid 开发的 **FontCraft** 是一款依托内置本地 WebUI 驱动的动态字体与 Emoji 管理引擎。它跨平台兼容 Magisk、KernelSU 与 APatch，允许用户直接在 Root 管理器内浏览手机内部存储中的 `.ttf` 文件，将字体与 Emoji 替换任务加入队列，并实时动态生成干净的无侵入式（Systemless）字体覆盖层。

## 核心界面与功能特性

### 1. 新拟态本地 WebUI
FontCraft 内嵌了一套运行在本地设备上的单页 Web 控制面板，无需任何外部后台服务进程，可在 **KernelSU Manager**、**APatch Manager** 或 **MMRL** 中直接呼出。该界面提供：
- 实时终端执行输出日志。
- 即时字体效果预览。
- 用于排查字体度量异常的集成调试控制台。

### 2. 双槽位混合构建队列
用户无需在安装 Emoji 模块或安装字体模块之间二选一。FontCraft 引擎支持统一的混合构建队列：
- **槽位 A（系统字体）**：替换系统默认的 Roboto / Google Sans 字体，覆盖 Regular、Medium、Bold 与 Italic 等字重。
- **槽位 B（彩色 Emoji）**：将 Android 原生的 `NotoColorEmoji.ttf` 替换为你偏好的表情风格（如 iOS、Fluent 或 JoyPixels Emoji）。
- 两个槽位将同步编译并一次性覆盖挂载至 `/system/fonts/`。

### 3. 离线内部存储文件浏览器
用户可从任意渠道下载原始 `.ttf` 或 `.otf` 字体文件并存放在内部存储的任意路径，无需互联网连接即可通过 FontCraft 内置文件选择器直接定位调用。

## 安装与使用指南

1. 从 GitHub Releases 下载并刷入 `FontCraft` `.zip` 模块包。
2. 重启设备。
3. 打开 **KernelSU Manager**、**APatch** 或 **MMRL**，进入模块列表并启动 **FontCraft WebUI**。
4. 通过内置文件浏览器选定本地 `.ttf` 字体文件与 Emoji 文件。
5. 点击 **Apply** 编译生成无侵入式覆盖挂载层。
6. 重启手机，即可在所有应用中体验全新的字体排版效果。
