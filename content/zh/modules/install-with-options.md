---
id: "install-with-options"
title: "Install with Options：基于 Shizuku 的设备端高级 APK 安装器"
sidebarTitle: "Install with Options"
description: "由 zacharee 开发的开源（FOSS）软件包安装工具，利用 Shizuku Shell 权限在现代 Android 上安装仅限测试包、拆分 APK 并绕过低目标 SDK 安装拦截。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Install with Options APK 下载"
  - "Android 14 绕过低版本目标 SDK 安装拦截"
  - "免电脑安装 testOnly 测试包"
  - "Shizuku 拆分 APK 安装工具"
  - "InstallWithOptions zacharee"
prerequisites:
  - "Android 8.0（Oreo）及更高版本（绕过目标 SDK 限制需 Android 14+）"
  - "通过无线 ADB 或 Root（Magisk/KernelSU/APatch）激活的 Shizuku 服务"
conflicts:
  - "CPU 架构不匹配（在 Pixel 7/8/9 等纯 64 位硬件上安装 32 位旧版应用会报 INSTALL_FAILED_NO_MATCHING_ABIS）"
  - "未打补丁系统上的签名不一致更新（覆盖安装不同签名需配合核心破解 CorePatch）"
configPaths:
  - "/data/data/dev.zwander.installwithoptions/"
features:
  - "低目标 SDK 拦截绕过：传递 --bypass-low-target-sdk-block 参数，在 Android 14+ 上顺利安装 Android 4/5 时代老应用"
  - "测试包支持：直接安装编译时带有 android:testOnly='true' 标记的开发测试包"
  - "拆分 APK 与 Bundle 安装：无需额外工具即可合并安装基础包与配置分包（.apks、.xapk）"
  - "纯手机端本地执行：彻底摆脱对电脑端 'adb install' 命令的依赖"
faq:
  - question: "为什么 Android 14 默认阻止安装旧版本应用？"
    answer: "从 Android 14 开始，Google 的 PackageManagerService 强制要求最低 targetSdkVersion 为 23（Android 6.0 Marshmallow），以防恶意软件借旧 API 规避现代运行时权限模型。使用系统默认安装器侧载老应用会失败并报错 `INSTALL_FAILED_DEPRECATED_SDK_VERSION`。Install with Options 通过 Shizuku Shell 自动附加 `--bypass-low-target-sdk-block` 参数解决该问题。"
  - question: "Install with Options 能绕过 APK 签名冲突吗？"
    answer: "不能。Install with Options 仅负责传递系统合法的安装参数（测试包、降级、目标 SDK），不会 Hook 系统内存。若需在不卸载原应用的前提下覆盖安装不同签名的更新包，必须在 LSPosed 中安装并启用 CorePatch（核心破解）模块。"
  - question: "为什么部分老应用仍提示 INSTALL_FAILED_NO_MATCHING_ABIS？"
    answer: "现代处理器（如 Google Tensor G3/G4、骁龙 8 Gen 3）已彻底移除硬件级 ARM32（armeabi-v7a）支持，仅以纯 64 位模式运行。若老应用仅包含 32 位原生库，硬件层面无法执行，无论传入何种安装参数都会失败。"
---

## 概述

自 Android 14 起，Google 大幅收紧了设备端侧载（Sideload）应用的限制：系统会拦截面向过旧 Android API 级别的应用（防止恶意软件绕过运行时权限机制）、拒绝开发者测试构建（`android:testOnly="true"`），并限制自定义安装参数。

过去要绕开这些限制，用户必须将手机连接至电脑并通过 ADB 执行命令行指令：
```bash
adb install --bypass-low-target-sdk-block -t app.apk
```

由知名 Android 开发者 zacharee（Zachary Wander）打造的 **Install with Options** 将桌面级 `pm install` 能力完整搬到了手机端。通过与 **Shizuku** 对接，该应用获得 Shell 级软件包安装权限，让用户可以随时按需勾选各种安装参数。

---

## 技术架构与安装参数

在 Install with Options 中打开 APK 或拆分安装包时，应用会经由 Shizuku 的特权 Shell IPC 直接向 `PackageInstaller.SessionParams` 传递参数：

- **Install with Options 界面**：用户选择 `.apk`、`.apks` 或 `.xapk` 文件并勾选目标安装选项（如绕过低 SDK、允许测试包、请求降级安装）。
- **Shizuku 服务**：借助 UID 2000 的特权 Shell IPC（`android.permission.INSTALL_PACKAGES`）分派安装会话参数。
- **Android PackageInstaller 会话**：应用选定标志执行安装：
  - `--bypass-low-target-sdk-block`（在 Android 14+ 上安装面向 Android 5.1 及以下系统的老应用）
  - `-t`（`INSTALL_ALLOW_TEST` - 允许安装仅限测试的应用包）
  - `-d`（`INSTALL_REQUEST_DOWNGRADE` - 允许覆盖安装更低版本号的应用）
  - `--dont-kill`（更新安装期间保持现有进程不被强行终止）

---

## 核心功能特性

### 1. 绕过 Android 14+ 低目标 SDK 拦截
现代设备默认拒绝安装针对 Android 5.1 或更早期版本编译的经典游戏与老旧实用工具。Install with Options 可自动传入 `--bypass-low-target-sdk-block`，让老应用在 Android 14 与 Android 15 上顺畅安装。

### 2. 测试版构建安装（`-t`）
Android Studio 默认会为调试构建添加 `android:testOnly="true"` 属性，标准系统安装器会抛出 `INSTALL_FAILED_TEST_ONLY` 错误。Install with Options 可直接接管并安装此类文件，无需对 APK 重新签名或反编译修改。

### 3. 原生支持拆分 APK / App Bundle
现代应用常以多拆分 APK 形式分发（基础 APK + 语言包 + 屏幕 DPI 资源包）。Install with Options 支持直接读取 `.apks`、`.xapk` 及多选拆分 APK 文件，将其流式写入同一原子安装会话中完成安装。

---

## 使用指南

1. 在设备上安装并激活 **Shizuku**。
2. 侧载安装并启动 **Install with Options**。
3. 在弹出的提示中授予 Shizuku 权限。
4. 点击 **选择文件（Select File）**，选取 `.apk`、`.apks` 或 `.xapk` 文件。
5. 在安装选项面板中按需勾选：
   - 在 Android 14+ 安装老应用时勾选 **Bypass Low Target SDK Block**。
   - 安装开发测试 APK 时勾选 **Allow Test-Only**。
   - 需要降级回退版本时勾选 **Allow Downgrade**。
6. 点击 **Install** 提交安装任务。

---

## 常见错误排查

### `INSTALL_FAILED_NO_MATCHING_ABIS`
- **原因**：安装包内仅包含设备不支持的 CPU 架构原生库（例如在 Pixel 7/8/9 等纯 64 位设备上安装 32 位 ARM 应用）。
- **解决办法**：此为硬件处理器物理限制，只能寻找包含 64 位（`arm64-v8a`）原生库的版本。

### `INSTALL_FAILED_UPDATE_INCOMPATIBLE`
- **原因**：待安装包的签名证书与设备上已安装应用的签名不一致。
- **解决办法**：Install with Options 无法伪造加密签名。请在 LSPosed 中启用 **CorePatch（核心破解）** 以绕过签名校验。
