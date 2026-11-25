---
id: "audio-samplerate-changer"
title: "Audio Samplerate Changer：全局 Hi-Fi 混音器与 768kHz USB 音频优化"
sidebarTitle: "Audio Samplerate Changer"
description: "自动化音频引擎，可将 Android 全局混音器采样率提升至最高 768kHz/32-bit，将 USB 传输抖动缩减至 2000µs，并优化蓝牙编解码同步。"
category: "system-utilities"
tier: 1
searchQueries:
  - "audio samplerate changer magisk 模块"
  - "zyhk audio samplerate changer"
  - "安卓 768khz 32bit usb 音频 root"
  - "android audio policy 7.0 混音采样率"
  - "降低 usb 音频抖动 magisk"
prerequisites:
  - "运行 7.0 版本 Audio Policy XML 配置的 Android 14 至 Android 16 系统"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "高通骁龙、联发科或 Google Tensor 芯片平台"
conflicts:
  - "drc-remover（本模块已原生集成该功能）"
  - "usb-samplerate-unlocker（本模块已原生集成该功能）"
  - "纯 AIDL 音频 HAL 设备（如 Google Pixel 9 系列）"
configPaths:
  - "/data/adb/modules/audio-samplerate-changer/"
  - "/data/adb/modules/audio-samplerate-changer/system/vendor/etc/"
features:
  - "突破 USB HAL 频率上限：自动解锁 USB DAC 输出至最高 768kHz / 32-bit（Google Tensor 设备上限为 192kHz/32-bit）"
  - "低抖动 USB 缓冲区调优：将 USB 音频数据传输间隔从 5000µs 降至 2000µs，大幅抑制声学抖动"
  - "蓝牙编码动态匹配：将 AOSP 蓝牙采样率直接同步至当前无线编码（LDAC、aptX HD），消除二次重采样"
  - "扬声器 DAC 解锁：在高通平台上将内置扬声器混音管线提升至 384kHz（其他平台为 48kHz）"
  - "集成 DRC 移除与 HAL 精简：去除动态范围控制（DRC）并禁用通话筛选音频框架，降低处理延迟"
faq: []
---

## 概述

默认情况下，Android 系统混音器采用一套以降低低功耗扬声器耗电为优先目标的折中音频管线，而非追求真正的高保真音质。即使使用专业 Hi-Fi 播放器，高解析度音频流仍会被迫经历粗糙的重采样、引发抖动的 5000µs USB 缓冲周期，以及厂商内置的动态范围控制（DRC）压缩滤波。

由 zyhk 开发的 **Audio Samplerate Changer** 彻底改造了 Android 全局音频混音器。该模块将作者广受好评的“USB SampleRate Changer”Root 脚本自动化，直接修改生效中的 7.0 版本 Audio Policy 配置，将 USB Audio Class HAL 驱动上限提升至 768kHz/32-bit，消除冗余蓝牙重采样阶段，并微调内核 I/O 参数以压低抖动。

## 架构级改进

### 1. USB HAL 与抖动抑制
- **768kHz 与 32-Bit USB 管线**：将 USB Audio Class 驱动的硬件通信上限提升至 768kHz（Google Tensor SoC 为防止硬件缓冲区溢出而限制在 192kHz）。
- **2000µs 传输周期**：将标准的 5000µs USB 数据包间隔缩减至 2000µs。更紧凑的时间窗口能显著抑制手机 USB 控制器与异步 DAC 时钟之间的相位时序抖动。

### 2. 智能蓝牙编解码同步
标准 Android 蓝牙音频栈在解码高解析无线流后，常会再次经过中间混音重采样器。Audio Samplerate Changer 将 AOSP 蓝牙音频驱动直接锁定至当前编解码器的原生频率（例如 Sony LDAC 的 96kHz），彻底消除破坏音质的二次重采样失真。

### 3. 集成 DRC 抑制与内置扬声器输出
- **全面移除 DRC**：在所有输出端禁用厂商动态范围控制（Dynamic Range Control），保留音乐的动态峰值与自然余韵。
- **内置扬声器混音提升**：将高通平台内置扬声器管线采样率提升至 384kHz / 32-bit，降低音频 DSP 中的谐波失真。
- **停用通话筛选钩子**：禁用音频 HAL 下的后台通话筛选（Call Screening）Hook，释放实时音频执行线程。

## 兼容性与冲突说明

- **支持固件**：专为采用标准 **7.0 Audio Policy Configuration** XML 架构的 Android 14、15 及 16 系统设计。
- **不支持的硬件**：较新的纯 AIDL 音频 HAL 固件实现（如 Google Pixel 9 系列）不再使用 7.0 XML 策略文件，因此不兼容本模块。
- **明确冲突**：
  - **切勿**与 **`drc-remover`** 或 **`usb-samplerate-unlocker`** 同时安装，这两款独立模块的功能已直接集成于本安装包内。

## 发烧友推荐设置

为获得最佳声场表现与 Bit 级透明传输：
1. **停用绝对音量**：打开 **设置** → **开发者选项**，开启 **停用绝对音量功能**。
2. **最大化硬件输出**：将手机端的蓝牙或 DAC 音量调至最大，改用耳放或耳机自身的硬件旋钮调节实际听音音量。
3. *（可选）* 可搭配 **Audio Misc. Settings** 或 **Audio Jitter Silencer** 等同类音频模块协同使用。

## 效果验证

如需确认音频混音器是否已按高采样率输出，可执行以下命令排查：

```bash
# Check USB DAC active hardware sample rate during playback
su -c cat /proc/asound/card*/pcm*p/sub*/hw_params

# Check active Android audio flinger tracks and sink sample rates
su -c dumpsys media.audio_flinger
```
在输出中查找对应 USB 或蓝牙设备的活动输出线程（Output Thread），其显示的采样率与位深应已解除限制。
