---
id: "twrp-keep"
title: "TWRP A/B Retention Script：OTA 系统更新后无缝保留 TWRP 第三方恢复环境"
sidebarTitle: "TWRP A/B 保留脚本"
description: "由 osm0sis 打造的专用 OTA 挂钩脚本，可在无缝 A/B 分区系统更新后保留 TWRP 自定义 Recovery，与 Magisk“安装到未使用的槽位”流程完美配合。"
category: "system-environment"
tier: 1
searchQueries:
  - "twrp keep Magisk 模块"
  - "twrp a/b retention script osm0sis"
  - "OTA 更新后保留 TWRP"
  - "Magisk 安装到未使用的槽位 保留 TWRP"
  - "Magisk OTA 保留脚本"
prerequisites:
  - "采用无缝 A/B 或虚拟 A/B 分区架构的 Android 设备"
  - "当前活动槽位的 `boot` 或 `vendor_boot` 内存盘（Ramdisk）中已安装 TWRP 或兼容的第三方 Recovery"
  - "Magisk v15.0 及以上版本"
conflicts:
  - "传统单分区（A-only）设备（不具备双槽位 A/B 架构的机型）"
configPaths: []
features:
  - "零残留保留机制：仅作为可刷入的安装挂钩脚本运行，不会在 `/data` 分区留下任何常驻二进制文件"
  - "无缝衔接官方 OTA：解决官方原厂 OTA 升级与保留第三方 Recovery 之间的兼容性痛点"
  - "配套 Magisk 升级流：专为紧接在 Magisk“安装到未使用的槽位”操作之前刷入而设计"
  - "防止恢复原厂 Recovery：拦截 OEM OTA 载荷切换过程，确保 TWRP 在槽位切换后依然完好保留"
---

## 概述

由 XDA-Developers 资深 Android 开发者 osm0sis 编写的 TWRP A/B Retention Script，解决了现代 A/B 与虚拟 A/B 分区 Android 设备上的一个核心痛点：在接收官方无线（OTA）系统更新的同时避免丢失第三方 Recovery。

在现代 A/B 设备上，官方 OTA 更新会下载完整的新版操作系统，并将其直接刷入后台处于非活动状态的另一个分区槽位。由于 Recovery 通常打包在 `boot` 或 `vendor_boot` 的内存盘（Ramdisk）内，OTA 升级流程会向该非活动槽位写入一份纯净的原厂 Boot 镜像。如果此时直接正常重启手机，TWRP 就会被覆盖抹除。TWRP A/B Retention Script 能够在设备重启前，将你当前生效的 TWRP 内存盘修补进非活动槽位刚写入的 Boot 镜像中，从而完整保留 TWRP。

## 前置要求与兼容性

- **分区方案**：设备**必须**采用 A/B 或虚拟 A/B 分区架构（Android 7.1 及以后出厂的机型普遍采用，包括 Google Pixel、一加、摩托罗拉及部分小米 A/B 机型）。传统“A-only”单槽位设备不兼容。
- **Root 管理器**：Magisk v15.0 及以上版本。
- **第三方 Recovery**：当前活动槽位的 Boot 镜像中已正常安装可用的 TWRP。

### 零残留特性

正如 osm0sis 在文档中明确指出的那样：
> **这并不是一个常规模块——它不会安装任何实际文件。**

该 ZIP 包仅作为一个自动化脚本执行器运行。尽管它可能会在 Magisk 模块列表中注册一个通用版本号以便追踪更新，但它不会在 `/data/adb/modules/twrp-keep/` 下维护任何运行时守护进程或持久化目录。

## 标准 OTA 更新操作流程

要在升级系统后同时完整保留 TWRP 与 Magisk Root，请严格遵循以下操作顺序：

1. **下载并安装 OTA**：前往 **系统设置 > 系统 > 系统更新**，按正常流程下载并等待系统更新完成第 1 步与第 2 步（后台安装）。
2. **切勿立即重启**：当更新提示安装完成并弹出“立即重启”按钮时，**千万不要点击重启**。
3. **刷入保留脚本**：
   - 打开 **Magisk** 应用。
   - 切换至 **模块** 标签页。
   - 点击 **从本地安装** 并选择 `TWRP_A_B_Retention_Script-Magisk-*.zip`。
   - 脚本会自动定位非活动槽位，并使用你当前的 TWRP 内存盘重新修补该槽位刚刚写入的 Boot 镜像。
4. **重新安装 Magisk**：
   - 返回 Magisk 主界面。
   - 点击 Magisk 卡片旁的 **安装** 按钮。
   - 选择 **安装到未使用的槽位（OTA 后）**。
   - 点击 **开始**，将 Root 权限修补写入非活动槽位。
5. **重启设备**：待 Magisk 完成非活动槽位安装后，直接在 Magisk 应用内点击 **重启** 按钮。设备随后会切换至更新后的槽位，TWRP 与 Root 权限均将完整保留。

## 故障排查与注意事项

- **在执行保留操作前误点重启**：如果在运行保留脚本和 Magisk 非活动槽位修补之前就立即重启了手机，设备将进入无 Root 且恢复为原厂 Recovery 的状态。此时你需要通过电脑使用 Fastboot 重新刷入 TWRP 或已修补的 Boot 镜像。
- **模块列表长期显示更新提示**：Magisk 可能会长期提示 `twrp-keep` 存在可用更新。这是开发者有意为之的设计，方便用户在需要执行 OTA 保留操作时随时重新下载并运行最新的脚本逻辑。
