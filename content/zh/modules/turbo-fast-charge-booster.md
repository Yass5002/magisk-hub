---
id: "turbo-fast-charge-booster"
title: "Turbo 极速快充电流步进增强：底层充电调优指南"
sidebarTitle: "Turbo 快充增强"
description: "内核电源供电参数调优模块，通过 init.d 阶段写入 sysfs 指令，统一锁定 AC 交流电、USB 接口与无线充电的最大输入电流步进上限。"
category: "battery-power-charging"
tier: 1
searchQueries:
  - "Turbo 快充增强 Magisk 模块"
  - "Android Root 提高充电电流"
  - "AC 充电 2000mA sysfs 解锁"
  - "Magisk 提升 USB 充电速率"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "内核支持 `power_supply` sysfs 节点读写"
conflicts:
  - "其他冲突的充电温控引擎修改模块"
configPaths:
  - "/data/adb/modules/KSCD/common/service.sh"
  - "/sys/class/power_supply/battery/current_max"
features:
  - "将 AC 交流充电输入电流上限锁定为 2000mA（2.0A）"
  - "将 USB 数据端口充电电流上限从默认的 500mA 提升至 1100mA（1.1A）"
  - "将无线充电输入电流上限提升至 1100mA"
  - "轻量化开机一次性注入脚本，无常驻后台守护进程，零 CPU 开销"
faq:
  - question: "这个模块能让普通的 5W 充电头强行输出 18W 功率吗？"
    answer: "不能。实际供电功率上限仍由充电器与手机之间的协议握手决定。该模块的作用是防止 Android 内核在接入大功率电源时因保守策略将电流不必要地压低至 500mA。"
  - question: "使用后机身发热量会明显增加吗？"
    answer: "提高充电电流自然会使电池温度略有上升，建议在快充期间保持设备周围通风散热良好。"
---

## 概述

**Turbo 极速快充电流步进增强（Turbo Fast Charge Current Step Booster）**（作者：XLIVE）专为解决部分机型原厂内核策略过于保守的问题而设计，可优化 Root 设备在 USB 与 AC 接口下的充电输入限流阈值。

---

## 技术架构与工作原理

在系统启动初始化阶段，模块会向对应的内核 sysfs 节点执行一系列电流上限写入操作：

```bash
# Configure maximum allowable charging currents across interfaces
for node in /sys/class/power_supply/*; do
    [ -f "$node/current_max" ] && echo 2000000 > "$node/current_max"
    [ -f "$node/hw_current_max" ] && echo 2000000 > "$node/hw_current_max"
done
```

这一操作可防止内核电池驱动在后台进程引起轻微温度波动时频繁下调电流档位，从而保持稳定高效的充电速度。
