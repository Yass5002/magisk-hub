---
id: "sunshine-global-high-refresh-rate"
title: "Sunshine 全局高刷新率解锁：强制全局 120Hz/144Hz"
sidebarTitle: "全局高刷解锁"
description: "通用显示刷新率调优模块，在所有用户应用、系统浮窗与视频播放器中强制维持 120Hz 或 144Hz 刷新率，避免动态降频。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Sunshine 全局高刷 Magisk"
  - "强制全局 120Hz Magisk 模块"
  - "所有应用解锁 120Hz Root"
  - "关闭安卓 60Hz 刷新率限制"
prerequisites:
  - "配备 90Hz、120Hz 或 144Hz 物理高刷屏幕的 Android 手机"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他强制锁定屏幕刷新率的同类型脚本"
configPaths:
  - "/system/bin/sunshine_rate"
  - "/data/adb/modules/Sunshine_Rate/service.sh"
features:
  - "在所有已安装的应用中全局强制启用屏幕面板最高刷新率"
  - "消除视频播放应用与相机取景器中令人困扰的 60Hz 强制降频"
  - "内置自动化后台守护，在机身触发温控限制时依然维持高刷锁定"
  - "极轻量的 Shell 脚本守护进程，几乎不产生可感知的 CPU 开销"
faq:
  - question: "全局强制 120Hz 会增加耗电吗？"
    answer: "会的。与动态可变刷新率（VRR）相比，屏幕在亮屏期间持续运行在最高刷新率下，整机功耗大约会增加 5% 至 10%。"
  - question: "该模块会损坏手机屏幕硬件吗？"
    answer: "不会。该模块仅激活设备显示控制器与内核驱动原生支持并声明的刷新率挡位，不会对硬件进行超频。"
---

## 概述

**Sunshine 全局高刷新率解锁（Sunshine Global High Refresh Rate Enabler）**（由 Everything by the sun 开发）是一款系统调优模块，专为消除手机厂商施加的软件层刷新率限制而设计。

如今主流智能手机均配备了 120Hz 甚至 144Hz 的高刷屏幕，但厂商固件常常在网页浏览器、视频流媒体应用（如 YouTube、Netflix）、地图导航以及相机取景器等高频场景中将刷新率强行限制在 60Hz。Sunshine Rate 能够绕过这些系统策略限制，在整个操作系统范围内提供始终如一的顺滑视觉体验。

---

## 技术架构与工作原理

该模块通过直接与 Android SurfaceFlinger 合成器及显示 HAL 层交互来实现控制：

### 1. 显示模式探测

在开机初始化阶段，后台服务会查询显示驱动当前可用的硬件显示模式 ID：

```bash
# Query hardware display configurations
dumpsys display | grep -E "mSupportedModes|mDefaultModeId"
```

### 2. 全局策略覆写

守护进程向 Android 窗口管理器与系统设置数据库下发指令，将最高刷新率与最低刷新率统一锁定为屏幕面板的最大物理规格：

```bash
settings put system min_refresh_rate 120.0
settings put system peak_refresh_rate 120.0
settings put global user_refresh_rate 120
```

通过持续评估 `sys.boot_completed` 状态与设备温控事件，模块能够阻止激进的 OEM 省电守护进程将屏幕刷新率重置回 60Hz。

---

## 故障排查与验证

- **实时帧率验证**：在系统**开发者选项**中开启**显示刷新率**，即可在屏幕左上角实时监控当前的实际刷新率。
- **游戏兼容性说明**：部分游戏在自身引擎内部写死了 60 FPS 帧率上限；针对这类游戏，建议搭配专用帧率解锁模块或厂商性能调度模块共同使用。
