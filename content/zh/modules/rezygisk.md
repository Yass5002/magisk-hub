---
id: "rezygisk"
title: "ReZygisk：面向现代 Root 方案的开源独立 Zygisk 引擎"
sidebarTitle: "ReZygisk"
description: "专为 KernelSU、APatch 及自定义 Root 方案设计的高性能独立 Zygisk API 实现，全开源且无遥测。"
category: "root-management"
tier: 1
searchQueries:
  - "ReZygisk 下载"
  - "ReZygisk 和 Zygisk Next 对比"
  - "KernelSU 独立 Zygisk 模块"
  - "PerformanC ReZygisk 使用教程"
  - "APatch 如何开启 Zygisk"
prerequisites:
  - "已安装 KernelSU 或 APatch（若使用 Magisk，须先关闭内置 Zygisk 开关）"
  - "Android 8.0 至 Android 15 系统"
conflicts:
  - "Zygisk Next（切勿同时运行两个独立 Zygisk 引擎）"
  - "同时开启 Magisk 内置 Zygisk 开关"
configPaths:
  - "/data/adb/rezygisk/"
  - "/data/adb/modules/rezygisk/"
features:
  - "100% 开源可审计的 Zygisk C/C++ 模块 API 实现"
  - "专为内核辅助型 Root 方案（KernelSU / APatch）打造，无需依赖 Magisk 框架"
  - "优化挂钩跳板（Hook Trampoline）设计，降低内存占用并加快应用进程 Fork 速度"
  - "零遥测、零追踪，专注保障 Zygisk 模块运行的长期稳定性"
faq:
  - question: "我已经用了 KernelSU，为什么还需要安装 ReZygisk？"
    answer: "KernelSU 纯粹在 Linux 内核层运行，原生并不向 Android 用户空间的 Zygote 进程注入代码。而许多热门 Root 模块（如 Shamiko、PlayIntegrityFork 与 Vector）都依赖 Zygisk 来拦截应用进程。ReZygisk 正是用于补齐这一 Zygote 注入桥梁。"
  - question: "可以在 Magisk 上使用 ReZygisk 吗？"
    answer: "可以，但你必须先在 Magisk 设置中关闭内置的 Zygisk 开关，否则会导致符号冲突并引发系统进程崩溃。"
---

## 概述

由 **PerformanC** 开发的 **ReZygisk** 是一款纯净、开源且独立运行的 **Zygisk API** 规范实现。

Magisk 将专有的 Zygisk 实现直接集成在 `magiskd` 守护进程中，而 KernelSU 与 APatch 等现代方案则秉持极简的内核空间设计理念。为了运行庞大的 Zygisk 生态模块（例如 Vector/Xposed、PlayIntegrityFork 以及各类音效增强模块），KernelSU 必须借助外部 Zygote 注入引擎。ReZygisk 以简洁高效的架构满足了这一核心需求。

---

## 技术架构与工作原理

### Zygote Ptrace 注入与加载器机制

1. **守护进程初始化**：系统启动时，ReZygisk 会启动后台监控守护进程，持续监听 Android 32 位与 64 位 Zygote 进程（`app_process32` 和 `app_process64`）的初始化时机。
2. **Ptrace 劫持注入**：在 Zygote 进程早期初始化阶段（首个应用尚未 Fork 之前），ReZygisk 通过 `ptrace` 将原生加载库（`librezygisk.so`）注入目标进程。
3. **完整 API 实现**：ReZygisk 注册完整的官方 Zygisk API 接口：
   - `preAppSpecialize`：在应用进程降权至标准沙盒 UID 之前执行。
   - `postAppSpecialize`：在沙盒权限生效后执行。
   - 伴生进程（Companion Process）IPC 通信通道。
4. **模块调度分发**：每当有应用进程派生时，ReZygisk 会扫描 `/data/adb/modules/` 下已启用的 Zygisk 模块，并将其原生 `.so` 载荷直接加载到目标进程空间。

---

## 安装与配置

1. 打开 **KernelSU** 或 **APatch** 管理器。
2. 从发布页下载最新的 `ReZygisk-vX.zip`。
3. 切换到 **模块（Modules）** 标签页刷入压缩包。
4. 重启手机。
5. 返回模块列表，确认 ReZygisk 已处于激活状态。此后即可继续刷入任意标准 Zygisk 模块（如 PlayIntegrityFork 或 Vector），所有功能均可无缝协同运行。
