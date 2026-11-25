---
id: "librepods"
title: "LibrePods：在已 Root 安卓设备上解锁 AirPods 苹果生态功能"
sidebarTitle: "LibrePods"
description: "开源 Android 客户端与 LSPosed 模块，通过逆向苹果私有蓝牙协议，在安卓手机上实现 AirPods 主动降噪切换、入耳检测与电量弹窗等功能。"
category: "system-utilities"
tier: 1
searchQueries:
  - "LibrePods 下载安装"
  - "安卓使用 AirPods 降噪切换"
  - "LibrePods LSPosed 蓝牙 Hook"
  - "AirPods 安卓电量显示"
  - "LibrePods v2 重写版 APK"
prerequisites:
  - "已部署 Magisk、KernelSU 或 APatch Root 环境"
  - "支持 libxposed API 101 的 LSPosed 框架（Android 17 之前版本需勾选蓝牙 `com.android.bluetooth` 与设置作用域）"
conflicts:
  - "将系统蓝牙进程 `com.android.bluetooth` 加入 Root 隐藏或卸载挂载名单（会阻断 `libfluoride_hooks.so` 注入）"
  - "旧版 v1 刷机包或不同签名的第三方版本共存导致的签名冲突"
configPaths:
  - "/data/adb/lspd/"
  - "/data/data/me.kavishdevar.librepods/"
features:
  - "v2 重写版独立 APK（`me.kavishdevar.librepods`）内置 `AirPodsQSService` 快捷磁贴服务与 `LibrePodsService` 后台协议核心服务"
  - "基于 libxposed API 101（`KotlinModule`）与全架构原生库 `libfluoride_hooks.so`（支持 arm64-v8a、armeabi-v7a、x86、x86_64）Hook 安卓 Fluoride 蓝牙栈"
  - "支持在快捷设置面板、桌面小组件（`NoiseControlWidget`）及应用内切换主动降噪、通透模式、自适应与关闭模式"
  - "支持光学入耳检测与自动音频路由切换，摘下耳机自动暂停播放并切回扬声器（依赖 `LibrePodsAccessibilityService` 与音频路由权限）"
  - "实时监测左耳、右耳与充电盒电量，支持系统通知栏展示及 `BatteryWidget` 桌面电量小组件"
faq:
  - question: "为什么 LibrePods 在当前安卓版本上仍然需要 LSPosed？"
    answer: "由于苹果采用了非标准的私有蓝牙控制通道，且 Android 原生 Fluoride 蓝牙协议栈存在已知限制，普通第三方应用无法直接建立与 AirPods 通信的控制链路。LibrePods v2 内置了基于 libxposed API 101 的模块（`me.kavishdevar.librepods.XposedService`）及 `libfluoride_hooks.so`，可在运行时修补 `com.android.bluetooth` 行为，直至 Android 17 上游修复落地。"
  - question: "LibrePods v2 重写版 APK 与早期 v1 模块有何区别？"
    answer: "v2 重写版不再局限于系统分区刷入包，而是直接发布一体化独立应用 `LibrePods-FOSS-v2.0.0-alpha.4-200000004-release.apk`（包名 `me.kavishdevar.librepods`），集成了 `AirPodsQSService` 快捷磁贴、`LibrePodsService` 后台服务、原生 `BatteryWidget` / `NoiseControlWidget` 小组件以及 libxposed 蓝牙钩子。"
---

## 概述

由 **librepods-org/librepods** 开源维护的 **LibrePods**，是一套面向 Android 设备的苹果 AirPods 私有配件协议逆向实现方案。

虽然 AirPods 在任意安卓设备上都能作为标准蓝牙 A2DP 耳机播放音频，但诸如主动降噪（ANC）与通透模式切换、光学入耳佩戴检测、对话感知以及左右耳与充电盒精确电量读取等高阶特性，均依赖苹果私有控制握手协议。**LibrePods v2 重写版**（包名 `me.kavishdevar.librepods`）将前端界面、后台守护服务、桌面小组件与 LSPosed 蓝牙协议栈钩子整合进单一 FOSS 安装包（`LibrePods-FOSS-v2.0.0-alpha.4-200000004-release.apk`），为安卓用户提供接近原生 iOS 的耳机交互体验。

---

## 技术架构与工作原理

### 独立应用与 libxposed API 101 协同机制

通过分析 `me.kavishdevar.librepods` 安装包结构，其 v2 架构由以下核心组件协同驱动：

1. **核心服务层（`LibrePodsService` 与 `AirPodsQSService`）**：
   - `me.kavishdevar.librepods.services.LibrePodsService` 作为 `connectedDevice` 类型前台服务（`FOREGROUND_SERVICE_CONNECTED_DEVICE`）运行，负责维持与 AirPods H1/H2 芯片的双向控制会话、解析分体电量数据包并执行音频路由状态调度。
   - `me.kavishdevar.librepods.services.AirPodsQSService` 实现系统快捷设置磁贴接口（`BIND_QUICK_SETTINGS_TILE`），支持下拉状态栏一键切换降噪、通透或关闭模式。
   - `me.kavishdevar.librepods.services.LibrePodsAccessibilityService` 辅助响应系统媒体播放控制与状态联动事件。
2. **libxposed API 101 运行时注入（`XposedService` 与 `KotlinModule`）**：
   - 应用在 `META-INF/xposed/module.prop` 中声明了 `minApiVersion=101`、`targetApiVersion=101` 与 `staticScope=true`，并通过 `io.github.libxposed.service.XposedProvider` 和 `me.kavishdevar.librepods.XposedService` 对接框架。
   - 激活后，LSPosed 会加载 Java 入口 `me.kavishdevar.librepods.utils.KotlinModule` 以及原生钩子库 `libfluoride_hooks.so`（`META-INF/xposed/native_init.list`）与 `libhiddenapi.so`，覆盖 `arm64-v8a`、`armeabi-v7a`、`x86` 与 `x86_64` 四大架构。
3. **蓝牙栈作用域（Scope）控制**：
   - `META-INF/xposed/scope.list` 默认声明目标为 `com.android.bluetooth`、`com.android.settings` 与 `com.google.android.settings`，绕过 Fluoride 蓝牙栈对苹果 VendorID 及非标 SDP 记录的拦截。

---

## 安装与配置指南

### 第一步：确认运行环境
- 确保设备已完成 Root，且 **Magisk**、**KernelSU** 或 **APatch** 运行正常。
- 安装并激活支持 **libxposed API 101** 的 **LSPosed** 框架。

### 第二步：安装 APK 并启用作用域
1. 下载官方发布的 `LibrePods-FOSS-v2.0.0-alpha.4-200000004-release.apk`。
2. 直接像普通应用一样安装该 APK，或通过 ADB 执行安装命令：
   ```bash
   adb install LibrePods-FOSS-v2.0.0-alpha.4-200000004-release.apk
   ```
3. 打开 **LSPosed 管理器** -> **模块**，启用 **LibrePods**，并确认作用域中已勾选系统蓝牙（`com.android.bluetooth`）与设置应用。
4. 重启设备，使 `libfluoride_hooks.so` 原生钩子随蓝牙进程重新加载生效。

---

## 功能使用与日常配置

- **蓝牙配对与授权**：先在系统蓝牙设置中配对 AirPods，随后打开 LibrePods 主界面（`MainActivity`）授予附近设备扫描连接（`BLUETOOTH_CONNECT` / `BLUETOOTH_SCAN`）、通知及所需权限。
- **快捷磁贴与桌面小组件**：在控制中心添加由 `AirPodsQSService` 提供的快捷开关，也可将 `BatteryWidget`（电量小组件）和 `NoiseControlWidget`（降噪控制小组件）添加到桌面。
- **佩戴检测与耳机手势**：在应用内开启摘下耳机自动暂停播放、重新佩戴自动恢复，并自定义耳机柄按压与长按触发的操作映射。

---

## 常见问题与排查

- **无法识别 AirPods 高级功能或连接失败**：请检查 LSPosed 模块列表是否已勾选 `com.android.bluetooth`。若同时使用了 Shamiko 或其他 Root 隐藏策略，请勿对系统蓝牙进程启用全局环境卸载或阻断 Zygisk 注入。
- **从旧版 v1 升级出现签名冲突**：早期 v1 刷机包或旧版客户端的签名可能与 v2 重写版不同，升级前请先彻底卸载旧版模块与残余系统特权目录并重启，再安装 v2 APK。
