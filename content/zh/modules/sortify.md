---
id: "sortify"
title: "Sortify：Android 下载目录自动整理与文件归类工具"
sidebarTitle: "Sortify 文件整理"
description: "按预设时间间隔自动将杂乱的 Android Download 文件夹分类归档至对应子目录，并提供原生 KernelSU WebUI 控制界面。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Sortify Magisk 模块下载"
  - "xCaptaiN09 Sortify"
  - "Android 自动整理 Download 下载文件夹"
  - "Root 自动分类下载目录文件"
  - "KernelSU WebUI 文件整理模块"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/sortify/"
features:
  - "后台自动归类：自动将未整理的下载文件按类型归入独立文件夹（图片、视频、音频、文档、APK、压缩包）"
  - "可配置扫描周期：按预设周期定时清理（默认每 5 分钟一次），不会造成后台额外耗电"
  - "原生 KernelSU WebUI：直接在 Root 管理器界面内调整归类规则、扫描间隔与忽略目录"
  - "支持手动 Action 按钮：点击 Magisk / KernelSU 中的模块 Action 按钮即可一键触发即时整理"
  - "重名文件安全处理：遇到同名文件时自动附加递增编号后缀，确保零数据覆盖与零丢失"
---

## 概述

日常使用智能手机数月后，Android 默认的 `/sdcard/Download/` 目录往往会堆积大量截图、安装包 APK、PDF 票据、ZIP 压缩包与视频片段，变得杂乱无章。使用常规文件管理器不仅需要频繁手动多选，整理起来也十分繁琐。

由 xCaptaiN09 编写的 **Sortify** 是一款面向 Root Android 设备的智能后台文件自动化整理模块。它在后台静默运行，定期扫描 `/sdcard/Download/` 目录，并将新下载的文件自动归类移动至整洁的专属子文件夹中。

## 文件分类结构

Sortify 会检测文件 MIME 类型与扩展名，并将文件归入以下直观分类目录：
- **APKs**：`.apk`、`.xapk`、`.apks`
- **Images**：`.jpg`、`.jpeg`、`.png`、`.webp`、`.gif`、`.svg`
- **Videos**：`.mp4`、`.mkv`、`.mov`、`.webm`、`.avi`
- **Audio**：`.mp3`、`.flac`、`.wav`、`.aac`、`.m4a`
- **Documents**：`.pdf`、`.docx`、`.xlsx`、`.pptx`、`.txt`、`.csv`
- **Archives**：`.zip`、`.rar`、`.7z`、`.tar`、`.gz`

## 交互功能与 WebUI

- **原生 WebUI**：针对 KernelSU 用户，Sortify 内嵌了完整的网页管理面板，无需离开 KernelSU 应用即可随时修改扫描频率、开关指定分类目录以及配置排除规则。
- **Action 快捷按钮**：在 Magisk 或 KernelSU 管理器中点击 Sortify 旁的 Action 按钮，即可随时触发一次即时归类扫描。
- **数据安全优先**：绝不直接覆盖已有文件。若目标分类目录中已存在同名文件，Sortify 会安全地为新文件重命名后再移入。

## 安装步骤

1. 从 GitHub Releases 下载最新版的 `Sortify-v*.zip` 安装包。
2. 在 **Magisk** 或 **KernelSU** 中刷入该模块。
3. 重启设备。
4. 之后照常下载文件即可，Sortify 会持续为你保持下载目录井井有条。
