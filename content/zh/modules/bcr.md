---
id: "bcr"
title: "BCR：Basic Call Recorder（无损本地系统级通话录音）"
sidebarTitle: "BCR"
description: "零依赖开源原生通话录音模块，直接从 Android 音频 HAL 捕获未压缩的双向通话语音流。"
category: "system-utilities"
tier: 1
searchQueries:
  - "bcr basic call recorder magisk 下载"
  - "安卓 root 双向通话录音模块"
  - "chenxiaolong bcr 通话录音"
  - "android 无损通话内录模块"
  - "bcr 通话录音设置指南"
prerequisites:
  - "Android 10.0 至 Android 15"
  - "Magisk、KernelSU 或 APatch（若授予直接系统权限也可作为普通 APK 安装）"
conflicts:
  - "基于无障碍服务的第三方通话录音应用（会引发音频焦点冲突）"
configPaths:
  - "/data/media/0/CallRecordings/"
  - "/data/adb/modules/bcr/"
features:
  - "直接捕获双向语音流（以纯净硬件音质同时录下己方与对方通话声音）"
  - "支持多种输出格式：FLAC（无损）、Opus、AAC 与 WAV"
  - "自动文件归档与自定义文件名模板（联系人姓名、号码、日期、通话时长）"
  - "100% 纯离线隐私保护：无联网权限、无统计遥测、无云端上传"
faq:
  - question: "为什么免 Root 通话录音应用只能录到我的声音，录不到对方的声音？"
    answer: "自 Android 10 起，Google 彻底封禁了普通应用访问通话上行与下行音频流的权限。第三方应用只能尝试通过麦克风去收听听筒外放，导致对方声音微弱且模糊。BCR 则利用无侵入式 Root 特权，在音频送达扬声器之前直接从电话音频 HAL 捕获原始语音流。"
  - question: "录制的通话音频保存在哪里？"
    answer: "默认情况下，BCR 会将录音文件保存在内部存储的 CallRecordings/ 目录下，你可以使用任意标准 Android 文件管理器查看。"
---

## 概述

由 **chenxiaolong** 开发的 **BCR**（Basic Call Recorder）被广泛公认为 Android 平台上最稳定、纯净且省电的通话录音解决方案。

受限于隐私政策及近年来 Android 版本中 Google 收紧的 API 限制，未 Root 设备通常无法直接录制通话内部音频流。BCR 通过以系统特权组件方式运行解决了这一限制：它向底层 Android 电话框架注册监听，直接从硬件混音器捕获通话双方的未压缩数字音频流。

---

## 技术架构与工作原理

### 原生电话框架音频捕获

1. **特权级安装**：以 Magisk / KernelSU 模块形式安装时，BCR 会将辅助组件挂载至 `/system/priv-app/`，并在 `/system/etc/permissions/privapp-permissions-bcr.xml` 中注入所需特权声明。
2. **音频录制源**：BCR 调用系统特权音频源常量：
   - `MediaRecorder.AudioSource.VOICE_CALL`
   - `MediaRecorder.AudioSource.VOICE_UPLINK`（己方麦克风输入）
   - `MediaRecorder.AudioSource.VOICE_DOWNLINK`（对方来电音频）
3. **硬件编码器推流**：音频缓冲区直接送入 Android 原生 `MediaCodec` 或软件编码器，实时编码为轻量级 Opus 或无损 FLAC 文件。
4. **零后台耗电开销**：录音服务仅在电话状态切换至摘机通话（`EXTRA_STATE_OFFHOOK`）时启动。当通话结束恢复空闲（`EXTRA_STATE_IDLE`）时，立即关闭文件句柄并让进程回归休眠。

---

## 安装与配置

### 方法一：Root 模块安装（推荐）
1. 从发布页下载 `BCR-vX.zip`。
2. 在 Magisk 或 KernelSU 中刷入模块并重启设备。
3. 开机后，在应用桌面找到并打开 **BCR** 应用图标。
4. 根据提示授予所需的存储与通知权限。

### 方法二：无侵入式系统集成
对于刷入第三方类原生或 AOSP 固件的设备，BCR 可直接无缝集成至原生拨号器与状态栏，无需额外的后台悬浮窗保活。

---

## 配置与实用技巧

在 BCR 应用内部可进行以下自定义设置：
- **音频输出格式**：建议选择 **Opus**（推荐 32kbps 或 64kbps，人声清晰且每 10 分钟通话仅约 500KB），如需归档级无损音质可选择 **FLAC**。
- **输出目录**：可指定本地存储文件夹，或配合 Nextcloud / Syncthing 目录实现自动多端同步。
- **文件名模板**：支持自定义变量组合：
  `%contact%_%number%_%year%-%month%-%day%_%hour%-%minute%`
- **自动清理规则**：支持设置保留策略，自动清理超过 30、60 或 90 天的旧录音文件。
