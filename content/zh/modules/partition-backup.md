---
id: "partition-backup"
title: "Partition Backup：面向 Android 的块级原始分区备份工具"
sidebarTitle: "Partition Backup"
description: "功能全面的 Root 分区工具，支持通过 CLI 命令行或 WebUI 界面查看、列出并生成 Android 关键分区的原始块级镜像备份。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Partition Backup Magisk 模块"
  - "rhythmcache partition-backup 下载"
  - "Android Root 备份分区镜像"
  - "手机提取 boot vendor system img 镜像"
  - "KernelSU WebUI 分区备份工具"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "具备充足的可用存储空间（内部存储或 USB OTG 闪存盘）以存放分区镜像文件"
conflicts: []
configPaths:
  - "/data/adb/modules/partition-backup/"
features:
  - "双交互界面支持：可通过直观的 WebUI 仪表盘（KernelSU/APatch）或终端命令行界面（CLI）管理备份"
  - "按需精准提取分区：指定具体分区名称（如 boot、init_boot、vendor_boot、persist）即可导出原始 .img 镜像"
  - "分区表查询：使用 partition -l 列出设备上所有物理块设备与当前活动分区"
  - "自定义输出路径：支持将导出的镜像保存至内部存储任意目录或外接 USB-C 闪存盘"
  - "全平台 Root 管理器兼容：在 Magisk、KernelSU 与 APatch 环境下均具备一致的运行表现"
---

## 概述

在刷入实验性内核、第三方 ROM、GSI 镜像或进行底层 Root 修改之前，对关键分区（如 `boot`、`init_boot`、`vendor_boot`、`persist` 以及基带 `efs` 分区）进行原始块级镜像备份，是防止设备变砖最有效的一道保险。

由 rhythmcache 开发的 **partition-backup** 是一款综合性系统实用工具，大幅简化了原始分区镜像的提取与归档流程。它同时提供独立的命令行可执行程序（`partition`）与适配现代 Root 管理器的集成 **WebUI** 控制面板，无需连接电脑或依赖有线 ADB，即可在手机本地安全导出与备份分区块数据。

## 命令行接口（`partition`）

在 Termux 中以 Root 权限运行 `partition` 命令：

```bash
Usage: partition [OPTIONS]

Options:
  -b, --backup PARTITIONS     Backup partitions (comma-separated list, e.g. boot,vendor)
  -d, --directory DIR         Target backup directory (default: current working directory)
  -l, --list                  List all available block partitions on the device
  -h, --help                  Show help information
```

### 常用命令示例

1. **列出所有可用分区**：
   ```bash
   su -c partition -l
   ```
2. **将关键引导与厂商分区备份至内部存储**：
   ```bash
   su -c partition -b boot,vendor_boot,init_boot -d /sdcard/PartitionBackups
   ```
3. **刷入第三方 ROM 前备份所有核心基础分区**：
   ```bash
   su -c partition -b boot,vendor,system,persist -d /sdcard/Download
   ```

## WebUI 可视化管理

对于使用 **KernelSU** 或 **APatch** 的用户，该模块内置了直观的 WebUI 界面。只需打开 Root 管理器应用，找到 Partition Backup 模块卡片并点击 WebUI 按钮，即可浏览全部设备分区并一键勾选执行备份。

## 安装步骤

1. 下载最新版本的 `partition-backup-*.zip` 发布包。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入该模块。
3. 重启设备以启用 CLI 命令行二进制文件及 WebUI 资源。
