---
id: "auto-charge-disconnect"
title: "满电自动断充保护模块：电池延寿使用指南"
sidebarTitle: "满电自动断充"
description: "零依赖的纯 Shell 守护脚本，在电池充至 100% 时自动切断充电输入，跌至 95% 时自动恢复充电，消除夜间长期涓流充电损耗。"
category: "battery-power-charging"
tier: 1
searchQueries:
  - "Magisk 满电自动断充"
  - "Root 防止夜间过充模块"
  - "input_suspend 自动断充保护"
  - "Android 电池过充保护 Magisk"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "支持 `input_suspend` 或 `charging_enabled` 节点的 Linux 内核"
conflicts:
  - "其他同类充电限制或断充模块"
configPaths:
  - "/data/adb/modules/Charge_control/data.sh"
  - "/data/adb/modules/Charge_control/service.sh"
features:
  - "满电自动断充：达到 100% 自动切断充电开关，避免高电压涓流持续冲击电芯"
  - "95% 自动复充：电量回落至 95% 时自动恢复供电，防止长时间插电后电量大幅流失"
  - "双节点兼容：同时检测并适配 `input_suspend` 与 `charging_enabled` 两个内核控制节点"
  - "纯 POSIX Shell 脚本运行：无需任何第三方二进制程序或常驻重型后台进程"
faq:
  - question: "为什么不使用此模块直接整夜插电会损伤电池？"
    answer: "电池长期在 100% 满电状态下承受持续高电压压力，会加速电解液分解与锂枝晶析出。充满后及时切断充电输入可有效避免此类老化。"
  - question: "可以把断充阈值从 100% 改成 90% 吗？"
    answer: "可以。打开 `/data/adb/modules/Charge_control/data.sh`，将其中的 `Stop=90` 与 `Start=85` 修改为你需要的电量阈值即可。"
---

## 概述

**满电自动断充保护模块**（作者：Jiu Shi Long Xia）专为需要长时间连接充电器（例如整夜充电）的智能手机提供电池保护。

---

## 技术架构与工作原理

守护脚本（`data.sh`）会持续轮询监测 `/sys/class/power_supply/battery/capacity` 的实时电量读数：

```bash
Charging_control=/sys/class/power_supply/battery/input_suspend
Charging_control2=/sys/class/power_supply/battery/charging_enabled

# When capacity hits upper limit:
echo 1 > $Charging_control 2>/dev/null || echo 0 > $Charging_control2

# When capacity drops to resumption floor:
echo 0 > $Charging_control 2>/dev/null || echo 1 > $Charging_control2
```
