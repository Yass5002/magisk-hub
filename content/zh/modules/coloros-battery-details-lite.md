---
id: "coloros-battery-details-lite"
title: "ColorOS Battery Details & Usage Display Lite：技术指南"
sidebarTitle: "ColorOS 电池详情 Lite"
description: "通知栏电池遥测守护进程，为 ColorOS、Realme UI 与 OxygenOS 实时展示充电功率、耗电速率与电池温度统计数据。"
category: "system-utilities"
tier: 1
searchQueries:
  - "coloros 电池详情通知栏 magisk"
  - "realme ui 电池放电电流监控"
  - "coloros 状态栏实时功耗显示"
  - "通知栏实时充电功率监控 root"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "OPPO ColorOS、Realme UI 或一加 OxygenOS"
conflicts:
  - "无"
configPaths:
  - "/data/adb/modules/ColorOS_details/service.sh"
  - "/data/adb/modules/ColorOS_details/Lite"
features:
  - "常驻通知中心小组件，实时展示当前电池状态"
  - "计算亮屏期间的实时工作电流（mA）与放电速率"
  - "显示精确的电池温度与电压遥测数据"
  - "极度轻量的 Shell 守护进程，系统资源占用近乎为零"
faq:
  - question: "这需要额外安装第三方应用吗？"
    answer: "不需要。该模块直接调用 Android 命令行通知发布器与系统服务，无需任何 APK 依赖即可原生渲染监测数据。"
  - question: "它兼容小米 MIUI 或通用 AOSP ROM 吗？"
    answer: "虽然本模块专为 ColorOS/Realme 通知样式及温控节点进行了调校，但具备标准 power_supply sysfs 接口的通用 AOSP 设备同样可以正常显示该通知。"
---

## 概述

**ColorOS Battery Details & Usage Display Lite**（作者：Everything by the sun）可在 ColorOS、Realme UI 与 OxygenOS 设备的 Android 通知栏中直接提供实时电池遥测监控。

---

## 技术架构与工作原理

该模块通过 `service.sh` 启动后台轮询脚本（`Lite`）持续采集电源状态：

```bash
# Sample power telemetry from kernel sysfs
current_now=$(cat /sys/class/power_supply/battery/current_now) # uA
voltage_now=$(cat /sys/class/power_supply/battery/voltage_now) # uV
temp=$(cat /sys/class/power_supply/battery/temp)               # 0.1 C

# Compute real-time wattage
wattage=$(awk "BEGIN {print ($current_now / 1000000) * ($voltage_now / 1000000)}")
```

脚本利用 Android 内部通知渠道发布格式化通知，让用户无需打开第三方检测软件即可一目了然地查看实时充电功率与待机耗电情况。
