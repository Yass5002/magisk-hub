---
id: "zygisknext"
title: "Zygisk Next：独立跨平台高性能 Zygisk 实现"
sidebarTitle: "Zygisk Next"
description: "由 Dr-TSNG / LSPosed 开发团队构建的高性能独立 Zygisk 注入实现，为 KernelSU、APatch 与 Magisk 提供现代化的 Zygisk API 支持。"
category: "root-management"
tier: 1
searchQueries:
  - "Zygisk Next 模块下载"
  - "Dr-TSNG ZygiskNext 教程"
  - "KernelSU APatch 怎么用 Zygisk"
  - "Zygisk Next 排除列表卸载策略"
  - "Magisk 关闭内置 Zygisk 替换"
prerequisites:
  - "KernelSU（内核 >= 10940，ksud >= 11575）、APatch（>= 10700）或 Magisk（>= 26402 且关闭内置 Zygisk）"
  - "仅运行单一 Root 实现（禁止同时混装 Magisk 与 KernelSU）"
conflicts:
  - "Magisk 内置 Zygisk 开关（必须在 Magisk 设置中关闭，否则将发生双加载器冲突）"
  - "其他同时启用的 Zygisk 加载器（如 ReZygisk、NeoZygisk）"
configPaths:
  - "/data/adb/modules/zygisksu/"
  - "/data/adb/zygisksu/"
features:
  - "独立生命周期：将 Zygisk 注入引擎与 Magisk 自身更新周期彻底解耦"
  - "全平台 Root 兼容：为 KernelSU、APatch 与 Magisk 提供完整一致的 Zygisk 模块生态支持"
  - "深度命名空间隔离：精准执行 DenyList 与 Umount 卸载策略，从目标进程视角剥离模块挂载痕迹"
  - "WebUI 与一键诊断报告：内置 WebUI 控制面板，并通过 `action.sh` 一键打包系统诊断报告"
  - "扩展原生接口：支持面向 init 进程的 `zygisk_next_api.h` 与 HyperOS Rust Runtime 原生回调"
faq:
  - question: "为什么要用 Zygisk Next 替代 Magisk 内置 Zygisk？"
    answer: "Magisk 内置 Zygisk 的内存特征与挂钩模式已被主流风控 SDK 广泛识别。由 LSPosed 团队（Dr-TSNG/ZygiskNext）打造的 Zygisk Next 采用独立现代化的 `zygiskd` 守护架构，隐蔽性与隔离能力更强，并原生支持 KernelSU 与 APatch。"
  - question: "如何在 Zygisk Next 中配置模块挂载卸载（Umount）？"
    answer: "在 KernelSU 或 APatch 中，可直接使用管理器的原生卸载模块开关或 Zygisk Next WebUI 进行控制；在 Magisk 中，请将目标应用加入“配置排除列表”，同时保持“遵守排除列表”处于关闭状态。"
  - question: "为什么模块的目录名是 `zygisksu`？"
    answer: "Zygisk Next 的内部模块 ID 为 `zygisksu`，因此安装目录位于 `/data/adb/modules/zygisksu/`，运行时状态与诊断目录位于 `/data/adb/zygisksu/`。"
---

## 概述

由 **LSPosed Developers** 维护于 **Dr-TSNG/ZygiskNext** 的 **Zygisk Next**（`v1.5.3`）是一套独立于管理器的 Android **Zygisk** 模块注入实现（自 `v4-0.9.2` 起采用闭源专有许可）。

早期 Zygisk 强依赖于 Magisk 的主线构建与更新节奏。随着 KernelSU、APatch 等内核级 Root 方案普及以及应用层风控检测日益严苛，开发团队推出了 Zygisk Next，以独立的守护进程架构提供更隐蔽的注入隔离、WebUI 管理面板与跨管理器兼容能力。

---

## 技术架构与工作原理

### Zygote 进程分化拦截与守护架构

Zygisk Next 通过 `zygiskd` 守护进程直接接入 Android 应用孵化链路：

1. **启动前与服务阶段初始化**：在 `post-fs-data.sh` 阶段启动 `zygiskd daemon` 并在 `/data/adb/zygisksu/` 下管理状态上下文（轮转 `znctx` 与 `modules_info`）；随后在 `service.sh` 中执行 `zygiskd service-stage` 并部署 `/data/adb/service.d/.zn_cleanup.sh`。
2. **Zygote Fork 挂钩**：同时挂载 32 位与 64 位 Android Zygote 进程，拦截应用分化回调（`preAppSpecialize`、`postAppSpecialize`）。
3. **API 分发与扩展能力**：加载 `/data/adb/modules/*/zygisk/` 下的标准 Zygisk 模块，并额外支持 `zygisk_next_api.h` 面向早期系统进程的原生注入及 HyperOS Rust Runtime 回调。
4. **命名空间挂载隔离**：在敏感应用进入用户态前清理挂载命名空间，防止不可信进程通过 `/proc/mounts` 探测模块痕迹。

---

## 安装与配置步骤

1. 刷入前请核对 Root 管理器版本要求（`customize.sh` 不支持在 Recovery 中刷入）：
   - **KernelSU**：内核版本代码 `>= 10940` 且 `ksud >= 11575`（不可与 Magisk 共存）。
   - **APatch**：版本代码 `>= 10700`。
   - **Magisk**：版本代码 `>= 26402`，且必须在 Magisk 设置中将内置 **Zygisk** 与 **遵守排除列表（Enforce DenyList）** 均设为 **关闭**。
2. 从 `Dr-TSNG/ZygiskNext` 下载最新版 `Zygisk-Next-1.5.3-*.zip`。
3. 在 Root 管理器中刷入模块并重启设备。

---

## 日常使用与诊断

- **WebUI 管理**：在 KernelSU、APatch 或支持 WebUI 的 Magisk 管理器中打开 Zygisk Next WebUI，即可查看运行状态与调整隔离策略。
- **一键导出 Bugreport**：点击管理器的 **Action** 按钮将触发 `action.sh`，自动采集内核信息、`zygiskd status`、`znctx` 与日志并打包为 `ZygiskNext-bugreport-*.tar.gz`。

---

## 常见问题与排查

- **刷入时提示报错中止**：确认未在设备中同时存在 Magisk 与 KernelSU（KernelSU 下检测到 `PATH` 中存在 `magisk` 二进制会直接中止安装），并确认管理器版本达到最低要求。
- **Zygisk 模块未生效**：检查 Magisk 内置 Zygisk 是否已完全关闭，升级后重启一次设备，并通过 **Action** 生成 Bugreport 检查 `zygiskd status` 输出。
