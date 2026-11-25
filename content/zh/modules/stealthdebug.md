---
id: "stealthdebug"
title: "StealthDebug：隐藏 USB 调试与 ADB 系统属性"
sidebarTitle: "StealthDebug"
description: "以无系统分区修改（Systemless）方式屏蔽 USB 调试与开发者选项相关系统属性，帮助绕过竞技手游及企业级应用对 ADB 环境的检测。"
category: "security-certificates"
tier: 1
searchQueries:
  - "StealthDebug Magisk 模块"
  - "Root 隐藏 USB 调试状态"
  - "sp11xy StealthDebug"
  - "绕过堡垒之夜手游 ADB 检测"
  - "Magisk 隐藏开发者选项"
prerequisites:
  - "已通过 Magisk 获取 Root 权限"
  - "若目标应用直接读取 Settings.Global 接口，建议搭配 LSPosed 框架使用"
conflicts: []
configPaths:
  - "/data/adb/modules/stealthdebug/"
features:
  - "属性级 ADB 隐藏：拦截并屏蔽暴露当前 USB 调试会话活跃状态的系统属性"
  - "绕过反作弊检测：防止《堡垒之夜（Fortnite Mobile）》等游戏的风控引擎标记已开启的开发者选项"
  - "保留正常 ADB 可用性：在不切断合法开发调试通道的前提下，仅对不可信应用隐藏调试属性"
  - "自动化后台服务：开机自动随系统启动生效，无需任何手动配置"
  - "可与 Xposed Hook 协同：配合 NotDeveloper 等 LSPosed 模块实现从底层属性到上层 API 的全方位伪装"
faq: []
---

## 概述

竞技类手机游戏（如 Fortnite Mobile）以及敏感的企业级移动银行应用往往集成了极其严苛的反篡改启发式检测机制。其中最常见的一项完整性检查，便是探测设备是否开启了 **USB 调试（`adb`）** 或开发者选项。一旦命中该检测，这类应用会立即拒绝启动或将玩家踢出对局，以此防止内存 Hook 注入与遥测数据窃取。

由 sp11xy 开发的 **StealthDebug** 是一款无系统分区修改（Systemless）的 Magisk 模块，专门用于向用户态应用程序屏蔽 USB 调试标志位与相关系统属性。

## 工作原理与推荐架构

移动反作弊扫描器通常会探查由 Android Bionic 属性服务暴露出的以下特定系统属性标记：
- `init.svc.adbd`（用于判断 ADB 守护进程当前是否正在运行）
- `sys.usb.config` 与 `sys.usb.state`（用于判断 USB 复合设备描述符中是否包含 `adb` 接口）
- `persist.sys.usb.config`

StealthDebug 会拦截对这些系统属性的读取请求，向非特权应用程序返回未开启调试时的常规标准状态。

> **重要架构提示**：尽管 StealthDebug 能够成功屏蔽底层原生系统属性，但现代应用还可能通过 Android 框架层的 Java API 直接查询设置项（`Settings.Global.getInt(getContentResolver(), Settings.Global.ADB_ENABLED, 0)`）。为了覆盖所有检测维度实现全面防护，建议将 StealthDebug 与 **NotDeveloper** 等 LSPosed 模块搭配使用。

## 安装步骤

1. 从 GitHub Releases 下载 `StealthDebug.zip` 安装包。
2. 打开 **Magisk**，进入 **模块（Modules）> 从本地安装（Install from storage）**。
3. 选择下载的压缩包并确认刷入。
4. 重启手机后，模块将在每次系统启动时自动于后台运行生效。
