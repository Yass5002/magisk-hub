---
id: "auto-skip-splash-screens"
title: "Auto Skip Splash Screen Ads：系统特权级开屏广告拦截指南"
sidebarTitle: "自动跳过（Auto Skip）"
description: "具备系统特权的无侵入式 Android 工具，自动拦截应用启动倒计时广告并触发秒级跳过。"
category: "system-utilities"
tier: 1
searchQueries:
  - "自动跳过开屏广告 magisk"
  - "Root 跳过应用启动广告"
  - "zdtg 自动跳过模块下载"
  - "系统应用级跳过开屏广告"
prerequisites:
  - "Magisk 17.0+、KernelSU 或 APatch"
  - "Android 8.0 至 Android 14"
conflicts:
  - "激进的无障碍服务进程清理工具"
configPaths:
  - "/system/app/ZDTG/自动跳过_3.4.5.apk"
  - "/data/adb/modules/ZDTG_9384/"
features:
  - "系统特权级部署，防止后台进程被厂商内存清理机制终止"
  - "高速 UI 节点检视，精准识别“跳过”及广告关闭文本节点"
  - "零额外耗电：仅在前台应用启动窗口事件触发时激活"
  - "纯本地独立运行，无任何云端遥测或数据采集行为"
faq:
  - question: "这需要开启无障碍服务（Accessibility Service）吗？"
    answer: "是的。内置应用依赖 Android 无障碍框架执行高速界面节点检测，并对倒计时跳过按钮触发模拟点击手势。"
  - question: "为什么将其作为系统应用安装，而不是普通 APK？"
    answer: "挂载至 /system/app 可赋予服务系统级特权，确保厂商激进的内存清理策略（如 MIUI 内存扩展或各类后台清理器）无法强行查杀该守护进程。"
---

## 概述

**Auto Skip Splash Screen Ads**（作者：Shui Nian Hua Lou Ta Yan）是一款轻量级实用工具，旨在消除拖慢应用启动速度的商业开屏广告，帮用户节省等待时间与流量消耗。

商业应用常强制展示 3 至 5 秒的开屏广告横幅，并把“跳过”按钮设计得极其微小、难以点击。本模块将经过优化的自动跳过引擎直接部署至 Android `/system/app/` 目录层级，使其无需用户手动配置电池白名单即可获得持久的系统特权驻留能力。

---

## 技术架构与工作原理

### 1. 系统特权应用挂载

普通用户空间下的跳广告工具极易被国产定制系统的激进内存管理机制（如 EMUI、MIUI、ColorOS）频繁杀掉后台。借助 Magisk/KernelSU 的无侵入式绑定挂载（Systemless Bind-Mount）：

```text
/system/app/ZDTG/
└── 自动跳过_3.4.5.apk
```

Android 运行时（`system_server`）会将其视为预装厂商系统应用，给予更高的 OOM 优先级调整值（`oom_score_adj`），并豁免于各类激进的后台待机限制。

### 2. 窗口状态事件检测

该引擎并非持续轮询屏幕画面（轮询会导致极高的 CPU 负载与电量消耗），而是注册了 `TYPE_WINDOW_STATE_CHANGED` 事件监听器：

算法会将当前活动窗口的 UI 节点文本与内容描述（Content Description）同预设正则表达式进行匹配，锁定跳过提示词（如 `Skip`、`Close`、倒计时文本），精确定位其边界坐标后立即派发模拟点击。

---

## 验证与启用步骤

1. 刷入模块并重启设备。
2. 前往 **设置 -> 无障碍 -> 已下载的应用 / 已安装的服务**。
3. 开启 **自动跳过（Auto Skip）** 开关。
4. 启动任意带有开屏广告的应用，确认已实现秒级自动跳过。
