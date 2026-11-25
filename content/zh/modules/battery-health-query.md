---
id: "battery-health-query"
title: "电池健康度与循环次数查询：Sysfs 硬件检测完整指南"
sidebarTitle: "电池健康度查询"
description: "实时电池诊断守护模块，直接读取 Linux power_supply sysfs 硬件寄存器，并在 Magisk 管理器界面直观展示真实容量保持率、充电循环次数与电池健康状态。"
category: "battery-power-charging"
tier: 1
searchQueries:
  - "Magisk 电池健康度查询模块"
  - "Android Root 查看电池循环次数"
  - "高通电池 SOH sysfs 检测"
  - "查询电池实际容量与设计容量"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "高通骁龙、联发科或 Exynos 平台 Android 智能手机"
conflicts:
  - "无"
configPaths:
  - "/data/adb/modules/custom.battery/service.sh"
  - "/data/adb/modules/custom.battery/custom_script.sh"
  - "/sys/class/power_supply/battery/charge_full"
  - "/sys/class/power_supply/battery/charge_full_design"
  - "/sys/class/qcom-battery/soh"
features:
  - "直接从内核 sysfs 读取高通电池健康状态（SOH）硬件寄存器"
  - "基于 `charge_full` 与 `charge_full_design` 计算真实电池容量衰减率"
  - "动态将实时健康数据与更新时间写入 `module.prop`，直接在 Root 管理器内展示"
  - "附带独立交互式查询脚本，支持通过 ADB 或终端即时查看详细电池遥测数据"
faq:
  - question: "为什么该模块测得的健康度百分比与手机原厂系统设置里的不一样？"
    answer: "厂商系统内置的电池健康算法通常会进行软件平滑处理，或采用偏保守的校准曲线。本模块直接读取电池电量计 IC 暴露的底层内核 sysfs 节点，呈现未经修饰的真实硬件遥测读数。"
  - question: "这个模块会在后台持续高负载轮询耗电吗？"
    answer: "不会。守护脚本仅在开机完成时及低频率定时间隔刷新一次数据，闲置时 CPU 占用率为 0%，几乎不消耗任何可测量的电池电量。"
---

## 概述

**电池健康度与循环次数查询（Battery Health Diagnostics & Cycle Monitor）**（作者：Wo Bu Shi Chen Sang & Duo Rou Yu Yuan Pu Tao）为已获取 Root 权限的 Android 设备提供精准的硬件级电池健康检测能力。

不同于依赖厂商私有估算接口或会长期持有唤醒锁（Wakelock）的第三方电池监测软件，该模块直接与硬件电源管理芯片（PMIC）暴露的 Linux 内核 sysfs 节点交互。

---

## 技术架构与工作原理

### 1. 内核 Sysfs 电量计节点读取

诊断脚本（`custom_script.sh`）会根据设备的 SoC 平台读取对应的硬件 sysfs 节点：

```bash
# Qualcomm State of Health (SOH) register
soh=$(cat /sys/class/qcom-battery/soh 2>/dev/null)

# Factory design capacity (uAh -> mAh)
charge_full_design=$(( $(cat /sys/class/power_supply/battery/charge_full_design) / 1000 ))

# Current maximum charge retention capacity (uAh -> mAh)
charge_full=$(( $(cat /sys/class/power_supply/battery/charge_full) / 1000 ))

# True capacity retention percentage
retention=$(( (charge_full * 100) / charge_full_design ))
```

### 2. 管理器描述实时回显

该模块无需安装额外的 APK 客户端，守护脚本会动态更新自身 `module.prop` 文件中的 `description` 字段：

```bash
sed -i "s/^description=.*/description=[${timestamp}] SOH: ${soh}% | Real: ${charge_full}\/${charge_full_design} mAh (${retention}%)/" $custombattery_Path/module.prop
```

用户只需打开 Magisk 管理器、KernelSU 管理器或 APatch WebUI 的模块列表，即可直接查看当前的电池健康度与剩余满充容量。

---

## 验证与手动查询

你也可以通过 Root 终端直接运行模块内置的独立诊断脚本：

```bash
su -c sh /data/adb/modules/custom.battery/点我直接查询.sh
```
