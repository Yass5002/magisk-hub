---
id: "meta-magic-mount-rs"
title: "Magic Mount-rs：基于 Rust 的无系统分区挂载元模块"
sidebarTitle: "Magic Mount RS"
description: "由 Tools-cx-app 开发的 Rust 原生元模块（Metamodule），为 KernelSU 与 APatch 提供高性能 Magic Mount 文件叠加、自定义绑定规则与 WebUI 配置。"
category: "root-management"
tier: 1
searchQueries:
  - "Magic Mount-rs 元模块下载"
  - "meta-magic_mount-rs 教程"
  - "KernelSU 元模块 Magic Mount"
  - "APatch Metamodule 挂载器"
  - "自定义 bind 挂载规则"
prerequisites:
  - "支持元模块（Metamodule）机制的 KernelSU 或 APatch（主要目标平台；Magisk 已内置 Magic Mount）"
  - "支持架构：arm64-v8a、armeabi-v7a、x86_64 或 riscv64"
conflicts:
  - "其他同时接管全局模块文件系统挂载的元模块（如 meta-overlayfs 或处于元模块模式的 Mountify）"
configPaths:
  - "/data/adb/magic_mount/config.toml"
  - "/data/adb/magic_mount/custom"
  - "/data/adb/modules/magic_mount_rs/"
features:
  - "Rust 原生二进制：内置适配 arm64-v8a、armeabi-v7a、x86_64 与 riscv64 的 `magic_mount_rs` 可执行文件"
  - "完整元模块生命周期：实现 `metainstall.sh`、`metamount.sh` 与 `metauninstall.sh`，并在安装时进行 SHA-256 校验"
  - "自定义规则引擎：支持 `ignore`、`bind` 与外部规则文件引入，无需重新打包完整模块"
  - "内置 WebUI 面板：通过 `webroot/` 可视化编辑 `config.toml` 并查看当前挂载状态"
  - "双环境默认模板：分别提供适配 KernelSU 的 `config.toml` 与适配 APatch 的 `config_apatch.toml`"
faq:
  - question: "为什么 KernelSU 和 APatch 需要额外安装元模块（Metamodule）？"
    answer: "不同于将 Magic Mount 逻辑硬编码进 `init` 的传统 Magisk，现代 KernelSU 与 APatch 将模块文件系统的挂载职责解耦给了可插拔的元模块，让用户自由选择 OverlayFS 或 Magic Mount 实现。"
  - question: "Magic Mount-rs 可以在 Magisk 上使用吗？"
    answer: "Magisk 本身已内置原生 Magic Mount 引擎，且 `meta-magic_mount-rs` 的 `customize.sh` 在安装阶段会检查 `$KSU` 或 `$APATCH` 环境变量，因此该元模块主要面向 KernelSU 与 APatch。"
  - question: "自定义绑定规则如何使用？"
    answer: "在 `/data/adb/magic_mount/custom` 中编写规则后，无需将零散文件单独打包为完整模块，即可执行针对特定路径的忽略或只读绑定挂载。"
---

## 概述

由 **Tools-cx-app** 开发的 **Magic Mount-rs**（`v4.1.12`，模块 ID 为 `magic_mount_rs`，声明 `metamodule=1`）是一款使用 **Rust** 重写 Magisk 经典 Magic Mount 无系统分区挂载逻辑的独立元模块。

**KernelSU** 与 **APatch** 专注于内核级 Root 授权与命名空间隔离，并不将具体的文件叠加方式强制绑定在内核中。Magic Mount-rs 作为系统挂载协调者，负责模块安装路径规范化（`metainstall.sh`）、早期启动挂载（`metamount.sh`）以及卸载清理（`metauninstall.sh`）。

---

## 技术架构与工作原理

### Rust 元模块挂载引擎

Magic Mount-rs 在 Android 启动早期完成系统级无侵入式文件挂载：

1. **SHA-256 校验安装（`customize.sh` + `verify.sh`）**：校验当前运行环境为 KernelSU 或 APatch，按设备 ABI 释放对应的 `magic_mount_rs`（支持 `arm64-v8a`、`armeabi-v7a`、`x86_64`、`riscv64`）并逐一校验 `.sha256` 摘要。
2. **分区软链接规范化（`metainstall.sh`）**：导出 `KSU_HAS_METAMODULE="true"`（`KSU_METAMODULE="mmrs"`），自动识别自带挂载逻辑的阻断名单模块并创建 `skip_mount`，同时在 `/system/{vendor,product,system_ext}` 为符号链接时自动整理模块目录层级。
3. **启动挂载与状态通知（`metamount.sh`）**：调用原生 Rust 挂载二进制，并在退出码为 `0` 时执行 `/data/adb/ksud kernel notify-module-mounted` 通知管理器模块已就绪。
4. **WebUI 与软重启辅助**：内置 `webroot/` 管理页面以及 `emulated-soft-reboot.sh` 辅助脚本。

---

## 安装与配置步骤

1. 确认设备正在运行支持元模块的 **KernelSU** 或 **APatch**（如之前安装了其他元模块，请先卸载）。
2. 从 `Tools-cx-app/meta-magic_mount-rs` 下载 `magic_mount_rs-4.1.12-959-universal.zip`。
3. 在 Root 管理器中刷入该模块。
4. 重启设备使元模块接管挂载流程。

---

## 配置文件说明

主配置文件位于 `/data/adb/magic_mount/config.toml`（APatch 模板 `config_apatch.toml` 默认使用 `mountsource = "APatch"`）：

```toml
mountsource = "KSU"
umount = false
partitions = []
extra_mount = []
```

- **`mountsource`**：挂载源标识（如 `"KSU"` 或 `"APatch"`）。
- **`umount`**：控制是否针对目标普通应用执行挂载点卸载。
- **`partitions` 与 `extra_mount`**：配置需要参与挂载的扩展分区（如 `mi_ext`、`my_stock`）及自定义挂载项。

---

## 常见问题与排查

- **提示 `! unsupported root platform` 中止安装**：`customize.sh` 仅允许在 KernelSU 或 APatch 环境中刷入，请勿在 Magisk 或 Recovery 中强行安装。
- **自定义规则挂载失败**：确认 `/data/adb/magic_mount/custom` 中的目标路径均为合法绝对路径，且不包含 `..` 相对路径片段。
