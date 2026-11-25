---
id: "frosty"
title: "Frosty：精细化 Google Play 服务冻结与深度省电优化套件"
sidebarTitle: "Frosty"
description: "适用于 Magisk、KernelSU 与 APatch 的全方位省电套件，通过 WebUI 实现 GMS 组件分类冻结、深度 Doze 强制休眠与内核内存调优。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Frosty Magisk 模块"
  - "Frosty Drsexo GitHub 下载"
  - "GMS 冻结省电 Magisk 模块"
  - "KernelSU 深度 Doze 强制休眠"
  - "解决 Google Play 服务后台耗电 Root"
prerequisites:
  - "Android 9（Pie）及以上系统"
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "已安装 Google Play 服务（仅 GMS 冻结功能依赖；内核调优与 Doze 功能可独立运行）"
  - "支持 WebUI 管理（KernelSU / APatch 原生内置，Magisk 需配合 KsuWebUI 或 WebUI-X）"
conflicts: []
configPaths:
  - "/data/adb/modules/frosty/"
  - "/data/adb/modules/frosty/config/"
features:
  - "颗粒度 GMS 服务控制：将 Google Play 服务组件划分为 8 个独立类别（遥测、后台、定位、连接、云服务、支付、穿戴等）按需禁用"
  - "智能深度 Doze：锁屏后强制进入设备空闲状态，在 Android 13+ 启用 JobScheduler 弹性空闲策略，息屏预览通知不会打断休眠"
  - "锁屏自动化动作：可配置锁屏延迟后自动关闭 Wi-Fi、蓝牙、移动数据或 GPS 射频并触发内存压缩"
  - "内核与内存调优：自动优化 ZRAM 压缩策略、LMKD / PSI 内存压力阈值以及 VM 回写参数"
  - "省电模式高刷保留：支持微调 Android 原生省电模式，在开启省电的同时保留 90/120Hz 高刷新率"
faq: []
---

## 概述

由 Drsexo 开发的 **Frosty** 是一款专为已 Root Android 设备打造的功能丰富的电源管理与 Google Play 服务（GMS）优化模块。无论是在原厂 ROM 还是第三方类原生 ROM 上，Google Play 服务都常因统计分析、Clearcut 遥测、Phenotype 标志位同步与位置轮询等任务频繁唤醒 CPU，成为待机耗电的重灾区。

Frosty 能在不破坏 Android 核心使用体验的前提下根治此类后台消耗。借助功能完备的 WebUI 控制面板，用户可以按类别精细冻结特定 GMS 组件、启用激进的深度 Doze 策略、调优 Linux 虚拟内存与调度参数，并在锁屏后自动接管射频硬件电源状态。

## 前置要求与兼容性

- **操作系统**：Android 9.0 至最新 Android 版本。
- **Root 方案**：Magisk 20.4 及以上、KernelSU 或 APatch。
  - 在 **KernelSU** 与 **APatch** 下，Frosty 支持免立即重启的热安装。
  - 在 **Magisk** 下，首次安装后需重启设备生效。
- **WebUI 控制界面**：
  - 在 KernelSU 与 APatch 中，可直接点击模块卡片上的 WebUI 按钮进入。
  - 在 Magisk 中，需通过 [KsuWebUI](https://github.com/KOWX712/KsuWebUIStandalone) 或 [WebUI-X](https://github.com/MMRLApp/WebUI-X-Portable) 打开。

目前尚无已知的模块冲突。首次安装后所有优化项默认处于关闭状态，由用户完全自主决定开启哪些功能。

## 核心功能与架构

### 1. 颗粒度 GMS 组件冻结
Frosty 将 Google Play 服务后台任务拆分为 8 个功能清晰明确的类别：

| 类别 | 影响与说明 |
| :--- | :--- |
| **Telemetry（遥测）** | **安全**。拦截 GMS 分析统计、Clearcut 遥测、Phenotype 轮询及广告追踪，不影响正常用户应用。 |
| **Background（后台）** | **安全**。削减周期性后台静默更新与同步轮询。 |
| **Location（定位）** | 可能影响 Google 地图导航精度、地理围栏及“查找我的设备”功能。 |
| **Connectivity（连接）** | 控制 Chromecast 投屏、Quick Share（快速分享）与 Fast Pair（快速配对）协议。 |
| **Cloud（云服务）** | 控制 Google 账号登录验证、云端备份与自动填充同步。 |
| **Payments（支付）** | 控制 Google 钱包、NFC 非接触式支付与交通卡功能。 |
| **Wearables（穿戴设备）** | 控制 Wear OS 手表伴侣同步与 Google Fit 健身数据记录。 |
| **Games（游戏服务）** | 控制 Google Play 游戏成就追踪与云端存档功能。 |

### 2. 深度 Doze 与应用 Doze
Frosty 重写了 Android 内部的 Doze 常量参数。原厂 Android 在口袋中触发运动传感器时便会自动退出空闲状态，而 Frosty 将 Doze 严格绑定至屏幕锁定状态：抬腕查看息屏显示（AOD）或预览锁屏通知不会打破休眠，仅当用户解锁屏幕时才会解除限制。在 Android 13 及以上系统，它还会自动开启 JobScheduler 弹性空闲策略。

### 3. 内核、内存与日志调优
- **RAM 优化器**：自动调校 ZRAM 压缩算法、低内存查杀守护进程（LMKD）阈值及内存压力失速信息（PSI）触发水位。
- **日志服务清理**：关闭不必要的调试日志守护进程（`logd`、追踪服务），消除后台持续写入引发的 CPU 唤醒与内存抖动。
- **省电模式微调器**：允许自定义 Android 原生省电模式行为，包括在开启省电模式时强制保留高刷新率（如 120Hz）。

## 配置与使用

1. 在 Root 管理器中刷入 `Frosty-*.zip`。
2. 从管理器入口打开 Frosty WebUI。
3. 按需配置各个功能面板：
   - **System Tweaks**：开启内核优化、日志服务禁用与内存调优选项。
   - **Doze**：配置应用 Doze 白名单，并选择偏好的深度 Doze 强度（适中 Moderate 或极致 Maximum）。
   - **Screen Off Optimization**：设置锁屏延迟时间，并勾选锁屏后需要自动关闭的射频开关。
   - **GMS Categories**：按需逐项开启或关闭各 GMS 类别。
4. Frosty 的配置文件与持久化状态保存于以下路径：
   ```bash
   /data/adb/modules/frosty/
   /data/adb/modules/frosty/config/
   ```

## 故障排查与验证

- **消息推送延迟**：若 Telegram、Signal、WhatsApp 等第三方即时通讯软件出现通知延迟，请在 WebUI 中将其加入深度 Doze 白名单。GMS/Firebase 本身默认处于白名单内，但当启用极致（Maximum）深度 Doze 时，部分独立聊天应用可能会受到调度节流影响。
- **在无谷歌环境（MicroG / 去谷歌 ROM）中使用**：如果你的系统未安装 Google Play 服务，除 GMS 冻结外的所有功能（深度 Doze、内核调优、内存优化、锁屏动作）依然可以完整独立运行。
