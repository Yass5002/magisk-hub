---
id: "ashlooper"
title: "AshReXcue (AshLooper)：智能差分防卡米与开机脚本保护"
sidebarTitle: "AshReXcue (AshLooper)"
description: "面向 Magisk、KernelSU 与 APatch 的智能防卡米保护引擎，利用差分状态分析精准隔离故障模块与开机脚本，避免误伤正常配置。"
category: "root-management"
tier: 1
searchQueries:
  - "AshReXcue Magisk 模块"
  - "AshLooper 防卡米保护"
  - "RipperHybrid AshLooper 下载"
  - "智能差分防卡米模块"
  - "Root SystemUI 崩溃循环保护"
prerequisites:
  - "运行 Magisk、KernelSU、APatch 或主流社区分支的已 Root Android 设备"
  - "具备设备音量键或触控界面以完成交互式安装选项设置"
conflicts: []
configPaths:
  - "/data/adb/modules/AshLooper/"
features:
  - "智能差分分析：每次开机计算所有模块与脚本的哈希指纹，故障时仅精准定位并隔离引起异常的变更项"
  - "开机脚本守护：将完整防卡米保护延伸至位于 `service.d`、`post-mount.d` 与 `post-fs-data.d` 中的独立脚本"
  - "SystemUI 看门狗：实时监控 `com.android.systemui` 健康状态，检测到连续崩溃（三次触发策略）即自动执行修复"
  - "交互式本地 WebUI：功能完善的图形面板，支持配置模块白名单、查阅开机活动日志及调整保护阈值"
  - "隔离恢复保险箱：将故障脚本移入安全隔离区而非直接删除，方便开机恢复后排查调试代码"
faq: []
---

## 概述

由 AshBorn（`@Ripper_Hybrid`）开发的 **AshReXcue**（前身为 AshLooper），是一款专为 Magisk、KernelSU 与 APatch 环境打造的智能启动保护引擎。传统的防卡米救砖脚本往往采用“一刀切”策略：一旦开机失败便禁用全部已安装模块，迫使用户在重启后逐一手动重新启用几十个模块。

AshReXcue 以 **智能差分分析（Smart Differential Analysis）** 彻底告别了这种粗暴方式。它在每次成功开机时记录所有模块目录与开机脚本的加密哈希值、文件大小及状态标记，因此精准掌握每次重启前的具体变更。一旦发生卡米或循环重启，它只会精准锁定并禁用新增或被修改的异常组件，确保其余正常模块与 Root 定制功能继续稳定运行。

## 前置要求与兼容性

- **Root 环境**：兼容官方 Magisk、KernelSU、APatch 及其活跃维护的社区分支。
- **Android 版本**：全面支持从 Android 8 直至最新现代版本的 Android 系统。
- **硬件架构**：通用支持 ARM、ARM64 与 x86 架构。

当前无已知模块硬性冲突，但应避免同时运行多个同类防卡米模块（例如将 AshReXcue 与 YetAnotherBootloopProtector 混用），以免多个看门狗计时器相互干扰。

## 核心架构与保护机制

### 1. 差分状态追踪
在开机后期阶段（`boot-completed`），AshReXcue 会为每个已安装模块目录以及 `/data/adb/service.d/`、`/data/adb/post-fs-data.d/`、`/data/adb/post-mount.d/` 中的所有独立脚本建立指纹基线。若下一次启动流程中断或崩溃，AshReXcue 会将当前状态与基线档案进行比对，从而将新增或发生变更的文件判定为潜在故障源。

### 2. 开机脚本守护与隔离保险箱
不同于仅管理 `/data/adb/modules/` 的常规防砖工具，AshReXcue 为 `service.d` 与 `post-fs-data.d` 中的独立脚本提供了同等的一级保护。它不会粗暴删掉报错脚本，而是将其转移至 `/data/adb/modules/AshLooper/` 内的独立恢复保险箱，方便用户正常进入系统后查错修复。

### 3. SystemUI 崩溃循环检测
某些不兼容的主题叠加层或字体模块虽然能顺利通过内核与 Zygote 阶段，却会导致 `com.android.systemui` 持续崩溃，使手机黑屏或无法操作。AshReXcue 在后台运行了轻量级看门狗以监控 SystemUI 进程稳定性；一旦 SystemUI 在短时间内连续崩溃三次，便会立刻触发自动恢复流程。

## 配置与 WebUI 控制面板

AshReXcue 提供开箱即用的本地交互式 WebUI 面板：

1. 在 Root 管理器中刷入 `AshReXcue_Bootloop_Protector_*.zip`。
2. 安装过程中按提示使用音量键选择基础选项（如是否启用开机脚本监控）。
3. 重启设备。
4. 打开 WebUI 控制台：
   - **KernelSU / APatch**：在模块卡片上直接点击 **WebUI** 按钮。
   - **Magisk**：通过 MMRL 或 WebUI X Standalone 打开面板。
5. 在 WebUI 中，你可以：
   - 配置 **白名单管理器（Whitelist Manager）**，确保核心安全模块永远不会被误禁用。
   - 查看 **活动日志（Activity Log）**，了解启动耗时、时间戳与守护进程状态。
   - 调整稳定判定时间窗口与崩溃触发阈值。
6. 模块配置与运行状态持久化保存于：
   ```bash
   /data/adb/modules/AshLooper/
   ```

## 验证与故障排查

- **安全测试保护机制**：若想在不弄坏系统的前提下验证看门狗是否生效，可在 `/data/adb/service.d/test_loop.sh` 创建一个立即退出的无害空脚本，随后打开 WebUI 活动日志，确认其已被纳入差分追踪目录。
- **从保险箱恢复被隔离模块**：如果因误报导致某个正常脚本被隔离，前往 WebUI 的 **Items** 标签页即可将其从隔离保险箱中一键还原。
