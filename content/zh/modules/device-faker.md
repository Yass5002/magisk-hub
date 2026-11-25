---
id: "device-faker"
title: "Device Faker：精细化分应用机型与硬件身份伪装模块"
sidebarTitle: "Device Faker"
description: "基于 Rust 构建的高性能 Zygisk 模块，支持按应用粒度进行设备型号伪装与硬件身份隐匿，并提供现代化 WebUI 控制界面。"
category: "security-certificates"
tier: 1
searchQueries:
  - "device faker magisk 模块"
  - "seyud device faker 教程"
  - "zygisk 机型伪装模块"
  - "android 分应用修改设备型号"
  - "device faker config.toml 配置"
prerequisites:
  - "启用 Zygisk 的 Magisk（v24+）、搭配 ZygiskNext 的 KernelSU（v0.7+）或 APatch"
conflicts:
  - "其他同时修改相同系统属性命名空间的 Zygisk 机型伪装模块"
configPaths:
  - "/data/adb/modules/device_faker/"
  - "/data/adb/device_faker/config/config.toml"
features:
  - "采用 Rust 基于原生 Zygisk API 编写，运行时开销极低且零常驻内存负担"
  - "分应用精细化控制：仅针对选定应用伪装设备属性，完全不影响系统全局稳定性"
  - "写时复制（COW）属性引擎：利用 `mmap` COW 内存映射技术实现进程隔离的系统属性读取"
  - "内置现代化 WebUI：支持机型模板管理、应用列表开关与实时参数配置"
  - "配置即时重载：修改配置后只需重启目标应用即可生效，无需重启手机"
faq:
  - question: "Device Faker 会永久修改我的全局系统属性吗？"
    answer: "不会。Device Faker 采用基于内存的写时复制（COW）属性伪装引擎。系统属性（如 `ro.product.model` 或 `ro.product.brand`）仅在目标应用进程隔离的内存空间内被替换，Android 全局系统与其他未配置应用均保持原厂状态不变。"
  - question: "每次更换伪装机型模板都需要重启设备吗？"
    answer: "不需要重启设备。在 WebUI 中更新配置或手动修改 `config.toml` 后，只需强行停止并重新启动目标应用，新的机型配置即可立即生效。"
---

## 概述

由 **Seyud** 开发的 **Device Faker** 是一款开源、高性能的 **Rust 语言编写的 Zygisk 模块**，专为实现分应用粒度的设备型号与硬件身份伪装而设计。

许多特定应用（如高帧率大型手游、厂商相机套件、流媒体平台与硬件检测工具）会将高画质预设、HDR 播放或独占功能限制在特定机型白名单内（例如要求 Galaxy S24 Ultra、iPad Pro 或 ROG Phone 型号标识）。与其直接修改全局 `build.prop` 参数——这极易引发全局系统不稳定或破坏厂商底层服务——Device Faker 允许你为每个目标应用独立分配自定义的硬件配置模板。

---

## 技术架构与工作原理

- **Zygisk 注入**：在应用进程从 Zygote Fork 启动时通过原生 Zygisk API（`zygisk-api-rs`）提前介入，先于应用自身初始化逻辑完成注入。
- **写时复制（COW）属性伪装**：Device Faker 摒弃了脆弱的用户态 Hook 方案，转而为目标进程创建系统属性内存区域的私有 `mmap` 写时复制（Copy-On-Write）副本。当应用调用 `__system_property_get` 或 `__system_property_read` 读取属性时，只会获取到伪装值，操作系统其余部分毫发无损。
- **统一执行流**：自动协同 JNI 字段伪装（`android.os.Build` 静态字段）、COW 系统属性替换与伴侣守护进程服务，无需用户手动切换注入模式。
- **TOML 配置引擎**：所有规则设置与机型模板均以结构清晰的 TOML 格式保存在 `/data/adb/device_faker/config/config.toml`。

---

## WebUI 管理界面

Device Faker 内置现代化的 WebUI，原生支持多语言界面（英文、简体中文、土耳其语）：

- **模板管理**：创建、编辑并维护常用硬件配置模板（如 Pixel 9 Pro XL、Xiaomi 14 Ultra、ASUS ROG Phone 8），并可一键分配给多个应用。
- **应用管理**：列出全部已安装软件包（涵盖多用户与工作资料应用），支持逐一开启或关闭机型伪装。
- **配置编辑器**：同时提供可视化图形配置面板与原始配置文件直编模式，满足高级参数调优需求。

---

## 安装与配置

1. 确认你的 Root 环境已开启有效的 Zygisk 支持：
   - **Magisk**：在 Magisk 设置中开启 **Zygisk**。
   - **KernelSU / APatch**：安装并启用 **ZygiskNext** 模块。
2. 从官方发布页下载最新的 `device_faker.zip` 压缩包。
3. 在 Root 管理器（Magisk、KernelSU 或 APatch）中刷入该模块并重启设备。
4. 通过 KernelSU / APatch 的 WebUI 管理器打开 **WebUI**，或直接编辑 `/data/adb/device_faker/config/config.toml`。
5. 为目标应用分配所需的机型模板，强行停止并重新打开目标应用即可生效。
