---
id: "thunderbolt-lock-unlock-sounds"
title: "Thunderbolt Lock & Unlock Sound Effects：Android 雷电电流锁屏解锁音效模块"
sidebarTitle: "Thunderbolt 雷电音效"
description: "无系统分区替换 Android 原生锁屏与解锁提示音，带来清脆高能的雷电电流声学反馈。"
category: "customization-ui"
tier: 2
searchQueries:
  - "Thunderbolt 锁屏音效 Magisk"
  - "修改安卓解锁提示音 Magisk"
  - "自定义锁屏声音 Root 模块"
  - "安卓系统 UI 音效替换"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他修改 /system/media/audio/ui/Lock.ogg 或 Unlock.ogg 的模块"
configPaths:
  - "/system/media/audio/ui/Lock.ogg"
  - "/system/media/audio/ui/Unlock.ogg"
features:
  - "无系统分区覆盖 /system/media/audio/ui/ 目录，不修改系统分区原始存储"
  - "将默认锁屏与亮屏解锁音效替换为极具未来感的雷电电流提示音"
  - "音频经过预先响度标准化母带处理，防止破音削波或音量骤增"
  - "无后台守护进程，零额外内存占用与续航损耗"
faq:
  - question: "安装模块后为什么听不到自定义音效？"
    answer: "请确保系统设置中的“锁屏提示音”开关已开启（通常位于 设置 -> 声音与振动 -> 更多声音设置），并确认手机当前未处于静音或仅振动模式。"
  - question: "刷入该模块后需要重启才能生效吗？"
    answer: "是的。系统交互音效由 Android AudioService 在系统框架启动阶段统一加载，因此刷入后必须重启设备才能生效。"
---

## 概述

**Thunderbolt Lock & Unlock Sound Effects**（由 ZHB 制作）是一款精简的无系统分区修改（Systemless）音频美化模块，旨在通过将枯燥的原生 Android 锁屏、解锁音效替换为清脆凌厉的电流声效，提升日常交互的听觉反馈质感。

原生 Android 锁屏提示音往往偏闷且音量微弱，在嘈杂环境下几乎难以察觉。Thunderbolt 针对手机扬声器的频响特性进行了专门的母带调校，在锁屏或唤醒屏幕时提供干脆利落的高辨识度听觉确认。

---

## 技术架构与工作原理

Android 通过系统框架层中的 AudioService 管理界面交互音效，并从 `/system/media/audio/ui/` 读取音频资源：

### 1. 覆盖挂载机制

本模块将预编码的 OGG Vorbis 音轨挂载覆盖至系统标准音效路径：

- `/system/media/audio/ui/Lock.ogg`：屏幕熄灭并进入锁屏界面时触发。
- `/system/media/audio/ui/Unlock.ogg`：生物识别认证成功或划开锁屏界面时触发。

得益于 Magisk/KernelSU 的无系统分区绑定挂载机制，原厂 ROM 分区保持完全纯净，不影响 SafetyNet 与 Play Integrity 环境检测。

### 2. 音频工程调校

内置音频采用高码率 OGG Vorbis 格式编码，并将峰值限制在 -0.5 dBFS，既保留了锐利的瞬态响应，又能防止在入门级手机功放电路上出现 DAC 削波破音。

---

## 生效验证与故障排查

- **检查系统设置**：前往 **设置 > 声音与振动 > 更多声音设置**，确认已开启 **锁屏提示音**。
- **检查挂载状态**：可在终端执行以下命令验证文件是否成功覆盖挂载：
  ```bash
  ls -l /system/media/audio/ui/Lock.ogg
  ```
- **音量通道调节**：锁屏音效绑定在 Android 系统的“通知/系统”音量通道上；若声音偏小，请适当调高系统音量滑块。
