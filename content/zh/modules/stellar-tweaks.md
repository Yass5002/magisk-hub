---
id: "stellar-tweaks"
title: "Stellar Tweaks：基于 Rust 的性能引擎、FEAS 调度与硬件协同中枢"
sidebarTitle: "Stellar Tweaks"
description: "由 Rust 编写的高性能 Android 守护进程，融合快速能量感知调度（FEAS）、GPU 调度器编排、旁路供电与全离线 Material You WebUI。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Stellar Tweaks Magisk 模块"
  - "kanaodnd Stellar Tweaks 下载"
  - "Android Rust 性能守护进程 Root"
  - "FEAS 快速能量感知调度模块"
  - "Stellar Tweaks WebUI KernelSU"
prerequisites:
  - "Android 9.0 及以上系统"
  - "通过 KernelSU、Magisk 或 APatch 获取 Root 权限（以获得完整内核与 FEAS 控制权限）"
  - "高通骁龙、联发科、三星 Exynos 或紫光展锐处理器"
conflicts:
  - "同时运行其他第三方性能模块或同类调度脚本（会与 Stellar 的 DVFS 控制器发生参数冲突）"
configPaths:
  - "/data/adb/modules/stellar-tweaks/"
features:
  - "快速能量感知调度（FEAS）：实时追踪渲染线程吞吐量，提前对齐升频节奏以消除掉帧"
  - "核心簇感知线程亲和性：将关键渲染线程定向绑定至超大核与大核集群，同时将后台任务限制在能效小核运行"
  - "跨架构 GPU 编排：针对 Adreno、Mali、Devfreq 与 KGSL 驱动提供各自独立的 GPU 调度配置"
  - "硬件旁路供电：允许兼容机型在充电时直接由充电器为主板供电，电流不再经过电池"
  - "显示管线控制：覆盖小米、三星、OPPO/一加/真我及传音机型的刷新率限制，并在开启省电模式时自动回归 60Hz"
  - "Material You 3 WebUI：完全离线的单文件暗色控制面板，直接在 Root 管理器内原生渲染"
---

## 概述

传统的 Android 性能优化脚本大多由 Shell 脚本编写，通过定时死循环调用 `dumpsys` 或暴力写入 sysfs 节点来工作。这类脚本不仅会因频繁的上下文切换白白消耗 CPU 算力，还容易在复杂动画过渡期间引入微卡顿，并与 Android 原生框架调度器产生冲突。

由 kanaodnd 完全采用 **Rust** 语言编写的 **Stellar Tweaks**，是一个面向低延迟内核与框架调度的确定性系统守护进程。它在后台静默运行，直接对接高通骁龙、联发科、三星 Exynos 与紫光展锐架构的 Linux 用户态及内核接口，以真正的快速能量感知调度（FEAS）、智能显示刷新率接管以及硬件级电池隔离，全面取代零散粗糙的调度黑客脚本。

## 架构与核心创新

### 1. 快速能量感知调度（FEAS）
- **实时渲染监控**：Stellar 不再等到掉帧发生后才被动补救，而是实时追踪当前前台应用 `RenderThread` 的吞吐量与延迟。一旦检测到复杂渲染帧即将到来，便会在绘制截止时间前提前拉升 CPU 频率。
- **核心簇亲和性映射**：自动将高优先级的游戏与 UI 渲染线程绑定至超大核（Prime）和大核（Big）性能集群，同时将非关键后台任务分流至小核（Little）能效集群。
- **协同空闲降频**：在画面静止时平滑地将硬件退回最低功耗状态，无需依赖高开销的 `evdev` 输入事件轮询。

### 2. 跨平台 GPU 与 I/O 控制
Stellar 为所有主流移动图形架构提供了量身定制的调度逻辑——包括高通 Adreno（KGSL）、ARM Mali 以及通用 Devfreq 节点：
- **游戏模式（Gaming Profile）**：锁定较高的 GPU 最低频率并自动激活旁路供电。
- **均衡模式（Balanced Profile）**：保持丝滑的 120Hz 滑动体验，同时在阅读和静态媒体浏览时降低整体功耗。
- **省电模式（Powersaver Profile）**：执行严格的频率上限封顶，并将屏幕刷新率锁定为 60Hz。

### 3. 温控旁路与充电管理
在长时间高负载游戏过程中，电池发热往往是导致 SoC 严重温控降频的首要推手。Stellar 可在支持硬件的机型上启用**旁路供电（Idle Battery State）**，使设备直接从连接的 USB 充电器取电运行而不再向锂电池充入电流，从而大幅降低机身内部工作温度。

### 4. 多厂商显示管线接管
各家 OEM 的显示管理服务（MIUI/HyperOS、One UI、ColorOS/OxygenOS、HiOS/XOS）经常在游戏或第三方浏览器内强行将屏幕刷新率降至 60Hz。Stellar 可以覆写厂商的刷新率锁定策略以强制维持目标高刷，同时依然会自动遵循 Android 系统自身的省电模式规则。

## 用户界面（M3 WebUI）

Stellar 内置了 **Material You 3（M3）** 风格的 WebUI 控制面板。作为独立的单文件分发包编译，它无需任何外部网络连接即可完全离线运行，并可在 **KernelSU Manager**、**APatch Manager** 或 **MMRL** 中原生渲染打开。

用户可以直接在界面中查看实时 CPU/GPU 频率、切换运行模式、管理分应用配置规则，以及执行组件清理操作。

## 安装与最佳实践

1. 安装前请确保未同时启用其他存在冲突的性能或电池调度模块。
2. 通过你常用的 Root 管理器刷入 **Stellar Tweaks** `.zip` 压缩包。
3. 重启设备，以便 Stellar 自动探测屏幕刷新率边界与内核 sysfs 节点。
4. 打开 Root 管理器中的模块列表面板，启动 Stellar WebUI。
5. 根据需求自定义情景规则，或直接交由自适应调度器自动管理负载。

> [!WARNING]
> 由于 Stellar 会主动统筹协调 CPU/GPU 调度器、EAS 任务放置以及 DVFS 调频曲线，同时运行其他性能脚本或调度模块将会引发参数冲突与帧率波动。
