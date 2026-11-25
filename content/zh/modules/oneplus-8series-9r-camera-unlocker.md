---
id: "oneplus-8series-9r-camera-unlocker"
title: "OnePlus 8 系列与 9R 相机解锁器：全副摄与长曝光权限开启"
sidebarTitle: "一加相机副摄解锁"
description: "为一加 8、8 Pro、8T 与 9R 解锁谷歌相机（GCam）及第三方拍照应用中的辅助镜头（超广角、长焦、微距）以及最长 5 秒的长曝光拍摄。"
category: "customization-ui"
tier: 1
searchQueries:
  - "一加 8 相机副摄解锁 Magisk"
  - "OnePlus 8 Pro 谷歌相机开启辅助镜头"
  - "一加 8T 9R 副摄解锁模块"
  - "一加手机 GCam 解锁长焦超广角"
  - "Open Camera 一加 8 长曝光解锁"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
  - "OnePlus 8、OnePlus 8 Pro、OnePlus 8T 或 OnePlus 9R 机型"
  - "OxygenOS（氧 OS）或兼容的 AOSP 第三方类原生 ROM"
conflicts: []
configPaths:
  - "/data/adb/modules/oneplus-8series-9r-camera-unlocker/"
features:
  - "完整辅助镜头访问权限：向第三方摄影应用（GCam 移植版与 Open Camera）开放超广角、长焦及微距相机传感器"
  - "不挑 OxygenOS 版本：可在不同 OxygenOS 构建版本间通用，无需针对特定 ROM 单独魔改相机"
  - "延长快门曝光时间：在受支持的相机应用中解锁最高 5 秒的长曝光快门时间"
  - "不限制应用包名：无需将应用伪装成特定白名单包名即可直接调用辅助传感器"
  - "无侵入相机提供程序叠加：以 Systemless 方式修改相机厂商 XML 权限配置，不改动系统分区"
faq: []
---

## 概述

在 OnePlus 8、8 Pro、8T 与 9R 设备上，原厂 OxygenOS 会将副摄传感器（如超广角镜头、光学长焦模组与独立微距镜头）的访问权限严格限制在一加自家原厂相机应用内。除非经过专门的包名伪装或打补丁处理，否则第三方应用与谷歌相机（GCam）移植版通常无法枚举这些辅助相机 ID。

**OnePlus 8-Series & 9R Camera Unlocker** 是一款无侵入式（Systemless）Magisk 模块，可彻底解除上述人为限制。通过修补厂商相机能力配置与系统权限配置文件，它能够让 GCam 及第三方拍照应用毫无阻碍地调用机身每一颗物理镜头。

## 核心特性

- **全副摄自由调用**：在主流 GCam 移植版（如 BSG、BigKaka 与 Arnova8G2 版本）中直接自由切换主摄、超广角与长焦镜头，无需更改安装包名来绕过白名单。
- **长曝光拍摄支持**：在 Open Camera 等应用中扩展手动曝光控制范围，支持长达 5 秒的长快门夜景拍摄。
- **跨 ROM 广泛兼容**：不仅稳定支持原厂 OxygenOS 11、12 与 13，同样兼容基于一加 8 系列内核树编译的 AOSP 与 LineageOS 第三方 ROM。

## 安装与配置

1. 从 Releases 页面下载最新的 `oneplus-8series-9r-camera-unlocker.zip` 压缩包。
2. 在 **Magisk** 中刷入该模块。
3. 重启设备。
4. 打开你常用的 GCam 移植版，在开发者设置或镜头配置菜单中开启辅助镜头选项即可。
