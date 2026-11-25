---
id: "rclone-fuse3-magisk"
title: "Rclone FUSE3 Magisk 模块：无系统分区修改云盘挂载与自动化"
sidebarTitle: "Rclone FUSE3 挂载"
description: "将 Rclone 与 FUSE 3.17.x 集成至 Android 系统，把 Google Drive、OneDrive、WebDAV 与 S3 等远程云存储直接挂载为本地目录。"
category: "system-utilities"
tier: 1
searchQueries:
  - "rclone fuse3 magisk 下载"
  - "NewFuture rclone magisk 模块"
  - "Android Root 挂载 Google Drive"
  - "手机 rclone fuse 挂载云盘到本地"
  - "Android WebDAV 挂载本地目录"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
  - "支持 FUSE 文件系统的 Android 设备内核（已启用 /dev/fuse）"
conflicts: []
configPaths:
  - "/data/adb/modules/rclone-fuse3-magisk/"
features:
  - "FUSE 3.17.x 集成：内置新版 libfuse3 二进制组件，将远程云存储映射为本地文件系统挂载点"
  - "开机自动挂载：系统启动时自动为已配置的云存储服务初始化挂载点"
  - "内嵌 Web GUI：可通过 Rclone Web UI 直观配置远程凭据、同步任务与目录管理"
  - "广泛云生态支持：兼容 Google Drive、Microsoft OneDrive、Dropbox、S3、WebDAV 与 SFTP 等数十种存储后端"
  - "应用无缝兼容：让本地媒体播放器、模拟器与文件管理器可直接读写云端文件"
---

## 概述

Rclone 素有“云存储界的瑞士军刀”之称，支持在 POSIX 操作系统上同步、复制并挂载数十种不同的云端存储服务。然而在 Android 平台上，将远程云盘直接挂载到本地文件系统目录树中，需要 Root 权限以及正常可用的 FUSE（用户空间文件系统）库支持。

由 NewFuture 维护的 **rclone-fuse3-magisk** 是一款无系统分区修改的 Magisk 模块，内建完整编译的 Rclone 二进制程序与 **libfuse 3.17.x**。借助该模块，已获取 Root 权限的 Android 设备可将远程云端存储空间直接挂载到可访问的本地目录（如 `/mnt/cloud/` 或 `/sdcard/Cloud/`），让任何本地 Android 应用都能像读取本地文件一样透明访问云盘内容。

## 核心特性

1. **原生 FUSE 挂载引擎**：采用针对 Android 内核 FUSE 接口（`/dev/fuse`）优化的 libfuse3 用户空间驱动。
2. **开机自动化脚本**：只需完成一次远程配置，模块即可在每次系统启动时自动执行挂载。
3. **Web 可视化控制台**：支持启动官方 Rclone Web GUI，直接在手机浏览器中管理远程存储节点与传输规则。
4. **透明文件流式访问**：无需预先将整部视频下载到本地，即可直接在 VLC 或 MX Player 中流畅播放 OneDrive 或 Google Drive 内的影音文件。

## 快速上手与使用

1. 从 GitHub 下载最新版的 `magisk-rclone_arm64-v8a.zip` 发布包。
2. 在 **Magisk** 中刷入模块并重启设备。
3. 生成你的 Rclone 远程配置文件：
   ```bash
   su -c rclone config
   ```
4. 根据交互式向导提示完成配置，关联你常用的云存储服务（如 Google Drive、OneDrive 或 WebDAV）。
5. 在模块的服务脚本中配置开机自动挂载，或直接通过 `rclone mount <remote>: <mountpoint> --daemon` 手动触发挂载。
