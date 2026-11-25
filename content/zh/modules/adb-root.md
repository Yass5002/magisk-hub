---
id: "adb-root"
title: "ADB Root：面向正式版 ROM 的免授权 Root 权限 ADB 守护进程模块"
sidebarTitle: "ADB Root"
description: "针对 Android 9/10 设备将系统 adbd 替换为修补版 AOSP 二进制文件，实现直接以 Root 权限运行 adb root 并跳过 USB 调试授权验证。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "adb root Magisk 模块下载"
  - "evdenis adb_root"
  - "Android 9 10 开启 adb root"
  - "跳过 ADB USB 授权验证 Root"
  - "adb remount 解锁验证模块"
prerequisites:
  - "仅支持 Android 9 (Pie) 或 Android 10 (Q)"
  - "64 位处理器架构（arm64/aarch64）"
  - "Magisk Root 环境"
conflicts:
  - "不支持 Android 11 及以上版本"
  - "不支持 Android 8 (Oreo) 及以下版本"
  - "不支持 32 位（armv7）或 x86/x86_64 架构设备"
configPaths:
  - "/data/adb/modules/adb_root/"
features:
  - "Root 权限 ADB 守护进程：让系统 adbd 进程默认以 root UID/GID 权限运行"
  - "免除 USB 密钥验证：连接开发主机时跳过 RSA 主机密钥确认弹窗"
  - "解锁重新挂载与写入能力：在正式版厂商固件上启用 adb remount 与 adb disable-verity 命令"
  - "纯净 AOSP 修补编译：直接基于官方 Android Open Source Project 源码树移除权限降级限制编译而成"
  - "专业开发调试利器：专为底层固件调试与自动化设备批量部署设计"
faq:
  - question: "为什么 ADB Root 仅兼容 Android 9 和 Android 10？"
    answer: "Android 11 对 adbd 进行了重大架构重构，引入了动态链接器命名空间隔离与独立的 APEX 模块分发机制（com.android.adbd）。本模块内置的修补版二进制文件仅针对 Android 9/10 的用户态运行库编译。"
  - question: "日常使用可以一直开启这个模块吗？"
    answer: "强烈不建议。本模块明确定义为非安全模式下的开发者调试工具。以 Root 身份运行 adbd 且禁用 USB 授权验证意味着，任何通过 USB 连接你手机的电脑无需解锁屏幕即可获取完整的存储读写与最高 Root 权限。调试完成后请务必关闭该模块。"
---

## 概述

由 **evdenis** 开发的 **ADB Root** 是一款专用的开发调试模块，能够强制 Android 的 ADB 守护进程（`adbd`）在正式版（user build）固件上以原生 Root 权限运行，同时跳过 USB 密钥认证步骤。

在正式出厂的“user”编译版本 Android 系统中，在电脑终端执行 `adb root` 会报错 `adbd cannot run as root in production builds`。ADB Root 通过将原厂 `adbd` 替换为移除 `ro.secure` 与 `ro.debuggable` 校验的 AOSP 编译版二进制程序，让你通过 USB 直接获得即时 Root 调试权限。

---

## 技术架构与工作原理

### 修补版 AOSP ADB 守护进程

本模块通过替换系统 `adbd` 二进制文件来实现提权：

1. **移除降权调用**：修补后的守护进程移除了 `should_drop_privileges()` 与 `should_drop_capabilities_bounding_set()` 函数调用，确保 `adbd` 始终保持 UID `0`（root）运行，而不会降权切换至低权限的 `shell` 用户。
2. **绕过 RSA 鉴权**：剥离主机 RSA 指纹校验逻辑，设备连接 USB 后自动授予调试授权。
3. **Magic Mount 挂载**：在开机阶段通过系统无侵入机制替换 `/system/bin/adbd`。

---

## 安装与配置

1. **核对系统兼容性**：确保设备运行 **Android 9 (Pie)** 或 **Android 10 (Q)** 且为 **arm64/aarch64** 架构。严禁在 Android 11+ 或 32 位设备上刷入。
2. 下载最新版的 `adb_root-*.zip` 安装包。
3. 在 Magisk 中刷入该模块。
4. 重启设备。
5. 使用数据线连接电脑并验证 Root 状态：
   ```bash
   adb shell whoami
   # 返回结果：root
   ```

---

## 配置与使用

本模块无需额外配置。启用模块并重启后，`adbd` 即自动在后台以 Root 权限监听调试连接。

---

## 常见问题与排查

- **在 Android 11+ 上卡开机动画（Bootloop）**：在 Android 11 及更高版本上刷入本模块会导致系统崩溃，因为新系统依赖 APEX 封装的 `adbd`。若设备无法正常开机，请进入 Magisk 安全模式或通过 TWRP 终端执行删除命令移除模块（`rm -rf /data/adb/modules/adb_root`）。
