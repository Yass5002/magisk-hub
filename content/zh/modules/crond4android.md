---
id: "crond4android"
title: "crond4Android：Android Root 原生 Cron 守护进程与定时任务自动化"
sidebarTitle: "crond4Android"
description: "在 KernelSU、APatch 与 Magisk 环境下部署基于 BusyBox 的轻量级 crond 调度器，支持 crontab CLI 命令、任务持久化及 WebUI 界面。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "crond4android Magisk 模块"
  - "powerAn2020 crond4android"
  - "Android Root cron 守护进程"
  - "KernelSU APatch crontab 命令"
  - "Android 后台定时脚本调度"
prerequisites:
  - "通过 KernelSU、APatch 或 Magisk 获取 Root 权限"
  - "BusyBox 环境（由 Root 方案自带或使用内置辅助程序）"
conflicts: []
configPaths:
  - "/data/adb/crond/logs/run.log"
  - "/data/adb/crond/spool/"
  - "/data/adb/crond/conf/"
  - "/system/bin/crontab"
features:
  - "原生 BusyBox crond 引擎：在后台静默执行标准 UNIX cron 语法格式的定时任务"
  - "WebUI 可视化管理：支持在 KernelSU、APatch 与 MMRL 界面中直接查看与编辑计划任务"
  - "防检测安装开关：支持不注入全局 `/system/bin/crontab` 二进制文件，以规避应用 Root 环境扫描"
  - "数据持久化保护：支持 `KEEP_ON_UNINSTALL` 标志，在模块更新或重装时保留自定义任务配置"
  - "精细化启动控制：创建简单的 `MANUAL` 标志文件即可按需禁用开机自启"
faq: []
---

## 概述

在 Android 上实现后台任务自动化（例如定时备份数据库、夜间清理缓存、切换网络状态或动态执行配置脚本），通常需要依赖 Tasker 或 Termux:Boot 等体积较重的应用长驻后台。相比之下，标准 Linux 服务器采用的是轻量且久经考验的 `cron` 守护进程。

由 powerAn2020 开发的 **crond4Android** 通过 **KernelSU**、**APatch** 与 **Magisk** 将原生 `crond` 守护进程移植到了 Android 平台。借助 BusyBox 高效的 cron 引擎，该模块提供了标准的 UNIX `crontab` 环境、完整的执行日志记录以及集成的 WebUI 界面，让你无需消耗额外电量即可轻松调度定时任务。

## 文件目录与存储结构

所有守护进程配置、计划任务队列（Spool）以及执行日志均独立存放在 `/data/adb/crond/` 目录下：

- **Cron 任务队列目录**：`/data/adb/crond/spool/`  
  存放按用户划分的 cron 任务表，Root 任务位于 `/data/adb/crond/spool/root`。
- **执行日志文件**：`/data/adb/crond/logs/run.log`  
  记录每次触发任务的时间戳、脚本输出内容与报错信息。
- **配置标志目录**：`/data/adb/crond/conf/`  
  存放用于调整模块行为的开关标志文件。

## 运行标志与个性化定制

该模块支持在 `/data/adb/crond/conf/` 目录下放置多种运行控制标志文件：

- **卸载时保留任务**：创建空文件 `/data/adb/crond/conf/KEEP_ON_UNINSTALL`，可确保在卸载或更新模块时不会清除你编写的 cron 脚本和任务队列。
- **禁用开机自启动**：创建 `/data/adb/crond/conf/MANUAL`，即可阻止 `crond` 在设备开机时自动启动。
- **隐蔽 / 防检测安装模式**：自 1.0.3 版本起，仅当你在安装前预先创建内容为 `1` 的 `/sdcard/crond4android.setup` 文件时，安装脚本才会创建 `/system/bin/crontab` 软链接。保持未设置状态可避免暴露全局二进制文件，降低被银行类应用检测的风险。

## 通过 CLI 管理 Cron 任务

你可以使用标准的 UNIX cron 语法来管理定时作业：

```bash
# Add a nightly log cleanup task running at 04:30 AM
echo '30 4 * * * echo "" > /data/adb/crond/logs/run.log' >> /data/adb/crond/spool/root

# List currently scheduled cron jobs
su -c crontab -l

# Open interactive crontab editor
su -c crontab -e
```

## 安装与使用 WebUI

1. 下载最新版本的 `crond4Android` 发布包（ZIP）。
2. 在 **KernelSU**、**APatch** 或 **Magisk** 中刷入该模块。
3. 重启设备。
4. 直接在 KernelSU 管理器或 MMRL 中打开该模块的 WebUI 即可图形化配置计划任务，或通过标准终端命令进行管理。
