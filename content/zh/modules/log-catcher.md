---
id: "log-catcher"
title: "Log-Catcher：自动化开机 Logcat 与内核日志收集归档工具"
sidebarTitle: "Log Catcher"
description: "在系统启动阶段自动抓取 logcat 与 dmesg 日志，并在设备解锁后自动将其打包归档为带时间戳的压缩文件保存至内部存储。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "Log-Catcher Magisk 模块"
  - "hxreborn Log-Catcher"
  - "Android Root 开机抓取 logcat"
  - "KernelSU 开机日志抓取模块"
  - "Android 内核 dmesg 捕获模块"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/local/logcatcher/config"
  - "/data/adb/modules/Log-Catcher/"
features:
  - "早期启动捕获：从系统最早期执行阶段起即开始记录内核 `dmesg` 与系统 `logcat` 日志"
  - "解锁后自动打包：在存储解密完成后，自动将捕获日志打包为带时间戳的 `.tar.gz` 压缩包并存放在 `/sdcard/Download`"
  - "可选缓冲区流：支持按需选择收集 `main`、`system`、`radio` 与 `crash` 等 logcat 缓冲区"
  - "自动轮转与清理：强制限制最大日志文件数量，并自动清理超过指定天数的旧归档（默认保留 7 天）"
  - "Root 管理器集成：为 KernelSU 与 APatch 提供原生 WebUI 面板，同时为 Magisk 提供简洁的纯文本配置文件"
faq: []
---

## 概述

在 Android 上排查早期启动崩溃、随机系统重启与内核 Panic 时，由于存储加密机制以及日志守护进程在首次解锁屏幕前无法向用户空间暴露日志文件，调试过程往往十分困难。

由 hxreborn 维护（基于 Jaida Wu 与 Howard Wu 的早期作品构建）的 **Log-Catcher** 是一款专为自动化收集系统启动诊断信息而设计的 Root 日志模块。它会在开机阶段拦截内核环形缓冲区（`dmesg`）与 Android 框架日志（`logcat`），并在解锁后将其整理归档为结构清晰、带时间戳的压缩包。

## 工作原理

1. **早期启动拦截**：只要 Root 守护进程服务初始化完成，Log-Catcher 便会立即开始捕获指定的 logcat 缓冲区（`main,system,crash`）以及内核诊断信息流。
2. **解锁后归档**：当设备锁屏成功解锁且内部存储 `/sdcard/` 完成挂载与解密后，模块会将捕获到的日志打包为带时间戳的 `.tar.gz` 压缩文件并输出至 `/sdcard/Download` 目录。
3. **保留策略与自动清理**：后台服务会执行例行清理任务，检查现有归档的修改时间，自动删除超过 `PRUNE_DAYS` 天数或超出 `MAX_LOGS` 上限的旧日志。

## 参数配置

在 **KernelSU** 和 **APatch** 中，你可以直接通过模块内置的 WebUI 控制面板管理各项配置。

在 **Magisk** 环境下，可通过编辑 `/data/local/logcatcher/config` 文件修改参数：

```sh
EXPORT_PATH=/sdcard/Download
MAX_LOGS=10
PRUNE_DAYS=7
BUFFERS=main,system,crash
PERSISTENT=false
```

- **`EXPORT_PATH`**：用于存放 `.tar.gz` 日志压缩包的目标目录。
- **`MAX_LOGS`**：触发自动删除旧文件前最多保留的日志归档数量。
- **`PRUNE_DAYS`**：旧归档文件的保留天数阈值，超过该天数将被自动清理。
- **`BUFFERS`**：以英文逗号分隔的待录制 logcat 缓冲区列表。
- **`PERSISTENT`**：设为 `true` 时将在后台持续不间断录制 logcat 日志。

## 安装步骤

1. 从 GitHub Releases 下载最新的 `hxr_logcat.zip` 模块包。
2. 通过 **Magisk**、**KernelSU** 或 **APatch** 安装。
3. 重启设备即可开启自动化日志收集。
