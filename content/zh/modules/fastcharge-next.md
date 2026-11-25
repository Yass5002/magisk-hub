---
id: "fastcharge-next"
title: "FastCharge Next：内核充电电流优化与热安全保护"
sidebarTitle: "FastCharge Next"
description: "通过优化内核温控限流阈值与 USB 电源参数，在安全温度边界内最大限度提升快充输入功率。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "FastCharge Next Magisk 模块"
  - "Dev97633 Fastcharge-next 下载"
  - "Root 提高安卓充电电流"
  - "Magisk 解除充电温控限流"
  - "安全快充内核优化模块"
prerequisites:
  - "Android 9.0 及以上系统"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "内核支持可调节电流上限的 sysfs power_supply 节点"
conflicts: []
configPaths:
  - "/data/adb/modules/fastcharge-next/"
features:
  - "提高充电电流上限：解除厂商在 USB-PD、Quick Charge 及私有快充协议上设置的保守电流限制"
  - "放宽温控降流曲线：避免设备在机身微热时就被内核过早砍半充电功率"
  - "内置电池安全边界：严格遵循硬件最高截止电压与紧急高温断充阈值，防止电芯鼓包"
  - "跨框架通用兼容：在 Magisk、KernelSU 与 APatch 上均可稳定工作"
faq: []
---

## 概述

如今的 Android 智能手机虽然普遍配备了高规格快充电池控制芯片与大功率充电器，但厂商原厂系统往往会将实际充电电流限制在远低于硬件承受能力的水准。许多厂商内核在电池温度刚达到 36°C 时，便会激进地将功率压低至 5W/10W 水平；或在检测到第三方 USB-PD 充电头时强制钳制输入电流。

由 Dev97633 开发的 **FastCharge Next** 通过调优系统及内核电源参数，帮助设备实现更快、更稳定的快充功率输出。它在内核 `power_supply` 节点层面安全调整电流缩放策略，在保留硬件热保护机制的前提下显著缩短完整充电耗时。

## 核心机制与安全防护

FastCharge Next 主要作用于 `/sys/class/power_supply/` 目录下的内核电源参数：
- **电流限制调节**：覆盖 USB 与 AC 充电通路的人为输入电流上限（`current_max`、`constant_charge_current_max`），让电源管理子系统能够跑满协商功率。
- **阶梯式温控过渡**：以更平缓、宽容的温度区间替代原厂断崖式降流策略，使高功率快充阶段维持更长时间。
- **硬件安全底线**：模块严格尊重底层电池管理芯片（PMIC）的硬件最高电压上限（如 4.35V / 4.45V）以及紧急过温断电保护，杜绝危险过压或电池加速老化风险。

## 安装与使用

1. 确认设备已通过 **Magisk**、**KernelSU** 或 **APatch** 获取 Root 权限。
2. 从 GitHub 发布页下载 `chargeboost-magisk` / `Fastcharge-next` 的 `.zip` 安装包。
3. 在 Root 管理器中刷入该压缩包并重启设备。
4. 连接原装快充头或高功率 USB-PD 充电器。
5. 可使用 Ampere 或 Franco Kernel Manager 等工具监测实时充电电流，验证功率提升效果。
