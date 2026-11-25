---
id: "audio-jitter-silencer"
title: "Audio Jitter Silencer：低频音频抖动抑制与 Doze 优化"
sidebarTitle: "Audio Jitter Silencer"
description: "由 zyhk 开发的专业音频优化模块，通过禁用自适应电池与网络节流机制，抑制蓝牙耳机与 USB DAC 上 50Hz 以下的数字音频流速率抖动。"
category: "system-utilities"
tier: 1
searchQueries:
  - "audio jitter silencer magisk 模块"
  - "zyhk 音频抖动抑制模块"
  - "安卓蓝牙音频抖动优化"
  - "USB DAC 抖动修复 Root"
  - "deviceidle.xml 音频白名单"
prerequisites:
  - "Android 11 至 Android 14"
  - "高通骁龙或联发科 SoC 架构（ARM32 或 ARM64）"
  - "Magisk Root 环境"
conflicts: []
configPaths:
  - "/data/system/deviceidle.xml"
  - "/data/adb/modules/audio-jitter-silencer/"
features:
  - "50Hz 以下音频流速率稳定：针对通过锁相环（PLL）干扰 DAC 主时钟的低频（<50Hz）数字音频数据速率波动进行抑制"
  - "禁用自适应电池限制：关闭导致 CPU 与射频模块短暂降频的自适应电量消耗监测与自适应连接调度"
  - "防止 Wi-Fi 休眠断流：禁用网络管理器中的 Wi-Fi 挂起优化，保障网络 DAC 流媒体传输稳定"
  - "自动整合 Doze 白名单：将音频播放器、音频服务与 DAC HAL 合并写入 Android 电源豁免清单（`deviceidle.xml`）"
  - "安全状态还原：完整备份 `/data/system/deviceidle.xml`，卸载模块时自动恢复原状"
faq: []
---

## 概述

Audio Jitter Silencer 由音频工程师 `zyhk` 开发，是一款针对性极强的无侵入式（Systemless）工具，旨在消除数字音频输出上的细微声学失真——尤其适用于蓝牙耳机（LDAC、aptX HD、AAC）、USB DAC 以及网络流媒体音频终端。

数字音频抖动（Jitter）包含两种截然不同的物理现象：DAC 主时钟的相位波动，以及传入数字音频数据速率的频率波动。在移动设备上，Android 的省电策略（如自适应电池追踪、Wi-Fi 挂起超时以及激进的 Doze 节流）会引发微停顿与突发性数据包传送。对于使用锁相环（PLL）与输入音频流同步的 DAC 而言，50 Hz 以下的速率波动会调制主时钟，产生短暂的人工混响，令声场显得浑浊发闷。Audio Jitter Silencer 通过 Systemless 方式彻底消除这些抖动诱因。

## 前置要求与兼容性

- **Android 版本**：已在 Android 11、12、13 及 14（LineageOS、crDroid、phh AOSP GSI）上经过充分测试。
- **SoC 兼容性**：支持 32 位及 64 位 ARM 架构的高通骁龙（Qualcomm Snapdragon）与联发科（MediaTek）处理器系列。
- **Root 框架**：Magisk。

目前尚无已知的模块冲突记录。

## 运行架构

该模块系统性地停用以下四大主要音频流速率抖动源：

1. **自适应电池耗电监测（Adaptive Battery Drain Monitor）**：禁用 Android 电池管理服务中的后台耗电监测启发式策略。
2. **自适应连接（Adaptive Connectivity）**：禁用网络管理器在后台媒体播放期间切换射频功耗状态的例程。
3. **Wi-Fi 挂起优化（Wi-Fi Suspend Optimizations）**：关闭 Wi-Fi 射频休眠计时器，确保流媒体音频持续且低延迟地传输数据包。
4. **Doze 白名单合并器（Doze Whitelist Merger）**：直接解析 Android 持久化电源管理配置（`/data/system/deviceidle.xml`），合并涵盖核心媒体服务的音频专属白名单，并创建备份以便卸载时干净还原。

## 安装与双重启规则

请严格按照以下安装顺序操作，以确保 Android 的 Device Idle Controller 正确加载修改后的 XML 配置：

1. 在 Magisk 管理器中刷入 `audio-jitter-silencer-*.zip`。
2. **第一次重启**：重启设备。在此启动过程中，模块会将音频白名单合并写入 `/data/system/deviceidle.xml`。
3. **第二次重启（关键步骤）**：进入桌面后，**立即再次重启设备**。第二次重启可确保 Android 的 Device Idle Controller 守护进程从磁盘重新读取更新后的 XML，而非继续使用内存中的旧缓存配置。
4. 模块资源与运行时状态持久化保存在：
   ```bash
   /data/adb/modules/audio-jitter-silencer/
   ```

## 故障排查与听音建议

- **关于“数字健康”（Digital Wellbeing）的手动优化建议**：开发者指出，若设备预装了“数字健康”系统应用，其活动追踪机制会产生严重的后台 CPU 峰值波动。强烈建议将其卸载，或在 Android 设置中将其电池用量从“优化”更改为“受限”。
- **后续手动修改电池优化设置**：安装本模块后，如果你在系统设置中手动调整了其他应用的电池优化选项，Android 可能会过滤覆盖已合并的白名单条目。如需刷新恢复，只需卸载模块（重启两次）后重新安装（再重启两次）即可。
