---
id: "infamick-script"
title: "Infamick Script：面向 Root Android 的多功能终端命令行工具箱"
sidebarTitle: "Infamick Script"
description: "交互式 Root 终端命令行实用工具，集成三星 CSC 地区修改、Knox 组件禁用、电池循环诊断、硬件按键重映射及底层分区备份功能。"
category: "system-environment"
tier: 1
searchQueries:
  - "infamick script Magisk 模块"
  - "infamousmick infamick script 下载"
  - "Android Root 命令行工具箱脚本"
  - "三星去 Knox 修改 CSC Magisk"
  - "Android Root 查看电池循环次数"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
  - "已安装终端模拟器应用（如 Termux）"
conflicts: []
configPaths:
  - "/data/adb/modules/infamick-script/"
features:
  - "电池健康与充电管理：读取真实电池健康度、循环充电次数、预估亮屏时间（SOT）并直接控制充放电状态"
  - "三星专属增强：内置 CSC 区域代码切换器及自动化 Knox 精简禁用工具（Deknoxer）"
  - "硬件按键重映射：便捷重新绑定 Bixby 键、电源键、音量加及音量减按键功能"
  - "底层分区备份：直接调用 `dd` 镜像转储并备份任意物理分区"
  - "系统维护与优化：支持多轮缓存清理、启动计数器重置、SELinux 模式切换与屏幕 DPI 缩放调整"
faq: []
---

## 概述

由 InfamousMick 打造的 **Infamick-script** 是一款功能全面、面向已 Root Android 智能手机的交互式命令行维护与优化工具箱。它将数十条繁琐的终端命令与工程暗码浓缩为统一的数字菜单交互界面，方便用户直接掌控硬件参数、电池充电状态、分区镜像备份以及各类 OEM 专属特性（尤其是三星 Galaxy 设备）。

## 核心功能模块

### 1. 电池与电源管理
- **硬件状态遥测**：直接从内核 `power_supply` 节点读取电池循环次数、温度传感器读数及设计容量。
- **充电启停控制**：按需系统级启用或暂停电池充电，非常适合长期插电或桌面固定运行的设备。
- **待机耗电优化**：禁用异常唤醒的后台服务以缓解待机掉电问题。

### 2. 三星系统定制工具
- **CSC 区域切换器**：无侵入式切换当前生效的三星国家/地区特定代码（CSC）配置。
- **Deknoxer（去 Knox 工具）**：选择性冻结或禁用 Knox 安全服务与企业级遥测组件，避免触发系统报错。
- **Bixby 按键重映射**：将专属 Bixby 实体按键重新绑定为启动自定义应用、快捷指令或手电筒开关。

### 3. 深度维护与备份
- **分区镜像转储**：自动执行 `dd` 命令将关键分区块（如 `boot`、`recovery`、`EFS`、`persist`）直接备份至 `/sdcard/`。
- **分辨率与屏幕 DPI 调整**：无需连接电脑或 ADB，直接在手机端查询并修改当前显示缩放参数。
- **SELinux 状态管理**：查看当前 SELinux 强制策略状态，并在调试 Root 模块时在 Permissive（宽容）与 Enforcing（强制）模式之间快速切换。

## 运行方法

1. 通过 **Magisk Manager** 安装该模块并重启手机。
2. 打开 **Termux** 或你常用的 Android 终端模拟器。
3. 申请 Root 权限并启动交互式菜单：
   ```bash
   su
   infamick
   ```
4. 根据屏幕上的数字编号菜单提示执行维护任务、调整显示参数或运行硬件诊断测试。
