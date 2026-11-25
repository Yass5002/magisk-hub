---
id: "dac-noise-floor-filter"
title: "DAC Noise Floor Filter & Stereo Fix：高敏耳机模拟底噪消除与立体声修复"
sidebarTitle: "DAC 底噪过滤"
description: "高通 ALSA 混音校准模块，消除高灵敏度入耳式耳机（IEM）在低音量播放下的背景电流底噪、接地噪声与数字底噪失真。"
category: "audio-dsp-acoustics"
tier: 1
searchQueries:
  - "DAC 底噪过滤 Magisk 模块"
  - "Android 消除耳机电流声沙沙声"
  - "mixer_paths tasha 底噪消除"
  - "低阻抗高敏耳机底噪修复 Root"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "搭载 WCD9335（Tasha）或 SKUK 音频硬件的高通骁龙设备"
conflicts:
  - "其他覆盖 `/vendor/etc/mixer_paths_tasha.xml` 的音频模块"
configPaths:
  - "/system/vendor/etc/mixer_paths_tasha.xml"
  - "/system/vendor/etc/mixer_paths_skuk.xml"
  - "/system/vendor/etc/mixer_paths_qvr.xml"
features:
  - "重新校准高通音频编解码器的模拟耳机功放增益级（HPHL 与 HPHR）"
  - "抑制静音间隙及低音量播放时可闻的静态电流底噪（沙沙声）"
  - "针对高灵敏度入耳式监听耳机（如多单元动铁 IEM）优化数模转换器（DAC）动态范围"
  - "恢复 3.5mm 有线输出接口出厂级硬件立体声串音隔离与声道分离度"
  - "零数字压缩与零频响裁剪：完整保留全频段原汁原味的音频响应"
faq:
  - question: "为什么高灵敏度耳机在某些 Android 手机上会出现明显底噪？"
    answer: "高灵敏度入耳式耳机（阻抗 16 欧姆及以下且灵敏度高于 110dB SPL/mW 的 IEM）极易暴露移动端音频电路的硬件本底噪声。当 OEM 音频驱动将模拟耳机功率放大器（HPH PA）固定在过高的静态增益、仅靠软件层面衰减音量时，功放会持续放大电路热噪声与接地电流噪声。"
  - question: "刷入该模块后耳机的最大音量会变小吗？"
    answer: "模块通过压低静态模拟功放底噪、同时拉高纯净数字动态余量（Headroom）来优化整体增益结构。输出依然保有充足响度，同时确保曲目之间的静默间隙完全漆黑纯净、无电流底噪。"
---

## 概述

**DAC Noise Floor Filter & Stereo Fix**（由 FK 制作）旨在解决高通骁龙智能手机上一个常见却颇具困扰的音频异常问题：当使用高灵敏度有线耳机聆听时，持续出现的背景电流底噪、接地环路电磁干扰以及过高的硬件本底噪声。

使用多单元动铁（BA）入耳式监听耳机或低阻抗动圈 IEM 的音频发烧友经常反馈，每当应用请求音频焦点时——即便音乐处于暂停状态——耳机里仍能听到明显的“海浪声”或持续的电流沙沙声。这一现象源于 OEM 厂商在混音路径配置中将模拟耳机功放（`HPHL`/`HPHR`）的基础增益设置过高，转而依赖下游软件数字衰减来调节音量。

本模块替换高通 WCD9335（代号“Tasha”）及 SKUK 音频编解码器的原厂混音路径定义，重新校准模拟增益结构，在保留真实立体声结像的同时，将底噪压低至人耳听阈之下。

---

## 技术架构与工作原理

本模块作用于 `/vendor/etc/` 目录下的核心 ALSA 混音路径配置文件：
- `mixer_paths_tasha.xml`
- `mixer_paths_skuk.xml`
- `mixer_paths_qvr.xml`

### 1. 模拟功放底噪抑制

原厂默认配置通常会将耳机功放寄存器（`HPHL Volume` 与 `HPHR Volume`）维持在 `15` 或 `20` 等较高数值，从而放大了内部 DAC 走线产生的约翰逊-奈奎斯特热噪声（Johnson-Nyquist noise）。

模块对这些模拟寄存器进行如下调整：

```xml
<!-- Optimized Headphone Power Amplifier (HPH) Gain Staging -->
<ctl name="HPHL Volume" value="9" />
<ctl name="HPHR Volume" value="9" />

<!-- Digital Headroom Optimization -->
<ctl name="RX1 Digital Volume" value="84" />
<ctl name="RX2 Digital Volume" value="84" />
```

通过降低模拟端增益倍率并采用纯净的高分辨率数字音量驱动信号，电路的信噪比（SNR）得以显著提升。

### 2. 立体声声道隔离

部分 OEM 系统更新会意外在 `mixer_paths.xml` 中引入单声道混音或失衡的立体声串音补偿。本模块显式恢复了 `SLIM RX1` 与 `SLIM RX2` 通道之间的独立左右声道路由，重新还原开阔的声场空间感与精准的乐器定位分离度。

---

## 兼容性与验证方法

- **支持硬件**：搭载高通骁龙 820、821、835、845 及配备 WCD9335 或兼容高通音频编解码器的相关平台设备。
- **效果验证**：插入高灵敏度有线耳机，将音量调至 10% 并暂停播放。安装模块前存在的背景沙沙底噪此时应已被彻底消除。
