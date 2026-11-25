---
id: "auto-rescue"
title: "Auto Rescue：自动化 Bootloop 看门狗与模块救砖工具"
sidebarTitle: "Auto Rescue"
description: "内核与 init 启动看门狗模块，用于追踪开机周期、检测系统崩溃并自动禁用异常的 Magisk/KernelSU 模块，防止设备变砖卡米。"
category: "system-utilities"
tier: 1
searchQueries:
  - "auto rescue magisk 模块"
  - "magisk 自动救砖防卡米"
  - "automatic brick rescue 下载"
  - "kernelsu 无限重启恢复"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他同时执行强力 killall 指令的激进防卡米救砖模块"
configPaths:
  - "/data/adb/modules/Automatic_brick_rescue/Number_of_starts.log"
  - "/data/adb/modules/Automatic_brick_rescue/whitelist.conf"
  - "/data/adb/modules/Automatic_brick_rescue/Automatic_brick_rescue.sh"
features:
  - "在 post-fs-data 与 late-service 阶段持续监控 Android init 早期启动流程"
  - "通过 Number_of_starts.log 中的持久化文件系统计数器记录启动尝试次数"
  - "达到崩溃阈值时，自动在第三方模块目录中生成 .disable 触发文件以禁用模块"
  - "支持自定义白名单配置，确保核心 Root 守护进程在救砖期间保持启用"
  - "内置 OTA 系统更新后 30 分钟宽限延迟，防止大版本升级首次启动耗时过长导致误禁用"
faq:
  - question: "Auto Rescue 如何判定设备陷入了 Bootloop（无限重启）？"
    answer: "在早期启动阶段（post-fs-data），模块会递增持久化启动计数器。如果操作系统未能成功抵达 sys.boot_completed=1 状态并发生连续重启，计数器就会超过预设阈值，从而触发紧急禁用机制，停用所有不在白名单中的模块。"
  - question: "如何防止重要模块在救砖时被一并禁用？"
    answer: "将关键模块在 /data/adb/modules/ 下的目录名添加到 /data/adb/modules/Automatic_brick_rescue/whitelist.conf 中即可。白名单内的任何模块 ID 在执行救砖流程时都会被跳过。"
---

## 概述

**Auto Rescue**（原作者为 Han 与 Qingfeideyic，现由 Fendou Youth 维护）是一款自动化无侵入式（Systemless）看门狗模块，专为解决因安装不兼容的 Magisk、KernelSU 或 APatch 模块而引发的软砖（Soft Brick）与无限重启（Bootloop）问题而设计。

修改底层 Android 框架库、音频特效或系统属性时，一段有缺陷的脚本就可能导致 Zygote 进程崩溃或 SystemUI 守护进程无限卡死。在没有第三方 Recovery（TWRP/OrangeFox）或未提前开启 USB 调试的情况下，用户往往只能清空全部数据才能恢复开机。Auto Rescue 通过在 Bootloader 交接与 init 引导序列期间执行自动化健康检查，彻底消除这一风险。

---

## 技术架构与工作原理

Auto Rescue 将监控职责划分为 Android 启动序列的两个阶段：

### 1. 早期启动阶段（post-fs-data.sh）

当 Root 管理器执行 `post-fs-data.sh` 时，`/data` 分区已挂载为可读写。Auto Rescue 会检查其持久化状态目录：

1. **启动计数记录**：读取 `/data/adb/modules/Automatic_brick_rescue/Number_of_starts.log`。若上一次启动未能发出完成信号，计数器即加 1。
2. **崩溃阈值评估**：当计数器达到阈值（通常为连续 2 次中断启动）时，Auto Rescue 会在后期服务与 Zygote Hook 加载之前立即启动故障安全恢复流程。
3. **选择性禁用**：Auto Rescue 扫描 `/data/adb/modules/`，并在每个已启用模块的目录中创建一个空的 `.disable` 文件。明确写入 `whitelist.conf` 的模块（如核心 Root 管理器组件或显示驱动）将被豁免。

### 2. 后期启动阶段（service.sh）

Android 框架初始化后，`service.sh` 会在后台异步运行：

1. **启动完成轮询**：守护进程定期通过 `getprop sys.boot_completed` 检查系统属性。
2. **计数器清零**：一旦 `sys.boot_completed` 返回 `1`，Auto Rescue 即确认用户空间与图形界面运行正常，并将 `Number_of_starts.log` 重置为 `0`。
3. **OTA 升级保护**：Android 系统版本升级后的首次开机因 ART dexopt 编译与包迁移需要较长时间。Auto Rescue 会识别系统更新状态并自动注入 30 分钟的宽限延迟阈值，避免过早误禁用模块。

---

## 配置与白名单管理

Auto Rescue 提供了本地配置文件用于保护核心模块：

```bash
# Whitelist configuration path
/data/adb/modules/Automatic_brick_rescue/whitelist.conf
```

### 将模块加入白名单

若需确保特定模块在触发救砖机制时继续保持启用，只需将其文件夹名称（Slug）逐行追加至该文件：

```text
# Example whitelist entries:
Automatic_brick_rescue
playintegrityfix
shamiko
```

---

## 故障排查与诊断

- **查看启动日志**：通过 Root Shell 或 Termux 读取 `/data/adb/modules/Automatic_brick_rescue/Number_of_starts.log`，检查已记录的开机次数。
- **重新启用被禁用的模块**：若因误判导致模块被禁用，删除 `/data/adb/modules/<module-slug>/.disable` 文件并重启设备即可恢复。
