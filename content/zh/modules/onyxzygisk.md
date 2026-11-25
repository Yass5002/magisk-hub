---
id: "onyxzygisk"
title: "OnyxZygisk：支持本地 WebUI 与热插拔 FN 模块的 Ptrace Zygisk 运行时"
sidebarTitle: "OnyxZygisk"
description: "不依赖内核的 Zygisk 实现，采用 ptrace Zygote 注入，提供免重启热插拔架构、内置 WebUI 与双层隐蔽排除列表。"
category: "root-management"
tier: 1
searchQueries:
  - "onyxzygisk magisk 模块"
  - "onyxzygisk ptrace zygote 注入"
  - "zygisk 免重启热插拔"
  - "onyxzygisk kernelsu apatch webui"
  - "functional node fn 模块 zygisk"
prerequisites:
  - "Android 8.1 至 Android 15+"
  - "通过 APatch、KernelSU（含 LKM 晚加载模式）或 Magisk 获取 Root 权限"
  - "无需专有内核补丁或定制内核模块"
conflicts:
  - "不可与其他独立 Zygisk 注入模块（如 ZygiskNext、NeoZygisk）同时启用"
configPaths:
  - "/data/adb/modules/OnyxZygisk/"
  - "/data/adb/onyx/"
features:
  - "通用 Ptrace 注入：通过标准 Linux ptrace 挂钩 Android Zygote 进程，无需内核级挂钩支持"
  - "零重启热插拔：无需重启 Android 系统即可实时启用、停用或重载 Zygisk 模块"
  - "Functional Node（FN）架构：支持声明式作用域模块扩展，在目标应用启动时即时生效"
  - "嵌入式 WebUI 控制台：基于 React、Vite 与 Tailwind 构建的丰富控制界面，直接在 Root 管理器内渲染，无需开放网络守护端口"
  - "双层隐蔽排除列表：结合 Zygote 文件系统卸载与 setns 挂载命名空间切换回退方案"
faq: []
---

## 概述

无论是 Magisk 官方内置的 Zygisk 还是借助内核辅助模块实现的方案，传统 Zygisk 运行时往往存在两大使用痛点：每当启用或停用模块时都需要重启整台设备，并且常常依赖特定内核特性或与某种 Root 方案深度绑定。

**OnyxZygisk** 将 Zygisk 运行时重构为跨平台、独立解耦的通用环境。它完全在用户态通过 Linux `ptrace` 系统调用向 Android Zygote 进程注入 API 桥接层，统一兼容 Magisk、KernelSU 与 APatch，并带来了动态热插拔、集成式本地 WebUI 以及新一代 Functional Node（FN）模块标准。

## 核心能力与架构设计

### 1. Ptrace 驱动的通用注入
由于 OnyxZygisk 依赖标准 Linux `ptrace` 原语拦截 Zygote 进程孵化，因此与底层 Root 实现完全解耦，全面支持：
- **Magisk**：替代自带 Zygisk，解锁模块免重启热插拔能力。
- **KernelSU 与 APatch**：即便在内核级 Zygote 挂钩可能延迟的晚加载（late-load）LKM 模式下也能稳定运行。

### 2. 免重启模块热插拔与 FN 节点
- **动态重载**：有别于传统 Zygisk 改动开关必须重启设备的限制，OnyxZygisk 允许用户实时切换已安装模块的启用状态，修改会在目标应用下次从 Zygote 孵化时立即生效。
- **FN（Functional Node）模块**：一种轻量级声明式扩展标准，无需编译完整的 Zygisk 二进制包即可将小型作用域挂钩挂载到单个应用沙盒中。

### 3. 双层隐蔽排除列表
为防止银行客户端或企业 MDM 等敏感应用探测到 Root 挂载与 Zygisk 挂钩，OnyxZygisk 构筑了多阶段隔离边界：
1. **Zygote 卸载**：在进程孵化阶段直接从进程挂载命名空间卸载模块目录与 Root 路径。
2. **命名空间切换（`setns`）**：针对更严苛的风控探测手段，在执行 Dalvik/ART 初始化代码前将进程切入未受污染的父级挂载命名空间。

### 4. 纯本地离线 WebUI
OnyxZygisk 内置基于 React、Vite 与 Tailwind CSS 构建的单页控制面板，可直接在 KernelSU 管理器、APatch 管理器或 MMRL 中渲染展示，全程完全离线运行，不启动本地 HTTP 服务器也不监听高风险网络端口。

## 安装与配置

1. 若使用 Magisk，请前往 **Magisk 设置**并关闭自带的 **Zygisk** 开关。
2. 若当前已安装其他 Zygisk 提供程序（如 ZygiskNext 或 NeoZygisk），请先停用或卸载以防注入冲突。
3. 通过你的 Root 管理器刷入 **OnyxZygisk** `.zip` 安装包。
4. 重启手机。
5. 在管理器的模块列表中打开 WebUI 界面，即可配置排除列表、检查活跃模块状态并实时查看 logcat 日志。

## 故障排查

- **与其他 Zygisk 引擎冲突**：若 Zygote 崩溃或陷入开机循环，请检查是否同时运行了第二个 Zygisk 注入器。
- **Ptrace 触发 SELinux 拒绝**：在策略极为严格的第三方 ROM 上，请确认你的 Root 管理器允许从 Root 域向 Zygote 进程域发起 ptrace 调用。
