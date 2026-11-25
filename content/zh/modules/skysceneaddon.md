---
id: "skysceneaddon"
title: "SkyScene Add-on：进阶 Android 内核内存与 ZRAM 优化"
sidebarTitle: "SkyScene Add-on"
description: "针对新老 ARM 设备全面优化内核内存管理、ZRAM 交换算法、LRU/MGLRU 页面回收策略与 cgroup 进程队列。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "SkyScene Addon Magisk 模块"
  - "WeirdMidas SkySceneAddon 下载"
  - "Android MGLRU ZRAM 优化"
  - "安卓内存抖动掉帧修复 Root"
  - "KernelSU 内存管理优化模块"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "运行 Linux 4.x、5.x 或 6.x 内核的 ARM 或 ARM64 Android 设备"
conflicts: []
configPaths:
  - "/data/adb/modules/SkySceneAddon/"
features:
  - "跨代内核内存支持：分别为现代 MGLRU（cgroups v2）与传统页面回收架构（LRU / cgroups v1）内置专属启发式调优参数"
  - "消除内存抖动：精细调节脏页回写与 kswapd 唤醒周期，防止高强度多任务切换时出现严重界面掉帧"
  - "ZRAM 与交换流调优：优化内存压缩交换队列，在解压延迟与内存可用密度之间取得最佳平衡"
  - "LMK 队列协同：将内核内存压力事件通知与 Android 用户态低内存杀手（LMK）队列紧密同步"
  - "通用无侵入式调优：在开机服务后期动态写入 sysctl 与 sysfs 内存参数，全程不修改系统分区"
---

## 概述

导致 Android 设备出现严重掉帧、界面冻结以及应用闪退的主要元凶之一是**内存抖动（Memory Thrashing）**——这是一种病理状态，此时 Linux 内核将大量 CPU 周期浪费在把内存页反复压缩进 ZRAM 以及驱逐文件缓存上，导致真正用于运行前台应用的算力所剩无几。原厂 Android 固件默认的内存回收阈值往往校准不当，进一步加剧了这一问题。

由 WeirdMidas 开发的 **SkySceneAddon**（SkyScene Add-on）是一款专业的内存管理优化模块。它旨在弥合新老两代 Android 内核架构之间的差异，应用经过验证的参数公式来理顺内存交换、页面缓存回收与 ZRAM 压缩流程。

## 架构与核心优化

### 1. 现代与传统内核分层调优
- **现代硬件平台（MGLRU 与 cgroup v2）**：精细调校多代 LRU（Multi-Gen LRU）的世代扫描间隔与收益比参数，使 Linux 5.10+ 内核能够更精准地识别不活跃内存页。
- **传统老旧平台（Active/Inactive LRU 与 cgroup v1）**：重新校准经典双链表页面扫描器参数，大幅减少老旧 32 位与 64 位设备上的 CPU 自旋锁竞争。

### 2. ZRAM 数据压缩与分页调度
- 优化匿名内存交换倾向（`vm.swappiness`）与文件系统缓存压力（`vm.vfs_cache_pressure`）。
- 确保高频读取的应用代码页尽可能保留在物理内存中，同时将极少访问的后台堆内存高效压缩至 ZRAM。

### 3. 防内存抖动与 LMK 协同
- 同步内核内存压力事件上报与用户空间低内存杀手（`lmkd`）守护进程的响应节奏。
- 在避免系统过早误杀后台进程的同时，确保前台大型游戏与相机拍摄任务始终能第一时间获得连续无碎片的物理内存页。

## 安装与支持

- **支持的 Root 方案**：完全兼容 **Magisk** 与 **KernelSU**。
- **安装步骤**：
  1. 从 GitHub Releases 下载 `SkyScene.Add-on.zip` 安装包。
  2. 在你的 Root 管理器中刷入模块并重启设备。
  3. 后台服务脚本会自动识别设备当前内核所支持的机制（LRU 或 MGLRU），并自动下发匹配的优化配置。
