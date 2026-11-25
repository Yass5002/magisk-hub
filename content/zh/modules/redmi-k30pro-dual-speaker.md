---
id: "redmi-k30pro-dual-speaker"
title: "Redmi K30 Pro 对称式双扬声器：听筒立体声改造模块"
sidebarTitle: "K30 Pro 立体声"
description: "专为 Redmi K30 Pro 与 POCO F2 Pro 设计的进阶 ALSA 混音路径与 DSP 路由模块，通过顶部听筒开启对称式立体声双扬声器输出。"
category: "audio-dsp-acoustics"
tier: 1
searchQueries:
  - "Redmi K30 Pro 双扬声器 Magisk 模块"
  - "POCO F2 Pro 立体声改双扬"
  - "K30 Pro 听筒外放模块"
  - "Redmi K30 Pro 对称双扬声器"
prerequisites:
  - "Redmi K30 Pro、K30 Pro 变焦版或 POCO F2 Pro（代号 lmi/lmipro）"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他修改供应商 ALSA 混音路径（`/system/vendor/etc/mixer_paths.xml`）的模块"
configPaths:
  - "/system/vendor/etc/mixer_paths.xml"
  - "/system/vendor/etc/mixer_paths_lmi.xml"
features:
  - "实现左声道（顶部听筒）与右声道（底部主扬声器）的真立体声分离输出"
  - "预设校准后的听筒数字增益（92 级），防止单元削波破音与硬件老化损伤"
  - "完整保留清晰稳定的通话语音路由，杜绝通话串音外泄"
  - "基于 Systemless 无系统分区修改部署，不影响后续 OTA 升级且保持 vendor 分区纯净"
faq:
  - question: "用听筒播放媒体音乐会损伤扬声器硬件吗？"
    answer: "不会。经过校准的数字增益值（92 级）完全处于听筒音圈的安全热功耗与振幅行程极限内，能够在不破音、不过热的前提下输出清晰响亮的声音。"
  - question: "刷入后接打电话是否依然保持私密听筒模式，不会外放漏音？"
    answer: "是的。混音 XML 定义文件已将多媒体播放路径与电话语音通话路由（`voice-earpiece`）彻底隔离，私人通话依然严格保持私密。"
---

## 概述

**Redmi K30 Pro Symmetric Dual Speakers**（原作者浅城墨白 Qiancheng Mobai，由 CallMeMiao 修改优化）是一款专门面向 Redmi K30 Pro 与 POCO F2 Pro（机型代号 `lmi` / `lmipro`）开发的声学优化模块。

尽管搭载了高通骁龙 865 旗舰平台，Redmi K30 Pro 出厂时仍仅配置了单颗底部扬声器。本模块通过重写高通音频 HAL 中的底层 ALSA 混音路径，将顶部听筒激活为辅助中高频声道，从而解锁均衡立体的双扬声器外放效果。

---

## 技术架构与工作原理

高通 SM8250 平台的音频子系统在开机时依赖 `/vendor/lib/hw/audio.primary.kona.so` 解析 XML 配置文件来建立声道路由：

### 1. ALSA 混音路径修改

模块在供应商文件系统上叠加挂载经过优化的 `mixer_paths.xml`：

```xml
<!-- Example stereo routing configuration -->
<path name="deep-buffer-playback">
    <ctl name="SLIM_0_RX Channels" value="Two" />
    <ctl name="SLIM_0_RX" value="SLIM_0_RX" />
    <ctl name="EAR PA Gain" value="POS_1_5_DB" />
    <ctl name="RX_EAR Digital Volume" value="92" />
</path>
```

- **声道分离**：将立体声左声道音频流路由至听筒功率放大器，右声道音频流交由底部主扬声器放大器输出。
- **增益平衡**：鉴于顶部听筒振膜尺寸小于底部扬声器音腔，数字音量缩放被精准设定为 `92`，以在避免声学失真的前提下保持左右声场响度均衡。

### 2. 音频场景隔离

补丁仅针对多媒体播放路径（`deep-buffer-playback`、`compress-offload-playback`、`multichannel-playback`）进行重映射，同时原封不动保留 `voice-call`、`voip-call` 与 `incall-rec` 的默认设置，确保语音通话不受任何干扰。

---

## 安装与验证

1. 在 Magisk、KernelSU 或 APatch 中刷入模块压缩包。
2. 重启手机使配置生效。
3. 打开 YouTube 或本地播放器播放双声道立体声测试曲目。
4. 贴近测试顶部听筒开孔与底部扬声器开孔，确认左右声道均能清晰出声且声场对称。
