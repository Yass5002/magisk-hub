---
id: "multiuseruienabler"
title: "Multi-User UI Enabler：在精简版 OEM ROM 上解锁多用户配置界面"
sidebarTitle: "Multi-User UI Enabler"
description: "通过无系统分区修改注入系统框架属性，在三星 One UI Core 等受限 OEM ROM 上恢复并显示隐藏的 Android 多用户设置界面。"
category: "system-environment"
tier: 1
searchQueries:
  - "multiuseruienabler Magisk"
  - "insertx2k multiuseruienabler 下载"
  - "三星 One UI Core 开启多用户"
  - "Android 隐藏多用户设置解锁"
  - "fw.show_multiuserui 面具模块"
prerequisites:
  - "通过 Magisk 20.4+ 获取 Root 权限"
  - "设备 ROM 必须保留原生用户管理命令支持（`pm create-user`、`am switch-user`）"
conflicts: []
configPaths:
  - "/data/adb/modules/multiuseruienabler/"
features:
  - "解锁原生多用户设置：在「设置 > 账号与备份 > 用户」中重新显示被隐藏的用户配置管理菜单"
  - "无系统分区修改属性注入：在不改动物理分区文件的前提下注入 `fw.max_users=5` 与 `fw.show_multiuserui=1`"
  - "无需 Zygisk 依赖：纯通过系统属性覆盖运行，不依赖 Zygisk 运行时挂钩"
  - "独立沙盒环境：为子用户或访客账户提供相互隔离的应用数据、存储空间与桌面布局"
  - "经过验证的 OEM 兼容性：已在三星 One UI Core 及多款定制 OEM 固件上成功验证"
faq: []
---

## 概述

Android 原生具备完善的多用户架构，允许多个相互独立的用户配置文件共享同一台设备——每个用户均拥有各自独立的应用实例、系统设置与沙盒化存储空间。然而，部分设备厂商（例如三星在其入门级“One UI Core”设备上）会刻意在系统“设置”应用中隐藏多用户配置入口。

由 InsertX2k 开发的 **multiuseruienabler** 是一款轻量化无系统分区修改（Systemless）Magisk 模块，通过注入 Android 框架属性标志，取消隐藏并恢复系统原生多用户管理界面。

## 前置要求与兼容性验证

在安装本模块前，请先确认设备所刷 ROM 未将底层多用户服务二进制文件彻底移除。你可以通过 ADB Shell 或 Termux 检测兼容性：

1. **验证用户切换能力**：
   ```bash
   su -c am get-current-user
   ```
   *（主系统用户应返回 `0`）。*
2. **验证用户创建能力**：
   ```bash
   su -c pm create-user TestUser
   ```
   *（若该命令顺利完成且无报错，则说明当前 ROM 包含底层多用户服务）。*
3. **清理测试配置文件**：
   ```bash
   su -c pm remove-user 10
   ```
   *（请将 `10` 替换为创建步骤实际返回的用户 ID，切勿尝试删除用户 `0`）。*

## 工作原理

该模块利用 Magisk 的 `system.prop` 机制，在系统启动阶段以无侵入方式注入框架配置属性：
- `fw.show_multiuserui=1`：强制 Android“设置”应用渲染并显示多用户偏好设置控制器。
- `fw.max_users=5`：将系统允许同时存在的最大用户配置文件槽位数设为 5 个。

## 安装步骤

1. 从 GitHub Releases 页面下载 `multiuseruienabler.zip`。
2. 在 **Magisk 管理器** 中从本地安装并刷入该模块。
3. 重启设备。
4. 前往 **设置 > 账号与备份 > 用户**（或 **设置 > 系统 > 多用户**），即可配置子账户与访客模式。
