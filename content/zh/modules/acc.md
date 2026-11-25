---
id: "acc"
title: "Advanced Charging Controller (ACC)：通过内核电源节点延长电池寿命"
sidebarTitle: "Advanced Charging Controller"
description: "由 VR25 开发的专业电源管理守护进程，通过读写内核 power_supply 节点控制充电电量阈值、电流上限与旁路供电（Idle Mode）。"
category: "battery-power-charging"
tier: 1
searchQueries:
  - "ACC 充电控制 Magisk 模块"
  - "Android Root 限制充电到 80%"
  - "ACC 旁路供电教程"
  - "VR25 ACC 下载配置"
  - "游戏直充旁路供电模块"
prerequisites:
  - "Android 5.0（Lollipop）及以上系统"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "内核支持可写的电源管理 sysfs 节点（`/sys/class/power_supply/`）"
conflicts:
  - "部分 OEM 激进私有快充守护进程（如部分一加 WARP / OPPO VOOC 协议服务可能强制覆盖限流参数）"
  - "不可与其他同类电池充电控制模块同时运行"
configPaths:
  - "/data/adb/vr25/acc-data/config.txt"
  - "/data/adb/vr25/acc-data/disable"
  - "/data/adb/modules/acc/"
features:
  - "电量阈值控制：到达指定上限（如 80%）自动停止充电，跌至下限后恢复"
  - "电池旁路供电（Idle Mode）：直接由 USB 充电器为主板供电，不再向电池充入电流"
  - "电流与电压限流：游戏或高负载场景下动态降低功率，有效防止电池过热衰减"
  - "自动充电开关测试：自动遍历内核 `power_supply` 节点以筛选稳定可用的控制开关"
faq:
  - question: "为什么将充电上限限制在 80% 有助于保护电池？"
    answer: "锂离子电芯在电压超过 4.10V（约 80%–85% 电量）后承受的电化学压力呈指数级上升。将充电上限控制到 80% 并避开高温高压满充阶段，可将电池循环寿命延长 3 至 5 倍。"
  - question: "停止充电时手机突然重启怎么办？"
    answer: "部分设备内核在切换不兼容的充电开关节点时会触发内核异常重启。请在终端执行 `su -c acc -t`，ACC 会逐一测试 `/sys/class/power_supply/` 下的每个开关并自动拉黑会引起重启的节点。"
  - question: "ACC 的防变砖紧急禁用保护是如何工作的？"
    answer: "ACC 在开机动画结束 60 秒后才会正式启动守护进程。若配置出错引发异常，你有充足的时间在开机一分钟内执行 `su -c accd -x` 或 `touch /data/adb/vr25/acc-data/disable` 立即中止启动。"
---

## 概述

由 VR25 开发的 **Advanced Charging Controller（ACC）** 是面向 Root Android 设备功能最完整、适配面最广的电源管理守护进程。

原厂 Android 系统通常会将锂电池持续充至 100% 满电并维持高电压（常见为 4.35V–4.45V），甚至在机身温度升高时依然保持大电流充电。这种高电压满充与热饱和状态会加速电芯鼓包、永久容量衰减与续航下降。

ACC 通过直接对接 Linux 内核的电源供应子系统（`/sys/class/power_supply/`），让你能够精细控制充放电电量阈值、最大充电电流（mA）、截止电压以及温控充电策略。

---

## 技术架构与内核电源开关

现代 Android 设备通过内核驱动控制硬件 PMIC（电源管理集成电路），这些驱动会在 `sysfs` 中暴露可写属性节点：

```
┌────────────────────────────────────────────────────────┐
│                   acc 守护进程 (accd)                   │
│   - 读取电池温度与实时电量                              │
│   - 执行暂停/恢复充电规则                               │
└───────────────────────────┬────────────────────────────┘
                            │ 写入 0 或 1
┌───────────────────────────▼────────────────────────────┐
│      内核 Sysfs 电源节点 (/sys/class/power_supply)      │
│  - battery/charging_enabled                            │
│  - battery/input_suspend                               │
│  - bms/charge_control_limit_max                        │
└───────────────────────────┬────────────────────────────┘
                            │ I2C / SPMI 总线
┌───────────────────────────▼────────────────────────────┐
│           硬件 PMIC（高通 / 联发科电源管理芯片）         │
│  控制电流分配至电池或直接供给主板                        │
└────────────────────────────────────────────────────────┘
```

当电量到达设定阈值（例如 80%）时，`accd` 会向内核充电开关写入禁用值。如果设备内核支持 **电池旁路供电（Battery Idle Mode）**，流入电池的电流将降至 0 mA，主板完全由外部充电器直接供电。

---

## 安装与初始配置

### 安装步骤
1. 从官方发布页下载 `acc_v*.zip`。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入该模块。
3. 重启设备。

### 验证安装与查看实时状态
打开任意 Root 终端（如 Termux）运行：
```bash
su
acc -i
```
命令将输出实时电池诊断数据：
- 当前剩余电量（%）
- 实时充放电电流（mA）
- 电池温度（°C）
- 当前充电状态及正在使用的内核开关路径

---

## 常用 CLI 命令与配置示例

ACC 通过 `acc` 命令行工具提供灵活控制：

### 1. 设置充放电电量阈值
充至 80% 自动停充，电量降至 70% 后恢复充电：
```bash
su -c acc 80 70
```

### 2. 限制最大充电电流
夜间慢充保护电池，将最大充电电流限制为 1500 mA（1.5A）：
```bash
su -c acc -s c_max=1500
```

### 3. 设置高温停充阈值
避免重度游戏或高温环境下边充边玩加速电池老化（高于 40°C 停充，降温至 37°C 恢复）：
```bash
su -c acc -s temp=40-37
```

### 4. 自动检测最稳定的充电开关
运行自动开关测试，筛选支持真旁路供电且不会触发重启的安全节点：
```bash
su -c acc -t
```
ACC 会依次检测每个可用开关、监控电流变化、确认是否进入真 Idle Mode，并自动屏蔽异常开关。

---

## 硬件注意事项与 OEM 机型差异

### 小米机型（Poco X3 Pro 及部分 PMIC 机型）
- **已知现象**：部分小米设备搭载的 PMIC 在极低电量下强行挂起充电可能出现芯片锁死。
- **应对建议**：保持低电量自动关机阈值开启（默认为 5%）：
  ```bash
  su -c acc -s shutdown_capacity=5
  ```
- 若意外遇到无法充电的情况，将设备重启至 Fastboot/Bootloader 模式后再选择 *Reboot System* 即可重置硬件 PMIC 寄存器。

---

## 紧急恢复与安全卸载

ACC 内置多重故障保护机制，最大限度避免不可逆的启动故障：

1. **开机 60 秒延迟保护**：守护进程会在开机动画结束 60 秒后才加载配置策略。
2. **一键紧急禁用**：
   连接电脑 ADB 后执行：
   ```bash
   adb wait-for-device shell
   su
   touch /data/adb/vr25/acc-data/disable
   reboot
   ```
3. **彻底卸载模块与数据**：
   ```bash
   rm -rf /data/adb/modules/acc
   rm -rf /data/adb/vr25
   ```
