---
id: "treat-wheel-zygisk"
title: "Treat Wheel (Zygisk)：高性能无痕 Root 隐藏与 ReVanced 挂载卸载引擎"
sidebarTitle: "Treat Wheel"
description: "基于纯 C99 开发的 Zygisk / ReZygisk 配套模块，提供低复杂度 Root 隐藏、动态挂载隔离及自动化 ReVanced 叠加挂载卸载（RVU）。"
category: "root-management"
tier: 1
searchQueries:
  - "Treat Wheel Zygisk 模块"
  - "PerformanC Treat-Wheel-Zygisk"
  - "ReZygisk Treat Wheel 隐藏"
  - "ReVanced 挂载卸载 RVU Magisk"
  - "Treat Wheel WebUI 配置"
prerequisites:
  - "Android 7.1 及以上系统"
  - "官方版 Magisk、符合 API 规范的官方版 KernelSU 或 APatch"
  - "ReZygisk build 508 及以上版本"
conflicts: []
configPaths:
  - "/data/adb/modules/treat_wheel/"
features:
  - "纯 C99 架构：无需加载臃肿的 C++ 运行时开销，内存占用极低且执行过程不留多余痕迹"
  - "ReVanced Umount（RVU）：依据模块化 `tw_config` 描述文件，动态探测并卸载 ReVanced 应用挂载点"
  - "现代化 WebUI 面板：内置支持多国语言的图形设置界面，可通过 KernelSU、APatch 或独立 WebUI 宿主打开"
  - "系统属性虚拟化：提供简洁且契合 Bionic 规范的系统属性操控例程"
---

## 概述

由 PerformanC 组织成员 ThePedroo 开发的 Treat Wheel 是一款严格遵循 C99 标准编写的轻量通用型 Zygisk 模块。该模块专为配合 ReZygisk（508 及以上构建版本）协同运行而设计，摒弃繁杂抽象层，提供高速、无痕的 Root 隐藏与进程隔离能力。

其核心亮点是 ReVanced Umount（RVU）子系统——它能够自动扫描整个 Root 环境中的模块配置，并在目标应用的挂载命名空间内清理叠加挂载记录，防止反篡改检测逻辑识别出经过修补的 APK 结构。

## 前置条件与兼容性

Treat Wheel 对运行环境设置了明确的技术前提以保证稳定性：

- **Android 版本**：Android 7.1（Nougat，API 25）及以上。
- **Root 环境**：官方版 Magisk、符合规范的 KernelSU 或 APatch。
- **Zygisk 实现**：**必须使用 ReZygisk build 508 及以上版本**。Treat Wheel 深度依赖 ReZygisk 专有的守护进程绑定接口与内存保护机制。

只要满足上述 ReZygisk 版本要求，目前无已知模块冲突。

## 核心能力与技术架构

### ReVanced Umount（RVU）

常规 Root 版 ReVanced 模块通常将修补后的 APK 直接绑定挂载覆盖到原厂 `/system` 或 `/data` 应用安装路径上。虽然功能正常，但这些绑定挂载点很容易被反篡改安全组件枚举发现。

Treat Wheel 通过 RVU 彻底解决这一问题。只要已安装的 ReVanced 模块提供了如下 `tw_config` 描述文件：
```properties
module_type=revanced
allow_umount=true
```
Treat Wheel 便会自动发现挂载点、统计预期的叠加层数量，并在非必要应用命名空间中将其卸载分离，使受保护的应用无法察觉已挂载的 APK 修改痕迹。

### 无痕原生核心组件

Treat Wheel 的原生 C 组件在编译阶段针对最小化 ELF 符号与内存残留进行了专门优化：
- `rz_daemon`：负责在 Zygisk 挂钩与 Root 命名空间之间执行后台协同调度。
- `hiding.c`：实现内存命名空间隔离例程。
- `system_properties`：内置安全的 Android 属性上下文管理逻辑，修改属性时不触发安全告警。

## WebUI 界面与配置

Treat Wheel 自带完整的 WebUI 控制面板，模块目录位于：
```bash
/data/adb/modules/treat_wheel/
```
你可以直接在 KernelSU 与 APatch 管理器中打开该界面，或在 Magisk 环境下配合 KSUWebUIStandalone、MMRL 等独立 WebUI 工具使用。面板内提供 RVU 开关、命名空间隔离配置项以及多语言本地化支持（包含英语、德语、西班牙语、波兰语、俄语、中文、越南语等）。

## 故障排查与常见误区

- **模块未能成功挂钩**：请确认当前已安装并激活 ReZygisk build 508+。由于缺少必需的守护进程接口，Treat Wheel 无法在传统旧版 Zygisk 实现上运行。
- **ReVanced 应用依然检测到挂载**：请检查对应的 ReVanced 模块目录（`/data/adb/modules/<module_name>/tw_config`）中是否包含格式正确的 `tw_config` 属性文件。若缺少该文件，Treat Wheel 将不会把该模块纳入自动卸载列表。
