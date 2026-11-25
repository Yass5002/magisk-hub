---
id: "magisk-samsung-dex-standalone-mode"
title: "Samsung DeX Standalone Mode：在三星手机本机屏幕开启独立 DeX 桌面模式"
sidebarTitle: "DeX Standalone Mode"
description: "无侵入式修补 floating_feature.xml 配置文件，使三星 Galaxy 手机无需外接显示器即可直接在手机屏幕上启动 Samsung DeX 独立桌面模式。"
category: "system-environment"
tier: 1
searchQueries:
  - "Samsung DeX 独立模式 Magisk 模块"
  - "supermarsx DeX Standalone Mode"
  - "三星手机屏幕直接运行 DeX"
  - "floating_feature.xml 开启独立 DeX"
  - "Galaxy 手机 Root 解锁本机 DeX"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "具备 DeX 硬件能力且运行三星 One UI（One UI 8 之前版本）的 Galaxy 智能手机"
conflicts: []
configPaths:
  - "/data/adb/modules/magisk-samsung-dex-standalone-mode/"
features:
  - "本机屏幕 DeX 桌面：无需连接外接 HDMI 显示器或电视，直接在手机原生触控屏上启动 Samsung DeX"
  - "无侵入特性注入：自动修补 `floating_feature.xml`，在 `SEC_FLOATING_FEATURE_COMMON_CONFIG_DEX_MODE` 中追加 `standalone` 参数"
  - "真正自由悬浮多窗口：支持在桌面窗口模式下并排运行并自由调整多个应用窗口大小"
  - "双 Root 框架兼容：在 Magisk 与 KernelSU 环境下表现完全一致"
  - "无损实现方式：不改动只读系统分区镜像完整性"
faq: []
---

## 概述

Samsung DeX 是移动端最强大的桌面融合环境之一，可将 Android 系统转换为具备任务栏、窗口控制按钮以及键鼠快捷键支持的多窗口桌面交互界面。虽然三星在 Galaxy Tab 平板系列上开放了“独立模式（Standalone Mode）”——允许直接在设备自带屏幕上运行 DeX，但在智能手机产品线上却人为将其限制为必须连接外部有线或无线显示器才能开启。

由 supermarsx 开发的 **magisk-samsung-dex-standalone-mode** 解除了这项人为限制。通过无系统分区修改（Systemless）地更新三星内部设备特性配置表，Galaxy 手机用户无需任何外设即可直接在手机屏幕上启动并使用 Samsung DeX。

## 技术原理：`floating_feature.xml`

三星 One UI 通过位于 `/system/etc/floating_feature.xml`（或 `/vendor/etc/floating_feature.xml`）的加密/XML 配置文件管理各机型的专属特性开关。

在原厂手机固件中，`SEC_FLOATING_FEATURE_COMMON_CONFIG_DEX_MODE` 键值通常仅包含 `dual,wireless` 或 `dock`。本模块会在开机早期阶段（`post-fs-data.sh`）将该属性无侵入式地修改为包含以下内容：

```xml
<SEC_FLOATING_FEATURE_COMMON_CONFIG_DEX_MODE>standalone,dual,wireless</SEC_FLOATING_FEATURE_COMMON_CONFIG_DEX_MODE>
```

完成无侵入替换后，One UI 的系统界面（System UI）与 DeX 管理器便会将手机识别为支持在主屏幕（`Display 0`）直接渲染 DeX 桌面的设备。

## 安装与启动方式

1. 确认手机运行的是 One UI 8 之前版本的三星 One UI 系统。
2. 从 GitHub Releases 页面下载 `magisk-samsung-dex-standalone-mode.zip` 安装包。
3. 在 **Magisk** 或 **KernelSU** 中刷入该压缩包并重启设备。
4. 开机后下拉打开 **快捷设置** 面板，点击 **DeX** 快捷开关（若未显示请进入编辑面板将其拖出）。
5. 设备屏幕将立即切换并进入本机直出的 Samsung DeX 桌面模式。
