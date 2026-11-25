---
id: "azenith"
title: "AZenith：全能型 Android 动态内核、进程与温控优化模块"
sidebarTitle: "AZenith"
description: "通用型 Android 性能优化模块，集成前台游戏优先级调度、后台智能冻结、Thermalcore 稳帧控温与专用控制面板。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "azenith Magisk 模块"
  - "liliya2727 azenith 下载"
  - "Android thermalcore 游戏稳帧"
  - "Android 游戏预加载调度优化"
  - "azenith 性能 均衡 省电模式"
prerequisites:
  - "Android 11 及以上系统"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "可选安装配套 APK 以使用图形化控制台配置"
conflicts: []
configPaths:
  - "/data/adb/modules/azenith/"
  - "/data/adb/modules/azenith/azenithApplist.json"
features:
  - "动态进程优先级调度：提升活跃前台游戏的线程调度权重，同时挂起高耗资源后台进程"
  - "Thermalcore 温控调度服务：平缓处理硬件温控降频台阶，持续守住稳定的最低帧率下限"
  - "游戏模式自动切换：根据前台启动的包名在省电（ECO）、均衡（Balanced）与性能（Performance）模式间自动切换"
  - "共享库内存预加载：提前将关键原生库缓存在内存中，加快游戏启动与关卡切换速度"
  - "内核子系统直调：提供 CPU 频率上限、CPU 调度器（Governor）与块设备 I/O 调度器的直接调节"
faq: []
---

## 概述

由 Liliya2727 开发的 **AZenith** 是一款一体化（All-In-One）动态性能调度模块，旨在兼顾高刷新率游戏的稳定性与日常使用的续航表现。与将 CPU 核心长期锁死在最高频率（容易导致机身迅速过热并触发断崖式降频）的静态脚本不同，AZenith 将智能后台守护进程与配套控制台应用相结合，根据当前场景对内核态与用户态参数进行动态微调。

当游戏或高负载应用进入前台时，AZenith 会优先保障其渲染线程，将关联的共享库预加载至内存，并启用专属的 **Thermalcore** 服务来消除突兀的掉帧卡顿。

## 核心架构与功能

### 1. 动态进程与内存管理
- **前台优先级提升**：自动为活跃游戏进程分配更高的 CPU 调度权重，降低触控输入延迟并减少掉帧。
- **后台冗余进程挂起**：临时冻结闲置后台服务而不强行杀掉进程，既消除了上下文切换抖动，又保留了用户的多任务恢复状态。
- **游戏预加载引擎**：在应用启动时预缓存高频访问的原生 `.so` 动态库，显著缩短冷启动与场景加载耗时。

### 2. Thermalcore 温控服务
原厂 OEM 温控策略通常采用激进的阶梯式降频：一旦温度越过阈值，CPU 与 GPU 频率便会被瞬间砍半，造成画面骤卡。Thermalcore 则通过平缓管理温控曲线来维持稳定的基准频率，在避免局部积热的同时保证长时间游戏过程中的帧率一致性。

### 3. 子系统调校与运行模式
AZenith 内置三套经过调校的运行模式：
- **Performance（性能模式）**：加快调度器升频响应速度，优化 I/O 队列深度，并将算力集群优先倾斜给前台任务。
- **Balanced（均衡模式）**：默认日常运行模式，在维持跟手触控响应与流畅界面动画的同时控制功耗。
- **ECO（省电模式）**：按用户设定比例限制最高频率，加强空闲降频力度，并抑制后台唤醒。

## 配置与应用控制台

用户既可通过专用配套应用管理 AZenith，也可以直接编辑模块配置文件：

- **自动模式（Automatic Mode）**：默认状态下，AZenith 会监听应用生命周期事件，每当启动 `azenithApplist.json` 中登记的应用时自动套用对应优化参数。
- **手动模式（Manual Mode）**：若希望全局锁定单一固定模式（如长期保持 Balanced 或 ECO），可在控制面板进入 **AZenith Settings** 并选择 **Disable Auto Mode**。
- **硬件调节选项**：
  - **CPU 调度器（Governor）**：可在内核支持的调度器间切换（如 `schedutil`、`walt` 等）。
  - **I/O 调度器**：支持在 `mq-deadline`、`kyber` 与 `bfq` 存储调度器间切换。
  - **CPU 频率限制器**：设定百分比频率上限，抑制高发热芯片的过热问题。

## 安装与配置

1. 确认设备运行 Android 11 及以上系统，且已安装 Magisk、KernelSU 或 APatch。
2. 在 Root 管理器中刷入 AZenith 模块 `.zip` 包。
3. 重启设备，等待守护进程与内核挂钩初始化完成。
4. *（推荐）* 安装配套 APK，用于查看实时状态遥测、管理游戏白名单及调整调度器参数。

## 故障排查

- **游戏未自动触发性能模式**：请确认对应游戏的包名已写入 `/data/adb/modules/azenith/azenithApplist.json`，或在配套应用控制台内手动添加。
- **出现异常耗电**：请检查是否误将手动模式长期锁定在了 Performance，重新开启 Auto Mode 即可让设备在空闲时回落至 Balanced 或 ECO 状态。
