---
id: "noogle-magisk"
title: "Noogle Magisk：在原厂 Android 固件中使用 microG 替代谷歌服务"
sidebarTitle: "Noogle Magisk"
description: "由 SelfRef 开发的无系统分区修改 Magisk 套件，可在原厂 Android 11 至 15 固件上用开源 microG 替代 Google Play 服务，支持一键自动授权与谷歌应用精简。"
category: "system-environment"
tier: 1
searchQueries:
  - "noogle magisk 模块下载"
  - "selfref noogle-magisk"
  - "Magisk microG 替换 Google Play 服务"
  - "原厂 Android 去谷歌 microG"
  - "noogle 原厂 ROM 签名欺骗"
prerequisites:
  - "Android 11 至 Android 15 系统"
  - "Magisk Root 环境"
  - "ROM 已启用签名欺骗（Signature Spoofing）支持（通过原生补丁或配套模块实现）"
conflicts: []
configPaths:
  - "/data/adb/modules/noogle-microg/"
  - "/system/priv-app/"
features:
  - "无系统分区修改部署 microG：将 microG GmsCore、Services Framework Proxy（GsfProxy）与 FakeStore 直接挂载至系统特权目录"
  - "安全屏蔽专有 GMS 服务：平稳覆盖并替代原厂 Google 服务，同时不破坏基础系统框架依赖"
  - "一键自动授权：集成 Magisk 的“操作（Action）”按钮，可自动为 microG 授予全部所需运行时权限"
  - "保留原厂相机与固件功能：在打造无谷歌、注重隐私的系统环境的同时，完整保留原厂 OEM 相机算法与厂商特性"
---

## 概述

由 SelfRef 开发的 Noogle Magisk 是一套无系统分区修改（Systemless）套件，旨在在原厂 Android 11 至 15 设备上移除专有 Google Play 服务，并以开源 microG 框架取而代之。

过去，用户若想摆脱 Google 的后台遥测追踪，往往必须解锁 Bootloader、清空用户数据并刷入 LineageOS 或 GrapheneOS 等第三方类原生 ROM。然而，第三方 ROM 常会导致原厂专有相机算法画质下降、双屏等特殊硬件功能失效，并失去原厂固件专属特性。Noogle Magisk 让用户能够继续保留官方原厂 OEM 固件，同时干净利落地将 Google 专有二进制组件替换为轻量、开源的 microG 服务。

## 前置要求与兼容性

- **Android 版本**：Android 11 至 Android 15。
- **Root 框架**：Magisk（稳定版或 Canary 版）。
- **签名欺骗要求**：为使 microG 能够模拟 Google Play 服务并让第三方应用正常工作，你的 ROM 必须支持 **签名欺骗（Signature Spoofing）**。若原厂 ROM 本身不支持签名欺骗，则必须提前刷入支持签名欺骗的 Zygisk 模块（例如 FakeGApps 或兼容的 LSPosed 挂钩模块）。

目前暂无已知的模块冲突记录。

## 核心功能与架构

- **特权目录无侵入挂载**：将 microG 组件挂载至 `/system/priv-app/`，赋予 microG 处理位置服务提供程序、云消息推送及账号同步所需的系统特权权限。
- **Action 按钮自动化授权**：无需手动通过 `adb shell` 授权或逐项点击 Android 设置菜单，Noogle Magisk 内置了 Magisk Action 按钮脚本，可一步到位授予全部必需权限（`ACCESS_FINE_LOCATION`、`ACCESS_COARSE_LOCATION` 及电池优化白名单）。
- **可选应用精简**：内置模块化精简逻辑，可抑制其余 Google 系统应用（如 Google Chrome、YouTube 或 Google 相册），方便用户改用 F-Droid 上的开源替代应用。

## 安装与配置流程

1. 建议在开始操作前先确保手机已开启 **ADB 调试** 作为稳妥保障。
2. 从项目仓库的 Releases 页面下载最新版 `noogle-microg.zip` 压缩包。
3. 在 Magisk 中刷入该模块并重启设备。
4. 打开 Magisk 应用，切换至 **模块** 标签页，点击 Noogle Magisk 旁的 **操作（Action）** 按钮以自动授予所需权限。
5. 在桌面启动器中打开 **microG 设置（microG Settings）**，进入 **自检（Self-Check）**：
   - 确认所有检查项均已勾选。
   - 确认“系统支持签名欺骗（System spoofs signature）”处于激活状态。
6. 如有推送通知或通过 FakeStore 获取应用的需求，可在 microG 中登录你的 Google 账号。
7. 生效中的模块文件保存在以下路径：
   ```bash
   /data/adb/modules/noogle-microg/
   ```

## 故障排查与常见问题

- **自检中提示“签名不正确”**：如果 microG 自检页面中的签名欺骗复选框仍未勾选，说明当前 ROM 缺少签名欺骗能力。请通过 Magisk 刷入签名欺骗模块，或在第三方 ROM 设置中开启签名欺骗开关。
- **首次开机后 microG 服务崩溃**：如果初次安装后 microG 服务出现间歇性崩溃，可使用维护者随附的 `install-user-apks.sh` 脚本，在保留模块的同时将独立版 microG APK 安装为普通用户应用，以解决 OEM 软件包数据库冲突。
