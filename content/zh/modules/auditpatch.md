---
id: "auditpatch"
title: "AuditPatch：通过原生 PLT 注入脱敏内核审计日志上下文"
sidebarTitle: "AuditPatch"
description: "利用 Rust 编写的 linjector 与 PLT Hook，在不重启 logd 的前提下实时擦除 Android 审计日志中的敏感安全上下文与权限拒绝记录。"
category: "root-management"
tier: 1
searchQueries:
  - "AuditPatch Magisk 模块"
  - "silvzr AuditPatch 下载"
  - "Android Root 隐藏审计日志"
  - "linjector-rs logd 注入"
  - "PLT Hook 脱敏 SELinux 审计记录"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "Android 10 至 Android 15+ 系统"
  - "运行于产生内核审计日志条目的系统环境"
conflicts: []
configPaths:
  - "/data/adb/modules/auditpatch/"
features:
  - "原生运行时注入：采用 `linjector-rs` 在 `post-fs-data` 阶段直接挂钩，无需 Zygisk 亦无需重启 `logd`"
  - "过程链接表（PLT）拦截：借助 PerformanC PLTI 在日志写入缓冲区前拦截格式化函数"
  - "SELinux 上下文脱敏：从系统审计追踪中抹除暴露 Root 特征的标记、包名及私有域名称"
  - "反检测防御：防止反作弊与银行类应用抓取 SELinux 审计日志以探测 Root 修改痕迹"
faq: []
---

## 概述

反篡改引擎与银行级风控检测工具经常会读取 Android 的内核审计缓冲区（`/dev/log/audit` 或 logcat 中的 audit 标签）。每当 Root 工具或自定义 `su` 二进制访问系统服务时，内核的 SELinux 子系统都会进行权限校验。即便该操作在宽容规则或自定义策略注入下顺利执行，一条包含主体上下文（`scontext`）、目标上下文（`tcontext`）及拒绝访问向量的审计记录依然会被直接广播至系统日志。

由 silvzr 基于 brunoanc 的研究成果开发的 **AuditPatch**，选择从日志产生的原生源头解决信息泄露问题。通过直接附加至 Android 日志守护进程（`logd`），AuditPatch 能够在审计日志完成序列化并写入内存缓冲区之前，对载荷内容进行实时脱敏净化。

## 技术架构

### 1. 零重启 Linjector 注入管线
传统的日志挂钩方案要么依赖 Zygisk 运行时，要么需要在启动早期强行重启 `logd`，而后者极易导致已持有日志子系统 Unix 套接字文件描述符的系统服务中断。AuditPatch 改用基于 Rust 编写的原生进程注入器 **`linjector-rs`**，在 `post-fs-data` 启动阶段直接将共享库注入正在运行的 `logd` 进程，全程保持日志服务不中断。

### 2. PLT（过程链接表）挂钩
借助 PerformanC 提供的轻量级 **PLTI** 库，AuditPatch 会修补负责拼装与分发审计日志行的内部函数调用：
- 扫描即将输出的日志记录，检索敏感安全域与已知 Root 进程特征。
- 就地改写上下文描述符，将其替换为常规、无害的 Android 系统服务标识。
- 彻底消除原本足以暴露 Magisk、KernelSU 或自定义 SELinux 策略规则的日志痕迹。

## 安装与部署

1. 从 GitHub 下载 `AuditPatch` 发布版 `.zip` 压缩包。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入该模块。
3. 重启设备，使模块在 `post-fs-data` 阶段完成对 `logd` 的注入。
4. 在终端中监控系统审计日志以验证脱敏效果：
   ```bash
   su -c logcat -d -b events -s auditd
   ```

## 兼容性与约束条件

- 完全独立于 Zygisk 运行，不会与现有 Zygisk 注入引擎发生冲突。
- 兼容 Android 10 至 Android 15+ 系统的 64 位 ARM 架构设备。
