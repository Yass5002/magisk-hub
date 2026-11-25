---
id: "ios-san-francisco-fonts"
title: "iOS San Francisco 字体套件：Android 无侵入式苹果字体替换方案"
sidebarTitle: "iOS SF 字体"
description: "将苹果 San Francisco Pro 与 SF Compact 字体无侵入式集成到 Android 系统界面、锁屏与应用中的字体模块，具备精确校准的字重与基线度量。"
category: "system-typography-fonts"
tier: 1
searchQueries:
  - "iOS 苹果字体 Magisk 模块"
  - "Android 安装 San Francisco 字体"
  - "SF Pro 字体面具模块下载"
  - "Android 14 SF Pro 字体模块"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "Android 8.0 (Oreo) 至 Android 14"
conflicts:
  - "其他无侵入式全局字体替换模块（如 Fontloader、Fontcraft、EvilFont）"
configPaths:
  - "/system/fonts/Roboto-Regular.ttf"
  - "/system/etc/fonts.xml"
features:
  - "以无系统分区修改（Systemless）方式将系统默认 Roboto 字体替换为苹果 San Francisco Pro (SF Pro)"
  - "提供从 Ultralight (100) 到 Black (900) 的全字重覆盖及配套斜体字形"
  - "精准校准字体上行高度（Ascent）、下行高度（Descent）与行距度量，防止厂商状态栏文字截断"
  - "完整保留 fonts.xml 中的中日韩（CJK）与区域语言字体回退链，确保多语言兼容"
  - "优化的 OpenType/TrueType 字形表，在高 DPI 屏幕上呈现锐利清晰的渲染效果"
faq:
  - question: "这个字体模块会破坏锁屏时钟或厂商自定义小部件吗？"
    answer: "不会。本模块严格遵循 Android 标准化字体度量规范，确保状态栏时钟、锁屏数字时钟及桌面小部件标题维持一致的垂直居中对齐，不会出现基线裁切。"
  - question: "安装后会改变系统自带的 Emoji 表情吗？"
    answer: "不会。iOS San Francisco 字体套件仅替换拉丁字母、数字及标准标点符号，底层的系统 Emoji 字体（如 NotoColorEmoji 或厂商自带 Emoji 字体库）将完全保持原样。"
---

## 概述

**iOS San Francisco 字体套件**（由 Chestnut EBQO 打包维护）通过无系统分区修改（Systemless）的叠加挂载方式，为已 Root 的 Android 设备带来苹果原生的 San Francisco（SF Pro）字体体验。

在原生 Android 系统中，Google 默认采用 Roboto 作为应用与系统界面的标准字体。尽管实用，但许多用户更青睐苹果 San Francisco 字体的几何比例、光学尺寸调节与清晰易读性。通过传统 Recovery 刷机直接替换系统字体极易损坏字体服务或破坏 `fonts.xml`。本模块采用安全可靠的模块化覆盖机制，将经过验证的 SF Pro TrueType 字体资产动态挂载至 `/system/fonts/`。

---

## 技术架构与工作原理

Android 通过位于 `/system/etc/fonts.xml` 的配置文件解析字体样式。系统定义了对应不同字重范围的命名家族（如 `sans-serif`）：

| Android 字体字重 | 映射文件名 | SF Pro 对应变体 |
|---|---|---|
| 100 (Thin) | `Roboto-Thin.ttf` | SF Pro Display Thin |
| 300 (Light) | `Roboto-Light.ttf` | SF Pro Display Light |
| 400 (Regular) | `Roboto-Regular.ttf` | SF Pro Text Regular |
| 500 (Medium) | `Roboto-Medium.ttf` | SF Pro Text Medium |
| 700 (Bold) | `Roboto-Bold.ttf` | SF Pro Text Bold |
| 900 (Black) | `Roboto-Black.ttf` | SF Pro Display Heavy |

### 1. 无侵入式 Magic Mount 挂载

在系统启动的 `post-fs-data` 阶段，Magisk / KernelSU 会拦截对 `/system/fonts/` 的目录访问请求。模块 `system/fonts/` 目录中的字体文件会在内存中动态绑定覆盖到物理系统分区之上，而底层的块设备始终保持完全只读状态。

### 2. 字形度量标准化

普通字体移植包最常见的故障是字体边界框不匹配（TrueType 文件中的 `OS/2` 度量表差异），这会导致状态栏文字上下裁切、下伸字母（如 `g`、`y`、`p`）被截断或应用标题错位。本套件中的所有字体文件均已针对 Android Roboto 标准行高与基线度量进行了精细调校。

---

## 安装与卸载方法

1. 打开你的 Root 管理器（Magisk Manager、KernelSU Manager 或 APatch WebUI）。
2. 进入“模块”页面，选择并刷入下载好的 `.zip` 安装包。
3. 重启设备，使 Android 字体缓存守护进程（`system_server`）重新加载字形表。
4. 如需随时还原回原厂默认字体，只需在 Root 管理器中关闭或卸载该模块并重启即可。
