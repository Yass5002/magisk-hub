---
id: "meta-overlayfs-kernelsu"
title: "KernelSU 专用 OverlayFS 元模块（OverlayFS MetaModule）"
description: "专为 KernelSU 与 APatch 打造的新一代 OverlayFS 元模块引擎，提供高性能无系统分区修改（Systemless）文件挂载、实时内核状态检查与原生 WebUI。"
category: "system-environment"
author: "AshBorn & KernelSU Devs"
version: "1.3.4"
updatedAt: "2026-10-04"
compatibility: ["KernelSU", "APatch"]
sidebarTitle: "OverlayFS MetaModule"
tier: 1
searchQueries: []
prerequisites: []
conflicts: []
configPaths: []
features: []
faq: []
---

## 概述与系统架构

**OverlayFS MetaModule**（`meta-overlayfs`）由 AshBorn（@Ripper_Hybrid）与 KernelSU 开发社区联合打造，是专为 KernelSU 与 APatch 设计的核心基础设施元模块（Metamodule）。

传统的 Magisk 模块依赖 `magic mount`（跨文件系统节点创建大量绑定挂载循环），不仅可能带来挂载开销与 inode 耗尽风险，也更容易被高阶完整性校验机制检测到异常。OverlayFS MetaModule 则直接利用 Linux 内核原生的 `overlayfs` 驱动，在虚拟文件系统（VFS）层透明地将模块目录合并挂载至系统分区。

## 核心架构优势

1. **原生 VFS 叠加挂载**：原生整合 `upperdir` 与 `lowerdir` 挂载层级，无需生成成百上千个独立的回环绑定挂载点。
2. **卓越 I/O 性能**：相比多层绑定挂载方案，文件检索与读取的额外开销几乎为零。
3. **集成 WebUI 管理面板**：支持直接在 KernelSU 管理器内打开内置 WebUI，实时检视挂载状态并排查模块冲突。
4. **规范化的元模块生命周期**：完整实现了 `metamount.sh`、`metainstall.sh` 与 `metauninstall.sh` 标准化生命周期钩子脚本。

## 安装与验证

### 第一步：刷入元模块
通过 KernelSU 或 APatch 管理器刷入 `meta-overlayfs_v1.3.4_13400.zip`。

### 第二步：验证 Overlay 挂载生效状态
重启设备后，在终端检查 `overlay` 文件系统是否已成功挂载：
```bash
mount | grep -i overlay
```

### 第三步：通过 KernelSU WebUI 检视状态
依次进入 **KernelSU 管理器 > 模块 > OverlayFS Enhanced > WebUI**，即可实时查看所有无侵入式分区合并挂载的运行状态。

## 兼容性与环境要求

- **Linux 内核**：要求 Linux 内核版本 4.9 及以上，且内核配置开启 `CONFIG_OVERLAY_FS=y`。
- **Root 管理器**：严格面向 KernelSU 与 APatch 设计；标准 Magisk 已内置自研 magic mount 实现，无需且不可用于 Magisk 环境。
