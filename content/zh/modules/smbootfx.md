---
id: "smbootfx"
title: "SMbootFX：适用于三星 One UI 的无侵入式 QMG 开/关机动画替换框架"
sidebarTitle: "SMbootFX"
description: "面向已 Root 三星 Galaxy One UI 设备的无系统分区修改开机与关机动画替换框架，原生采用三星专有 QMG 图像格式。"
category: "system-environment"
tier: 1
searchQueries:
  - "smbootfx Magisk 模块"
  - "john0n1 smbootfx 下载"
  - "三星 QMG 开机动画 Magisk"
  - "One UI Root 自定义开机动画"
  - "bootsamsung.qmg 无侵入替换"
prerequisites:
  - "运行 One UI 或 TouchWiz 的三星 Galaxy 智能手机或平板电脑（Android 7 至 16）"
  - "通过 Magisk v27+ 或 KernelSU 获取 Root 权限"
  - "设备固件采用三星专有的 `.qmg` 开机图形渲染引擎"
conflicts:
  - "非三星 OEM 设备（Google Pixel、小米、一加、摩托罗拉）及纯 AOSP ROM（这些系统仅支持标准的 `bootanimation.zip`）"
configPaths:
  - "/data/adb/modules/smbootfx/"
  - "/system/media/bootsamsung.qmg"
  - "/system/media/bootsamsungloop.qmg"
  - "/system/media/shutdown.qmg"
features:
  - "原生支持三星 QMG 引擎：以无系统分区修改方式替换专有的 `bootsamsung.qmg`、`bootsamsungloop.qmg` 与 `shutdown.qmg`"
  - "精选主题资源库：涵盖复古 Android、CyanogenMod、Kali NetHunter 与赛博朋克等多种视觉设计风格"
  - "开/关机动画视觉统一：关机动画与开机视觉风格保持协调一致"
  - "零分区修改：将自定义动画资产覆盖挂载至 `/system/media/`，不会破坏系统分区完整性校验"
---

## 概述

与主流 Android 生态（普遍使用包含连续 PNG 帧与 `desc.txt` 时序描述文件的标准 `bootanimation.zip` 压缩包）不同，三星 Galaxy 固件采用了一套完全私有的开机图形渲染管线。三星的引导程序与 `bootchecker` 二进制组件通过读取位于 `/system/media/` 下的已编译 `.qmg`（Qualcomm Multimedia Graphics）图像容器来渲染开机与关机画面。

正因这一专有格式限制，标准的 AOSP 开机动画模块无法在三星 One UI 上生效。

由 John0n1 开发的 **SMbootFX** 是一款专为三星 Galaxy 设备打造的开源无系统分区修改（Systemless）定制框架。SMbootFX 以开箱即用的 Magisk 与 KernelSU 模块形式提供，在不改动只读系统分区的前提下，将高清晰度、专业转换的 `.qmg` 动画资源覆盖挂载到三星原厂开机与关机动画路径之上。

## 兼容性与格式限制

- **三星设备专属**：本模块仅适用于运行原厂 One UI 或基于三星官方固件制作的三方 ROM 的 Galaxy 手机与平板（支持 Android 7 至 Android 16）。
- **非三星设备不兼容**：Google、小米、摩托罗拉、索尼或一加等品牌机型，以及基于 AOSP 的第三方 ROM（如 LineageOS、PixelOS），均依赖标准的 `bootanimation.zip` 格式，无法解析 `.qmg` 动画文件。
- **Root 管理器要求**：需要 Magisk v27+ 或 KernelSU。

## 主题视觉风格

SMbootFX 打包了丰富多样的主题视觉套装，每套均同时包含开机与关机动画资源：

- **经典与现代 Android 风格**：Android Purple、Android Red、Android Green on Black、Android White on Plum、KitKat Classic 与 KitKat Easter Egg。
- **经典第三方 ROM 致敬风格**：CyanogenMod Android、AOKP 与 AOKP Magical。
- **赛博朋克与安全极客美学**：Kali NetHunter、NetHunter Glitch、CTOS（《看门狗》风格）以及 NSA Terminal。
- **极简与品牌风格**：Apple Static Black、Apple Static White 以及 MIUI Multi-Color 变体。

## 三星 QMG 动画文件结构

该模块会将预先渲染好的高帧率 `.qmg` 文件挂载至 `/system/media/` 目录：
- **`bootsamsung.qmg`**：内核完成交接后立即播放的初始引导启动动画。
- **`bootsamsungloop.qmg`**：在 Android 系统服务启动与 ART 编译预热期间循环展示的过渡动画。
- **`shutdown.qmg`**：设备执行重启或关机指令时触发的平滑关机动画。

## 安装与配置

1. 确认你的三星设备已通过 Magisk v27+ 或 KernelSU 获取 Root 权限。
2. 从 SMbootFX 官方仓库的 Releases 页面下载心仪的主题模块包（例如 `android-bootfx-*-magisk.zip` 或 `nethunter-bootfx-*-magisk.zip`）。
3. 打开 Root 管理器并刷入模块 ZIP 包。
4. 重启手机，系统在越过初始 Bootloader 静态 Logo 后便会平滑过渡至你的自定义 `.qmg` 动画序列。

## 故障排查

- **开机仍显示三星原厂动画**：请在 Root 管理器中确认模块已启用。在部分较新的 One UI 版本上，请检查 Root 管理器的挂载命名空间（Mount Namespace）设置，确保 `/system/media` 路径未被隔离在系统服务进程之外。
- **卡在 Samsung Logo 界面**：若开机动画卡死，请确认设备在开机早期阶段拥有充足的可用内存分配，且未同时安装其他会往 `/system/media/` 挂载资源的开机动画模块。
