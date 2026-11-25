---
id: "magisk-manager-for-recovery-mode"
title: "Magisk Manager for Recovery Mode (mm)：恢复模式终端救砖工具"
sidebarTitle: "Magisk Manager (Recovery)"
description: "专为 TWRP 与 OrangeFox 打造的交互式终端救援工具，可在模块引发卡开机（Bootloop）时无需清除用户数据即可停用或删除问题 Magisk 模块。"
category: "root-management"
tier: 1
searchQueries:
  - "magisk manager for recovery mode 下载"
  - "mm recovery magisk rikj000"
  - "twrp 终端修复面具卡开机"
  - "recovery 模式禁用 magisk 模块"
  - "sh sdcard mm 救砖命令"
prerequisites:
  - "Magisk v19.0 至 v30.X"
  - "带有内置终端或支持 ADB Shell 访问的第三方 Recovery 环境（TWRP、OrangeFox、PBRP）"
conflicts: []
configPaths:
  - "/sdcard/mm"
  - "/data/adb/modules/"
features:
  - "Bootloop 救砖引擎：列出所有已安装的 Magisk 模块，支持选择性停用或彻底删除故障模块而不丢失用户数据"
  - "文件系统完整性修复：通过 `e2fsck -fy` 自动检查并修复 `magisk.img` 文件系统"
  - "全局模式切换：直接在恢复模式中开关仅核心模式（Core-Only Mode）或 Magic Mount 设置"
  - "交互式命令行向导：简洁的数字菜单，适配 TWRP 内置触屏终端及 `adb shell` 操作"
  - "全版本 Magisk 兼容：持续维护，覆盖从 v19.0 到最新 v30.X 的各代 Magisk 构建"
faq: []
---

## 概述

Magisk Manager for Recovery Mode（简称 `mm`）最初由 VR25 构思开发，现由 Rikj000 全面重构与持续维护，是 Android 玩机用户与模块开发者必备的救砖利器。当刷入不兼容模块导致无限重启（Bootloop）时，系统无法进入桌面打开图形化的 Magisk 应用来关闭故障模块。

`mm` 完美解决了这一困境：它直接在 TWRP、OrangeFox 或 PitchBlack Recovery Project（PBRP）等第三方 Recovery 中提供完整的交互式模块管理界面。只需一条终端命令，用户即可查看已安装模块列表、切换禁用标志或彻底移除异常模块，全程无需恢复出厂设置。

## 前置要求与兼容性

- **Magisk 版本**：广泛兼容 Magisk v19.0 至 v30.X。
- **Recovery 环境**：任意内置交互式终端控制台，或支持在电脑端通过 `adb shell` 连接的第三方 Recovery。
- **存储要求**：为确保 Recovery 下挂载路径稳定，建议将安装包存放在设备内置存储而非外置 SD 卡中。

该工具仅作为系统维护与诊断组件运行，与其它模块不存在已知冲突。

## 安装与部署

`mm` 可通过多种渠道获取并刷入：

1. **Magisk 管理器 / MRepo / MMRL**：在 Magisk 应用或 MMRL 等社区管理器中搜索并安装 `Magisk Manager for Recovery Mode (mm)`。
2. **Recovery 直接刷入**：也可直接将 `MagiskManagerForRecovery_v*.zip` 拷入手机，在 TWRP 恢复模式中刷入。
3. 安装完成后，系统会自动在 `/sdcard/mm` 生成终端启动脚本。

## 使用方法与终端命令

当设备遇到卡开机或在系统外管理模块时，请按以下步骤操作：

1. 将设备重启进入第三方 Recovery（例如 TWRP）。
2. 确保 `/data` 分区已完成解密并处于已挂载状态。
3. 在 Recovery 界面中打开 **Advanced > Terminal**（高级 -> 终端），或在已连接的电脑上启动 `adb shell`。
4. 执行以下任意一条命令：
   ```bash
   */mm
   # 或者
   sh /sdcard/mm
   ```
5. 随后屏幕将显示交互式菜单：
   - **列出已安装模块**：显示 `/data/adb/modules/` 中所有模块及其启用/禁用状态。
   - **切换模块状态**：输入对应模块编号即可快速禁用或重新启用该模块。
   - **移除模块**：从 `/data/adb/modules/` 中彻底删除指定模块目录。
   - **切换仅核心模式（Core-Only Mode）**：强制 Magisk 在下次启动时仅加载核心组件并跳过全部第三方模块。

## 故障排查与实用技巧

- **终端提示找不到文件（File Not Found）**：若执行 `sh /sdcard/mm` 报错，请前往 Recovery 的 Mount（挂载）菜单，确认 `/data` 与内置存储分区已正确解密并勾选挂载。
- **禁用模块后依然无法开机**：部分模块会持久修改 vendor 属性或系统配置。如果单独禁用问题模块仍无法进入系统，请使用 `mm` 开启**仅核心模式（Core-Only Mode）**，开机进入系统后再彻底清理残留的配套应用或配置。
