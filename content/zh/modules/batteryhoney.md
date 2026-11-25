---
id: "batteryhoney"
title: "Battery Honey：基于 Zig 的高能效省电优化与 Devfreq 调频模块"
sidebarTitle: "Battery Honey"
description: "采用 Zig 语言编写的超轻量电源与能效管理守护进程，结合 RaiRin-AI 省电算法与 GPU/Devfreq 总线动态调频。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "battery honey Magisk 模块"
  - "kaminarich batteryhoney 下载"
  - "zig android 省电优化模块"
  - "rairin ai 省电逻辑 Root"
  - "Android devfreq gpu 降功耗模块"
prerequisites:
  - "仅支持 64 位 ARM 架构（严格要求 AArch64）"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "Android 10 及以上系统"
conflicts: []
configPaths:
  - "/data/adb/modules/batteryhoney/"
features:
  - "原生 Zig 编译架构：以静态编译的 Zig 二进制替代早期 Rust 与 Shell 脚本，CPU 与内存占用极低"
  - "RaiRin-AI 电源启发式算法：根据当前前台负载特征动态匹配核心供电状态"
  - "Devfreq 与 GPU 总线调频：在轻负载 UI 操作期间降低内存总线频率与 GPU 空闲基频"
  - "内置 WebUI 面板：支持在主流 Root 管理器内直接渲染交互式网页控制台"
faq: []
---

## 概述

市面上大多数省电模块依赖后台 Shell 循环定时轮询 `dumpsys`，或套用激进的 CPU 降频规则。这种做法不仅容易导致日常滑动界面明显掉帧，持续启动 Shell 解释器本身也会额外消耗电量。

由 kaminarich 开发的 **Battery Honey（Awaken 版）** 是一款高效能电源与性能协同守护进程。该模块采用 **Zig** 语言编写，具备极小的内存占用且无运行时垃圾回收（GC）开销，可直接对接 Android 内核接口，并引入 **RaiRin-AI** 启发式模型，在深度休眠省电与瞬时界面响应之间取得平衡。

## 架构亮点

### 1. 高性能 Zig 原生二进制
Battery Honey 已从早期 Rust 代码库重构为静态编译的 **Zig** 可执行文件。这一架构升级使后台监控进程几乎不占用 CPU 周期，消除了上下文切换延迟，并在现代 64 位 ARM（AArch64）Android 内核上稳定运行。

### 2. RaiRin-AI 电源调度逻辑
守护进程会持续评估系统负载指标以动态计算电源状态：
- **活跃交互**：在浏览器滚动与即时通讯切换时提供无阻塞的升频响应，保障 90Hz/120Hz 流畅滑动。
- **静态亮屏阅读**：当屏幕保持点亮但用户正在阅读静态图文内容时，快速下调中间档频率以削减多余功耗。
- **息屏深度休眠**：锁屏后立即压低非必要硬件时钟并下调内存总线最低频段。

### 3. Devfreq 与 GPU 总线调节
Battery Honey 不仅关注 CPU 频率，还会主动调校 **Devfreq**（内存总线动态调频）与 GPU 空闲状态。在视频播放或轻度浏览网页时削减内存控制器的冗余时钟余量，可显著降低持续亮屏功耗。

## WebUI 控制台

Battery Honey 内置兼容 **KernelSU**、**APatch** 与 **MMRL** 的 `webroot` 交互界面：
- 实时查看当前调度器行为与频率状态。
- 监控动态电源状态切换记录。
- 无需编辑终端脚本即可直接调整运行配置参数。

## 安装与环境要求

1. 确认设备采用 **AArch64（ARM64）** 处理器。
2. 从 GitHub 下载 `batteryhoney` `.zip` 模块包。
3. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入压缩包。
4. 重启设备，Zig 守护进程将通过 `service.sh` 自动启动。
