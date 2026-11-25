---
id: "basiccleaner"
title: "BasicCleaner：自动化周期存储整理、缓存清理与 ART 优化"
sidebarTitle: "BasicCleaner"
description: "自主运行的系统维护工具，按周期自动调度 fstrim 分区整理、应用缓存清理、APK zipalign 对齐与 ART 配置文件优化。"
category: "system-utilities"
tier: 1
searchQueries:
  - "basiccleaner magisk 模块"
  - "weirdmidas basiccleaner 下载"
  - "安卓自动 fstrim 存储优化 root"
  - "art 运行时自动编译优化 magisk"
  - "android 定时清理维护模块"
prerequisites:
  - "Android 8.0 或更高版本"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "采用标准 Linux 分区布局的设备存储"
conflicts: []
configPaths:
  - "/data/adb/modules/basiccleaner/"
  - "/sdcard/Android/basiccleaner.log"
features:
  - "周期性分区 fstrim（每 7 天）：回收 /system、/data、/cache、/persist、/vendor 与 /product 等分区的闲置 NAND 闪存块"
  - "应用缓存清理（每 7 天）：清除应用临时垃圾与目录缓存，不会清除用户登录状态"
  - "字节码 zipalign 对齐（每 15 天）：将未压缩 APK 资源偏移量按 4 字节边界对齐，加快内存映射速度"
  - "ART 运行时优化（每 30 天）：同步运行时配置文件、清理失效编译产物并执行后台 dexopt 编译"
  - "开机延迟触发：设备启动 2 分钟后再执行检查，避免开机阶段与系统争抢 CPU 资源"
faq: []
---

## 概述

Android 设备在日常使用数月后，会逐渐积累存储碎片、无主 Dalvik/ART 缓存文件以及未对齐的应用程序包。虽然市面上存在手动优化脚本，但定期在终端手动执行命令并不现实；而每次开机都执行全盘缓存清理，又会造成不必要的 NAND 闪存写入损耗并拖慢应用冷启动速度。

由 WeirdMidas 开发的 **BasicCleaner** 是一款面向已 Root Android 设备的自动化定期间隔维护工具。该模块设计为完全自主运行，通过评估上次执行的时间戳按周期分级执行维护任务——从每周一次的 NAND 闪存整理（Trim）到每月一次的 ART 预先编译（AOT），确保持久流畅的系统性能。

## 定时维护周期

BasicCleaner 会在**开机 2 分钟后**启动周期评估，确保关键系统引导流程与前台 UI 渲染完全不受后台 I/O 操作干扰。

### 1. 每 7 天：存储整理与缓存清理
- **分区 `fstrim`**：对所有活动分区（`/system`、`/data`、`/cache`、`/persist`、`/vendor`、`/system_ext`、`/product`）下发 discard 指令，通知 UFS/eMMC 主控擦除未使用的闪存块，恢复写入吞吐性能。
- **应用缓存清理**：清扫临时目录与应用缓存，且不破坏用户偏好设置、登录凭证或本地数据库文件。

### 2. 每 15 天：应用字节对齐
- **`zipalign` 检查**：扫描用户已安装的 APK 安装包，将数据边界按 4 字节偏移量对齐，降低 Android 通过 `mmap` 直接从磁盘读取资源时的内存占用。

### 3. 每 30 天：Android 运行时（ART）深度清理
- **ART 同步**：清除已卸载应用或系统更新后遗留的过期编译产物。
- **后台 `dexopt` 编译**：依据实际使用配置文件将高频调用的应用方法重新编译为优化的本地机器码（`cmd package bg-dexopt-job`）。

## 状态监控与运行日志

BasicCleaner 会将各项操作记录及耗时统计以可读日志形式直接保存在内部存储中：

```
/sdcard/Android/basiccleaner.log
```

你可以在 Termux 或任意文本查看器中直接查阅近期的维护时间戳：
```bash
cat /sdcard/Android/basiccleaner.log
```

## 安装与配置

1. 从官方仓库发布页下载 `BasicCleaner` `.zip` 安装包。
2. 使用 **Magisk** 或 **KernelSU** 刷入该模块。
3. 重启设备。
4. 无需额外手动配置，维护调度器将在后台自动追踪周期并按计划执行任务。
