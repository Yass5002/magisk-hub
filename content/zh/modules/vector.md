---
id: "vector"
title: "Vector：新一代 ART 方法挂钩与 Xposed 框架"
sidebarTitle: "Vector"
description: "由 JingMatrix 维护的 LSPosed 官方现代继任框架，为 Android 14 与 Android 15 带来高兼容性的 ART 运行时方法挂钩能力。"
category: "root-management"
tier: 1
searchQueries:
  - "Vector Xposed 框架下载"
  - "Android 14 15 LSPosed 替代"
  - "JingMatrix Vector 模块"
  - "Vector Zygisk 安装教程"
  - "现代 Xposed 框架推荐"
prerequisites:
  - "Android 9.0 至 Android 15 系统"
  - "开启 Zygisk 的 Magisk、搭配 Zygisk Next / ReZygisk 的 KernelSU 或 APatch"
conflicts:
  - "原版 LSPosed（安装 Vector 前必须先卸载）"
  - "EdXposed（已停止维护的旧框架）"
configPaths:
  - "/data/adb/lspd/"
  - "/data/adb/modules/vector/"
features:
  - "无缝兼容既有生态：支持绝大多数标准 Xposed 与 LSPosed 模块"
  - "原生适配现代 ART 运行时：针对 Android 14 与 Android 15 的编译器变更及内联优化提供完整支持"
  - "精细化作用域（Scope）管理：仅对选定目标应用生效，杜绝全局耗电与安全风险"
  - "现代化 Material You 管理器应用：提供直观的模块开关与作用域配置界面"
faq:
  - question: "为什么应该选择 Vector 而不是原版 LSPosed？"
    answer: "上游原版 LSPosed 仓库自 2023 年底停止活跃开发后，在 Android 14 QPR 更新及 Android 15 上频繁出现崩溃或挂钩失效。Vector 由原核心贡献者（JingMatrix）持续维护，彻底修复了 ART 内联去优化（Deoptimization）崩溃问题，并与最新 Android 版本保持同步兼容。"
  - question: "我以前使用的 Xposed 模块还能在 Vector 上正常运行吗？"
    answer: "完全可以。Vector 完整实现了现代 LSPosed 与 Xposed Bridge API，原本能在 LSPosed 上运行的模块无需重新编译即可直接在 Vector 上使用。"
---

## 概述

在原版 LSPosed 项目停止活跃维护后，由 **JingMatrix** 主导开发的 **Vector** 成为了社区公认的现代 Android ART 挂钩运行时正式继任者。

Xposed 机制允许开发者在无需反编译或修改磁盘上 APK 文件的情况下，于内存中动态改变系统组件与第三方应用的行为逻辑。Vector 依托 **Zygisk** 将自身注入 Android 的 Zygote 进程，在原生 ART 运行时层完成 Java 方法挂钩，兼顾极低的性能损耗与出色的系统稳定性。

---

## 技术架构与工作原理

### 基于 SandHook / Pine 的 ART 方法挂钩

1. **Zygisk 初始化注入**：当 Android 系统启动 64 位与 32 位 Zygote 守护进程时，Vector 的伴生原生库（`liblspd.so`）会被注入对应进程空间。
2. **作用域精准解析**：不同于早期 Xposed 强行挂钩所有系统进程的粗放做法（极易导致卡顿掉帧），Vector 会读取本地 SQLite 数据库（`/data/adb/lspd/config.db`），仅向明确勾选进模块作用域（Scope）的目标应用植入挂钩跳板。
3. **ART 内联挂钩**：目标应用加载时，Vector 通过 ART 运行时挂钩拦截类加载流程，在内存中修补内部 `ArtMethod` 结构，将原方法调用重定向至模块的回调接口（`beforeHookedMethod` 与 `afterHookedMethod`）。
4. **隔离式管理器通信**：管理端界面通过原生 Unix 域套接字与后台守护进程通信，防止被检测应用探测到框架自身的存在。

---

## 安装与配置

### 第一步：刷入框架模块
1. 从项目仓库下载最新的 `Vector-vX.zip`（Zygisk 版本）。
2. 打开 **Magisk**、**KernelSU** 或 **APatch**。
3. 在 **模块（Modules）** 页面刷入压缩包并重启设备。

### 第二步：安装 Vector 管理器
1. 设备重启完成后，通知栏通常会弹出安装 **Vector Manager** APK 的引导提示（或可打开内置 Web 界面）。
2. 若未收到通知提示，可前往 `/data/adb/lspd/` 目录找到 `manager.apk` 手动安装。

### 第三步：启用与配置模块
1. 安装任意所需的 Xposed 模块 APK（例如 FingerprintPay、CustoMIUIzer、KnoxPatch 等）。
2. 打开 **Vector Manager** → 切换到 **模块（Modules）** 页面。
3. 开启对应模块开关并配置其 **作用域（Scope）**，仅勾选需要修改的目标应用。
4. 强行停止目标应用或重启设备，使挂钩配置立即生效。
