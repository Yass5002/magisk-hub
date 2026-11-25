---
id: "freepps-xiaomi-fast-charge"
title: "FreePPS 小米公版 PPS 快充协议解锁模块"
description: "支持 KernelSU、APatch 与 Magisk 的快充解锁模块，用于在小米与红米智能手机上启用完整标准的 USB-PD 可编程电源（PPS）公版快充协议。"
category: "battery-power-charging"
author: "Seyud"
version: "v1.7.0"
updatedAt: "2026-10-04"
compatibility: ["KernelSU", "APatch", "Magisk"]
sidebarTitle: "FreePPS 小米公版 PPS 快充解锁"
tier: 1
searchQueries: []
prerequisites: []
conflicts: []
configPaths: []
features: []
faq: []
---

## 概述与系统架构

由 Seyud 开发的 **FreePPS** 是一款开源电池与充电子系统模块，专为解锁并启用小米、红米（Redmi）及 POCO 智能手机的完整公版 **PPS（Programmable Power Supply，可编程电源）** 快充协议而设计。

小米原厂固件通常会将第三方 USB-PD 充电器的功率限制在基础的 18W–27W 档位，而将高功率快充（33W、67W、120W）锁定给私有协议的小米 Charge Turbo 原装充电头。FreePPS 通过修改内核充电握手协商参数与 sysfs 电源供电限制，解除厂商充电协议限制，让兼容 PPS 协议的第三方多口氮化镓（GaN）充电器也能稳定输出高达 55W–65W 以上的快充功率。

## 核心充电特性

1. **绕过 PPS 握手限制**：覆盖并解除 `/sys/class/power_supply/battery/` 与 `/sys/class/qcom-battery/` 中的厂商供电策略限制。
2. **广泛兼容第三方氮化镓充电头**：支持 Anker、倍思（Baseus）、绿联（Ugreen）及酷态科（CUKTECH）等支持标准 PPS 的 USB-PD 充电器以设备硬件允许的更高功率为小米手机充电。
3. **亮屏快充提速**：防止设备在点亮屏幕使用期间大幅下调充电输入电流。

## 安装与验证

### 第一步：刷入模块压缩包
通过 KernelSU、APatch 或 Magisk 刷入 `FreePPS_v1.7.0.zip`。

### 第二步：重启后验证实际功率
连接经过验证的 65W+ 或 100W 支持 PPS 协议的 USB-PD 充电器，并在终端执行以下命令查看电流与电压：
```bash
cat /sys/class/power_supply/battery/current_now
cat /sys/class/power_supply/battery/voltage_now
```
实时充电功率计算公式：`(current_now * voltage_now) / 10^12 = Watts（瓦特）`。

### 第三步：检查内核充电协议日志
```bash
dmesg | grep -iE "pps|pd_policy|charge" | tail -n 20
```

## 硬件安全与温度控制

- 设备主板上的硬件级电池保护 IC 依然全程保持有效工作，可可靠防止过压或热失控风险。
- 建议在刷入模块后的前几次快充循环中留意电池温度变化，确保环境散热良好。
