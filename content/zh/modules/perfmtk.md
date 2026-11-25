---
id: "perfmtk"
title: "PerfMTK：联发科内核调度、Mali GPU、触控采样与温控旁路引擎"
sidebarTitle: "PerfMTK"
description: "专为联发科天玑（Dimensity）与 Helio 芯片定制的硬件性能及温控调度套件，集成 Mali GPU 提频、触控面板超频与充电温控旁路功能。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "PerfMTK Magisk 模块下载"
  - "联发科天玑性能优化 Root 模块"
  - "Mali GPU GED HAL 加速"
  - "PerfMTK 旁路供电电池保护"
  - "天玑芯片触控采样率解锁"
prerequisites:
  - "搭载 Mali GPU 的联发科 SoC（Helio 或天玑系列）"
  - "Android 9.0（Pie）至 Android 15/16 系统，Linux 内核版本 4.14 至 6.1+"
  - "通过 Magisk（推荐 v27+）、KernelSU 或 APatch 获取 Root 权限"
  - "KernelSU 与 APatch 环境需配合 Magic Mount 辅助模块（如 Hybrid Mount 或 Mountify）"
conflicts: []
configPaths:
  - "/data/adb/modules/perfmtk/config/app_profiles.conf"
  - "/data/adb/modules/perfmtk/config/performance.conf"
  - "/data/adb/modules/perfmtk/config/balanced.conf"
  - "/data/adb/modules/perfmtk/config/powersave.conf"
features:
  - "四级前台应用识别：结合 LSPosed Hook、Netlink 进程连接器（cn_proc）与 cgroup inotify 精准追踪前台焦点应用"
  - "硬件触控加速：直接调用触控面板 ioctl 接口解锁最高 480Hz/2160Hz 采样率，并将触控中断 IRQ 从小核解绑"
  - "智能快充旁路：在保持高速充电的同时将热负载从电芯剥离，使游戏时电池温度稳定控制在 36°C 以下"
  - "预测式温控守护（Thermal Guardian）：实时监测温度变化斜率（ΔT/Δt），平滑调节频率以避免锯齿状剧烈降频"
  - "联发科专属底层调优：配置 DRAM DVFSRC LPDDR5X 总线频率、Mali GED HAL 频率余量与 `/sys/kernel/fpsgo` 驱动参数"
  - "交互式终端 TUI 与 CLI：内置完整命令行工具套件，支持实时遥测流输出、情景模式切换及温控覆写"
---

## 概述

不同于高通骁龙平台拥有广泛的第三方内核生态与标准化的能量感知调度（EAS），联发科天玑（Dimensity）和 Helio 平台高度依赖厂商私有驱动，例如联发科游戏加速引擎（GBE）、GED HAL、DVFSRC 内存控制器以及 `fpsgo` 帧率预测子系统。市面上的通用 Android 性能脚本在联发科芯片上往往会失效，因为它们尝试调节的都是高通平台才存在的 sysfs 节点。

由 JUANIMAN 开发的 **PerfMTK** 是一款专为联发科 SoC 打造的工程级性能与能耗调度守护进程。PerfMTK 直接接入联发科底层内核驱动，能够解锁触控采样率、将内存总线频率动态管理至最高 8533 MHz，并在 120 FPS 高帧率竞技游戏中提供硬件级旁路供电，从而延长电池寿命。

## 核心硬件子系统与能力

### 1. 四级前台应用识别
PerfMTK 通过监测当前活跃的前台应用，在 **Performance（性能）**、**Balanced（均衡）**、**Powersave（省电）** 与 **Powersave+（深度省电）** 之间自动切换情景模式，并采用按优先级递进的检测机制：
1. **LSPosed Hook（`PerfMTK-Hook`）**：进程内窗口管理器挂钩（Hook），响应近乎零延迟。
2. **Netlink 进程连接器（`cn_proc`）**：内核级 Socket 监听器，实时捕获进程 fork 与 exec 事件。
3. **cgroup.procs inotify**：基于内核 cgroup 层级结构的文件描述符监听。
4. **自适应防抖轮询兜底**：面向非标准系统环境的轮询回退方案。

### 2. 触控采样加速与 IRQ 隔离
- **解锁触控采样率**：直接对接触控驱动接口（`/dev/xiaomi-touch`、`/proc/touchpanel`、`/sys/class/touch/touch_dev`、三星 TSP），启用硬件支持的最高采样率（480Hz 至 2160Hz）。
- **IRQ 亲和性解绑**：避免触控输入中断集中堆积在能效小核上，消除高频滑动或连点操作时的线程抢占与微卡顿。

### 3. 温控旁路与电池保护
- **游戏旁路供电**：允许在游戏期间保持高功率接入，同时智能调控充电电流阈值，将电池温度稳定压制在 31°C 至 36°C 之间。
- **可配置熔断保护**：内置紧急硬件断电保护阈值（默认 52°C）。
- **电池保养（Battery Care）**：设定充电电量上限（例如充至 80% 自动停止），减少长期满充带来的电芯衰减。

### 4. 联发科专属硬件调优接口
- **DRAM DVFSRC**：在高纹理负载场景下动态拉升 LPDDR5X 内存总线频率，最高可达 8533 MHz。
- **Mali GPU 与 GED 调优**：在 Linux 5.x 与 6.x 内核上精细调整 `dvfs_margin_value` 与 `gpu_boost_level`。
- **FPSGO 优化**：针对 Android 14 至 Android 16 系统自适应配置 `/sys/kernel/fpsgo` 调度节点。

## 终端命令行用法（`perfmtk`）

在 Root 终端中执行 `su -c perfmtk` 即可启动交互式控制面板，或直接通过命令行切换配置：

```bash
# Apply operating profiles manually
su -c perfmtk performance
su -c perfmtk balanced
su -c perfmtk powersave

# Manage Smart Fast Charge Bypass
su -c perfmtk --charge-bypass on      # Force charging bypass during gaming
su -c perfmtk --charge-bypass off     # Revert to standard charging
su -c perfmtk --charge-bypass status  # Query current thermal bypass state

# Configure Battery Care charge limiter (e.g., cap at 80%)
su -c perfmtk --battery-care on 80
su -c perfmtk --battery-care off

# Manage Predictive Thermal Guardian
su -c perfmtk --tg on 75 2            # Target 75°C with max 2 clamp steps
su -c perfmtk --tg status             # Display real-time thermal slope

# Telemetry streaming
su -c perfmtk -s                      # Live formatted status snapshot
su -c perfmtk --stream 1000           # Stream telemetry as JSON every 1000ms
```

## 配置与情景模式自定义

情景模式保存在 `/data/adb/modules/perfmtk/config/` 目录下的纯文本配置文件中：
- **`app_profiles.conf`**：将应用包名映射至指定性能模式及附加开关（例如 `com.tencent.ig=performance;thermal=off;touch=game`）。
- **`performance.conf` / `balanced.conf`**：定义底层 CPU 调度器（Governor）、频率上下限以及 UCLAMP 最小/最大调度权重。
