---
id: "magisk-asoulopt"
title: "AsoulOpt：智能内核调度器与温控调优模块"
sidebarTitle: "AsoulOpt"
description: "面向高通骁龙、联发科天玑与三星 Exynos 芯片的内核优化模块，动态调节 CPU/GPU 调度器、I/O 调度策略与温控阈值。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "AsoulOpt Magisk 模块下载"
  - "Android Root 游戏内核优化模块"
  - "nakixii Magisk_AsoulOpt 配置教程"
  - "Android Root CPU 调度器调校"
  - "改善温控降频 Root 模块"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "ARM64 架构 Android 设备（高通骁龙 / 联发科天玑 / 三星 Exynos）"
conflicts:
  - "其他冲突的性能优化模块（例如同时安装 FDE.AI、LKT、NFS Injector）"
configPaths:
  - "/data/adb/modules/Magisk_AsoulOpt/"
  - "/data/adb/asoulopt/"
features:
  - "逐核心 CPU 调频与能效感知调度（EAS）精细调校"
  - "GPU 温控阈值优化，抑制大型 3D 手游（如《原神》《战区》）突发掉帧"
  - "动态场景识别：检测到游戏启动自动提升频率下限，熄屏后自动降频省电"
  - "针对 UFS 3.1 与 UFS 4.0 闪存精细调优 Linux I/O 调度配置"
faq:
  - question: "使用 AsoulOpt 会导致耗电增加吗？"
    answer: "不会。由于模块使用更平滑且注重能效的 EAS 调频策略取代了激进紊乱的原厂温控调度，日常刷信息流或社交应用时的续航往往反而有所提升，同时减少高负载游戏时的峰值功耗浪费。"
  - question: "模块是如何识别游戏正在运行的？"
    answer: "AsoulOpt 会监听 Android 前台 Activity 状态与 SurfaceFlinger 渲染窗口。当游戏配置列表中的应用切换至前台时，会自动抬升 CPU/GPU 最低频率并放宽温控预算。"
---

## 概述

由 **nakixii** 开发的 **AsoulOpt**（Magisk_AsoulOpt）是目前 Android 玩机与手游社区中最受青睐的性能调优模块之一。

众多现代旗舰处理器（如骁龙 8 Gen 1/2/3 与天玑 9000 系列）均受制于保守的原厂温控降频策略：一旦机身温度触及设定阈值，OEM 温控引擎便会直接将 CPU 频率腰斩 50% 以上，从而引发剧烈的帧率波动。AsoulOpt 通过经过校准的调度策略替代原厂温控降频曲线，显著稳定帧时间输出并充分发挥硬件能效。

---

## 技术架构与工作原理

### EAS 与 sysfs 节点调优

1. **CPU 能量模型校准**：
   - 模块直接向内核 sysfs 节点（`/sys/devices/system/cpu/cpu*/cpufreq/`）写入调优参数。
   - 调整 `schedutil` 调度器核心参数（如 `up_rate_limit_us`、`down_rate_limit_us` 与 `hispeed_freq`），让升降频过渡更加顺滑自然。
2. **温控区间（Thermal Zone）调节**：
   - 调整 `/sys/class/thermal/thermal_zone*/trip_point_*_temp` 触发温度节点，在硬件安全耐受范围内适当放宽保守的原厂温控墙。
3. **内存与 ZRAM 压缩策略**：
   - 微调内核 VM 参数（`swappiness`、`vfs_cache_pressure`、`dirty_ratio`），避免 Android 低内存杀手（LMK）过度回收后台应用。
4. **存储 I/O 调度优化**：
   - 针对 UFS 块设备（`/sys/block/sd*/queue/read_ahead_kb`）优化请求队列深度与预读缓冲区，加快游戏加载与资源流式读取速度。

---

## 安装与配置

1. 打开 **Magisk**、**KernelSU** 或 **APatch**。
2. 刷入最新版本的 `Magisk_AsoulOpt-vX.zip`。
3. 重启设备。
4. 模块会在开机过程中自动运行硬件探测脚本，针对设备具体的 SoC 架构（如 big.LITTLE 双簇或三簇架构）匹配对应参数。
