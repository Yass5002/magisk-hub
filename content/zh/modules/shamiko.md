---
id: "shamiko"
title: "Shamiko：高隐蔽性 Zygisk Root 与挂载信息隐藏模块"
sidebarTitle: "Shamiko"
description: "由 LSPosed 团队开发的闭源 Root 隐藏模块，用于向银行软件与风控检测机制全面隐匿 Magisk、KernelSU 及 Root 痕迹。"
category: "root-management"
tier: 1
searchQueries:
  - "Shamiko 模块下载"
  - "如何安装配置 Shamiko"
  - "Shamiko 白名单模式开启教程"
  - "Shamiko 与 Magisk 排除列表区别"
  - "银行软件隐藏 Root Shamiko"
prerequisites:
  - "开启 Zygisk 的 Magisk 26.0+，或搭配 Zygisk Next 的 KernelSU / APatch"
  - "必须在 Magisk 设置中关闭“遵守排除列表（Enforce DenyList）”（Shamiko 会直接读取该列表）"
conflicts:
  - "同时开启 Magisk 的“遵守排除列表”（会导致钩子与挂载逻辑冲突）"
configPaths:
  - "/data/adb/shamiko/whitelist"
  - "/data/adb/modules/shamiko/"
features:
  - "深度 Root 环境隐匿（隐藏 `su` 二进制文件、Magisk 挂载点与被修改的 `init` 进程痕迹）"
  - "支持黑名单模式（仅对选中应用隐藏）与白名单模式（全局隐藏，仅向授权应用开放 Root）"
  - "强化 `ptrace` 与内存扫描防护，有效应对反作弊及银行安全加固 SDK"
  - "可绕过 Native Root Checker、Momo 及 Riru/Zygisk 特征探针检测"
faq:
  - question: "为什么使用 Shamiko 必须在 Magisk 中关闭“遵守排除列表”？"
    answer: "如果开启了“遵守排除列表”，Magisk 会在任何模块运行之前就把目标进程中的 Zygisk 彻底卸载，导致 Shamiko 根本无法加载进目标进程。关闭该选项后，Zygisk 才能先载入 Shamiko，由 Shamiko 完成更精细的动态环境清洗后再自行脱离内存。"
  - question: "如何将 Shamiko 切换为白名单模式？"
    answer: "只需在 `/data/adb/shamiko/` 目录下创建一个名为 `whitelist` 的空文件即可：`su -c 'touch /data/adb/shamiko/whitelist'`。开启白名单模式后，系统默认对所有应用隐藏 Root，仅对明确未勾选的应用暴露环境。"
---

## 概述

由 **LSPosed 开发团队** 打造的 **Shamiko** 是当前 Android 生态中隐蔽性最高的 Root 隐藏方案之一。Magisk 原生排除列表仅仅是将 `tmpfs` 挂载从目标进程卸载，而现代银行客户端、游戏反作弊引擎以及商业安全加固 SDK（如 Promon、DexGuard、SecNeo）会深入检查内核挂载命名空间、扫描 `/proc/self/mountinfo`、探测 `/dev/pts` 描述符并分析系统调用耗时。

Shamiko 依托 Zygisk 在 Zygote 阶段切入应用生命周期，能够在原生代码执行前动态抹除 `su` 可执行文件痕迹、隐藏 Magisk 回环挂载点、伪装 SELinux 状态并清理泄露的文件描述符。

---

## 技术架构与工作原理

### 进程启动前隐身拦截链

1. **Zygote 注入**：当 Android Zygote 收到创建新应用进程的 fork 请求时，Shamiko 会在初始化阶段拦截执行流。
2. **读取排除列表**：即使 Magisk 设置中关闭了“遵守排除列表”，Shamiko 依然会直接读取 Magisk SQLite 数据库（`/data/adb/magisk.db`）中的目标包名清单（在 KernelSU/APatch 中则读取对应管理器的卸载列表）。
3. **命名空间与挂载清洗**：若新启动的应用命中隐藏规则，Shamiko 会执行以下清理：
   - 净化 `/proc/self/mounts` 与 `/proc/self/mountinfo`，剔除 Magisk 叠加挂载记录。
   - 遮蔽或卸载 `/system/bin/su`、`/system/xbin/su` 与 `/sbin` 敏感目录。
   - 清理会暴露 Root 环境的残留文件描述符（如 `/dev/pts`、`/dev/socket/magisk`）。
4. **自我抹除（Unlinking）**：完成进程环境净化后，Shamiko 会将自身的注入动态库从内存映射中卸载并移除 Hook 跳板，使扫描 Zygisk 特征的探测器无从察觉。

---

## 安装与配置步骤

### 第一步：调整 Magisk 设置
1. 打开 **Magisk App** → 点击右上角 **设置**。
2. 确认 **Zygisk** 已 **开启**。
3. 确认 **遵守排除列表（Enforce DenyList）** 处于 **关闭** 状态。
4. 点击 **配置排除列表**，勾选需要隐藏 Root 的目标应用（如银行、支付、政务或游戏应用）。

### 第二步：刷入 Shamiko
1. 下载官方发布的最新版压缩包（`Shamiko-vX.zip`）。
2. 在 Magisk / KernelSU / APatch 的 **模块** 页面刷入该 ZIP 文件。
3. 重启设备。

### 第三步：核验运行状态
重启后在 Root 管理器模块列表中查看 Shamiko 的状态描述：
- 配置正确时会显示 `Shamiko is working as normal (Blacklist mode)` 或 `(Whitelist mode)`。

---

## 白名单模式 vs 黑名单模式

- **黑名单模式（默认）**：
  Root 对未勾选应用可见，仅对排除列表中的应用隐藏。适合日常仅需屏蔽少数银行或风控软件的用户。
- **白名单模式（推荐高强度隐藏场景使用）**：
  对设备上的所有应用全局隐藏 Root 环境，仅对明确授予超级用户权限的应用生效。
  ```bash
  # 开启白名单模式：
  su -c "mkdir -p /data/adb/shamiko && touch /data/adb/shamiko/whitelist"

  # 恢复为黑名单模式：
  su -c "rm -f /data/adb/shamiko/whitelist"
  ```
