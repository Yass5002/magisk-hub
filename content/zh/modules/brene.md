---
id: "brene"
title: "BRENE：抗卡米启动保护与自动恢复引擎"
sidebarTitle: "BRENE"
description: "智能开机保护看门狗，能够侦测启动卡死与循环重启（Bootloop），并自动禁用引发故障的 Magisk 与 KernelSU 模块以挽救设备。"
category: "root-management"
tier: 1
searchQueries:
  - "BRENE Magisk 模块"
  - "rrr333nnn333 BRENE 下载"
  - "Magisk 防卡米保护模块"
  - "卡米自动禁用故障模块"
  - "Android Root 防无限重启救砖"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
conflicts:
  - "明确说明：与其他模块无已知冲突"
configPaths:
  - "/data/adb/modules/brene/config.sh"
  - "/data/adb/modules/brene/"
features:
  - "自主防卡米检测：全程监测 Android 各启动阶段，识别 Zygote 启动失败或系统框架崩溃"
  - "自动安全恢复：当设备未能在超时时间内完成开机时，自动禁用新刷入或存在故障的模块"
  - "Action 按钮控制：支持直接在 Root 管理器内测试恢复触发器并查阅模块日志"
  - "自定义超时参数：可在 `config.sh` 中按需调整触发干预前的最大允许开机时长"
  - "轻量级守护进程：极简 Shell 看门狗实现，成功开机后后台零额外耗电"
faq:
  - question: "BRENE 是如何检测卡米（Bootloop）的？"
    answer: "BRENE 在启动早期的 `post-fs-data` 阶段即介入运行，持续追踪系统向 `sys.boot_completed=1` 推进的进度。如果设备在未完成开机状态下连续重启多次或超过设定阈值，便会自动禁用近期新增的模块。"
  - question: "恢复过程中被禁用的模块会被移动到哪里？"
    answer: "BRENE 会在问题模块位于 `/data/adb/modules/` 下的目录内生成 `disable` 标记文件，使其在下次开机时不再挂载，同时完整保留所有模块文件以便用户后续排查。"
---

## 概述

由 **rrr333nnn333** 开发的 **BRENE**（*Bootloop-Resistant Environment & Recovery Engine*）是一款专为已 Root Android 设备打造的安全护航工具，用于防范不稳定模块引发的致命卡米故障。

刷入不兼容的系统框架微调、字体替换或音效模块极易导致手机卡死在开机动画界面。在未安装第三方 Recovery（如 TWRP）的情况下，手动救砖往往需要繁琐的 ADB 排错甚至恢复出厂设置。BRENE 通过运行一套智能看门狗服务，在故障发生时自动介入并禁用问题模块。

---

## 技术架构与工作原理

### 早期启动看门狗与状态追踪

BRENE 在 Android 初始化序列的极早期即开始执行：

1. **看门狗初始化**：于 `post-fs-data` 阶段启动，并在临时存储区建立递增式开机计数器。
2. **启动阶段校验**：持续等待 Android 系统服务广播 `sys.boot_completed=1` 标志。
3. **自动修复处置**：一旦看门狗计时超时，或设备在进入桌面之前反复意外重启，BRENE 就会为疑似冲突的模块目录写入 `.disable` 禁用标记，让手机得以顺利完成开机。

---

## 安装与部署

1. 下载最新版本的 `BRENE-*.zip` 安装包。
2. 在 Magisk、KernelSU 或 APatch 中刷入该模块。
3. 重启设备。
4. 至此，BRENE 已激活并开始为后续刷入的模块提供开机安全保障。

---

## 配置与使用

如需微调超时上限与安全判定规则，请编辑以下配置文件：
```bash
/data/adb/modules/brene/config.sh
```
- **Action 按钮**：在 Root 管理器中点击模块的 Action 按钮，即可查看当前运行状态并测试安全恢复触发钩子。

---

## 故障排查与常见问题

- **慢速开机导致模块被误禁用**：若某次正常的慢速开机（例如清理 Dalvik 缓存或系统大版本升级后首次开机）触发了 BRENE 提前介入，请适当调大 `config.sh` 中的开机超时阈值。
