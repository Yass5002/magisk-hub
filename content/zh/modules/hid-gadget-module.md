---
id: "hid-gadget-module"
title: "USB HID Gadget Module：将 Android 手机变身为 USB 键鼠与 DuckyScript 注入器"
sidebarTitle: "HID Gadget Module"
description: "在 Android 设备上启用 USB 人机接口设备（HID）模拟功能，提供交互式终端 TUI 键盘/鼠标以及 DuckyScript 3.0 自动化脚本执行。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "hid-gadget-module Magisk 模块"
  - "kelexine hid-gadget-module"
  - "Android Root USB 键盘鼠标模拟"
  - "DuckyScript 3.0 BadUSB 安卓 Magisk"
  - "hid-tui 终端键盘控制"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "内核已启用 USB ConfigFS 与 HID Gadget 驱动（`CONFIG_USB_CONFIGFS_F_HID`）"
  - "用于连接宿主机电脑的 USB-C 或 Micro-USB 数据线"
conflicts: []
configPaths:
  - "/data/adb/modules/hid-gadget-module/"
features:
  - "完整硬件级 HID 模拟：使连接的 PC 或 Mac 将 Android 识别为原生物理 USB 键盘、光电鼠标及多媒体遥控器"
  - "基于 musl 静态编译：零共享库依赖，兼容 ARM、ARM64、x86 与 x86_64 环境"
  - "交互式终端 TUI（`hid-tui`）：在 Termux 中渲染可触控操作的 75% 配列键盘与触控板导航界面"
  - "DuckyScript 3.0 执行引擎：支持注入自动化按键载荷，适用于快速系统运维、救援脚本与渗透测试"
  - "驱动自动自愈：当宿主机发生 USB 总线重置时，自动重置并重新绑定 Linux ConfigFS gadget 子系统"
faq: []
---

## 概述

无论是在键盘损坏的情况下救援无头家庭服务器、在未携带外设的现场管理工业设备，还是执行渗透测试任务，随身携带一台物理 USB 人机接口设备（HID）都极为实用。

由 kelexine 开发的 **USB HID Gadget Module & Terminal Controller** 可将已获取 Root 权限的 Android 智能手机变成一台 USB 键盘、鼠标和多媒体遥控器。该模块基于静态链接的 `musl` 工具链构建，并配备交互式终端图形界面（`hid-tui`），通过初始化 Linux 内核的 ConfigFS gadget 框架，使手机能够向任何连接的 PC、Mac 或游戏主机发送底层 USB 扫描码，全程无需蓝牙配对，也无需在目标主机上安装任何配套软件。

## 核心功能

### 1. 交互式终端 TUI（`hid-tui`）
模块内置了一款功能完整的控制台程序，可直接运行于 Termux 内部：
- **75% 笔记本键盘布局**：直接在手机屏幕上发送功能键、字母数字字符、方向键以及修饰键（`Ctrl`、`Alt`、`Super/Win`）。
- **鼠标与触控板模拟**：通过 USB 传输精准的光标移动、鼠标点击及滚轮滚动指令。
- **多媒体遥控**：控制目标设备的音量、媒体播放状态与屏幕亮度。

### 2. DuckyScript 3.0 载荷执行
面向系统管理员与安全测试人员，该模块集成了兼容 **DuckyScript 3.0** 规范的脚本解释器。你可以直接加载 `.ducky` 脚本文件，在数秒内向目标电脑注入复杂的自动化按键序列。

### 3. 原生 ConfigFS Gadget 管理
模块直接工作在内核 USB 层（`/dev/hidg0`、`/dev/hidg1`），在系统启动早期即完成 USB 描述符配置。一旦宿主机重置 USB 总线，后台看门狗例程会通过 `su` 自动重新绑定 gadget 驱动，确保连接稳定不中断。

## 启动 TUI 控制器

1. 使用标准 USB 数据线将 Android 手机连接至目标电脑。
2. 在手机上打开 Termux，获取 Root 权限并启动控制界面：
   ```bash
   su -c hid-tui
   ```
3. 使用屏幕触控按键直接输入文字并控制目标电脑上的鼠标光标。

## 安装与环境要求

- 从 GitHub Releases 下载最新的 `hid-gadget-module` `.zip` 安装包。
- 在 **Magisk** 或 **KernelSU** 中刷入该模块。
- 重启设备使配置生效。
- *注意*：设备内核必须支持 USB ConfigFS 与 HID 端点功能（`CONFIG_USB_CONFIGFS_F_HID`）。绝大多数现代第三方定制内核及原生 AOSP 内核均已默认包含该支持。
