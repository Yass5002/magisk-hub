---
id: "installerx-revived"
title: "InstallerX Revived：支持 Root / Shizuku / Dhizuku 的现代安卓安装包管理器"
sidebarTitle: "InstallerX Revived"
description: "社区持续维护的现代 Android 安装包管理器（com.rosan.installer.x.revived），原生支持 APK、APKS、APKM、XAPK 与批量安装，并可对接免 Root、Shizuku、Dhizuku 与 Root 后端。"
category: "system-utilities"
tier: 1
searchQueries:
  - "InstallerX Revived 下载"
  - "InstallerX Revived Shizuku 配置"
  - "安卓 APKS XAPK APKM 安装器"
  - "替代系统默认安装包安装器"
  - "Dhizuku 静默安装工具"
prerequisites:
  - "支持免 Root（Rootless）模式运行，或已配置 Shizuku、Dhizuku、Magisk / KernelSU / APatch Root 授权"
conflicts:
  - "若同时保留原版已停更的 `iamr0s/InstallerX`，需注意默认文件打开方式与安装器偏好冲突"
configPaths:
  - "/data/data/com.rosan.installer.x.revived/"
features:
  - "全格式打包支持：原生解析并安装 APK、APKS、APKM、XAPK、ZIP 压缩包内嵌 APK 以及多包批量安装队列"
  - "多后端授权引擎：无缝切换 **Shizuku**、**Dhizuku**、**Root**（`app_process`）与 **免 Root** 系统包管理器模式"
  - "多样化安装流：支持弹窗交互安装、后台通知安装、自动安装、高权限静默安装，并支持 Android 16+ 实时活动（Live Activity）进度通知"
  - "智能批量选择记忆：在分析界面取消勾选再重新选中单版本行时，自动恢复此前的 Split 拆分包与 Dex 元数据选择"
  - "内置实用套件：集成 `UninstallerActivity` 卸载器、`UnarchiveActivity` 解归档处理、快捷设置磁贴（`SettingsTileService`）及生物识别确认（`BiometricsAuthenticationActivity`）"
faq:
  - question: "在 Shizuku、Dhizuku 和 Root 后端之间该如何选择？"
    answer: "日常使用最推荐 **Shizuku**，它直接复用常驻的 Shell 或 Root Binder 服务（`rikka.shizuku.ShizukuProvider`），响应速度最快；直接 **Root** 模式（Magisk / KernelSU / APatch）拥有完整系统权限但因每次需冷启动 `app_process` 进程会略慢；**Dhizuku** 适合已在免 Root 设备部署设备管理员权限的场景；未配置上述权限时也可直接以 **免 Root（Rootless）** 模式调用系统标准安装会话。"
  - question: "InstallerX Revived 支持哪些安装包格式？"
    answer: "除常规单包 `.apk` 外，完整支持 `.apks`、`.apkm`、`.xapk` 拆分包格式、嵌套在 `.zip` 压缩包内的 APK 文件，以及多文件批量安装。"
  - question: "InstallerX Revived 与原版 InstallerX 是什么关系？"
    answer: "InstallerX Revived（`wxxsfxyzm/InstallerX-Revived`，包名 `com.rosan.installer.x.revived`）是由社区接力维护的 `iamr0s/InstallerX` 延续版本，持续跟进 Material 3 界面优化、Android 16+ Live Activity 进度提示与高版本系统兼容性修复。"
---

## 概述

**InstallerX Revived**（仓库 `wxxsfxyzm/InstallerX-Revived`，包名 `com.rosan.installer.x.revived`）是广受好评的现代 Android 包安装器，也是原版 `iamr0s/InstallerX` 的社区接力维护版本。

许多厂商自带的系统安装器不仅对 `.apks`、`.apkm`、`.xapk` 等拆分包束手无策，还常常夹带广告推荐或强行拦截应用安装。InstallerX Revived 提供了清爽的 Material 3 交互体验、完整的拆分包解析能力以及高度可定制的安装配置，并兼容 **免 Root（Rootless）**、**Shizuku**、**Dhizuku** 与 **Root**（**Magisk** / **KernelSU** / **APatch**）等多种授权后端。

---

## 技术架构与多后端支持

通过分析 `InstallerX-Revived-online-26.11.caccb78.apk`（`26.11.caccb78`）应用结构，其核心能力依托以下后端与组件实现：

### 四类授权后端（Authorizers）
1. **Shizuku（`rikka.shizuku.ShizukuProvider` / `moe.shizuku.manager.permission.API_V23`）**：
   - 通过 Shizuku 获取 ADB Shell 或 Root 级 `PackageInstaller` 会话能力；由于复用常驻服务，安装响应速度通常明显快于直接冷启动 Root。
2. **Dhizuku（`com.rosan.dhizuku.permission.API`）**：
   - 调用 Dhizuku 提供的 DevicePolicy / DeviceOwner 接口，在免 Root 环境下实现无感授权安装。
3. **Root（`Magisk` / `KernelSU` / `APatch`）**：
   - 借助 `su` 启动 `app_process` 执行完整特权安装与管理操作（涵盖 `INSTALL_PACKAGES`、`DELETE_PACKAGES`、`INTERACT_ACROSS_USERS_FULL` 等权限）。
4. **免 Root / 系统包管理器模式（Rootless）**：
   - 无需 Root 或 Shizuku，通过标准 `REQUEST_INSTALL_PACKAGES` 权限引导系统完成基础安装确认。

### 核心应用组件与特性
- **完整组件体系**：包含后台前台服务 `InstallerService`、安装界面 `InstallerActivity`、卸载器 `UninstallerActivity`、应用解归档界面 `UnarchiveActivity`（响应 `UNARCHIVE_DIALOG`）、快捷设置磁贴 `SettingsTileService` 以及可选的生物识别验证 `BiometricsAuthenticationActivity`。
- **多形态安装流程**：支持弹窗安装、后台通知安装、自动安装、高权限静默安装，以及适配 Android 16+ 系统的 Live Activity 实时进度通知（`POST_PROMOTED_NOTIFICATIONS`）。
- **智能批量状态记忆**：在多包或拆分包弹窗分析时，临时取消勾选某单版本行后再重新勾选，可自动恢复此前的分包与 Dex 优化选项。

---

## 安装与配置步骤

1. 从 `wxxsfxyzm/InstallerX-Revived` 官方发布页下载 `InstallerX-Revived-online-26.11.caccb78.apk` 并安装：
   ```bash
   adb install InstallerX-Revived-online-26.11.caccb78.apk
   ```
2. 打开 **InstallerX Revived** -> **设置**（`SettingsActivity`），在授权器设置中选择你的后端方案：
   - **Shizuku**：启动 Shizuku 服务后点击授权即可。
   - **Dhizuku**：在 Dhizuku 管理器中授予 API 调用权限。
   - **Root**：在 Magisk、KernelSU 或 APatch 中授予超级用户权限。
   - **无 / 系统模式**：直接使用免 Root 兼容模式。
3. 可根据系统习惯将其设为 `.apk` 与安装包的默认打开方式，或在文件管理器中通过“分享 / 用其他应用打开”（`SEND` / `VIEW`）直接调用 InstallerX Revived。

---

## 常见问题与排查

- **Root 模式下唤起安装略有延迟**：因为直接 Root 模式需要冷启动 `app_process` 进程；若设备已运行 Root 版或无线调试版 **Shizuku**，推荐将授权后端切换为 **Shizuku** 以获得更快的响应速度。
- **部分国内定制系统无法直接接管系统默认安装器**：MIUI / HyperOS、ColorOS 等系统可能限制第三方应用直接取代自带包安装器。此时可通过第三方文件管理器“打开方式”或系统“分享”菜单将安装包发送至 InstallerX Revived 执行安装。
