---
id: "deepsuppressor"
title: "DeepSuppressor：后台子进程精细压制与 AMMF2 WebUI 管理模块"
sidebarTitle: "DeepSuppressor"
description: "基于 AMMF2 框架构建的后台进程管理器，通过 JSON 规则与 WebUI 精准压制应用的冗余子进程（推送、统计与小程序进程）。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "deepsuppressor Magisk 模块"
  - "aurora nasa deepsuppressor 下载"
  - "Android Root 压制后台子进程"
  - "ammf2 webui 后台管理"
  - "Android 压制 appbrand 小程序进程"
prerequisites:
  - "通过 KernelSU 或 Magisk 获取 Root 权限"
  - "Android 9.0 及以上系统"
  - "支持 WebUI 的管理器（KernelSU 管理器、KsuWebUIStandalone 或 MMRL）"
conflicts: []
configPaths:
  - "/data/adb/modules/DeepSuppressor/"
  - "/data/adb/modules/DeepSuppressor/module_settings/suppress_config.json"
features:
  - "子进程级精细控制：精准冻结独立的辅助后台子进程（如 `:push`、`:channel`、`:video`），不影响主应用核心服务"
  - "AMMF2 模块化框架：基于 Aurora-Magisk-Modules-Framework-2 构建，CPU 与内存开销极低"
  - "KernelSU WebUI 集成：提供图形化仪表盘，支持按应用一键开关压制策略"
  - "JSON 规则自定义：可在 `suppress_config.json` 中灵活增删目标子进程与启用状态"
faq: []
---

## 概述

现代社交、影音与电商应用往往会衍生出大量独立的辅助子进程（例如 `:push`、`:analytics`、`:mini_program`、`:channel` 与 `:video`）。即便主应用已经退居后台或从最近任务列表中划掉，这些辅助进程仍会常驻内存，持续唤醒 CPU 核心、执行定时后台任务并无端消耗电量。

由 Aurora-Nasa-1 开发并基于 **Aurora-Magisk-Modules-Framework-2（AMMF2）** 构建的 **DeepSuppressor** 是一款智能后台进程监测与压制工具。它不像传统清后台工具那样粗暴杀掉整个父应用（容易导致消息推送失效或重新切回时重载崩溃），而是仅对规则中指定的辅助子进程进行精准拦截与冻结。

## JSON 配置文件结构（`suppress_config.json`）

所有应用定位与子进程规则均保存在 `/data/adb/modules/DeepSuppressor/module_settings/suppress_config.json` 中：

```json
{
  "com.tencent.tim": {
    "enabled": true,
    "processes": [
      "com.tencent.tim:appbrand0",
      "com.tencent.tim:video"
    ]
  },
  "com.example.bloatapp": {
    "enabled": true,
    "processes": [
      "com.example.bloatapp:pushservice",
      "com.example.bloatapp:downloader"
    ]
  }
}
```

- **`enabled`**：控制是否对该包名启用压制策略（`true` 或 `false`）。
- **`processes`**：明确指定当主应用切换至后台时，DeepSuppressor 需要拦截并压制的子进程名称列表。

## WebUI 控制界面

DeepSuppressor 原生集成 **KernelSU WebUI**、**KsuWebUIStandalone** 与 **MMRL**：
- 直观浏览所有已安装应用及其衍生出的子进程。
- 一键开启或关闭指定应用的压制策略。
- 无需手动编辑 JSON 语法即可即时保存规则变更。

## 安装与配置

1. 从发布渠道下载最新的 `DeepSuppressor` `.zip` 安装包。
2. 通过 **KernelSU** 或 **Magisk** 刷入模块。
3. 重启 Android 设备。
4. 打开 Root 管理器的 WebUI 页面，查看已识别的应用列表并配置需要压制的规则。
