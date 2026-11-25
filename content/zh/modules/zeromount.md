---
id: "zeromount"
title: "ZeroMount：面向 Root Android 的无挂载 VFS 模块加载引擎"
sidebarTitle: "ZeroMount"
description: "由 Enginex0 开发的进阶挂载编排引擎，通过拦截内核 VFS getname() 调用实现零挂载表污染的 Root 模块加载，并深度集成 SUSFS 隐匿机制。"
category: "root-management"
tier: 1
searchQueries:
  - "zeromount android root 模块"
  - "enginex0 zeromount 下载配置"
  - "kernelsu 无挂载模块加载器"
  - "内核 vfs getname 路径重定向"
  - "zeromount susfs 集成隐藏"
prerequisites:
  - "已通过 KernelSU、APatch 或 Magisk 获取 Root 权限的 Android 设备"
  - "支持 VFS 重定向或具备 SUSFS 补丁的 Linux 内核（用于启用 Tier 1 VFS 无挂载模式）"
conflicts: []
configPaths:
  - "/data/adb/modules/zeromount/"
features:
  - "内核级 VFS 重定向：在 `getname()` 阶段拦截文件系统路径解析，直接将文件请求转向模块存储目录而无需生成挂载表条目"
  - "三级降级编排策略：根据内核特性自动在 VFS（无挂载）→ OverlayFS（叠加挂载）→ MagicMount（绑定挂载）之间切换"
  - "零挂载表痕迹：让 `/proc/mounts`、`/proc/self/mountinfo` 与 `/proc/self/mountstats` 保持完全纯净，与官方原厂 ROM 状态一致"
  - "全面集成 SUSFS：协同 SUSFS 实现 `kstat` 属性伪装、`/proc/maps` 清理与路径隐藏"
  - "交互式 WebUI 控制台：实时监控挂载引擎状态、按模块配置加载策略以及查阅启动日志"
faq: []
---

## 概述

由 Enginex0 开发的 **ZeroMount** 革新了 Root Android 环境下无系统分区修改（Systemless）模块的加载方式。传统 Root 框架（如 Magisk 与原生 KernelSU）高度依赖 Linux 绑定挂载（Bind Mount）或 OverlayFS 层。虽然功能有效，但这些挂载操作会在 `/proc/mounts`、`/proc/self/mountinfo` 与 `/proc/self/mountstats` 中留下明显痕迹。现代防篡改系统与银行风控引擎只需扫描挂载表中的异常文件系统叠加记录，就能轻松检测出 Root 环境。

ZeroMount 从根源上消除了挂载污染。通过定制内核驱动配合高性能 Rust 用户态守护进程，ZeroMount 在 Linux 虚拟文件系统（VFS）的 `getname()` 层执行拦截。当应用或系统进程查询文件路径时，内核会在文件系统正式处理请求*之前*将其读取重定向至模块目录。所有模块均能正常加载，同时系统挂载表保持 100% 原厂纯净。

## 前置要求与兼容性

- **Root 环境**：KernelSU、APatch 或 Magisk。在搭配 GKI 内核或合入 SUSFS 补丁源码的 KernelSU 环境下，可充分释放 VFS 无挂载重定向的全部能力。
- **架构支持**：ARM64（`aarch64`）。

目前没有已知的模块冲突。ZeroMount 可与现有 Root 模块协同工作，并自动识别配套的安全隐匿层。

## 三级挂载策略（Three-Tier Mount Cascade）

ZeroMount 会在开机时自动探测内核能力，并选择最优的模块加载策略：

1. **Tier 1：VFS 重定向（首选模式）**：
   - 模块文件直接在内核 VFS 层完成路径重定向。
   - 挂载表中不产生任何条目。
   - 目录项注入机制确保 `readdir()` 与 `ls` 将覆盖后的文件显示为原生系统文件。
   - 动态对齐 SELinux 安全上下文，避免触发 AVC 拒绝日志。
2. **Tier 2：OverlayFS（自动降级）**：
   - 当内核缺少定制 VFS 重定向挂钩时启用。
   - 利用 Overlay 文件系统挂载，并应用 SUSFS 隐匿层隐藏 Overlay 挂载点。
3. **Tier 3：MagicMount（兜底方案）**：
   - 当 OverlayFS 也不可用时，回退至传统的逐文件绑定挂载级联方案。

用户还可以在 WebUI 中为特定模块单独覆写策略，从而为具有特殊加载要求的模块强制指定加载模式。

## 安装与配置

1. 从项目仓库下载最新的 `ZeroMount-*.zip` 发布包。
2. 通过 KernelSU、APatch 或 Magisk 刷入模块。
3. 重启设备。
4. 在 Root 管理器中打开 **ZeroMount WebUI**：
   - 查看所有已安装模块当前使用的挂载策略。
   - 配置 SUSFS 隐匿特性（`kstat` 伪装、`/proc/maps` 隐藏）。
   - 检查启动管线健康状态，确认挂载无任何泄漏。
5. 模块二进制文件与配置状态存放于：
   ```bash
   /data/adb/modules/zeromount/
   ```

## 故障排查与验证

- **验证挂载表纯净度**：在无 Root 权限的普通 Shell 终端中执行以下命令，确认未暴露任何模块挂载点：
  ```bash
  cat /proc/self/mountinfo | grep -E "adb|modules"
  # 在 VFS 重定向模式下应返回空结果
  ```
- **触发了降级模式**：若 WebUI 显示 ZeroMount 降级到了 OverlayFS 或 MagicMount，说明当前内核缺少所需的 VFS 挂钩。请刷入兼容的第三方内核或合入 SUSFS 补丁以启用 Tier 1 无挂载重定向。
