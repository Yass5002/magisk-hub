---
id: "earpiece-stereo-volume-boost"
title: "Earpiece Stereo & Volume Boost：听筒双扬声器模拟与 ALSA 混音增益增强"
sidebarTitle: "听筒双扬声器"
description: "通过重配 ALSA 混音路径将前置通话听筒复用为副扬声器，并提升硬件功率放大器增益级以增强外放与通话音量。"
category: "audio-dsp-acoustics"
tier: 1
searchQueries:
  - "听筒双扬声器 Magisk 模块"
  - "Android 单扬声器改双扬声器"
  - "mixer_paths 音量放大教程"
  - "EAR PA Gain 听筒增益模块"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "使用 ALSA mixer_paths.xml 的高通骁龙设备"
conflicts:
  - "其他直接替换 `/vendor/etc/mixer_paths.xml` 的音频模块"
configPaths:
  - "/system/vendor/etc/mixer_paths.xml"
  - "/system/vendor/etc/mixer_paths_overlay_static.xml"
features:
  - "将左声道媒体音频路由至前置通话听筒扬声器发声"
  - "在仅有单底部扬声器的机型上生成双扬声器立体声空间分离效果"
  - "将 EAR PA Gain（功率放大器）寄存器提升至正分贝值（POS_1P5_DB）"
  - "拉高数字音量寄存器（RX1 与 RX2 Digital Volume），改善通话听筒声音过小问题"
  - "严格区分私密语音通话与公开媒体外放的声学配置文件"
faq:
  - question: "用听筒播放媒体音频会损坏扬声器硬件吗？"
    answer: "通话听筒主要针对语音频段（300Hz–3.4kHz）设计，音圈尺寸小于专用的底部外放扬声器。尽管本模块在厂商安全功率容限内稳妥提升了增益，但仍不建议长时间以最大音量播放重低音或严重失真的音频，以延长单元使用寿命。"
  - question: "开启后接听私人电话时旁人会听到通话内容吗？"
    answer: "不会。混音路径文件对通话专用的 `earpiece` 路径与媒体外放用的 `speaker-and-earpiece` 路径做了严格隔离。日常语音通话仍会保持私密、正常的听筒音量输出。"
---

## 概述

**Earpiece Stereo & Volume Boost**（由 Stir-Fried Pufferfish 制作）是一款声学增强模块，无需改动任何物理硬件，即可将单扬声器 Android 手机改造为双声道立体声外放系统。

许多中端机型与早期旗舰手机仅配备一颗底部扬声器用于播放音乐、视频和游戏音效，而前置听筒在媒体播放时始终处于闲置状态。通过重新配置设备的高级 Linux 声音架构（ALSA）混音路径，该模块控制高通音频编解码器将左声道音频路由至前置听筒发声单元，同时将右声道交由底部主扬声器输出。

与此同时，模块还会重新校准模拟功率放大器与数字增益寄存器，彻底改善通话声音偏小的问题，并提供充沛的外放声学动态余量。

---

## 技术架构与工作原理

Android 音频驱动通过存储在 `/vendor/etc/mixer_paths.xml` 中的 XML 混音定义文件与硬件编解码器（如高通 WCD93xx 或 PMIC 音频编解码器）进行交互。

### 1. 双声道路由控制

当媒体播放启动时，Android 会调用 `speaker` 音频路径。本模块拦截并改写该路径定义，同步激活上下两套发声电路：

```xml
<!-- Modified Speaker Path with Simultaneous Earpiece Routing -->
<path name="speaker">
    <path name="earpiece" />
    <ctl name="SLIM RX0 MUX" value="AIF_MIX1_PB" />
    <ctl name="EAR PA Gain" value="POS_1P5_DB" />
    <ctl name="EAR PA Boost" value="ENABLE" />
</path>
```

### 2. 增益级校准

为确保尺寸较小的听筒音圈在与高功率底部扬声器同时发声时清晰可闻且不发生破音，模块对模拟与数字两级增益进行了联合调校：

- **模拟功率放大器（EAR PA）**：从默认的负衰减（如 `-1.5dB`）调整为正增益（`+1.5dB`）。
- **数字 DAC 音量（RX Digital Volume）**：同步提升 `RX1` 与 `RX2` 寄存器数值，在数模转换前进一步优化信噪比。

---

## 兼容性与恢复方法

由于该模块采用高通硬件平台通用的标准 ALSA 控制标识符，因此可在数十款骁龙芯片机型上稳定运行。

如需立即恢复出厂默认音频路由与原厂音量设定，只需在 Root 管理器中禁用本模块并重启手机即可。
