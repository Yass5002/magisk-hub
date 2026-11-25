---
id: "background-app-slayer"
title: "Background App Slayer (BAS)：面向游戏的自动化后台清理守护进程"
sidebarTitle: "Background App Slayer"
description: "支持游戏感知的后台进程清理守护进程，提供三档清理强度，有效消除游戏过程中的后台内存争抢与 CPU 抢占。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "background app slayer Magisk 模块"
  - "unknuw background app slayer 下载"
  - "Android 游戏自动杀后台 Root"
  - "smartappclose Magisk 替代方案"
  - "KernelSU 游戏后台清理模块"
prerequisites:
  - "Android 8.0 及以上系统"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/background-app-slayer/"
features:
  - "游戏自动识别：检测到指定游戏进入前台时，立即触发深度内存释放逻辑"
  - "三档清理强度：支持在普通（Normal）、激进（Aggressive）与极限（Extreme）模式间灵活切换"
  - "纯文本配置：通过简单的文本配置文件即可自定义应用白名单与运行参数"
  - "零终端命令依赖：开机自动常驻运行，无需每次在 Termux 中手动执行命令"
faq: []
---

## 概述

现代 Android 大型手游（如多人战术竞技与大型开放世界游戏）需要持续独占充足的 CPU 核心与可用系统内存。然而，后台即时通讯服务、社交应用刷新进程及系统预装守护进程会频繁唤醒拉取通知，极易在团战或高负载场景中造成帧生成时间波动与卡顿。

**Background App Slayer (BAS)** 由 UNKNUW 基于早期 SmartAppClose 项目重构打造，是一款专为手游玩家设计的自动化后台任务终止守护进程。当游戏切换至前台时，BAS 会实时扫描进程列表，并依据用户设定的强度模式有选择地清理非必要后台进程。

## 运行模式说明

BAS 通过简洁的数字标志位控制清理强度：

1. **Mode 1（Normal 普通模式）**：
   - 温和保守的清理策略。
   - 清除常见缓存任务、临时 Web 服务及非必要缓存进程，同时保留后台聊天软件、音乐播放器与闹钟服务。
2. **Mode 2（Aggressive 激进模式）**：
   - 关闭运行在当前游戏后台的常规社交应用、浏览器实例以及流媒体播放进程。
3. **Mode 3（Extreme 极限模式）**：
   - 终止除明确加入白名单之外的所有第三方后台应用，为当前前台游戏释放最大可用内存与无干扰的 CPU 线程调度空间。

## 参数配置与白名单设置

所有配置均通过 `/data/adb/modules/background-app-slayer/` 目录下的纯文本文件管理：
- **模式选择**：编辑配置文件，将运行模式设为 `1`、`2` 或 `3`。
- **游戏检测列表**：填入目标游戏包名（例如 `com.tencent.ig`、`com.miHoYo.GenshinImpact`），指定哪些应用进入前台时触发清理机制。
- **白名单保护**：添加游戏期间绝不能被结束的关键应用（如音乐播放器、VPN 工具或 Discord 等语音开黑客户端）。

## 安装与配置

1. 从官方仓库下载最新的 `Background-App-Slayer` `.zip` 压缩包。
2. 在 **Magisk** 或 **KernelSU** 中刷入该模块。
3. 重启设备。
4. *（可选）* 打开 `/data/adb/modules/background-app-slayer/` 配置目录，按需调整清理模式或添加需要保活的后台音频应用白名单。
