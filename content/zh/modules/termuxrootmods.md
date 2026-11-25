---
id: "termuxrootmods"
title: "Termux Root Modifications：原生级 Root Shell 集成"
sidebarTitle: "Termux Root Mods"
description: "由 rompelhd 开发的无侵入式 Magisk 模块，通过修补 `/system/etc/mkshrc` 并搭配自定义 C++ 启动器，将 Root 环境无缝集成至 Termux。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "termuxrootmods magisk 模块"
  - "rompelhd termux root 增强"
  - "termux mkshrc root 环境变量"
  - "termux su 路径修复 magisk"
  - "termux 无缝进入 root shell"
prerequisites:
  - "已刷入 Magisk v20.4 或更高版本的 Android 设备"
  - "已安装 Termux 应用（推荐使用 F-Droid 或 GitHub 发布版）"
  - "ARM64、ARM（armhf）或 x86_64 处理器架构"
conflicts: []
configPaths:
  - "/data/adb/modules/TermuxRootMods/"
  - "/system/etc/mkshrc"
features:
  - "无侵入式 `mkshrc` 修补：拦截 Android 默认的 MirBSD Korn Shell 配置文件以运行自定义 Root 初始化钩子"
  - "环境变量统一协调：在 Android Toybox 与 Termux GNU 用户态之间正确配置 `PATH`、`LD_LIBRARY_PATH` 及终端变量"
  - "高性能 C++ 启动器：专门编译的原生二进制启动器以亚毫秒级开销拉起 Shell"
  - "零宿主机系统污染：完全依托 Magisk 挂载架构维持 Root 增强配置，不触碰物理 `/system` 分区"
---

## 概述

由 rompelhd 开发的 TermuxRootMods 旨在解决开发者在已 Root 的 Android 设备上使用 Termux 时的常见痛点：Termux 用户态环境与 Android 原生 Root Shell 之间的割裂。

在 Termux 中输入 `su` 后，Android 默认会将用户切换至简陋且未经配置的 MirBSD Korn Shell（`mksh`）。此时，Termux 核心二进制目录（如 `/data/data/com.termux/files/usr/bin`）会从 `PATH` 中丢失，自定义别名与函数均无法使用，且终端属性（`TERM`）往往会回退至原始默认值，导致 `htop`、`tmux` 或 `nano` 等交互式终端工具显示异常。

TermuxRootMods 通过无侵入式修补 Android 的 `/system/etc/mkshrc` 来调用专用 C++ 二进制程序，确保执行 `su` 时能够直接进入配置完整、体验统一的 Linux Root Shell。

## 前置要求与兼容性

- **Root 框架**：Magisk v20.4 或更高版本。
- **应用版本**：Termux（请确保使用 F-Droid 或 GitHub 发布的现代构建版本；Google Play 商店版本早已停止维护）。
- **支持架构**：`arm64`、`armhf`（32 位 ARM）以及 `x86_64`。

目前无已知模块冲突。

## 技术架构

在 Android 系统中，交互式 Root Shell 启动时会执行 `/system/etc/mkshrc`：
1. TermuxRootMods 为 `/system/etc/mkshrc` 注入无系统分区修改（Systemless）的覆盖层。
2. 当 Root Shell 初始化时，修改后的脚本会调用模块内置的原生编译 C++ 二进制程序。
3. 该二进制程序会检测调用进程的上下文，判断会话是否源自 Termux，随后注入自定义环境变量导出、历史记录追踪及 Shell 提示符样式。
4. 若检测到用户配置了自定义 Shell（例如 GNU Bash 或 Zsh），该二进制程序还能平滑移交控制权并启动目标 Shell。

## 安装与使用

1. 从仓库发布页下载最新的 `TermuxRootMods-v*.zip` 安装包。
2. 通过 Magisk 刷入模块并重启设备。
3. 打开 **Termux** 应用。
4. 输入 `su` 并按回车键。
5. 在 Magisk 弹出授权请求时授予 Root 权限。
6. Root Shell 将立即完成初始化，并自动加载增强后的环境变量与工具路径。
7. 已启用的模块资源位于以下路径：
   ```bash
   /data/adb/modules/TermuxRootMods/
   ```

## 故障排查与验证

- **执行 `su` 后仍进入默认简化 Shell**：确认模块已在 Magisk 中启用，且安装后已重启设备。随后检查 `/system/etc/mkshrc` 是否已正确挂载生效：
  ```bash
  grep -i "TermuxRootMods" /system/etc/mkshrc
  ```
- **终端界面显示错乱**：若在 Root 模式下运行全屏交互程序出现线条错位或乱码，请确保已正确导出 `TERM` 环境变量：
  ```bash
  export TERM=xterm-256color
  ```
