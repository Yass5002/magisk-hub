---
id: "tsukushi-a-round-gothic-font"
title: "筑紫 A 丸体（Tsukushi A Round Gothic）套件：85% 均衡光学缩放版"
sidebarTitle: "筑紫 A 丸体"
description: "优雅圆润的日式筑紫 A 丸体无侵入式移植套件，已修正大陆标准简体中文字形并针对高分屏校准 85% 紧凑光学缩放比例。"
category: "system-typography-fonts"
tier: 1
searchQueries:
  - "筑紫A丸体 Magisk 字体模块"
  - "筑紫A丸体大陆简中修正版"
  - "日式圆体 Android 字体模块"
  - "筑紫丸体 85% 缩放 Magisk"
prerequisites:
  - "Android 8 至 Android 15"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他全局系统字体替换模块"
configPaths:
  - "/system/etc/fonts.xml"
  - "/system/etc/fonts_base.xml"
  - "/system/fonts/Roboto-Regular.ttf"
features:
  - "完整移植标志性的筑紫 A 丸体设计，保留温润优雅的笔画收尾弧度"
  - "集成大陆标准简体中文字形修正，彻底避免日系汉字异体字错位问题"
  - "经过校准的 85% 光学缩放比例，打造精致且高信息密度的系统界面排版"
  - "以无系统分区修改（Systemless）方式替换系统默认字体，完全不触碰只读系统镜像"
faq:
  - question: "85% 缩放比例在日常使用中会带来什么效果？"
    answer: "在现代高分辨率屏幕上，标准 Android 系统字体往往显得偏大。85% 光学缩放让字符尺寸略微收窄、字距更紧凑，在保持清晰易读的同时显著提升单屏信息承载量。"
  - question: "在聊天软件中使用这款字体会出现缺字方框（豆腐块）吗？"
    answer: "不会。模块内置了完善的回退字体定义，确保标准 Emoji、特殊符号以及生僻 Unicode 字符能够平滑回退至系统默认字体显示。"
---

## 概述

**筑紫 A 丸体套件（Tsukushi A Round Gothic Typography Suite）**（由心雨 Xin Yu 打包适配）是一款无侵入式（Systemless）字体模块，将筑紫 A 丸体独具匠心的日系美学排版体验引入 Android 平台。

筑紫 A 丸体以柔和圆润的笔画末端与均衡舒展的中宫结构而闻名，能够呈现出温润而不失精致的视觉层次感。本版本针对中文 Android 使用环境进行了专项适配，将原版中的日文汉字异体字型全面修正为规范的大陆简体中文标准字形，并应用了 85% 的光学缩放比例，使整体界面观感更加细腻平衡。

---

## 技术架构与工作原理

Android 通过由 `/system/etc/fonts.xml` 控制的 FreeType 渲染引擎呈现界面文字：

### 1. 字体别名重映射

模块将筑紫 A 丸体二进制字体文件挂载至 `/system/fonts/`，并对系统标准字重进行别名映射：

- `Roboto-Regular.ttf` -> Tsukushi Round Regular
- `Roboto-Medium.ttf` -> Tsukushi Round Medium
- `Roboto-Bold.ttf` -> Tsukushi Round Bold

### 2. 光学缩放优化

若仅通过调整系统显示密度（DPI）来缩小文字，往往会导致应用布局变形或网页视图错位。本模块直接在字体文件内部的 Em-square 度量层面上校准了 85% 的基线高度，从而在不破坏任何应用原生布局几何结构的前提下，呈现出精致紧凑的文字排印效果。

---

## 排查与验证

- **刷新 SystemUI 字体缓存**：刷入模块后必须完整重启设备，以便 Android 的 Zygote 进程与系统字体缓存完成重建。
- **第三方输入法**：部分输入法（如 Gboard）自带独立的键盘字体渲染机制；若按键文字未立即生效，请强行停止并重启该输入法进程。
