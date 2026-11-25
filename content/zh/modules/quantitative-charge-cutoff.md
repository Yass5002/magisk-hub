---
id: "quantitative-charge-cutoff"
title: "BH 定量断充保护：高级锂电池延寿控制指南"
sidebarTitle: "BH 定量断充"
description: "内核级充电阈值控制器，可按用户设定的电量上下限（例如 80% 停充、70% 复充）自动切换硬件充电开关，有效延长电池寿命。"
category: "battery-power-charging"
tier: 1
searchQueries:
  - "Magisk 限制充电 80% 模块"
  - "BH 定量断充 Root 模块"
  - "input_suspend 电池充电控制"
  - "Android 电池保护停充限制"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "内核支持 `input_suspend` 或 `charging_enabled` 电池 sysfs 节点"
conflicts:
  - "其他电池旁路供电或充电阈值控制守护进程（如 ACC、Battery Charge Limit）"
configPaths:
  - "/data/media/0/Android/BHcharging/files.conf"
  - "/data/adb/modules/BHcccc/service.sh"
  - "/data/adb/modules/BHcccc/B.sh"
  - "/sys/class/power_supply/battery/charging_enabled"
features:
  - "可自定义充电截止上限（如设置 80% 停充，避开高电压对锂电芯的压力）"
  - "可自定义回落复充下限（如电量跌至 75% 时自动重新开启充电）"
  - "双硬件开关兼容：同时支持操作 `input_suspend` 与 `charging_enabled` sysfs 节点"
  - "支持将实时充电与断充状态直接回写至 Root 管理器的 `module.prop` 界面展示"
faq:
  - question: "为什么将充电上限控制在 80% 对电池有益？"
    answer: "锂离子电芯在 4.2V 至 4.45V 高电压区间（通常对应 80% 以上的电量）承受的化学老化与正极材料衰减最为剧烈。将日常充电上限限制在 80% 可将电芯循环寿命提升 200% 至 300%。"
  - question: "如何修改停充的电量百分比阈值？"
    answer: "编辑 `/data/media/0/Android/BHcharging/files.conf` 文件，调整其中的 `Stop_charging` 参数为你希望的电量百分比即可。"
---

## 概述

**BH 定量断充与电池保护（BH Quantitative Charging Cutoff & Battery Guard）**（作者：Bu Tai Hui Qi Wang Ming & HChai）是一款自动化充电控制模块，旨在保护锂离子电池免受过充及高电压热衰减损伤。

该模块作为后台守护脚本运行，持续采样电池荷电状态（SOC）。一旦电量达到用户设定的上限阈值，便会直接向 Linux 内核电源供应子系统下发硬件级断充指令。

---

## 技术架构与工作原理

### 1. Sysfs 充电开关节点探测

守护脚本（`B.sh`）会自动定位当前设备可用的硬件充电控制节点：

```bash
# Common Qualcomm / MediaTek sysfs control nodes:
# 1. /sys/class/power_supply/battery/charging_enabled (1=enable, 0=disable)
# 2. /sys/class/power_supply/battery/input_suspend (0=enable, 1=suspend)

echo 0 > /sys/class/power_supply/battery/charging_enabled
# or
echo 1 > /sys/class/power_supply/battery/input_suspend
```

### 2. 状态监控主循环

守护进程会依据 `/data/media/0/Android/BHcharging/files.conf` 中定义的阈值实时比对当前 `capacity`：

```bash
if [ "$current_capacity" -ge "$Stop_charging" ]; then
    echo 0 > "$USBpath"
    sed -i "s/状态：.*/状态：已停充 (${current_capacity}%)]/g" "$module"
elif [ "$current_capacity" -le "$Resume_charging" ]; then
    echo 1 > "$USBpath"
    sed -i "s/状态：.*/状态：充电中 (${current_capacity}%)]/g" "$module"
fi
```

---

## 配置与状态验证

在 Root 终端中检查当前硬件充电开关节点状态：

```bash
# Check charging switch state (0 = charging disabled)
cat /sys/class/power_supply/battery/charging_enabled
```
