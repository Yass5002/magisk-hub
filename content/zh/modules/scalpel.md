---
id: "scalpel"
title: "Scalpel：Android 精准系统精简与用户应用系统化工具"
sidebarTitle: "Scalpel 系统精简"
description: "专为 Root Android 设备打造的精准精简（Debloat）与应用系统化工具，安全禁用厂商与运营商预装软件，并将用户应用提升为系统 priv-app 特权应用。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Scalpel Magisk 系统精简"
  - "Enginex0 Scalpel 模块"
  - "KernelSU 用户应用转为系统应用"
  - "Magisk 安全屏蔽厂商预装软件"
  - "Root 精简系统内置应用模块"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/scalpel/"
features:
  - "外科手术级精准精简：选择性替换或屏蔽运营商预装软件、遥测组件以及厂商自带臃肿应用"
  - "应用系统化（Systemize）：将选定的第三方用户应用提升至 /system/priv-app/ 目录，获取系统级特权权限"
  - "零风险安全回滚：全程通过无系统分区修改的叠加挂载机制运行，出现异常时可瞬间恢复原状"
  - "跨 Root 管理器引擎：原生兼容 Magisk、KernelSU 与 APatch 环境"
  - "内置预设精简清单：提供经社区验证的各大主流厂商（小米、三星、一加、Google）精简配置模板"
---

## 概述

现代 Android 厂商固件通常预装了大量冗余统计守护进程、重复云同步服务以及运营商推广软件。若直接从只读系统分区中手动删除这些安装包，极易触发 dm-verity 校验异常、破坏系统 OTA 升级，甚至在误删关键依赖组件后导致设备无法开机。

由 Enginex0 编写的 **Scalpel** 是一款专为 Root Android 设备设计的精准系统精简与应用系统化工具。Scalpel 兼顾安全性与易用性，让用户能够零风险地清理不必要的系统臃肿组件，并将第三方应用提升为拥有特权的系统级应用。

## 核心功能

### 1. 精准系统精简（Debloat）
- **无侵入式屏蔽**：在 `/system/app/`、`/product/app/` 或 `/system/priv-app/` 中需要精简的目标 APK 文件夹上挂载空目录以实现屏蔽。
- **故障安全机制**：若屏蔽某个应用后导致系统不稳定，只需在 Root 管理器中关闭本模块并重启，原厂预装应用即可完好无损地恢复。

### 2. 应用系统化（App Systemization）
- **特权等级提升**：将用户安装的应用（例如第三方桌面启动器、自动化工具或网络代理工具）迁移挂载至 `/system/priv-app/`。
- **解锁系统限制权限**：直接赋予应用受限的 Android 系统级权限——如 `ACCESS_BACKGROUND_LOCATION`、通知监听权限或设备管理能力——无需在每次重启后反复通过 ADB 授权。

## 支持的 Root 环境

Scalpel 从底层架构即针对现代主流 Root 管理框架进行了适配：
- **Magisk**（v20.4+）
- **KernelSU**（v0.6.0+）
- **APatch**（v10.5+）

## 安装与使用

1. 从 GitHub Releases 下载最新版的 `scalpel-v*.zip` 压缩包。
2. 通过你的 Root 管理器刷入该模块。
3. 重启设备。
4. 按照模块的交互式终端向导指引操作，或直接编辑 `/data/adb/modules/scalpel/` 目录下的配置文件，指定需要精简或转为系统应用的目标软件。
