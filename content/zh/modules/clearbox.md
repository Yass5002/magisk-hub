---
id: "clearbox"
title: "ClearBox：高速系统清理、文件分类与磁盘 GC 套件"
sidebarTitle: "ClearBox"
description: "全面高效的系统清理与文件系统维护引擎，提供基于规则的缓存清理、深度文件分类过滤、磁盘 GC 以及终端 TUI 控制。"
category: "system-utilities"
tier: 1
searchQueries:
  - "clearbox magisk 模块"
  - "flycom-e clearbox 下载"
  - "安卓 f2fs 磁盘 gc 清理 root"
  - "clearbox wipe_cache 规则配置"
  - "终端 tui 安卓系统清理模块"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "Android 8.0 或更高版本"
  - "用于运行 TUI 的终端模拟器（Termux）或配套 Android 管理应用"
conflicts: []
configPaths:
  - "/data/adb/wipe_cache/"
  - "/data/adb/wipe_cache/CleanConfigs/"
  - "/data/adb/wipe_cache/FileConfigs/"
  - "/data/adb/modules/ClearBox/"
features:
  - "一键系统优化：快速清理应用临时垃圾、缩略图、空目录并触发内核磁盘 GC"
  - "自定义目录清理规则：支持在 CleanConfigs 中通过纯文本规则文件定义自定义清理目标"
  - "深度文件分类与体积过滤：可在 FileConfigs 中按扩展名及最小/最大字节阈值分组清理文件"
  - "超低开销调度器：由轻量级 Timed 后台进程驱动自动维护，告别常驻守护进程臃肿"
  - "完整终端 TUI：在任意 Root 终端输入 ClearBox 即可启动交互式彩色管理面板"
faq: []
---

## 概述

传统的手机清理工具往往要求常驻前台服务、充斥弹窗广告，且仅清理表面缓存目录，对深层系统残留与存储碎片束手无策。

由 FLYCOM-E 开发的 **ClearBox** 是一款面向已 Root Android 设备的开源高吞吐系统维护套件。专为兼顾执行速度与配置灵活性而打造，兼容 Magisk、APatch 与 KernelSU，可通过交互式终端界面（TUI）或可选配套 APK 实现深层文件系统垃圾清理、空文件夹清除、自定义路径清理以及文件系统垃圾回收（GC）。

## 核心功能

### 1. 高速缓存与垃圾清理
- **第三方应用缓存清扫**：清理已安装应用积累的 WebView 缓存、网络缓冲区与缩略图数据库，同时保留持久化的用户数据与登录状态。
- **空目录清除**：递归扫描内置与外置存储，删除已卸载应用遗留的空目录树。
- **磁盘垃圾回收（GC）**：在现代 F2FS 分区上触发文件系统级垃圾回收，整理合并数据块以改善读写延迟。

### 2. 自定义目录规则（`CleanConfigs`）
用户只需将文本规则文件放入 `/data/adb/wipe_cache/CleanConfigs/`，即可声明需要自动清理的指定目录或缓存位置：
- 支持初始根路径锚点定义（`@/sdcard/Download/temporary`）。
- 逐行编写相对路径与绝对文件路径，实现精准的规则化清理定位。

### 3. 深度文件分类（`FileConfigs`）
在 `/data/adb/wipe_cache/FileConfigs/` 目录下，用户可创建 `.conf` 配置文件，按文件扩展名与体积范围进行筛选清理：
```conf
# Target archive files between 10MB and 1GB
@MAX=1/G @MIN=10/M
zip 7z

# Remove specific temporary installation extensions regardless of size
@max=-1
apk tmp
```

## 管理界面

ClearBox 无需常驻图形应用，提供以下两种便捷的操作模式：

1. **交互式终端 TUI**：
   打开 Termux 或 ADB Shell，获取 Root 权限后直接调用命令：
   ```bash
   su -c ClearBox
   ```
   该命令会启动交互式菜单控制台，方便你执行一键清理、管理白名单及查看存储统计信息。
2. **图形化配套应用**：
   模块安装过程中提供可选的图形化管理应用，满足偏好 Android UI 交互的用户需求。

## 安装与配置

1. 从 GitHub 下载最新版 `ClearBox` 发布压缩包。
2. 使用 **Magisk**、**APatch** 或 **KernelSU** 刷入模块。
3. 重启设备。
4. 打开 Termux，运行 `su -c ClearBox` 并执行首次一键系统优化。
