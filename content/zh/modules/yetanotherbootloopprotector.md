---
id: "yetanotherbootloopprotector"
title: "Yet Another Bootloop Protector (YABP)：多阶段开机故障防护引擎"
sidebarTitle: "Yet Another Bootloop Protector"
description: "由 rhythmcache 开发的全面防卡米（Bootloop）与 SystemUI 崩溃防护引擎，兼容 Magisk、KernelSU 与 APatch，具备基于状态标记的崩溃恢复及 Recovery 刷入急救触发机制。"
category: "root-management"
tier: 1
searchQueries:
  - "yetanotherbootloopprotector magisk 模块"
  - "YABP 防卡米保护 rhythmcache"
  - "Magisk SystemUI 崩溃恢复模块"
  - "TWRP 刷入一键禁用全部模块 YABP"
  - "Magisk 开机超时自动救砖恢复"
prerequisites:
  - "已通过 Magisk、KernelSU 或 APatch 获取 Root 权限的 Android 设备"
  - "用于追踪状态标记文件的可读写 `/data` 分区"
conflicts: []
configPaths:
  - "/data/adb/YABP/allowed-modules.txt"
  - "/data/adb/YABP/allowed-scripts.txt"
  - "/data/adb/systemui.monitor.disable"
  - "/data/local/tmp/service.log"
features:
  - "基于状态标记的 Bootloop 追踪：在未完成启动时逐步创建标记文件，连续第三次启动失败时自动禁用所有模块"
  - "开机超时看门狗：若设备在 120 秒内未上报启动完成状态，自动触发模块解除武装并重启"
  - "可选 SystemUI 监控：主动监测 SystemUI 进程健康状况，当界面持续崩溃或卡死超过 25 秒时触发恢复"
  - "全方位脚本禁用：将 `service.d`、`post-fs-data.d`、`post-mount.d` 与 `boot-completed.d` 中的脚本权限重置为不可执行的 `644`"
  - "Recovery 急救触发：在 TWRP 或 OrangeFox 中直接刷入模块压缩包，即可立即禁用全部模块与脚本以便手动救援"
faq: []
---

## 概述

由 rhythmcache（`triple_fault`）开发的 **Yet Another Bootloop Protector（YABP）** 是一款自动化看门狗模块，旨在保护已 Root 的 Android 设备免受问题 Magisk、KernelSU 或 APatch 模块引起的无限重启（Bootloop）、开机动画卡死及 SystemUI 崩溃困扰。

修改 Android 系统组件时，不兼容的 SELinux 规则、框架层覆盖（Overlay）或厂商系统属性可能导致操作系统在启动阶段停滞或循环崩溃。YABP 充当自动化安全网：它追踪系统启动完成的状态机，强制执行最长允许启动时间，并在系统无法进入稳定可交互桌面时自动中和异常模块与脚本。

## 前置要求与兼容性

- **Root 环境**：Magisk、KernelSU 与 APatch。
- **第三方 Recovery**：兼容 TWRP、OrangeFox 与 PBRP，支持紧急救援刷入。
- **设备支持**：通用架构兼容，覆盖 ARM、ARM64 与 x86 设备。

目前没有已知的模块冲突。

## YABP 工作原理

### 1. 渐进式标记机制
- 每次开机启动时，YABP 会检查其工作目录中是否存在历史标记文件。
- 如果上一次启动未能到达 `boot_completed` 阶段，系统会记录一个标记文件。
- 当累计出现三个标记（`marker1`、`marker2`、`marker3`）时，YABP 会判定设备已陷入确定的 Bootloop：
  - 在 `/data/adb/modules/` 下的每个已安装模块目录中创建 `disable` 标志文件。
  - 移除 `/data/adb/service.d/`、`/data/adb/post-fs-data.d/`、`/data/adb/post-mount.d/` 与 `/data/adb/boot-completed.d/` 下所有自定义脚本的可执行权限（`chmod 644`）。
  - 触发安全重启，使设备在无第三方干扰的情况下正常进入 Android 系统。

### 2. 开机完成超时熔断
YABP 每 5 秒检查一次系统状态。如果 Android 在 2 分钟（120 秒）内未广播 `sys.boot_completed=1`，YABP 会判定设备卡在开机动画阶段，随即执行模块解除武装流程并重启。

### 3. 可选 SystemUI 崩溃监控
安装模块期间，用户可选择启用 SystemUI 监控器（SystemUI Monitor）。该看门狗每 5 秒检测一次 `com.android.systemui` 的运行状态。若 SystemUI 持续崩溃或无响应超过 25 秒，YABP 将停用当前启用的模块以恢复界面显示。
- 禁用该监控器：
  ```bash
  su -c touch /data/adb/systemui.monitor.disable
  ```
- 重新启用该监控器：
  ```bash
  su -c rm -f /data/adb/systemui.monitor.disable
  ```

### 4. Recovery 急救刷入
如果设备卡在 Recovery 界面且无法访问 Shell 终端，只需在 TWRP 中直接刷入 `YetAnotherBootloopProtector-*.zip`，即可立即禁用全部模块并恢复默认脚本权限，无需输入任何终端命令。

## 配置与白名单

若需避免关键安全或诊断模块在自动恢复过程中被禁用，可将其模块 ID 或脚本名添加至以下白名单：
- **允许的模块**：`/data/adb/YABP/allowed-modules.txt`
- **允许的脚本**：`/data/adb/YABP/allowed-scripts.txt`

运行时执行日志输出至：
```bash
/data/local/tmp/service.log
```

## 故障排查与局限性

- **内核级卡死**：如果第三方内核在文件系统挂载前或 `init` 早期阶段发生 Panic，YABP 将无法运行。此类内核崩溃需通过 Fastboot 重新刷写内核镜像。
- **直接修改系统分区**：YABP 仅针对无系统分区修改（Systemless）模块提供防护；若用户直接对物理 `/system` 或 `/vendor` 分区进行了破坏性修改，本模块无法修复。
