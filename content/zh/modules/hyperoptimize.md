---
id: "hyperoptimize"
title: "HyperOptimize：面向小米澎湃 OS 的系统与内核省电调优模块"
sidebarTitle: "HyperOptimize"
description: "调校 HyperOS 内核参数、SurfaceFlinger 渲染管线、唤醒锁与 I/O 调度，最大限度降低后台与待机功耗。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "HyperOptimize Magisk 模块"
  - "澎湃 OS 省电优化模块"
  - "TatshSiow HyperOptimize 下载"
  - "HyperOS 内核调校续航优化"
  - "小米澎湃 OS 后台省电 Magisk"
prerequisites:
  - "通过 Magisk 20.4+ 或 KernelSU 0.6.6+ 获取 Root 权限"
  - "运行小米澎湃 OS（Xiaomi HyperOS）的小米、红米或 POCO 机型"
  - "建议提前安装防变砖救砖模块作为安全保障"
conflicts:
  - "Nakixii Pandora Kernel"
  - "存在重复 sysctl 调校的其他内核或功耗优化模块"
configPaths:
  - "/data/adb/modules/HyperOptimize/"
features:
  - "精准功耗控制：重配置系统与内核可调参数以抑制异常耗电，而非盲目追求跑分"
  - "SurfaceFlinger 与渲染调优：优化图形队列参数，减少静态屏幕状态下的 GPU 活跃周期"
  - "日志与唤醒锁抑制：削减冗余 logcat 调试日志开销，缓解激进的后台唤醒"
  - "I/O 与 CPU 调度器优化：调整 Linux 调度器能效配置，优先让低负载任务驻留能效核心"
  - "纯无侵入式（Systemless）执行：在开机后期服务阶段应用配置脚本，不修改物理 system 或 vendor 分区"
faq: []
---

## 概述

小米澎湃 OS（HyperOS）集成了大量底层系统服务、后台遥测与高开销动效引擎，在部分早期或未充分优化的官方固件上容易造成明显的待机耗电。

由 TatshSiow 开发的 **HyperOptimize** 是一款专注降低功耗、延长电池续航的无侵入式（Systemless）参数调优模块。它不以极限游戏跑分为目标，而是着力约束搭载澎湃 OS 的小米、红米及 POCO 手机中不必要的后台活动、冗余日志输出与频繁唤醒。

## 核心调优机制

该模块在系统开机后期（`service.sh`）执行定向参数调整：

1. **内核与调度能效**：重新配置 CPU 调度器（Governor）降频速率与调频周期，当前台高负载任务结束后，尽快引导后台线程回落至能效小核运行。
2. **SurfaceFlinger 与 GPU 渲染**：优化帧分发队列与显示合成参数，防止静态 UI 界面下 GPU 管线反复空转。
3. **唤醒锁与遥测抑制**：限制非关键系统广播唤醒，并降低 User 版系统中的持续调试日志写入频率。
4. **I/O 存储调度**：调整块设备预读队列与回写计时器，减少闪存芯片的无效频繁唤醒。

## 安装与安全措施

HyperOptimize 会调整底层内核参数，强烈建议在刷入前安装防变砖保护模块。

1. 从项目官方 Releases 页面下载 `HyperOptimize_v*.zip`。
2. 打开 **Magisk Manager** 或 **KernelSU Manager**。
3. 从本地存储设备选择并刷入模块压缩包。
4. 重启手机使配置生效。

## 已知冲突

- **Nakixii Pandora Kernel**：因调度器参数存在竞争，HyperOptimize 与 Nakixii Pandora 第三方内核存在已知冲突。
- **同类性能优化模块**：请勿将 HyperOptimize 与其他同样修改 `sysctl` 或 `/sys/devices/system/cpu/` 节点的一体化优化模块同时启用。

## 异常恢复

若刷入后出现无法开机或系统不稳定情况，请按以下步骤恢复：
1. 进入第三方 Recovery（TWRP / OrangeFox）或执行 `adb reboot recovery`。
2. 打开 Recovery 内置文件管理器或终端。
3. 删除 `/data/adb/modules/HyperOptimize` 模块目录。
4. 重启设备即可。
