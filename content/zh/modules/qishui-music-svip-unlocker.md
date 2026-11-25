---
id: "qishui-music-svip-unlocker"
title: "汽水音乐 SVIP 与去广告模块 (me.bingyue.fuckqishui)"
description: "面向汽水音乐（海外版 Luna Music）的 LSPosed 运行时 Hook 模块，用于解锁 SVIP 会员特权、去除应用内广告并开启无损音质串流。"
category: "xposed-runtime-hooks"
author: "bingqiu456"
version: "3.0"
updatedAt: "2026-10-04"
compatibility: ["LSPosed"]
---

## 概述与系统架构

由开发者 bingqiu456 制作的 **汽水音乐 SVIP 与去广告（Soda Music SVIP & AdBlock，`me.bingyue.fuckqishui`）** 是一款专为字节跳动旗下流媒体音乐平台 **汽水音乐**（国际版为 *Luna Music*）打造的 Xposed/LSPosed 运行时 Hook 模块。

该模块借助 LSPosed 在目标应用的 ART 进程运行时内存空间中直接运作，动态拦截账户鉴权逻辑、功能开关校验以及广告 SDK 调度器。由于所有修改均在易失性进程内存中完成，无需对目标 APK 进行反编译重打包或二次签名，从而完整保留了原版应用的签名完整性及自动更新兼容性。

## 安装包技术分析

对发布版 APK（`_3.0.apk`）的分析证实了其现代化的 Xposed 技术实现：

- **模块包名**：`me.bingyue.fuckqishui`
- **Hook 核心架构**：集成原生 DexKit 检索库（`lib/arm64-v8a/libdexkit.so`、`lib/armeabi-v7a/libdexkit.so`、`lib/x86_64/libdexkit.so`），在代码混淆的版本迭代中依然能够精准定位目标类与方法符号。
- **Hook 入口声明**：采用标准 Xposed 初始化入口配置（`assets/xposed_init`）。

## 核心功能

1. **SVIP 会员特权模拟**：Hook 用户账户信息校验方法，将当前账号状态模拟为高级订阅会员，解锁 VIP 专享曲库与独家专辑试听权限。
2. **高规格无损音质解锁**：无需开通月度 VIP 订阅即可直接切换并播放无损音质（FLAC / 高码率 AAC）音频流。
3. **全方位广告屏蔽**：彻底拦截冷启动开屏广告、推荐信息流音频插播广告以及界面横幅广告。
4. **本地缓存下载限制解除**：绕过 VIP 离线下载配额限制，支持将音频缓存至本地供离线收听。

## 安装与配置

### 前置要求
- 已通过 Magisk、KernelSU 或 APatch 获取 Root 权限的 Android 9.0–14 设备。
- 已安装并启用 **LSPosed 框架**（Zygisk 或 Riru 版本均可）。

### 第一步：安装模块 APK
使用系统安装器或通过 ADB 安装 `_3.0.apk`：
```bash
adb install _3.0.apk
```

### 第二步：在 LSPosed 管理器中配置作用域
1. 通过通知栏或桌面图标打开 **LSPosed 管理器**。
2. 进入 **模块** 标签页，找到 **汽水音乐 SVIP & 去广告**（Soda Music SVIP & AdBlock）。
3. 打开模块启用开关。
4. 在作用域列表中勾选 **汽水音乐**（`com.luna.music` / `com.ss.android.ugc.aweme.music`）。

### 第三步：重启目标应用
强制停止并重新启动音乐客户端以加载 Hook：
```bash
am force-stop com.luna.music
```

## 安全与使用注意事项

- **严格隔离作用域**：请仅将 LSPosed 作用域限定在汽水音乐客户端本身，切勿勾选系统框架或其他无关应用。
- **账号与服务端鉴权说明**：本模块仅在本地客户端层面绕过界面与播放权限检查；部分受严格服务端令牌（Token）实时校验的版权限定曲目仍可能受到服务器鉴权限制。
