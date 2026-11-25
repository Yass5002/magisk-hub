---
id: "vexzygisk"
title: "VexZygisk：内置自定义链接器的纯 C 独立 Zygisk 运行时"
sidebarTitle: "VexZygisk"
description: "专为 KernelSU 与 APatch 打造的纯 C 独立 Zygisk 运行时，集成自定义 csoloader 动态链接器以抵御反作弊与 Root 检测。"
category: "root-management"
tier: 1
searchQueries:
  - "VexZygisk KernelSU 下载"
  - "Lxiaoyao077 VexZygisk"
  - "ReZygisk 纯 C 重写版"
  - "csoloader Zygisk 隐藏过检测"
  - "APatch 独立 Zygisk 模块"
prerequisites:
  - "已通过 KernelSU 或 APatch 获取 Root 权限"
conflicts:
  - "其他独立 Zygisk 实现（例如 Zygisk Next 或 ReZygisk）"
configPaths:
  - "/data/adb/modules/vexzygisk/"
features:
  - "纯 C 引擎：从零采用现代纯 C 重写，彻底剔除 C++ 标准库依赖并缩减二进制体积"
  - "自定义 `csoloader` 动态链接器：绕过系统链接器，直接将标准 Zygisk 模块库映射至应用地址空间"
  - "隐匿防检测设计：有效规避现代移动端反作弊引擎对链接器符号表与已加载库的扫描"
  - "双路径模块加载：标准 Zygisk 模块交由 `csoloader` 加载，同时为 Zygisk Next 专属模块保留系统链接器通道"
  - "零 Fork 延迟：在 Zygote 派生应用进程时实现近乎瞬时的注入，内存与 CPU 开销极低"
---

## 概述

在 KernelSU 与 APatch 生态中，要将 Zygisk 模块支持引入 Android 应用生命周期，必须依赖独立的 Zygisk 注入守护进程。然而，许多传统 Zygisk 实现会直接调用 Android 标准系统动态链接器（`/linker` 或 `/linker64`）加载第三方 `.so` 模块库。由于安全扫描程序与反作弊系统常会检查动态链接器的内部命名空间以及 `/proc/self/maps` 内存映射区域，经系统链接器加载的模块极易暴露行踪。

由 Lxiaoyao077 开发（衍生自 ReZygisk）的 **VexZygisk** 是一款完全采用纯 **C** 语言重写的进阶独立 Zygisk 实现。它引入了自研自定义动态加载器（**csoloader**），专门用于从根源上瓦解基于链接器特征的 Root 检测。

## 核心架构创新

### 1. 纯 C 代码基座
通过彻底移除 C++ 标准模板库（`libc++_shared.so`）与相关运行时依赖，VexZygisk 产出的二进制文件体积显著更小，在 Zygote 派生进程阶段具备更低的内存开销以及更紧凑的 CPU 缓存局部性。

### 2. `csoloader` 自定义链接器
当应用进程从 Android Zygote 守护进程 Fork 派生时：
- **标准 Zygisk 模块**：VexZygisk 不再通过 Android Bionic 链接器调用 `dlopen()`，而是由 `csoloader` 手动完成 ELF 二进制文件的内存映射与重定位。此举可绕过针对系统链接器的挂钩监控，令常规链接器检查 API 无法探测已加载的模块库。
- **Zygisk Next 模块**：针对依赖官方系统链接器 ABI 契约的模块，仍保留标准加载通道，确保对整个模块生态实现 100% 兼容。

### 3. 按 Root 方案独立编译
VexZygisk 不再打包臃肿的通用兼容脚本，而是分别针对 KernelSU 与 APatch 编译专属优化的独立构建包。

## 安装与冲突警示

- **重要冲突提示**：**切勿**将 VexZygisk 与其他 Zygisk 提供方（如 Zygisk Next 或 ReZygisk）同时运行。刷入前请先禁用或卸载现有的 Zygisk 模块。
- **安装步骤**：
  1. 从 GitHub 发布页下载适配对应 Root 方案的最新版 `VexZygisk-*.zip`。
  2. 在 **KernelSU** 或 **APatch** 中刷入模块。
  3. 重启设备。
  4. 刷入后，常用的 Zygisk 模块（如 LSPosed、PlayIntegrityFix、Shamiko 等）即可正常加载运行。
