---
id: "hifi-maximizer-mod"
title: "Hi-Fi Maximizer：低频数字音频抖动抑制与内核调优模块"
sidebarTitle: "Hi-Fi Maximizer"
description: "由 zyhk 开发的发烧友级内核与子系统优化模块，通过锁定内核调度器及停用后台干扰服务，最大限度降低 USB DAC、蓝牙 A2DP 与 DLNA 输出的数字音频流抖动。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Hi-Fi Maximizer Magisk 模块"
  - "yzyhk904 hifi-maximizer-mod 下载"
  - "Android 降低音频抖动优化"
  - "禁用 thermal-engine 改善音质"
  - "Magisk 发烧级音频内核调优"
prerequisites:
  - "已通过 Magisk 获取 Root 权限的 Android 设备"
  - "高解析度音频回放硬件（USB DAC、蓝牙 LDAC/A2DP 接收器或专业数字音频播放器 DAP）"
conflicts:
  - "尝试在息屏听歌期间强制对 CPU 降频的同类性能调度或省电模块"
configPaths:
  - "/data/adb/modules/hifi-maximizer-mod/"
features:
  - "50Hz 以下低频抖动抑制：专门消除会通过锁相环（PLL）干扰 DAC 主时钟的长周期数据速率波动"
  - "性能调度器锁定：将 CPU 与 GPU 调度器固定为 performance 模式，防止频率切换引发音频缓冲区欠载"
  - "温控守护进程压制：终止会引入调度抖动的 OEM 温控降频进程（`thermald`、`mi_thermald`、`thermal-engine`）"
  - "音效处理链中和：干净绕过 `audio_effects.xml`，消除厂商均衡器与虚拟环绕声带来的失真"
  - "动态范围控制（DRC）禁用：修改音频策略 XML 文件以移除硬件级动态范围压缩"
faq: []
---

## 概述

由音频研究者 `zyhk` 打造的 **Hi-Fi Maximizer** 是一款专为已 Root 的 Android 智能手机与数字音频播放器（DAP）设计的硬核发烧级调优模块。尽管移动音频发烧友常将音质欠佳归因于模拟放大电路，但研究表明，极易被忽视的元凶是低频数字音频抖动（50 Hz 以下波动，即周期长于 20 毫秒的时序起伏）。

高频抖动可轻易被现代数模转换器（DAC）内部的锁相环（PLL）硬件滤除；然而，由激进 CPU 调频、Android Doze 休眠周期、Wi-Fi 轮询突发以及温控守护进程干预引发的 10 Hz 以下超低频抖动，会直接调制 DAC 主时钟，产生细微的互调失真与模糊的声场结像。Hi-Fi Maximizer 通过内核与服务层调优彻底消除这些抖动源。

## 前置条件与兼容性

- **Root 环境**：Magisk（正式版或 Canary 版）。
- **目标音频链路**：外接 USB DAC（同步、自适应及异步模式均适用）、高端蓝牙 LDAC/A2DP 耳机以及高保真 3.5mm DAC 输出。
- **Android 版本**：已在 AOSP、LineageOS、crDroid 及多款 OEM 原厂系统上完成广泛测试。

### 冲突说明

由于 Hi-Fi Maximizer 会将 CPU 调度器锁定至高性能状态并在播放期间禁用 Android Doze，切勿与激进省电模块或同类 CPU 调度微调模块混用。该模块的设计取向是优先保障音频时钟稳定性，而非电池续航。

## 核心技术优化项

### 1. 内核调度器与 I/O 锁定
- 将 CPU 与 GPU 频率调度器设为 `performance` 模式。
- 将 Linux I/O 调度器切换为 `deadline`（或 `cfq`），降低存储访问延迟。
- 将虚拟内存 `swappiness` 调整为 `0%` 并启用 laptop mode，最大限度减少后台磁盘抖动。
- 禁用联发科 EAS+ 调度例程（`/proc/cpufreq/cpufreq_sched_disable`）。

### 2. 音频管线与音效链中和
- 通过中和 `/vendor/etc/audio_effects.xml` 禁用厂商音效处理链，绕过冗余的后期数字处理算法。
- 在 `audio_policy_configuration.xml` 中关闭 OEM 动态范围控制（DRC），还原自然动态范围。
- 在 Google Tensor 与高通设备上绕过 Android 13+ 内置空间音频管线，避免额外重采样与混音通道处理。

### 3. 后台服务与传感器静默
- 终止后台温控守护进程（`thermal-engine`、`mi_thermald`、`thermald`）。
- 停用会在播放期间频繁唤醒 CPU 的 `camera server`、`logd`、`traced` 与 `traced_probes` 服务。
- 禁用高通 MPDecision CPU 热插拔机制，避免核心切换带来瞬时脉冲干扰。

## 配置与使用

1. 通过 Magisk Manager 刷入 `magisk-hifi-maximizer-mod-*.zip` 发布包。
2. 重启设备。
3. 插入 USB DAC 或连接蓝牙耳机。
4. 生效的模块资源位于：
   ```bash
   /data/adb/modules/hifi-maximizer-mod/
   ```

## 故障排查与注意事项

- **耗电增加**：由于 CPU 核心保持稳态高频率且 Doze 被禁用，息屏播放音乐时的电池消耗会明显升高。这是为换取无抖动数字音频流而有意采用的设计策略。
- **机身发热**：在温控降频服务被压制的情况下，播放音乐时请避免同时运行大型 3D 游戏或进行高功率快充。
