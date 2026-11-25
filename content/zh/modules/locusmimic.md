---
id: "locusmimic"
title: "LocusMimic·位置模拟与路线仿真模块 (com.locusmimic.app)"
description: "面向 Android 11+ 已 Root 设备的 LSPosed 高级 GPS 位置伪装、自定义路线模拟与分应用独立兼容 Hook 模块。"
category: "xposed-runtime-hooks"
author: "wchunlin1006"
version: "2.1.0"
updatedAt: "2026-10-04"
compatibility: ["LSPosed"]
sidebarTitle: "LocusMimic·位置模拟 (com.locusmimic.app)"
tier: 1
searchQueries: []
prerequisites: []
conflicts: []
configPaths: []
features: []
faq: []
---

## 概述与系统架构

由开发者 wchunlin1006 在 GitHub 开源维护的 **LocusMimic（`com.locusmimic.app`）** 是一款专为运行 LSPosed 的 Android 11 至 Android 15 已 Root 设备打造的高级位置模拟与轨迹导航欺骗模块。

常规基于开发者选项的模拟位置应用很容易触发反作弊风控或企业安全检测（例如 `Location.isFromMockProvider()` 会直接返回 `true`）。与之不同，LocusMimic 通过 Xposed 直接在 Java 系统框架层工作：它在目标应用的运行进程空间内实时拦截定位请求，并返回高度逼真的 GPS 坐标、NMEA 语句、Wi-Fi BSSID 及蜂窝基站参数，使客户端应用完全感知不到任何模拟痕迹。

## 核心模拟能力

1. **零模拟标记检测**：无需开启开发者选项中的“选择模拟位置信息应用”，从根源上绕过常规模拟位置状态校验。
2. **拟真路线插值仿真**：支持自定义绘制行进轨迹，并可叠加真实的速度波动、海拔漂移与 GPS 航向角动态修正。
3. **分应用独立配置**：可同时为不同目标应用分配各自独立的坐标或行进路线，完全不影响系统全局及其他应用的正常定位。
4. **基站与 Wi-Fi 协同伪装**：同步模拟匹配的蜂窝基站标识（MCC/MNC/LAC/CID）与周边 Wi-Fi 扫描列表，轻松应对高德地图、百度地图及 Google Play 服务等多源融合定位 SDK。
5. **现代 Jetpack Compose 界面**：基于 Material 3 与 Jetpack Compose 构建，界面流畅响应迅速。

## 安装与配置

### 前置要求
- 运行 Android 11.0 及以上版本的设备。
- 已通过 Magisk、KernelSU 或 APatch 获取 Root 权限。
- 已安装并在 Zygisk 模式下正常运行的 **LSPosed 框架**。

### 第一步：安装 APK
从 GitHub Releases 下载并安装最新版 `LocusMimic` 安装包。

### 第二步：在 LSPosed 中启用作用域
1. 打开 **LSPosed 管理器**。
2. 在模块列表中找到并点击 **LocusMimic**。
3. 打开模块启用开关。
4. 在作用域（Scope）列表中勾选需要模拟位置的目标应用（如社交、外送或运动打卡类应用）。

### 第三步：设置坐标并启动模拟
1. 打开 **LocusMimic** 应用。
2. 在交互式地图上选点，或直接输入精确的经纬度坐标。
3. 选择定点静态模式或规划多点行进路线。
4. 点击 **开始模拟**，随后打开目标应用即可生效。

## 效果验证

如需在命令行确认目标应用已正确获取到模拟坐标：
```bash
# 转储系统定位管理器客户端缓存状态
dumpsys location | grep -A 5 "Last Known Locations"
```

## 安全与合规使用

- **作用域隔离**：除非模块文档明确要求，切勿勾选“系统框架（System Framework）”作用域；严格遵循按需分应用勾选原则可避免系统出现稳定性异常。
- **使用规范**：本模块仅适用于开发者定位调试、个人隐私保护及应用兼容性测试场景。
