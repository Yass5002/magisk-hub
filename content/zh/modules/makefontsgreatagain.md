---
id: "makefontsgreatagain"
title: "MakeFontsGreatAgain (MFGA)：通用多文字与 Emoji 字体引擎"
sidebarTitle: "MakeFontsGreatAgain"
description: "融合多套字体的通用排版引擎，实现完整的 Unicode 字符覆盖、Unicode 17/18 Emoji 支持以及自定义字形着色功能。"
category: "customization-ui"
tier: 1
searchQueries:
  - "MakeFontsGreatAgain Magisk 模块"
  - "MFGA 字体模块下载"
  - "Numbersf MakeFontsGreatAgain"
  - "安卓 Root 全 Unicode 字符字体"
  - "MFGA 屏蔽 GMS 字体冲突"
prerequisites:
  - "Android 9 及以上系统（COLRv0 彩色字形功能需 Android 10+）"
  - "Magisk、KernelSU 或 APatch"
conflicts:
  - "GMS 字体屏蔽功能与 Play Integrity Fix (PIF) 模块的默认卸载挂载（Unmount）设置冲突；需为 Play 服务与 Play 商店单独配置取消卸载例外"
  - "严禁将 Shamiko 白名单模式与 GMS 字体屏蔽功能同时启用"
configPaths:
  - "/data/adb/modules/MakeFontsGreatAgain/"
features:
  - "全量 Unicode 字符覆盖：完整覆盖现代 Unicode 规范、私用区（PUA）以及辅助平面的各类字形"
  - "Unicode 17 与 18 Emoji 抢先支持：提前体验最新版本的彩色 Emoji 表情字形"
  - "GMS 字体提供程序屏蔽：拦截 Google Play 服务的动态字体下载，确保各类 Google 应用内字体全局一致"
  - "交互式 WebUI 与字形着色：在支持 COLRv0 的设备上直接为单个符号或特定字形区间自定义颜色"
  - "Xposed 模块联动：提供配套 Xposed 模块，针对内置硬编码字体资源的应用强行应用字体替换"
faq:
  - question: "为什么屏蔽 GMS 字体会与 Play Integrity Fix (PIF) 产生冲突？"
    answer: "屏蔽 GMS 动态字体提供程序需要拦截 Google Play 服务与 Google Play 商店进程。如果你的 Root 管理器或 PIF 模块对 Play 服务执行了模块卸载挂载（Unmount），字体屏蔽 Hook 就会失效。你需要在 PIF 中配置允许 Play 服务看到模块，或关闭全局卸载挂载。"
  - question: "MFGA 如何处理未定义的 Unicode 符号？"
    answer: "未定义或保留字符会交由 ZUno-Number.ttf 处理，该字体会直接显示字符对应的精确十六进制 Unicode 码位，而不会渲染成毫无信息量的空白方框或问号。"
---

## 概述

由 **Numbersf** 开发的 **MakeFontsGreatAgain (MFGA)** 是一款面向已 Root Android 设备的综合字体排版引擎。

原生 Android 系统字体在多语种字符集、古文字、数学符号以及最新 Emoji 修订版上往往存在字形缺失问题。MFGA 将多套顶尖字体整合为统一的字体回退栈，在实现完整 Unicode 字符覆盖的同时，提供丰富的高级自定义工具。

---

## 技术架构与工作原理

### 字体回退注入与 GMS 屏蔽

MFGA 工作在系统字体配置层：

1. **回退字体栈合成**：叠加覆盖 `/system/etc/fonts.xml` 与 `/etc/font_fallback.xml`，注入高优先级字体链，全面涵盖常规文字、私用区（PUA）及 Emoji。
2. **GMS 字体提供程序拦截**：拦截 Google Play 服务中的远程字体下载服务，确保 Gmail、Google Chrome 等应用调用本地 MFGA 字形，而非在线拉取原生 Google 字体。
3. **COLRv0 字形着色**：在 Android 10+ 设备上修改 OpenType 字体中的彩色矢量图层，允许用户为特定 Emoji 类别定制专属调色板。

---

## 安装与配置

1. 下载最新版本的 `MakeFontsGreatAgain-*.zip` 安装包。
2. 在 Magisk、KernelSU 或 APatch 中刷入该模块。
3. 重启设备。
4. 打开模块 WebUI，自定义字体覆盖范围与 GMS 屏蔽选项。

---

## 配置与使用

在 MFGA WebUI 界面中，你可以调整以下选项：

- **GMS 字体屏蔽（GMS Font Blocking）**：开关针对 Google 应用动态字体的拦截功能。
- **字体范围遮罩（Font Range Masking）**：如果你希望某些特定文字保留厂商自带的本地字体，可将对应的 Unicode 字符区间排除在替换范围之外。
- **颜色自定义（Color Customization）**：在 Android 10+ 设备上为符号自定义强调色。

---

## 故障排查与常见问题

- **Play Integrity 认证失败**：若开启 GMS 字体屏蔽后导致 Play Integrity 过检失败，请确认未在 Shamiko 或 PIF 中针对 Google Play 服务启用全局卸载挂载（Global Unmount）。
