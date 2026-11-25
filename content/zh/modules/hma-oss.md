---
id: "hma-oss"
title: "Hide My Applist (HMA-OSS)：隐藏已安装应用与 Root 软件包"
sidebarTitle: "Hide My Applist"
description: "无需依赖 LSPosed 的独立 Zygisk 模块，可为指定目标应用过滤已安装应用列表及相关包查询请求。"
category: "root-management"
tier: 1
searchQueries:
  - "HMA-OSS Zygisk 模块下载"
  - "Hide My Applist 隐藏应用列表 Zygisk"
  - "银行应用隐藏 Root 应用教程"
  - "Zygisk 包管理器过滤隐藏应用"
  - "HMA-OSS 模板配置指南"
prerequisites:
  - "已启用 Zygisk 的 Magisk，或已安装 Zygisk 提供层（如 ZygiskNext）的 KernelSU / APatch"
  - "具备兼容 Zygisk 运行环境的已 Root Android 设备"
conflicts:
  - "同时运行多个相互冲突的 Zygisk 加载器"
  - "旧版基于 Xposed 的隐藏应用列表模块（刷入前请先卸载历史 LSPosed 版本）"
configPaths:
  - "/data/adb/modules/hma_oss_zygisk/"
  - "/data/user/0/org.frknkrc44.hma_oss/"
features:
  - "独立 Zygisk 模块，完全无需安装 LSPosed"
  - "为已配置的目标应用精准过滤应用列表及相关包查询接口"
  - "内置常见检测应用预设清单，支持分应用精细配置保护规则"
  - "自 oss-168 版本起增强应用列表清理能力并进一步减少暴露检测点"
  - "社区多语言开源项目，上游保持积极维护更新"
faq:
  - question: "为什么已经隐藏或重命名 Magisk，银行应用依然能检测到 Root？"
    answer: "许多应用并不仅仅扫描 `su` 二进制文件，还会枚举手机上安装的应用包名。HMA-OSS 能够为指定目标应用过滤应用列表及相关查询，但它并非能对抗所有 Root 检测、完整性校验或设备状态检查的万能方案。"
  - question: "使用 HMA-OSS 是否需要配合 LSPosed 或 Vector？"
    answer: "不需要。HMA-OSS 在架构上被设计为原生 Zygisk 模块，其当前 Zygisk 工作流完全不依赖 LSPosed。"
  - question: "HMA-OSS 的配套管理应用是如何安装的？"
    answer: "在 oss-168 发行包 ZIP 内已包含 `manager.apk` 与 `35-install-manager-app.sh` 安装钩子。通过兼容的 Root 管理器刷入该发行包时，系统会自动安装配套的 HMA-OSS 管理应用；若使用更新的发行版本，建议提前核对压缩包内附带的文件内容。"
  - question: "可以在 KernelSU 或 APatch 上使用 HMA-OSS 吗？"
    answer: "本项目以 Zygisk 模块形式分发。KernelSU 与 APatch 用户需预先配置好可正常运行的 Zygisk 实现模块；安装前建议对照最新的上游文档确认兼容性。"
---

## 概述

由 **frknkrc44** 及开源社区贡献者共同维护的 **HMA-OSS**（Hide My Applist 开源版）是一款 Zygisk 模块，专门用于管控特定应用获取设备上已安装应用信息的能力。

Android 应用可通过包可见性 API（Package Visibility API）及其他检测手段探测设备内安装了哪些软件。部分银行、企业级安全软件及风控系统会将这些应用清单视作风险评估依据之一。HMA-OSS 会为已配置的目标应用过滤受支持的应用列表及相关查询请求，但请注意不要将其视为绝对严密或包治百病的万能隐藏层。

虽然原版 Hide My Applist 项目最早与 Xposed 生态绑定，但 **HMA-OSS 提供了一套无需依赖 LSPosed 的纯 Zygisk 工作流**，只要设备的 Root 管理器与 Zygisk 环境兼容即可运行。

### oss-168 版本更新亮点

`oss-168` 版本（发布于 2026 年 9 月 13 日）包含以下上游改进：
- 在预设名单中补充了新的检测类应用；
- 新增 `NativeZygoteProcess` 支持；
- 在清理已卸载应用配置时执行更彻底的应用列表清理；
- 新增向 Root 管理器上报模块运行状态的功能；
- 移除冗余或可靠性较弱的依赖项以及若干旧版 Hook；
- 修复或削减了多个已知检测点。

该版本同时整合了最新的社区翻译更新。由于上游 README 有意精简了公开技术细节描述，具体实现机制请参阅官方发行说明与 Wiki 文档。

---

## 技术架构与工作原理

### 1. Zygisk 进程集成
HMA-OSS 借助 Android Root 环境提供的 Zygisk 注入通道，对用户指定的目标应用施加以过滤规则。其内部具体的 Hook 集合会随版本迭代而变化，请以上游源码及版本更新日志为准，切勿假定某组固定的 Java 或原生函数列表始终不变。

### 2. 定向应用列表过滤

模块旨在拦截或过滤已配置目标的应用列表请求，并针对常见检测应用提供了现成预设。实际生效效果取决于具体目标应用、Android 系统版本、Root 环境以及当前运行的 HMA-OSS 版本。在需要配合 DenyList、兼容的 Zygisk 提供层或其他设备级隐藏措施的场景下，HMA-OSS 并不能替代它们。

---

## 安装与配置指南

### 第一步：在 Root 管理器中刷入模块
1. 点击上方的下载按钮获取最新的 `HMA-OSS-ZYGISK-*.zip`。
2. 确认当前 Root 环境已激活 **Zygisk**：
   - **Magisk**：进入 Magisk 设置，确认已开启 **Zygisk** 开关。
   - **KernelSU / APatch**：确保已刷入并启用 Zygisk 实现模块（例如 **ZygiskNext**）。
3. 打开你的 Root 管理器（Magisk、KernelSU 或 APatch），切换至 **模块（Modules）** 页面。
4. 点击 **从本地安装（Install from storage）**，选择下载好的 `HMA-OSS-ZYGISK-*.zip`。
5. 等待安装脚本执行完毕。以 `oss-168` 为例，安装器会自动部署 Zygisk 动态库并安装配套的 **HMA-OSS** 管理应用（`manager.apk`）。
6. 重启设备。

### 第二步：配置 HMA-OSS 预设与隐藏规则
1. 从桌面启动 **HMA-OSS** 应用。
2. 点击 **应用管理（Manage apps）**，选中需要隐藏保护的目标应用（例如银行应用或环境检测工具）。
3. 将 **启用隐藏（Enable hide）** 开关拨至开启状态。
4. 在 **模板配置（Template config）** 下点击 **使用 X 预设（Using X presets）**：
   - 勾选 **检测类应用（Detector apps）**、**Root 管理器 / 已授权 Root 应用（Root managers / rooted apps）**、**Shizuku / Dhizuku 应用** 以及 **Xposed 模块**。
5. 若当前版本提供 **使用 X 设置预设（Using X settings presets）** 选项，可进一步：
   - 勾选 **开发者选项（Developer options）** 与 **无障碍服务（Accessibility）**，屏蔽与 Root 相关的系统设置状态检测。
6. （推荐）确认已开启 **Activity 启动保护（Activity launch protection）**，防止通过 Intent 组件发起的探测扫描。
7. 强行停止目标应用并重新打开以测试效果。请注意自行核验结果，部分受保护应用仍可能采用 HMA-OSS 未覆盖的其他检测手段。

## 官方参考资料

- GitHub 仓库：https://github.com/frknkrc44/HMA-OSS
- 版本发布页：https://github.com/frknkrc44/HMA-OSS/releases
- 官方 Wiki：https://github.com/frknkrc44/HMA-OSS/wiki
