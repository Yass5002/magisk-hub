---
id: "sui"
title: "Sui：无系统分区修改超级用户接口与系统级 Shizuku 服务"
sidebarTitle: "Sui"
description: "将 Shizuku API 直接注入系统服务的现代 Root 接口实现，让应用无需频繁派生完整 su 子壳即可直接调用特权 Android API。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Sui Magisk 模块下载"
  - "Sui 与 Shizuku 替代方案对比"
  - "XiaoTong6666 Sui 模块"
  - "无侵入式系统级 Shizuku 服务"
  - "Android Sui 交互式 Root Shell"
prerequisites:
  - "Android 8.0 及以上系统"
  - "Magisk、KernelSU 或 APatch，且已启用 Riru 或 Zygisk 注入支持"
conflicts:
  - "在用户空间后台同时运行独立版 Shizuku 应用（可能引发 Binder 服务注册冲突）"
configPaths:
  - "/data/adb/sui/"
  - "/data/adb/modules/sui/"
features:
  - "原生 Shizuku API 集成：为已授权应用直接提供访问 Android 框架层特权 Java API 的能力"
  - "消除进程派生开销：无需为每条指令单独启动 su 二进制外壳进程，大幅降低执行延迟与内存占用"
  - "系统设置集成管理界面：将授权弹窗与权限管理面板直接嵌入 Android 原生“设置”应用"
  - "多种授权策略模式：支持每次询问确认、自动允许或完全禁止"
  - "内置交互式 Root Shell 与 adb root 辅助工具：直接通过 Binder 提供高速 Root 终端访问能力"
faq:
  - question: "Sui 与普通的 Shizuku 应用有什么区别？"
    answer: "常规 Shizuku 应用是作为外部后台进程运行的，需要通过 ADB 或 Root Shell 脚本拉起；而 Sui 是一个无系统分区修改模块，在开机阶段直接注入 system_server 与应用进程，开机即用无需人工干预，并直接在 Android 系统框架内部运行。"
  - question: "在哪里管理 Sui 的应用授权？"
    answer: "Sui 不会在桌面生成独立图标。它直接将管理面板嵌入手机原生“设置”应用的“系统”或“开发者选项”中，并在应用首次请求权限时主动弹出系统级授权对话框。"
---

## 概述

由 **RikkaApps** 开发并由 **XiaoTong6666** 持续维护的 **Sui**，是一款面向 Android 平台的现代超级用户接口（Super User Interface，SUI）实现。

传统的 Unix 风格 `su` 子壳方案每次都需要启动较重的 `/system/bin/sh` 进程并解析脆弱的文本输出流；与之不同，Sui 直接将 **Shizuku API** 注入 Android 系统框架内部，使获得授权的应用能够依托真实系统权限，通过高速 IPC 直接调用隐藏及系统级的 Android Java API。

---

## 技术架构与工作原理

### 系统服务注入与 Binder IPC

Sui 直接运行在 Android 操作系统运行时内部：

1. **System Server 挂钩（Hook）**：在开机早期阶段，Sui 借助 Zygisk 或 Riru 挂钩进入 `system_server`，并注册一个安全的本地 Binder 服务以对外暴露特权平台能力。
2. **直接框架调用**：客户端应用链接 Shizuku API 库后，在执行应用管理、权限授予或显示控制等操作时，请求会通过 Binder IPC 直达 `system_server`，全程无需派生任何 Shell 子进程。
3. **集成化安全弹窗**：当未授权应用发起请求时，Sui 会直接在用户屏幕上触发原生系统框架样式的授权确认对话框。

---

## 安装与启用

1. 确认你的 Root 环境（Magisk、KernelSU 或 APatch）已启用可用的 Zygisk 实现。
2. 从官方仓库 Releases 下载最新版的 `Sui-v*.zip` 模块包。
3. 在 Root 管理器中刷入该模块并重启设备。
4. 打开任意支持 Shizuku 的应用（如 App Ops、Swift Backup 或各类 Shizuku 工具），Sui 将自动接管并提供授权管理。

---

## 配置与使用

- **管理界面**：直接在 Android 系统设置中打开 Sui 权限管理面板，或在终端中运行配置辅助程序：
  ```bash
  su -c /data/adb/modules/sui/bin/sui
  ```
- **细粒度权限策略**：可针对每个应用单独配置策略（允许、拒绝、每次询问），无需在桌面上额外安装独立的管理端 APK。

---

## 故障排查与常见问题

- **Shizuku 服务冲突**：若部分应用无法识别到 Sui，请检查后台是否同时运行了独立版 Shizuku 应用。请停止并卸载独立版 Shizuku APK，确保 Sui 能够正常绑定默认的 Shizuku IPC 端点。
- **进入 Root Shell**：如需启动由 Sui 驱动的交互式 Root 终端，可在终端模拟器中执行 `sui shell`。
