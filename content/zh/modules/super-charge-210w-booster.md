---
id: "super-charge-210w-booster"
title: "210W 亮屏极限快充模块：底层温控与架构解析"
sidebarTitle: "210W 亮屏快充"
description: "高级厂商温控引擎调优模块，解除小米与红米手机亮屏状态下最高 210W 充电电流限制，同时保留严格的 80°C 硬件级安全温控边界。"
category: "battery-power-charging"
tier: 1
searchQueries:
  - "210W 亮屏快充 Magisk 模块"
  - "小米 Root 解除亮屏充电限流"
  - "MIUI 旁路与亮屏快充电流限制解除"
  - "修改温控引擎实现满速快充"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "小米、红米（Redmi）或 POCO 智能手机（骁龙或联发科平台）"
  - "高功率氮化镓 / 小米 HyperCharge 充电器及配套 6A/10A 数据线"
conflicts:
  - "其他激进的温控引擎禁用模块或同类温控配置修改模块"
configPaths:
  - "/system/vendor/etc/thermal-*.conf"
  - "/system/vendor/bin/thermal-engine-v2"
  - "/system/vendor/lib/modules/thermal_pause.ko"
  - "/data/adb/modules/鹤征/service.sh"
features:
  - "消除亮屏时的人为限流降功率（避免 67W/120W 亮屏骤降至 15W）"
  - "全面解锁 18W、33W、55W、67W、120W 及 210W 全档位快充策略"
  - "无系统分区修改替换 `/vendor/etc/` 与 `/vendor/etc/thermal/` 下的厂商温控配置"
  - "硬件安全护栏：设定 80°C 强制断流保护阈值，防止电池过热老化"
faq:
  - question: "刷入这个模块会损坏手机或电池吗？"
    answer: "该模块解除了系统在亮屏状态下刻意降低充电速度的软件限流策略。由于大功率充电本身会产生热量，模块内置了严格的 80°C 紧急断流保护以防热失控。若在边玩高负载游戏边快充的场景下使用，强烈建议配合手机散热背夹。"
  - question: "原本只支持 33W 的手机刷了这个模块能变成 210W 快充吗？"
    answer: "不能。最大充电功率从根本上取决于设备硬件规格（电荷泵芯片、双电芯串联架构及电源管理 PMIC）。本模块的作用是让手机在亮屏状态下也能跑满自身硬件支持的最大物理快充上限，避免被系统温控强行压低功率。"
---

## 概述

**210W 亮屏极限快充模块**（作者：He Zheng & Class 6 Grade 1）是一款面向小米、红米（Redmi）与 POCO 智能手机的底层充电功率解锁模块。

在原厂 MIUI 与 HyperOS 系统中，只要手机点亮屏幕，系统就会激进地限制快充功率——经常将原本 67W 或 120W 的快充连接强行压低到 15W–18W 左右，以控制机身表面温度。该模块通过重构设备温控引擎规则，让用户在边玩游戏、导航或看视频的亮屏场景下依然能够体验全速快充。

---

## 技术架构与工作原理

该模块跨内核模块、用户态守护进程与配置文件三层执行完整的无系统分区修改（Systemless）厂商策略覆盖：

### 1. 温控引擎与二进制守护进程替换

模块修补并替换位于 `/system/vendor/bin/` 目录下的厂商温控二进制文件：
- `thermal-engine-v2`
- `mi_thermald`
- `thermal_manager`

这些程序直接与 Linux sysfs 节点（`/sys/class/power_supply/battery/current_now` 与 `/sys/class/qcom-chg/`）通信，用以动态调节充电步进电流。

### 2. 厂商温控策略覆盖

模块在 `/system/vendor/etc/` 目录提供了全套自定义温控配置文件：
- `thermal-global-u-chg-only.conf`
- `thermal-global-u-nolimits.conf`
- `thermal_configs.xml`（游戏引擎联动配置）

在这些自定义策略下，系统移除了亮屏触发的阶梯降流阈值，指示充电控制器持续维持最高握手功率。

### 3. 安全护栏（80°C 硬件级过热保护）

解除厂商限流后必须具备可靠的硬件兜底机制。该模块内置了以下保护策略：
- **80°C 紧急熔断阈值**：一旦电池温度传感器读数超过 80°C，守护逻辑会立即切断充电电流 10 秒或强制切换为涓流充电，从根本上杜绝热失控风险。

---

## 验证与功率监控

在亮屏充电状态下实时监测当前充电电流与功率：

```bash
# Query active battery charging metrics
cat /sys/class/power_supply/battery/current_now
cat /sys/class/power_supply/battery/voltage_now

# Calculate real-time charging wattage:
# (current_now [uA] / 1,000,000) * (voltage_now [uV] / 1,000,000) = Watts
```
