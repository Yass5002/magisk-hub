---
id: "charging-bypass-magisk"
title: "Charging Bypass：基于亮息屏状态的硬件级自动旁路供电模块"
sidebarTitle: "Charging Bypass"
description: "亮屏时自动暂停电池充电，息屏后自动恢复充电，有效缓解边充边玩及开发调试期间的发热降频问题。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "charging bypass Magisk 模块"
  - "abhishektor55 charging bypass 下载"
  - "Android Root 亮屏暂停充电"
  - "游戏旁路供电 Android 14 15 16"
  - "miatoll aosp 电池旁路直充"
prerequisites:
  - "Android 14、Android 15 或 Android 16"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "内核需提供可写的电源控制节点（`/sys/class/power_supply/battery/charging_enabled` 或 `input_suspend`）"
conflicts: []
configPaths:
  - "/data/adb/modules/charging-bypass-magisk/"
  - "/sdcard/charging_bypass.log"
features:
  - "屏幕状态同步门控：屏幕点亮后立即切断电芯充电电流"
  - "息屏自动恢复：屏幕熄灭或锁屏后瞬间恢复常规快充"
  - "缓解游戏发热降频：防止插电长时间高负载游戏导致电芯过热与系统降频"
  - "适配开发调试场景：保护长期连接电脑进行 ADB 连续调试的测试机电池寿命"
  - "状态变化日志可查：将亮息屏事件与内核电池驱动响应记录至 `/sdcard/charging_bypass.log`"
faq: []
---

## 概述

在连接快充适配器时游玩高帧率手游或进行长时间编译调试，会对锂电池造成极大的热压力。常规充电电路会同时向锂离子电芯输入数千毫安电流，而 SoC 也在高负载大电流放电，双重热负荷会迅速将机身温度推高至 42°C 以上，进而触发 Android 温控 HAL 主动降低屏幕刷新率并大幅限制 CPU/GPU 频率。

由 AbhishekTor55 开发的 **Charging Bypass** 实现了基于亮息屏状态的自动硬件充电门控。该模块适配 Android 14、15 与 16，通过内核事件监听机制捕获显示状态变化：亮屏时向内核电池驱动发送暂停充电指令，使设备直接由外部电源供电；息屏后则自动恢复正常充电。

## 硬件充电门控原理

该模块运行一个与系统屏幕显示状态触发器绑定的事件驱动后台监听进程：

1. **亮屏事件（Screen ON）**：
   - 守护进程检测到显示面板点亮。
   - 随后写入标准内核电源控制节点（如 `/sys/class/power_supply/battery/charging_enabled`、`input_suspend` 或厂商定制的步进充电接口）。
   - 流向电芯的充电电流被切断，外部供电电路直接满足 SoC 功耗需求而不给电池充入电量，从而避免电池自身发热。
2. **息屏事件（Screen OFF）**：
   - 玩家结束游戏、手动锁屏或屏幕自动超时熄灭。
   - 守护进程立即将充电控制节点重置为默认启用状态（`charging_enabled = 1`）。
   - 系统恢复原厂速率的正常快充。

## 安装与验证

1. 从 GitHub Releases 下载 `charging-bypass-v1.0.zip` 安装包。
2. 打开 Magisk 或 KernelSU 管理器，选择“从本地安装”刷入该模块。
3. 重启设备。
4. 将手机连接原装充电器或电脑 USB 数据线。
5. 在保持亮屏的状态下观察充电图标与电流变化：
   - 系统状态栏仍显示已连接电源，但电量百分比保持静止，且电池温度明显下降。
6. 可查看活动日志确认实时切换状态：
   ```bash
   cat /sdcard/charging_bypass.log
   ```

## 兼容性与硬件说明

- **Android 系统版本**：专为 **Android 14、Android 15 与 Android 16** 第三方固件（如 Miatoll 等机型的 AOSP 与 LineageOS 构建版本）开发并测试。
- **内核节点前提**：若某些厂商原厂内核未开放标准的 `sysfs` 充电控制接口，用户态进程将无法接管并暂停充电。
