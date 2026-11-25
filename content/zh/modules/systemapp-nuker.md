---
id: "systemapp-nuker"
title: "System App Nuker (SAN)：基于 Overlay 白名单隐藏的现代无侵入系统精简工具"
sidebarTitle: "System App Nuker"
description: "面向 Magisk、KernelSU 与 APatch 的高阶无系统分区修改精简模块，集成了现代化的 WebUI 界面、OverlayFS 目录白名单隐藏以及开机循环自动恢复保护。"
category: "system-utilities"
tier: 1
searchQueries:
  - "System App Nuker Magisk 模块下载"
  - "SAN 系统应用精简工具"
  - "KernelSU WebUI 精简系统预装软件"
  - "OverlayFS 无损隐藏系统应用"
  - "Root 精简预装防卡开机模块"
prerequisites:
  - "已通过 Magisk、KernelSU 或 APatch 获取 Root 权限的 Android 设备"
  - "新版 KernelSU 环境需搭配可用的元模块（Metamodule，如 Mountify）以提供 Overlay 挂载支持"
  - "支持 WebUI（KernelSU / APatch 原生内置，Magisk 用户需配合 KSUWebUIStandalone 或 WebUI X）"
conflicts: []
configPaths:
  - "/data/adb/modules/systemapp_nuker/"
  - "/sdcard/Download/"
features:
  - "OverlayFS 白名单隐藏挂载：创建字符型白名单节点（Whiteout）在不改动 `/system` 分区的前提下无侵入隐藏 APK 目录"
  - "可视化 WebUI 管理界面：支持检索、查看并按移除风险等级与依赖严重程度分类筛选系统软件包"
  - "双运行模式切换：可自由选择透明的 OverlayFS 文件系统白名单隐藏模式，或标准的 `pm uninstall --user 0` 卸载模式"
  - "开机循环自动保护：监测开机早期阶段状态，若检测到 Bootloop 则自动禁用模块并保留精简列表以恢复系统"
  - "便携式 JSON 配置迁移：支持将精简列表导出至 `/sdcard/Download/` 或跨 ROM、跨设备导入复用"
---

## 概述

由开发者 chisewaguri 打造的 **System App Nuker（简称 SAN）** 是一款专为 Magisk、KernelSU 与 APatch 设计的现代无侵入式系统精简（Debloat）模块。传统的精简脚本往往依赖繁琐的终端交互命令，甚至直接破坏性删除系统分区文件；而 SAN 将直观易用的 WebUI 管理界面与 Linux OverlayFS 白名单（Whiteout）技术融为一体。

SAN 并不会真正从只读的 `/system`、`/vendor` 或 `/product` 分区中删除物理文件，而是在选定应用的目录下创建文件系统白名单节点进行覆盖屏蔽。在 Android 虚拟文件系统（VFS）层看来，目标 APK 目录如同彻底消失一般，既能干净地移除预装臃肿应用，又能随时一键无损回滚而不丢失任何数据。

## 前置要求与兼容性

- **Root 方案**：支持 Magisk、KernelSU 与 APatch。
- **KernelSU 挂载说明**：对于未内置 Overlay 挂载能力的新版 KernelSU 环境，需安装并启用可正常工作的元模块（如 [Mountify](https://github.com/backslashxx/mountify)），或配合模块自带的 Mountify 辅助脚本使用。
- **WebUI 交互界面**：
  - **KernelSU / APatch**：直接在管理器模块列表中点击打开。
  - **Magisk**：通过模块操作（Action）按钮启动，需提前安装 [KSUWebUIStandalone](https://github.com/KOWX712/KsuWebUIStandalone) 或 WebUI X。

目前尚未发现明确的模块冲突记录。

## 核心功能与运行模式

### 1. OverlayFS 白名单隐藏模式（默认）
在默认模式下，SAN 会记录所选 APK 的精确文件系统路径，并在系统启动早期向其父目录挂载 Overlay 白名单字符设备，使 Android 系统判定该目录已被删除。尤为关键的是，SAN 会在隐藏应用前先行保存其原始路径，确保后续模块升级或系统刷新时，即便包管理器（`pm path`）已无法检索到对应包名，仍能持续维持白名单隐藏状态。

### 2. 仅卸载模式（Uninstall Only）
如果更倾向于使用 Android 原生的包管理卸载行为，可在设置中将 SAN 切换为执行 `pm uninstall --user 0`。在此模式下，模块会跳过文件系统白名单挂载机制，仅在当前主用户空间内停用并隐藏指定软件包。

### 3. 内置开机防变砖保护（Bootloop Guard）
误删关键系统依赖组件（如 SystemUI 或电话服务组件）可能会导致设备无法正常开机。为此，SAN 内置了全自动开机防变砖守护机制：
- 守护程序会持续追踪设备在开机后是否成功拉起模块的后台服务。
- 若连续两次在启动早期阶段未能顺利进入后台服务，模块将判定系统发生 Bootloop，随即自动禁用自身、清除所有已生效的白名单节点、备份当前精简列表并重启设备。
- 系统恢复进入桌面后，你可以通过 WebUI 安全地排查问题并恢复原有配置。

## 配置与使用方法

1. 通过你的 Root 管理器刷入 `SAN_v*.zip` 并重启设备。
2. 打开 **System App Nuker** 的 WebUI 管理界面。
3. 在 **Home** 标签页中浏览已安装的系统应用，列表会按安全风险等级分类展示，辅助你判断可移除范围。
4. 勾选希望移除的软件包并点击 **Nuke**。
5. 重启设备使文件系统白名单屏蔽生效。
6. 若需恢复某个已精简的应用，进入 **Restore** 标签页选中对应包名，点击恢复并重启即可。
7. 如需迁移或备份清单，点击 **Export Config** 即可在 `/sdcard/Download/` 目录生成可复用的 JSON 配置文件。
8. 模块运行时配置与核心文件位于：
   ```bash
   /data/adb/modules/systemapp_nuker/
   ```

## 故障排查与验证

- **安装时提示挂载错误**：若在 KernelSU 环境下安装时提示缺乏挂载能力，请确认已安装并启用 Mountify 元模块。
- **系统更新后预装应用重新出现**：若 OEM 系统 OTA 升级为预装应用新增了 APK 目录路径，请重新打开 WebUI 扫描并将新路径加入白名单隐藏。
