---
id: "ttf-twemoji"
title: "Twemoji Replacer：为 Android 无侵入替换 Twitter Twemoji 彩色表情字体"
sidebarTitle: "Twemoji Replacer"
description: "无系统分区修改地将 Google 原生 NotoColorEmoji 替换为 Twitter 开源的彩色 Twemoji 表情字体包，全系统应用全局生效。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Twemoji Magisk 模块下载"
  - "ttf-twemoji 安卓 Root 替换表情"
  - "Google Emoji 替换为 Twitter 表情"
  - "无损更换安卓系统表情字体"
  - "开源 Twemoji 彩色字体模块"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
conflicts:
  - "其他同样修改系统 Emoji 字体文件的表情替换模块"
configPaths:
  - "/data/adb/modules/ttf-twemoji/"
features:
  - "Twitter Twemoji 视觉风格：将系统默认或 OEM 厂商定制 Emoji 替换为 Twitter 标志性的扁平化高饱和彩色表情"
  - "CBDT/CBLC 位图格式兼容：严格采用 Android 原生彩色字形编码规范，确保在高 DPI 屏幕上渲染清晰锐利"
  - "全系统全局覆盖：在 Gboard 等输入法、社交应用、网页浏览器与系统通知栏中统一显示 Twemoji 表情"
  - "零系统分区改动：借助 Magisk Magic Mount 机制实现无侵入挂载，完整保留系统分区完整性"
  - "随时无损还原：只需在 Magisk 中停用或卸载该模块并重启，即可立即恢复原厂 Emoji 字体"
---

## 概述

Twitter 推出的 **Twemoji** 表情图标集以鲜明的色彩、现代化的扁平设计以及清晰直观的情绪表达能力在全网广受好评。尽管 Android 系统默认搭载了 Google 原生的 NotoColorEmoji，但许多用户更偏好在桌面网页端与移动端设备之间保持一致的 Twemoji 视觉体验。

由 Magisk-Modules-Alt-Repo 维护（基于 JoeBlakeB 与 WhyNotHugo 的构建脚本打包）的 **ttf-twemoji** 是一款无系统分区修改（Systemless）Root 模块，可将 Android 默认的系统表情字体（`NotoColorEmoji.ttf`）无缝替换为 Twemoji。

## 技术实现

- **彩色字形编码（CBDT/CBLC）**：采用 Android 原生支持的 `CBDT/CBLC` 彩色字体表结构，确保表情在 1080p、1440p 乃至 4K 高分屏上均可保持锐利缩放，不发虚、不模糊。
- **完整 Unicode 字符覆盖**：同步收录新版 Unicode 标准新增的表情符号，全面支持肤色修饰符、多成员组合家庭图标及各类现代社交反应表情。
- **系统安全性**：不直接修改任何只读系统分区文件，不影响 Google Play Integrity 认证状态及后续 OTA 系统更新。

## 安装步骤

1. 从 GitHub Releases 下载最新的 `ttf-twemoji-*.zip` 模块压缩包。
2. 打开 **Magisk**，进入 **模块 > 从本地安装（Install from storage）** 并选中已下载的 zip 文件。
3. 确认刷入后重启手机。
4. 打开系统键盘或即时通讯应用，即可查看全局生效的 Twemoji 彩色表情。
