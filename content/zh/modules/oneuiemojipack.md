---
id: "oneuiemojipack"
title: "OneUI Emoji Pack：Android 无系统分区三星 Emoji 字体模块"
sidebarTitle: "OneUI Emoji Pack"
description: "无系统分区修改将 AOSP 与谷歌默认 Emoji 字体替换为三星 OneUI 表情字体，全面适配各类应用与系统输入法。"
category: "customization-ui"
tier: 1
searchQueries:
  - "OneUI Emoji Magisk 模块下载"
  - "安卓替换三星表情字体 Root"
  - "AloozChips OneUIEmojiPack"
  - "谷歌原生表情替换三星 OneUI"
  - "OneUI Emoji KernelSU APatch 模块"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
conflicts:
  - "KernelSU 2.0+ 环境下的 FontLoader 模块（元模块分层挂载冲突可能导致系统不稳定）"
  - "其他修改系统 Emoji 字体文件的 Magisk 字体模块"
configPaths:
  - "/data/adb/modules/oneuiemojipack/"
features:
  - "原汁原味三星风格：将通用 NotoColorEmoji 替换为三星官方 OneUI Emoji 字体"
  - "全系统级覆盖：在 WhatsApp、Telegram、Instagram 等社交应用与虚拟键盘（如 Gboard）中统一渲染 OneUI 表情"
  - "全平台 Root 兼容：完整支持 Magisk、KernelSU 与 APatch Root 管理器"
  - "零系统分区修改：以无系统分区修改（Systemless）方式挂载字体资源，完整保留 dm-verity 校验与无缝 OTA 更新"
  - "即装即用可逆：禁用或卸载模块即可立即恢复原生系统表情"
---

## 概述

三星 OneUI 系统的表情符号以明快、圆润且富有表现力的设计风格广受好评。虽然谷歌原生的 NotoColorEmoji 拥有广泛的 Unicode 字符覆盖范围，但许多用户更偏好在社交动态与即时聊天中看到三星极具辨识度与清晰度的 Emoji 视觉效果。

由 AloozChips 开发的 **OneUI Emoji Pack** 是一款无系统分区修改（Systemless）的 Root 模块，可将 Android 系统默认的 Emoji 字体文件（`NotoColorEmoji.ttf` 或 OEM 厂商变体）替换为原版 OneUI 表情包。

## 兼容性与注意事项

- **Root 管理器**：支持 **Magisk**、**KernelSU** 与 **APatch**。
- **KernelSU 2.0+ 重要提示**：若设备运行支持元模块（Metamodule）机制的 KernelSU 2.0 及以上版本，**切勿**将本模块与独立的 `fontloader` 模块同时启用。两者叠加可能导致字体配置冲突并引发系统框架崩溃。
- **字体冲突**：避免同时刷入其他 Emoji 替换模块（如 iOS 表情包或 Twemoji 模块），以免造成字体定义冲突。

## 安装指南

1. 从 GitHub Releases 下载最新版的 `OneUI_Emoji_Pack-v*.zip` 压缩包。
2. 打开你所使用的 Root 管理器（**Magisk**、**KernelSU** 或 **APatch**）。
3. 进入 **模块 > 从本地安装**，选择该 ZIP 压缩包并确认刷入。
4. 重启设备，即可在全系统生效新的 Emoji 字体。
