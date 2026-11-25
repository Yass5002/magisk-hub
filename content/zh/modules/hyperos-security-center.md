---
id: "hyperos-security-center"
title: "HyperOS Security Center 修改版：解锁游戏加速、隐私管控与系统诊断功能"
sidebarTitle: "HyperOS Security Center"
description: "修改版小米澎湃 OS 手机管家套件，解锁游戏加速媒体控制、隐藏系统应用、FBO 存储优化及全应用联网控制，同时去除 Root 与账号校验。"
category: "system-environment"
tier: 1
searchQueries:
  - "澎湃 OS 手机管家修改版 Magisk"
  - "Kashi HyperOS Security Center 下载"
  - "小米游戏工具箱解锁媒体控制"
  - "澎湃 OS Root 隐藏系统应用"
  - "澎湃 OS 核心破解禁用签名校验"
prerequisites:
  - "运行官方或移植版澎湃 OS 的小米、Redmi 或 POCO 设备"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "Android 14 及以上系统需预先禁用 APK 签名校验（使用核心破解 Core Patch 或安装包保护补丁）"
conflicts:
  - "非小米系第三方 ROM（AOSP、LineageOS、Pixel Experience、OxygenOS）"
  - "不兼容 HyperOS Security Center V7+ 的旧版 MIUI 固件"
configPaths:
  - "/data/adb/modules/hyperos-security-center/"
features:
  - "游戏工具箱媒体控制：在游戏浮窗侧边栏直接添加音频与媒体播放快捷控制"
  - "隐藏系统应用：将原厂应用锁与隐藏应用功能扩展至系统预装应用"
  - "联网自由管控：解除限制，允许用户彻底禁用系统应用的 Wi-Fi 或移动数据联网权限"
  - "硬件诊断解锁：开放焕新存储（FBO）手动优化与更详尽的应用亮屏耗电统计"
  - "去除 Root 检测：剥离原厂手机管家内置的 Root 与 Bootloader 解锁状态检测例程"
  - "解除账号绑定限制：取消部分功能菜单对小米账号登录或插入激活 SIM 卡的强制校验"
faq: []
---

## 概述

**HyperOS Security Center** 由 Kashi 修改并托管于 Mods-Center，是针对小米核心系统应用 `com.miui.securitycenter`（手机管家）的无侵入式修改模块。在出厂固件中，小米会依据销售地区（国际版与国行版）及机型定位人为屏蔽部分特性，同时内置 Root 检测机制以禁用特定安全与电池管理功能。

本模块通过无系统分区修改（Systemless）方式覆盖挂载已解锁补丁版澎湃 OS 手机管家，在不修改只读 `/system` 分区的情况下恢复跨区域功能完整性，开放焕新存储（FBO）等隐藏开关、启用系统应用隐藏，并移除底层遥测与环境校验。

## 前置要求与兼容性

- **适用固件**：仅兼容搭载官方或移植版澎湃 OS（HyperOS）的小米、Redmi 与 POCO 手机，无法在原生 AOSP 或其他厂商定制系统上运行。
- **Root 环境**：支持 Magisk v24+ 与 KernelSU。
- **Android 14+ 核心破解要求**：
  - Android 14 对系统级 APK 覆盖挂载引入了更严格的签名校验机制。
  - 若在 Android 14 及更高版本（HyperOS 1.0 / 2.0）刷入本模块，必须事先通过 LSPosed 配合 Core Patch（核心破解）或专用包管理补丁 **禁用 APK 签名验证**。未打补丁直接刷入会导致开机异常或系统界面持续闪退。

## 核心增强特性

### 1. 游戏内媒体控制集成
在游戏加速（Game Turbo）悬浮工具栏中集成专用媒体播放控制面板，玩家无需下拉通知栏即可在游戏过程中直接暂停、切歌或调节流媒体音频。

### 2. 全方位应用管理
- **隐藏系统应用**：解除此前保护预装系统应用免被隐藏或上锁的白名单限制。
- **精细化联网隔离**：恢复禁用预装厂商应用 Wi-Fi 与蜂窝移动网络权限的能力。
- **解耦 SIM 卡与小米账号**：禁用在缺少有效 SIM 卡或未登录小米账号时拦截特定优化子菜单的强制校验。

### 3. 诊断与存储底层优化
- **焕新存储（FBO）**：开放手动及自动 FBO（File-Based Optimization）整理入口，对 UFS 闪存碎片块进行优化。
- **扩展电池遥测**：公开原本在国际版固件中被隐藏的屏幕耗电详情与分组件功耗统计数据。
- **剥离 Root 检测**：中和安全扫描器内部将 Magisk 或 KernelSU 二进制文件标记为风险威胁的逻辑。

## 安装与配置步骤

1. 确认设备正在运行兼容的澎湃 OS 系统版本。
2. 若为 Android 14 及以上系统，请先确保已通过 LSPosed 与核心破解（Core Patch）开启签名验证绕过。
3. 在 Magisk 或 KernelSU 模块管理器中刷入发布的 ZIP 压缩包。
4. 重启手机。
5. 从桌面打开 **手机管家**，依次进入 **省电与电池** 及 **游戏加速**，确认已解锁各项增强功能。

## 故障排查

- **开机后手机管家持续闪退**：通常由 APK 签名校验未通过引起。请重新检查 LSPosed 中是否已激活核心破解（Core Patch），并在启用本模块前确认已勾选禁用签名校验相关选项。
- **全局隐身模式快捷开关缺失**：下拉打开控制中心编辑面板，找到新解锁的“隐身模式（Incognito Mode）”磁贴并拖入常用快捷开关区域即可。
