---
id: "nohello"
title: "Zygisk NoHello：高隐蔽 Root 与模块检测隐藏引擎"
sidebarTitle: "NoHello"
description: "基于 Zygisk 的反检测模块，旨在向敏感应用隐藏 Root 二进制文件、Zygisk 痕迹以及模块挂载修改。"
category: "root-management"
tier: 1
searchQueries:
  - "nohello zygisk 模块"
  - "mhmrdd nohello 下载"
  - "nohello 隐藏 root zygisk"
  - "nohello 挂载规则系统"
  - "nohello 绕过 root 检测"
prerequisites:
  - "KernelSU、KernelSU Next、APatch 或 Magisk（推荐 v28.0+）"
  - "可用的 Zygisk 提供程序（强烈推荐使用 ZygiskNext 或 ReZygisk）"
conflicts:
  - "Magisk 设置中的「遵守排除列表（Enforce DenyList）」（必须禁用）"
  - "ZygiskNext 或 ReZygisk 设置中的「Enforce DenyList」（必须禁用）"
configPaths:
  - "/data/adb/nohello/"
  - "/data/adb/modules/nohello/"
features:
  - "隐蔽 Root 隐藏：向目标应用隐藏 su 二进制文件、守护进程与包管理器特征"
  - "自定义挂载规则系统：支持精细化规则以卸载或伪装特定文件系统修改"
  - "白名单模式支持：可切换为默认隔离所有应用，仅对受信任工具放行"
  - "Zygisk 注入混淆：模块执行后抹除运行时内存 Hook 与入口痕迹"
  - "跨管理器兼容：无缝适配 KernelSU、APatch 与 Magisk 平台"
faq:
  - question: "为什么使用 NoHello 时必须关闭「遵守排除列表（Enforce DenyList）」？"
    answer: "NoHello 自行管理卸载与隔离流程。如果在 Magisk 或 Zygisk 提供程序中开启 Enforce DenyList，会激活相互竞争的挂载命名空间，从而破坏 NoHello 的隐藏逻辑。"
  - question: "日常使用应该选择 debug 版本还是 release 版本的 NoHello？"
    answer: "日常使用请务必选择 release 版本。debug 版本包含详尽的日志输出与导出符号，容易触发反作弊软件和银行应用的安全风控检测。"
---

## 概述

**Zygisk NoHello** 由 **MhmRdd** 开发，是一款专为应对现代应用完整性校验而生的反检测模块，用于隐藏 Root 权限、Zygisk 运行时产物以及无侵入式文件系统挂载痕迹。

面对会扫描开放端口、检查 `/proc/mounts`、分析已加载共享库并探测执行权限的多维度现代风控套件，常规 Root 隐藏方案往往力不从心。NoHello 直接工作在 Zygisk 层，在应用完成启动自检前便拦截相关检测例程。

---

## 技术架构与工作原理

### 进程隔离与挂载规则

NoHello 在 Zygote 进程孵化（fork）生命周期内挂钩应用进程：

1. **挂载卸载**：对于管理器排除列表或目标配置中标记的应用，NoHello 会从进程挂载命名空间中剥离模块叠层与挂载点。
2. **动态规则处理**：内置基于规则的处理引擎，支持用户针对特定检测向量精确指定路径屏蔽、文件重定向与属性覆写策略。
3. **痕迹抹除**：在控制权移交给应用主入口之前，清理内部 Hook 存根并重置进程权限能力集（Capabilities）。

---

## 安装与配置

### KernelSU 与 APatch 用户
1. 安装可用的 Zygisk 实现（**ZygiskNext** 或 **ReZygisk**）。
2. 确保在管理器中为目标应用开启了**卸载模块（Umount modules）**开关。
3. 如果 ZygiskNext/ReZygisk 设置中存在 **Enforce DenyList**，请将其关闭。
4. 刷入 NoHello 模块并重启设备。

### Magisk 用户
1. 推荐使用 Magisk v28.0+ 以获得最佳命名空间隔离效果。
2. 搭配 **ZygiskNext** 或 **ReZygisk**（推荐替代内置 Zygisk）。
3. 在 Magisk 设置中**关闭** `Enforce DenyList`。
4. 将目标应用添加至 Magisk 的**配置排除列表（Configure DenyList）**。

---

## 实战配置与使用

- **白名单模式**：从 0.0.4+ 版本起，你可以反转工作策略为白名单模式，使所有应用默认处于隔离状态，仅对显式授权的应用开放 Root 可见性。
- **自定义挂载规则**：将特定的卸载与屏蔽规则写入 `/data/adb/nohello/rules`，以处理非标准的设备系统修改。

---

## 故障排查与常见问题

- **依然触发检测**：请确认已将目标应用的全部后台服务及辅助进程均加入排除列表，并核实所有管理器设置中的 `Enforce DenyList` 均已关闭。
- **Root 管理器应用崩溃**：切勿为 Root 管理器自身（KernelSU 管理器、APatch 或 Magisk）开启模块卸载隔离。
