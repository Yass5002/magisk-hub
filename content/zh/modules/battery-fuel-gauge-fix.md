---
id: "battery-fuel-gauge-fix"
title: "Battery Fuel Gauge Fix：高通 BMS 电量计校准与系统 UI 同步"
sidebarTitle: "电量计校准修复"
description: "内核驱动级电量同步工具，通过读取高通 BMS 硬件寄存器并强制对齐 Android BatteryService，解决状态栏电量显示漂移与跳电问题。"
category: "battery-power-charging"
tier: 1
searchQueries:
  - "Magisk 电量校准修复模块"
  - "高通 BMS capacity_raw 电量修复"
  - "Android 电量跳电虚高修复"
  - "Battery Fuel Gauge Fix 下载"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "搭载硬件 BMS sysfs 接口的高通骁龙平台设备"
conflicts:
  - "其他激进的电量百分比伪装或修改类模块"
configPaths:
  - "/sys/class/power_supply/bms/capacity_raw"
  - "/sys/class/power_supply/bms/capacity"
  - "/data/adb/modules/bat_capacity_fix/service.sh"
features:
  - "直接从高通 BMS 内核 sysfs 节点读取硬件库仑计原始数据"
  - "通过 `dumpsys battery set level` 持续将硬件真实电量同步至系统 `BatteryService`"
  - "动态自适应轮询周期：充电期间每 5 秒同步一次，放电期间每 20 秒同步一次"
  - "内置编译好的原生伴随二进制程序 `bat_capacity_fix`，实现极低开销的后台监听"
  - "有效预防电量骤降与突然关机（例如从 20% 直接跳变至 1% 或直接断电）"
faq:
  - question: "为什么 Android 系统显示的电量百分比会与实际剩余电量产生偏差？"
    answer: "Android 框架层依赖结合电池电压、开路电压曲线与负载补偿的软件估算算法。在长期使用的旧电池或更换过电芯的设备上，系统软件估算值容易与硬件电量计（BMS 库仑计）产生明显偏离，导致状态栏电量不准或提前关机。"
  - question: "这个模块能修复已经物理老化的电芯吗？"
    answer: "不能。该模块无法恢复老化电芯的化学容量，但能确保屏幕右上角显示的电量百分比准确反映物理电池管理芯片（PMIC）实时计算出的真实电量。"
---

## 概述

**Battery Fuel Gauge Fix**（作者：DuduSki）是一款底层电池校准模块，用于消除 Android 状态栏显示电量与物理电池管理系统（BMS）真实电量之间的偏差。

在搭载高通骁龙（Snapdragon）平台的设备上，电源管理集成电路（PMIC）内置了独立的电池监控系统（BMS）。硬件 BMS 通过高精度检流电阻持续计量进出电芯的电荷量（即库仑计数）。然而，Android 框架层服务（`BatteryService`）会叠加复杂的平滑估算算法，在刷写第三方 ROM、更换内核或电池老化后，系统估算值往往会与底层硬件失步。

这种失步会带来令人困扰的故障：例如手机显示还有 15% 电量却突然关机，或者充电时长期卡在 100% 之后迅速掉电。Battery Fuel Gauge Fix 绕过系统框架层的平滑算法，直接将界面显示绑定至内核 BMS 的硬件遥测数据。

---

## 技术架构与工作原理

该模块在 `late_start` 服务启动阶段建立监管守护进程：

### 1. 硬件寄存器节点探测

模块会检测 Linux `/sys` 文件系统中的电源供应类节点层级：

```bash
# Primary Qualcomm BMS raw capacity node (measured in basis points: e.g., 8500 = 85.00%)
/sys/class/power_supply/bms/capacity_raw

# Secondary fallback hardware capacity node
/sys/class/power_supply/bms/capacity

# Real-time charging state node
/sys/class/power_supply/battery/status
```

### 2. 同步循环机制

1. **遥测采样**：后台守护进程将 `capacity_raw` 返回的原始整数除以 100，提取出精确的整数百分比。
2. **框架层对齐**：当检测到真实电量发生变动时，脚本通过标准 Shell IPC 指令刷新 Android 电池状态机：
   ```bash
   dumpsys battery set level <calibrated_level>
   ```
3. **自适应功耗调度**：
   - **放电状态**：守护进程以 20 秒为周期休眠轮询，最大限度减少 CPU 唤醒次数，避免额外待机耗电。
   - **充电状态**：轮询间隔缩短至 5 秒，确保充电过程中电量数值平滑、及时地递增。

### 3. 原生二进制加速

除了 `service.sh` 中的 POSIX Shell 监控脚本外，模块还内置了优化的原生二进制可执行文件 `bat_capacity_fix`。在支持的内核上，该程序可直接挂钩内核 sysfs 事件，彻底消除 Shell 脚本频繁调起带来的进程开销。

---

## 验证与手动测试

如需确认你的设备内核是否支持该模块依赖的 BMS sysfs 节点，可在终端执行：

```bash
su -c "cat /sys/class/power_supply/bms/capacity_raw"
```

如果设备返回了一个整数（例如 `7842` 代表约 78.4%），说明高通硬件电量计节点可正常访问且已启用。
