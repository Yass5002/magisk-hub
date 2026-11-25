---
id: "thermal-controller-bypass"
title: "Thermal Controller Disabler：无侵入式系统温控解除与降频旁路"
description: "由爱玩机工具箱（AiWanJi ToolBox）出品的无侵入式温控移除模块，用于旁路系统温控限制、覆盖原厂温控配置文件并防止 CPU/GPU 激进降频。"
category: "performance-kernel"
author: "Xiao Bai Yang / AiWanJi"
version: "183.72"
updatedAt: "2026-10-04"
compatibility: ["Magisk", "KernelSU", "APatch"]
---

## 概述与系统架构

**Thermal Controller Disabler** 是知名工具“爱玩机工具箱（AiWanJi ToolBox）”作者小白杨（Xiao Bai Yang）开发的一款性能优化模块。各家 Android 厂商通常会在系统内预设极其保守的温控守护策略，一旦电池温度达到 38°C–42°C，便会立刻触发激进的 CPU/GPU 降频、强制降低屏幕亮度并限制充电功率。

该模块采用无侵入式（Systemless）叠加挂载技术，将 `/vendor/etc/` 目录下的原厂温控策略文件替换为精简的空置/中和配置文件。由于底层温控引擎（`thermald` / `thermal-engine`）无法读取到原有的限频表，设备便可在高强度竞技游戏与重度 3D 渲染场景下持续稳定地发挥峰值性能。

## 模块覆盖文件清单

经对模块刷机包结构分析，该模块对下列原厂温控配置文件进行了全面屏蔽与覆盖处理：

- `/system/vendor/etc/thermal-phone.conf`（常规手机日常温控策略）
- `/system/vendor/etc/thermald-devices.conf`（设备温度传感器映射表）
- `/system/vendor/etc/thermal-chg-only.conf`（充电电流温控限流策略）
- `/system/vendor/etc/thermal-4k.conf`（4K/8K 视频录制温控封顶）
- `/system/vendor/etc/thermal-camera.conf` 与 `thermal-per-camera.conf`（相机拍摄温控保护）
- `/system/vendor/etc/thermal-normal.conf` 与 `thermal-per-normal.conf`（通用性能功耗限制包络）
- `/system/vendor/etc/thermal-video.conf` 与 `thermal-per-video.conf`（视频播放温控限频）
- `/system/vendor/etc/thermal-map.conf` 与 `thermal-navigation.conf`（GPS 导航场景温控限制）
- `/system/vendor/etc/thermal-class0.conf` 与 `thermal-per-class0.conf`（低功耗阈值策略）

## 核心性能优势

1. **维持满帧输出**：避免在《原神》《崩坏：星穹铁道》《PUBG Mobile》等大型高负载游戏中因温度上升而突然从 120 FPS 跌落至 60 FPS。
2. **防止屏幕强制变暗**：屏蔽因屏幕面板触及厂商温控阈值而触发的自动强行降亮度行为。
3. **保持亮屏快充速度**：通过中和 `thermal-chg-only.conf` 策略，确保边玩边充或亮屏使用时依然维持较高的快充功率。

## 安装与验证

### 第一步：刷入模块
通过 Magisk、KernelSU 或 APatch 直接刷入模块压缩包，`install.sh` 脚本会自动将处理后的温控配置解压部署至 `$MODPATH`。

### 第二步：验证文件挂载生效
重启设备后，在终端检查 `/vendor/etc/` 下的温控文件是否已成功由模块挂载替换：
```bash
ls -la /vendor/etc/thermal-normal.conf
# File size should reflect the module's neutralized configuration
```

### 第三步：高负载下验证核心频率
运行 CPU 烤机测试或启动大型 3D 基准测试，同时实时观察各核心当前频率：
```bash
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq
```

## 散热安全与硬件注意事项

> [!WARNING]
> 虽然本模块屏蔽了软件层面的温控降频策略，现代 SoC 芯片内部依然保留了硬件级高温熔断保护（通常位于 95°C–105°C 左右），以防止芯片物理烧毁。但长期处于高温状态仍会显著加速锂电池老化与鼓包风险，因此强烈建议在长时间重度游戏时搭配半导体散热背夹使用。
