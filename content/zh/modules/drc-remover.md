---
id: "drc-remover"
title: "DRC Remover：解除高通骁龙 Android 设备的音频动态范围压缩"
sidebarTitle: "DRC Remover"
description: "通过修改厂商音频策略 XML 配置，禁用扬声器、3.5mm 耳机孔、蓝牙与 USB DAC 输出通路上的强行动态范围控制（DRC）压缩滤镜。"
category: "system-utilities"
tier: 1
searchQueries:
  - "DRC Remover Magisk 模块下载"
  - "zyhk drc-remover 模块"
  - "Android 关闭 speaker_drc_enabled"
  - "高通骁龙禁用音频动态压缩 Root"
  - "Magisk 移除系统音频压限器"
prerequisites:
  - "Android 10 至 Android 14"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "原厂固件启用了 DRC 压缩的设备（主要为高通骁龙 SDM 与 SM 系列芯片平台）"
conflicts:
  - "audio-samplerate-changer（已内置相同的 DRC 移除逻辑）"
configPaths:
  - "/data/adb/modules/drc-remover/"
  - "/data/adb/modules/drc-remover/system/vendor/etc/"
features:
  - "策略文件自动检测：识别厂商音频配置文件中是否启用了 DRC 压缩"
  - "精准 XML 修补：将所有硬件输出通路中的 speaker_drc_enabled='true' 替换为 'false'"
  - "全通道输出覆盖：同时解除内置扬声器、3.5mm 有线模拟输出、蓝牙 A2DP 及 USB DAC 上的动态压缩"
  - "零音频延迟开销：仅作用于厂商 XML 声明文件，不运行任何常驻后台守护进程"
faq: []
---

## 概述

动态范围控制（Dynamic Range Control，简称 DRC）是一种音频 DSP 算法，通过抬高微弱声音并强力衰减瞬态音量峰值来压缩声学动态范围。尽管该机制有助于防止智能手机小型低功率扬声器破音，但许多厂商（尤其是高通骁龙 SDM 与 SM 系列芯片平台）会将其强制施加到 **全部** 音频管线上——包括外接 USB DAC、高保真蓝牙编解码器以及 3.5mm 耳机接口。

启用 DRC 后，音乐段落会丧失冲击力，交响乐渐强段落听感扁平，高阻抗耳机也会显得局促受限。由于该压缩处理发生在音频离开 Android 混音引擎之前的厂商音频 HAL 层，第三方播放器软件无法绕过。

由 zyhk 开发的 **DRC Remover** 会定位设备当前生效的厂商音频策略配置文件，关闭硬件压缩开关，并以无系统分区修改（Systemless）方式挂载修正后的配置。

## 工作原理

在模块初始化及安装阶段：

1. **硬件配置巡检**：扫描 `/vendor/etc/` 与 `/vendor/etc/audio/` 目录，查找当前激活的音频策略描述文件（如 `audio_policy_configuration.xml`、`audio_policy_configuration_a2dp_offload_disabled.xml` 等）。
2. **条件触发判定**：检查文件中是否声明了 `speaker_drc_enabled="true"`。若 OEM 固件默认已关闭 DRC（常见于联发科 SoC 设备），安装脚本会提示状态正常并直接退出，不做多余修改。
3. **XML 属性替换**：将生效的策略 XML 复制到 `$MODDIR/system/vendor/...` 目录并修改对应布尔属性：
   ```xml
   <!-- Stock Qualcomm Configuration -->
   <globalConfiguration speaker_drc_enabled="true"/>

   <!-- DRC Remover Patched Configuration -->
   <globalConfiguration speaker_drc_enabled="false"/>
   ```
4. **Systemless 挂载**：在系统启动时将修补后的 XML 直接覆盖挂载至 vendor 分区对应路径。

## 重要使用注意事项

- **A2DP 硬件卸载开关变更**：如果在开发者选项中更改了会切换生效音频配置文件的设置（例如开启或关闭“停用蓝牙 A2DP 硬件卸载”），必须重新刷入或更新 DRC Remover，使其重新定位并修补当前生效的 XML 文件。
- **第三方类原生 ROM 属性反转**：极少数第三方定制 ROM 在其自定义 HAL 代码树中反转了 `speaker_drc_enabled` 的程序语义。若所用 ROM 明确要求反转标识，请谨慎试听并对比输出动态表现。
- **明确冲突提示**：切勿与 **Audio Samplerate Changer**（`audio-samplerate-changer`）同时安装，该模块已在安装流程中完整内置了相同的 DRC 移除逻辑。

## 安装与验证

1. 下载并在 Magisk 或 KernelSU 中刷入 `drc-remover` `.zip` 压缩包。
2. 查看刷入日志输出，确认脚本已检测到并成功修补生效的 DRC 策略文件。
3. 重启设备。
4. 验证修补后的配置是否已成功挂载：
   ```bash
   su -c grep "speaker_drc_enabled" /vendor/etc/audio_policy_configuration.xml
   ```
   终端输出应显示 `speaker_drc_enabled="false"`。
