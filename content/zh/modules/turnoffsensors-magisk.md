---
id: "turnoffsensors-magisk"
title: "Turn Off Sensors：开机自动启用硬件传感器隐私关闭模块"
sidebarTitle: "Turn Off Sensors"
description: "通过 Android 原生 sensor_privacy 服务，在系统启动时自动禁用摄像头、麦克风、陀螺仪及加速度计等硬件传感器。"
category: "security-certificates"
tier: 1
searchQueries:
  - "Turn Off Sensors Magisk 模块"
  - "AdalynAstatine TurnOffSensors"
  - "Android Root 开机自动关闭传感器"
  - "sensor_privacy Android Root 禁用"
  - "Android 硬件传感器隐私总开关"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
  - "Android 10 及以上系统（已在 Android 10 至 Android 17 版本中测试通过）"
conflicts: []
configPaths:
  - "/data/adb/modules/turnoffsensors-magisk/"
features:
  - "开机自动化隐私防护：系统启动完成时自动触发 Android 内部 Sensors Off（关闭传感器）状态"
  - "全硬件通道静音屏蔽：阻断来自摄像头、麦克风、陀螺仪、加速度计与磁力计的数据流读取"
  - "系统框架级原生集成：调用 Android 官方 `sensor_privacy` 服务，向应用返回干净的空值或零值，避免触发闪退"
  - "防范后台静默窃听：防止不可信应用在设备开机早期阶段偷采传感器数据或监听麦克风音频"
  - "支持随时手动恢复：可通过快捷设置中的开发者磁贴或 Shell 命令临时重新启用传感器"
faq: []
---

## 概述

自 Android 10 起，Google 新增了一项名为「关闭传感器（Sensors Off）」的开发者功能，其底层由系统 `sensor_privacy` 服务驱动。启用该开关后，系统相当于拉下了一道软件级隐私总闸：摄像头对所有应用显示不可用、麦克风仅返回静音数据，而惯性传感器（陀螺仪、加速度计、距离传感器）则统一返回零值或静态数值。但遗憾的是，Android 默认会在重启后重置或无法自动持久化这一开关状态，从而在每次重启后留下隐私暴露窗口。

由 AdalynAstatine 编写的 **TurnOffSensors-Magisk** 是一款轻量级安全模块，会在系统启动后期自动调用 Android 原生 `sensor_privacy` 服务，确保设备从系统加载完毕的那一刻起即保持传感器严格禁用状态。

## 为什么需要开机自动关闭传感器？

1. **防范静默窃听**：恶意应用无法在设备开机早期后台初始化阶段偷偷唤醒麦克风或录制环境音频。
2. **阻断陀螺仪与加速度计追踪**：现代广告追踪 SDK 常借助惯性传感器的微小抖动来构建设备指纹或推断用户的输入按键习惯，屏蔽此类传感器可彻底消除运动轨迹追踪向量。
3. **保障应用稳定性**：由于本模块直接对接 Android 平台原生的 `sensor_privacy` 管理器，应用在传感器被禁用时能够优雅降级处理，不会抛出未捕获异常导致崩溃闪退。

## 使用方法与控制选项

当传感器处于关闭状态时：
- 相机应用打开后会提示摄像头已被禁用。
- 麦克风将无法采集任何声音信号。
- 屏幕不会随手机物理方向旋转而自动切换横竖屏。

如需临时重新开启传感器：
- 前往 **设置（Settings）> 系统（System）> 开发者选项（Developer options）> 快捷设置开发者磁贴（Quick settings developer tiles）> 关闭传感器（Sensors Off）**，将该磁贴添加至下拉控制中心。
- 点击该磁贴即可立即恢复全部传感器功能，直至下次重启或再次手动关闭为止。

## 安装步骤

1. 确认设备运行 Android 10 或更高版本系统。
2. 从 GitHub Releases 下载最新版的 `TurnOffSensors-Magisk.zip` 压缩包。
3. 在 **Magisk** 中刷入该模块。
4. 重启手机，系统启动后所有硬件传感器即会自动进入禁用保护状态。
