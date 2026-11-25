---
id: "rsync-magisk"
title: "Rsync Binary for Magisk：无系统分区修改增量文件同步工具"
sidebarTitle: "Rsync 二进制工具"
description: "通过无系统分区修改方式将静态编译的独立 rsync 二进制程序安装至 /system/bin，用于差异增量备份与远程服务器同步。"
category: "system-utilities"
tier: 1
searchQueries:
  - "rsync magisk 模块下载"
  - "AdalynAstatine rsync-magisk"
  - "Android Root 安装 rsync 命令"
  - "手机 rsync 增量备份教程"
  - "Android 静态编译 rsync 二进制"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/rsync-magisk/"
features:
  - "静态链接二进制文件：完全独立的可执行程序，零动态库依赖，确保在 Android Bionic 环境下稳定运行"
  - "无侵入式注入 /system/bin：自动进入系统 PATH 环境变量，在各类 Root Shell、Termux 与后台脚本中开箱即用"
  - "高效差异增量传输：通过校验文件块差异仅传输改动部分，大幅节省网络带宽与闪存 I/O 开销"
  - "服务器与 NAS 同步：可将手机内部存储目录、相册图库与分区备份镜像同步至远程 Linux 或 SSH 存储节点"
  - "零系统分区改动：借助 Magisk Magic Mount 机制实现无损挂载部署"
---

## 概述

对于系统管理员、开发者和进阶玩机用户而言，**rsync** 是跨 POSIX 系统进行高速增量文件复制与远程同步的黄金标准工具。然而标准 Android 系统出厂并未自带 rsync，用户在传输海量相册图库或大型备份目录时，往往只能依赖笨重的 Termux 环境或速度缓慢的 USB MTP 协议。

由 AdalynAstatine 开发的 **rsync-magisk** 是一款轻量级无系统分区修改工具模块，可直接将静态编译好的 `rsync` 二进制文件部署至 `/system/bin/` 目录。

## 常见应用场景

1. **局域网增量备份**：通过 SSH 将手机的 `/sdcard/DCIM/Camera/` 相册目录直接增量同步至家庭服务器或网络附加存储（NAS）：
   ```bash
   su -c rsync -avz --progress /sdcard/DCIM/Camera/ user@nas.local:/volume1/backups/phone_photos/
   ```
2. **自动化定时同步**：将 rsync 与 Tasker、Cron（例如通过 `crond4android`）或开机脚本结合，在手机连入家庭 Wi-Fi 且接通电源时自动镜像备份重要文件夹。
3. **分区镜像与应用备份同步**：快速将本地导出的分区 `.img` 镜像或 Titanium/Swift Backup 备份目录镜像至外接硬盘，无需重复拷贝未发生变更的文件。

## 安装与验证

1. 从 GitHub 下载最新版的 `rsync-magisk.zip` 发布包。
2. 打开 **Magisk**，进入 **模块 > 从本地安装** 并刷入压缩包。
3. 重启设备。
4. 在 Termux 或 ADB Shell 中验证可执行文件是否就绪：
   ```bash
   su
   rsync --version
   ```
