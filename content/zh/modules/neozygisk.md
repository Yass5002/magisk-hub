---
id: "neozygisk"
title: "NeoZygisk：基于 Ptrace 的轻量级 Zygote 注入与隐蔽隔离框架"
sidebarTitle: "NeoZygisk"
description: "极简设计的 ptrace Zygote 注入框架，完整兼容 Zygisk API，同时提供干净的命名空间卸载与内存痕迹清理能力。"
category: "root-management"
tier: 1
searchQueries:
  - "neozygisk magisk 模块"
  - "neozygisk kernelsu apatch"
  - "安卓 ptrace zygote 注入"
  - "neozygisk denylist 命名空间卸载"
  - "jingmatrix neozygisk 下载"
prerequisites:
  - "KernelSU、APatch 或 Magisk"
conflicts:
  - "Magisk 内置的「遵守排除列表（Enforce DenyList）」选项（必须关闭，否则会引发命名空间冲突与隔离失效）"
  - "Magisk 内置 Zygisk 功能（使用独立 NeoZygisk 时必须在 Magisk 设置中关闭自带 Zygisk）"
configPaths:
  - "/data/adb/modules/neozygisk/"
  - "Per-application 'Umount modules' toggles in KernelSU / APatch Manager"
  - "Configure DenyList menu in Magisk"
features:
  - "基于 Ptrace 的 Zygote 注入：在 Linux 系统调用层挂钩 Android zygote 进程，无需修改磁盘上的 zygote 二进制文件"
  - "彻底的痕迹清理：模块执行完毕后立即清除所有注入残留并卸载加载器内存映射"
  - "Zygote 直接卸载：在应用进程 fork 前尝试直接在 Zygote 内部卸载 Root 相关挂载点"
  - "命名空间切换回退：通过 setns 系统调用将目标应用切换至纯净的缓存挂载命名空间"
  - "完整 Zygisk API 兼容：在 APatch 与 KernelSU 上无缝运行为 Magisk 设计的标准 Zygisk 模块"
faq:
  - question: "为什么使用 NeoZygisk 时必须关闭 Magisk 的「遵守排除列表」？"
    answer: "Magisk 的「遵守排除列表」会运行独立的挂载隐藏守护进程，与 NeoZygisk 的命名空间隔离机制产生冲突。NeoZygisk 会自动读取 Magisk「配置排除列表」中的目标包名，但若同时开启 Magisk 自身的强制执行引擎，会导致挂载状态互相打架。"
  - question: "NeoZygisk 如何向银行应用隐藏 Root 与模块挂载？"
    answer: "NeoZygisk 会先尝试在应用特化（Specialization）之前，直接从 Zygote 进程中干净地卸载 Root 叠层挂载。若直接卸载可能影响关键系统资源，则会退回使用 fork 后调用 setns 的方案，将应用进程切换进一个完全纯净、隔离的 Linux 挂载命名空间，使进程视图中不存在任何 Root 或叠层文件系统节点。"
---

## 概述

**NeoZygisk** 由 **JingMatrix** 开发，是面向 **APatch**、**KernelSU** 与 **Magisk** 的高性能极简 Android Zygisk API 实现。

与容易产生可检测特征的侵入式框架 Hook 或守护进程封装不同，NeoZygisk 直接利用 Linux 原生的 `ptrace` 系统调用向 Android `zygote` 进程干净地注入代码。它在保证第三方 Zygisk 模块完整 API 兼容性的同时，将内存清理与 Root 隐藏作为核心设计目标。

---

## 技术架构与工作原理

### Ptrace 注入与双层排除列表隔离

NeoZygisk 基于四项核心原则运行：

1. **Ptrace 系统调用附加**：NeoZygisk 在运行时通过 `ptrace` 附加至 32 位与 64 位 Zygote 守护进程，在不修改磁盘上的 zygote 二进制文件的前提下完成模块加载器注入。
2. **加载后痕迹清理**：所有已注册的 Zygisk 模块在进程初始化阶段执行完毕后，NeoZygisk 会立即解除加载器内存映射、清理内存描述符，并抹除自身在目标应用 `/proc/[pid]/maps` 中的全部踪迹。
3. **主隔离策略（Zygote 直接卸载）**：对于列入排除列表的应用，NeoZygisk 会在应用进程完成特化*之前*，尝试直接从 Zygote 进程中卸载 Root 与模块文件系统叠层。若某处叠层承担了关键系统资源供给（例如 `/product` 运行时依赖），系统会自动跳过该步以确保稳定运行。
4. **回退隔离策略（命名空间切换）**：出于安全性跳过直接卸载时，NeoZygisk 会在 `fork` 后立即调用 `setns` 系统调用，将子应用进程切换至预先缓存的隔离 Linux 挂载命名空间中，使其看到的系统分区视图保持原生无修改状态且不存在任何模块挂载。

---

## 安装与配置

### 1. 刷入模块
1. 从项目官方发布页下载最新的 `NeoZygisk-v*.zip`。
2. 在你的 Root 管理器（Magisk、KernelSU 或 APatch）中刷入该模块。
3. 如果你正在使用 **Magisk**：
   - 打开 Magisk 设置，确保关闭内置 **Zygisk** 开关（避免两个 Zygisk 引擎同时运行产生冲突）。
   - 确保关闭**遵守排除列表（Enforce DenyList）**。
4. 重启设备。

---

## 实战配置与使用

向敏感应用隐藏 Root 与模块的操作直接通过 Root 管理器原生界面完成：

- **APatch 或 KernelSU 用户**：打开管理器应用，在应用列表中找到目标应用并开启**卸载模块（Umount modules）**开关。
- **Magisk 用户**：打开 Magisk，进入**配置排除列表（Configure DenyList）**，勾选目标应用及其名下所有独立子进程。请勿在设置中开启「遵守排除列表」。

配置完成后，NeoZygisk 会在所选应用启动时自动将其隔离在纯净的挂载命名空间内。

---

## 故障排查与常见问题

- **银行应用仍然检测到 Root**：请确认排除列表中已勾选目标应用的全部子进程（例如独立后台服务或辅助进程），并检查是否已关闭 Magisk 内置的「遵守排除列表」，避免与 NeoZygisk 命名空间隔离发生冲突。
- **Zygisk 模块未加载**：请确认目标模块已针对设备 Zygote 进程架构（`arm64-v8a` 或 `armeabi-v7a`）编译，并在 Root 管理器中核对 NeoZygisk 处于已启用状态。
