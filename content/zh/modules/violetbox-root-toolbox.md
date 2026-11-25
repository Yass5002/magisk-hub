---
id: "violetbox-root-toolbox"
title: "VioletBox Root Toolbox：Android 全能高级 Root 系统管理套件"
description: "由 Smart-Paocai 打造的一站式 Android Root 玩机工具箱，涵盖 SELinux 模式切换、物理分区读写刷入、基带字库备份、模块批量刷写与设备 ID 修改。"
category: "system-utilities"
author: "Smart-Paocai"
version: "1.0.0"
updatedAt: "2026-10-04"
compatibility: ["Magisk", "KernelSU", "APatch"]
---

## 概述与系统架构

由开发者 Smart-Paocai 打造的 **VioletBox（紫罗兰工具箱）** 是一款专为极客玩家、ROM 修改者与设备维护人员打造的高级移动端 Root 工具箱。作为电脑端紫罗兰工具箱（Violet PC Toolkit）的独立手机端版本，VioletBox 将数十项底层 Android 系统维护与刷机操作整合进统一的图形化界面，无需连接电脑即可在手机上直接完成操作。

## 核心内置功能

1. **SELinux 模式控制器**：支持在 Enforcing（严格模式）与 Permissive（宽容模式）之间自由切换，并支持配置开机自动持久化生效。
2. **可视化分区管理**：提供直观的分区浏览器，可直接对底层 eMMC/UFS 物理存储块执行原始镜像读取、写入、提取（Dump）与擦除操作。
3. **基带与字库备份**：一键生成 `modem`、`persist` 及 `NVRAM/EFS` 等关键分区的完整二进制备份，格式兼容高通 9008（EDL）紧急救砖模式或 Fastboot/Bootloader 线刷恢复。
4. **Root 模块批量管理器**：支持在 Magisk、KernelSU 与 APatch 环境下批量安装、更新及统筹管理模块。
5. **系统应用管理**：集成特权级应用冻结、卸载、APK 提取及后台进程管控功能。
6. **全局机型与设备 ID 伪装**：内置设备参数伪装及 Android ID 修改工具。
7. **云端 OTA 提取器**：支持从 Android 官方 OTA 刷机包中快速云端解析并提取指定镜像文件（Payload）。

## 安装与配置

### 第一步：安装 APK
下载并安装 `VioletBox_V1.0.0_release.apk`。

### 第二步：授予 Root 权限
启动 VioletBox，并在 Magisk、KernelSU 或 APatch 弹出授权请求时授予永久超级用户（Superuser）权限。

### 第三步：验证 SELinux 状态
在应用内尝试切换 SELinux 模式后，可通过终端命令确认当前生效状态：
```bash
getenforce
```

## 安全注意事项

> [!CAUTION]
> “分区管理”与“原始块写入”功能会直接向底层物理存储分区（`/dev/block/bootdevice/by-name/`）写入数据。若将损坏或不匹配的镜像刷入 `boot`、`abl`、`xbl` 或 `modem` 等核心引导分区，将导致设备彻底变砖（硬砖）。在执行任何写入操作前，请务必再三核对分区名称与镜像来源。
