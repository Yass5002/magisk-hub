---
id: "nlsound-module-qcom"
title: "NLSound（高通骁龙版）：系统级高解析音频与麦克风优化引擎"
sidebarTitle: "NLSound（高通版）"
description: "专为高通骁龙设备打造的无系统分区修改音频引擎，提供 DIRECT_PCM 直通模式、tinymix 硬件混音器调校、ACDB 校准及麦克风增益优化。"
category: "system-utilities"
tier: 1
searchQueries:
  - "NLSound 高通 Magisk 模块"
  - "NLSound Briclyaz GitHub 下载"
  - "Android Root DIRECT_PCM 独占直通"
  - "高通 tinymix 硬件音量增益调音"
  - "Magisk ACDB 音频校准补丁"
prerequisites:
  - "高通骁龙处理器（骁龙 625 / MSM8953 及以上型号）"
  - "已获取 Root 权限的 Android 设备"
  - "Magisk、KernelSU 或 APatch"
conflicts:
  - "会无差别覆盖高通音频 HAL 配置或 ALSA 混音器路径的通用全局音效修改模块"
configPaths:
  - "/data/adb/modules/NLSound/"
features:
  - "DIRECT_PCM 音频通路：启用位精确（Bit-Perfect）PCM 音频流传输，消除多余的软件重采样并降低播放延迟"
  - "采样率与位深锁定：支持从标准 16-bit / 48 kHz 到 32-bit 浮点 / 384 kHz 的多档输出配置"
  - "tinymix 硬件混音器集成：精细调校内置 DAC 寄存器、硬件音量步进间隔与模拟放大器增益级"
  - "麦克风录音修复：提升拾音灵敏度，并禁用容易导致失真的压限器（Compander）与激进限幅器"
  - "ACDB（音频校准数据库）补丁：解析并修改厂商专有 ACDB 二进制文件，解除 OEM 响度压制限制"
---

## 概述

由 Briclyaz 与 NLSound Team 开发的 **NLSound 高通版** 是一款专为高通骁龙平台设备打造的高级音频增强模块。与仅在原生 Android 音频服务之上叠加软件 EQ 滤镜的普通均衡器方案不同，NLSound 直接作用于 HAL（硬件抽象层）、ALSA 驱动以及 DSP 校准层级。

通过对接高通专有的 ACDB（Audio Calibration Database，音频校准数据库）结构与 `tinymix` ALSA 底层工具，NLSound 有效解决了智能手机长期存在的音频痛点：嘈杂环境下麦克风拾音发闷、激进的动态范围压缩（压限器）、人为限制的音量调节步数，以及有线与蓝牙音频输出的高延迟问题。

## 前置要求与兼容性

运行 NLSound 高通版前，设备需满足以下技术条件：

1. **系统芯片（SoC）**：搭载高通骁龙处理器，最低要求骁龙 625（MSM8953）或更新型号。本构建版本不支持联发科（MediaTek）、三星 Exynos、紫光展锐（Unisoc）或 Google Tensor 平台设备。
2. **Root 管理器**：Magisk、KernelSU 或 APatch。
3. **Android 版本**：支持采用标准高通音频 HAL 实现的现代 Android 系统版本。

### 冲突与兼容性说明

尽管 NLSound 对第三方音频系统具备良好的兼容处理机制（包括对 Dolby Atmos 配置进行智能打补丁，以及屏蔽 MusicFX 或 AudioFX 等冗余音效组件），但如果同时运行多个会激进修改同一套 ALSA 混音器路径（`mixer_paths.xml`）的音频模块，仍可能导致设备无声或通话音频异常。建议在叠加其他 DSP 音效模块前，先在纯净环境下测试音频播放是否正常。

## 架构与音频特性

NLSound 实现了多项底层音频链路优化：

- **DIRECT_PCM 通路**：在使用兼容的音频播放器时绕过默认的 Android AudioFlinger 软件混音器，将位精确音频流直接输出至高通硬件解码器。
- **硬件寄存器校准**：调用 `tinymix` 直接控制高通音频编解码器（如 WCD93xx 系列）中的模拟增益节点，在提升最大纯净输出音量的同时防止数字削波失真。
- **移除限幅器与压限器**：剥离硬编码的音频压缩算法，解决音乐动态范围被压缩以及录像时音量忽大忽小的问题。
- **精细音量步进**：将生硬的 15 级媒体音量滑块替换为更细腻的多级步进控制，方便搭配高灵敏度入耳式监听耳机（IEM）进行低音量微调。

## 配置与使用

通过 Root 管理器的模块安装界面即可部署 NLSound：

1. 在 Magisk、KernelSU 或 APatch 中刷入发布包（`NLSound.*.Qualcomm.Devices.zip`）。
2. 安装向导会引导你选择各项音频参数（例如音量增益等级、首选采样率与麦克风灵敏度）。
3. 若需无人值守部署，NLSound 也支持在安装前预先放置配置文件清单进行自动读取。
4. 生效的模块资源与持久化配置均位于：
   ```bash
   /data/adb/modules/NLSound/
   ```

## 故障排查与验证

- **麦克风无声或通话失真**：若麦克风无法录音或在通话时出现破音削波，请重新刷入模块并在安装向导中选择更低一档的麦克风增益倍率。
- **蓝牙耳机播放卡顿爆音**：若高解析音频流在蓝牙传输时发生丢包，请确认开发者选项中的蓝牙音频设置与耳机实际支持的编码规格匹配（例如 LDAC / aptX HD 24-bit / 96 kHz）。
- **系统 OTA 更新后音效失效**：Android 系统升级通常会重新覆盖厂商音频配置文件。若 OTA 更新后音质恢复为原厂默认状态，重新刷入 NLSound 即可再次应用 ACDB 与混音器补丁。
