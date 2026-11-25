---
id: "usb-samplerate-unlocker"
title: "USB Samplerate Unlocker：为 Android USB DAC 解锁 192kHz、384kHz 与 768kHz 音频输出"
sidebarTitle: "USB Samplerate Unlocker"
description: "通过二进制修补厂商 ALSA 工具动态链接库，突破 Android 默认 96kHz USB 音频 HAL 上限，实现更高规格的无损音频输出。"
category: "system-utilities"
tier: 1
searchQueries:
  - "USB Samplerate Unlocker Magisk 模块"
  - "安卓 USB 小尾巴突破 96kHz 采样率"
  - "zyhk usb-samplerate-unlocker 下载"
  - "Android 修补 libalsautils 解锁 384kHz"
  - "Magisk 高解析度 USB 音频直出"
prerequisites:
  - "Android 10 至 Android 14 系统"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "支持 192kHz、384kHz 或 768kHz PCM 播放的外接 USB DAC 解码器"
conflicts:
  - "audio-samplerate-changer（已原生集成该模块的修补逻辑）"
configPaths:
  - "/data/adb/modules/usb-samplerate-unlocker/post-fs-data.sh"
  - "/data/adb/modules/usb-samplerate-unlocker/system/vendor/"
features:
  - "动态 ALSA 库二进制修补：设备开机时自动提取并原地修改 `libalsautils.so` 与 `libalsautils_v2.so`"
  - "多档采样率解锁：将原厂 96kHz 硬件采样率查找表替换为 192kHz、384kHz 或 768kHz 配置文件"
  - "Google Tensor 平台专项优化：针对 Tensor SoC 修补厂商 `audio_platform_configuration.xml`，将 USB 卸载直通上限从 96kHz 提升至 192kHz"
  - "可定制 `post-fs-data` 运行档位：自由切换 `default`（192kHz）、`full`（384kHz）与 `max`（768kHz）三种上限模式"
---

## 概述

现代流媒体音乐平台（如 Tidal、Apple Music、Qobuz）已广泛提供 192kHz 及以上采样率的无损母带音频。然而，标准 Android USB 音频硬件抽象层（HAL，即 `libalsautils.so`）在代码中将支持的采样率数组（`std_sample_rates[]`）硬编码限制在最高 96kHz。即便音频发烧友外接了支持 384kHz 甚至 768kHz 解码的高端 USB DAC，Android 系统仍会强制将超过 96,000 Hz 的音频流重采样降频输出。

由 zyhk 开发的 **USB Samplerate Unlocker** 无需重新编译自定义内核即可打破这一限制。该模块会在开机早期阶段提取设备当前生效的厂商 ALSA 工具二进制文件，定位十六进制采样率数组签名并原地修改表项数值，随后通过无侵入式挂载覆盖原厂库文件。

## 二进制修补机制原理

模块核心逻辑在系统启动的 `post-fs-data` 阶段自动执行：

1. **库文件提取**：扫描 `/vendor/lib/` 与 `/vendor/lib64/` 目录，定位当前设备中存在的 `libalsautils.so` 及 `libalsautils_v2.so`。
2. **反汇编特征检索**：将二进制内容读入临时内存缓冲区，检索原厂采样率数组的字节特征签名：
   ```c
   std_sample_rates[] = {96000, 88200, 192000, 176400, 48000, 44100, 32000, 24000, 22050, 16000, 12000, 11025, 8000}
   ```
3. **数组重排与注入**：依据所选配置档位重新构造数组序列：
   - **`default`（192kHz）**：在 `96000` 之前插入 `{192000, 176400}`。
   - **`full`（384kHz）**：在头部插入 `{384000, 352800, 192000, 176400}`。
   - **`max`（768kHz）**：在头部插入 `{768000, 705600, 384000, 352800, 192000, 176400}`。
4. **Tensor 平台专项覆盖**：针对 Google Tensor 设备（Pixel 6 至 Pixel 8 系列），同步重写 `/vendor/etc/audio_platform_configuration.xml`，将 USB 音频卸载流（Offload）定义提升至 192kHz。
5. **无侵入挂载**：将修补后的 `.so` 二进制文件重构至 `$MODDIR/system/vendor/{lib,lib64}/`，在启动时接管原厂 vendor 分区文件。

## 运行模式与配置

模块安装后默认启用 **`full`（384kHz）** 档位，该规格在绝大多数高速 USB 控制器上既能发挥极致解析力，又能避免音频抖动（Jitter）。

若你的特定 DAC 或手机 USB 控制器在 384kHz 下出现爆音或卡顿，可手动将采样率上限调低至 192kHz：

1. 使用 Root 文件管理器或终端打开 `/data/adb/modules/usb-samplerate-unlocker/post-fs-data.sh`。
2. 找到修补模式参数：
   - 将 `full` 修改为 `default`（上限锁定为 192kHz）。
   - 若使用超高端桌面级 DAC 且总线缓冲稳定，也可将 `full` 修改为 `max`（解锁 768kHz）。
3. 保存文件并重启设备即可生效。

## 兼容性与冲突说明

- **Android 版本**：已在搭载高通、联发科与 Google Tensor SoC 的 Android 10、11、12、13 及 14 设备上经过广泛实测。
- **明确冲突**：切勿与 **Audio Samplerate Changer**（`audio-samplerate-changer`）同时刷入。后者已完整包含本模块的修补脚本并附加了全局系统混音器（Mixer）覆盖逻辑，叠加安装会在 `post-fs-data.sh` 阶段引发竞态冲突。

## 验证方法

如需确认 ALSA 音频子系统是否已实际按更高采样率完成硬件握手：

1. 连接外置 USB DAC 并开始播放高解析度无损音乐。
2. 在 Termux 或 ADB Shell 中执行以下命令查看实时音频流参数：
   ```bash
   su -c cat /proc/asound/card*/pcm*p/sub*/hw_params
   ```
3. 观察输出的 `rate:` 字段；正常情况下应显示音轨的原生采样率（例如 `rate: 192000 (192000/1)` 或 `rate: 384000 (384000/1)`），而不再被强制降频为 `96000`。
