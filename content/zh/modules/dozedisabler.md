---
id: "dozedisabler"
title: "Doze Disabler：开机自动永久禁用 Android DeviceIdle 打盹限制"
sidebarTitle: "Doze Disabler"
description: "开机阶段自动禁用 Android Doze 与 DeviceIdle 休眠维护窗口限制，保障消息实时推送与后台同步服务不中断。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "dozedisabler Magisk 模块"
  - "draumaz dozedisabler 下载"
  - "Android Root 关闭 Doze 模式"
  - "dumpsys deviceidle disable 开机自启"
  - "修复 Android 息屏推送延迟 Root"
prerequisites:
  - "Android 8.0 至 Android 15+ 系统"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/dozedisabler/"
features:
  - "开机自动禁用：在系统服务启动后期自动执行 `dumpsys deviceidle disable` 命令"
  - "消除推送延迟：阻止 Android 在息屏期间对高优先级 FCM/GCM 推送消息进行批处理延迟"
  - "保障后台持续运行：确保 VoIP 通话、SSH 服务、BT 下载与文件同步工具在后台不休眠"
  - "纯无侵入式执行：通过系统框架 IPC 调用修改运行状态，不改动任何系统分区文件"
faq: []
---

## 概述

自 Android 6.0 起，Google 引入了 **Doze 模式**（`deviceidle`）这一省电框架子系统：当设备未接通电源、处于静止且息屏状态时，系统会激进地切断网络访问、推迟后台任务并忽略同步请求。虽然该机制有助于延长待机时间，但也经常导致即时通讯应用、VoIP 网络电话、智能家居监控以及本地后台服务（如 Syncthing 或 Termux 服务）出现严重的推送延迟甚至断连。

由 draumaz 开发的 **Doze Disabler** 是一款轻量级无侵入式工具，可在开机阶段自动关闭 Android 的深度与轻度 Doze 限制。通过在系统启动时执行框架服务指令，它能够让网络通道与后台工作线程始终保持实时响应。

## 后台应用为何会休眠

当 Doze 机制生效时，Android 会强制施加以下限制：
- 切断所有未加入白名单应用的网络连接。
- 完全忽略应用持有的唤醒锁（Wakelock）。
- 将常规 `AlarmManager` 定时唤醒推迟至间隔极长的维护窗口统一执行。
- 挂起后台同步适配器与 `JobScheduler` 计划任务。

即便用户已经在系统设置中将某个应用设为“不受电池优化限制”，系统在进入深度 Doze 状态后依然会对网络与定时唤醒进行节流。Doze Disabler 通过全局关闭 `deviceidle` 控制器彻底解决这一问题。

## 工作原理

该模块在 Android System Server 与 `DeviceIdleController` 完全初始化后的 `late_start` 服务阶段执行以下指令：

```bash
dumpsys deviceidle disable
```

该指令会通知系统框架禁止进入 Doze 状态切换。息屏后设备依然可以正常进入低功耗的 Linux CPU 挂起状态，但网络套接字与后台定时任务能够实时触发，不再被合并推迟。

## 安装与验证

1. 从 GitHub 仓库 Releases 页面下载 `dozedisabler`。
2. 使用 **Magisk**、**KernelSU** 或 **APatch** 刷入 `.zip` 压缩包。
3. 重启设备。
4. 通过终端或 ADB 验证 Doze 是否已成功禁用：
   ```bash
   su -c dumpsys deviceidle enabled
   ```
   若命令返回 `0`，则确认 Doze 子系统已处于关闭状态。
