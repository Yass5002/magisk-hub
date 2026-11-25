---
id: "disable-flag-secure"
title: "DisableFlagSecure (Enable Screenshot)：解除 Android 12–16 截屏限制与截屏录屏检测"
sidebarTitle: "DisableFlagSecure"
description: "由 LSPosed/DisableFlagSecure 官方维护的 Xposed 模块（io.github.lsposed.disableflagsecure），支持 Android 12–16 及各大厂商系统，解除 FLAG_SECURE 限制并屏蔽截屏与录屏检测。"
category: "xposed-runtime-hooks"
tier: 1
searchQueries:
  - "DisableFlagSecure 下载"
  - "Enable Screenshot LSPosed 模块"
  - "Android 15 16 解除禁止截屏"
  - "屏蔽 Android 14 截屏检测"
  - "HyperOS ColorOS One UI 绕过 FLAG_SECURE"
prerequisites:
  - "官方 LSPosed 框架（需支持 libxposed API 101；明确不支持非官方第三方魔改 LSPosed）"
  - "Android 12–16 原生或厂商官方固件（支持小米 HyperOS、OPPO/一加/真我 ColorOS/RealmeUI/OxygenOS 与三星 One UI；不支持第三方类原生 Custom ROM）"
conflicts:
  - "非官方魔改版 LSPosed 框架或旧版 Xposed 框架"
  - "其他同时 Hook `WindowManagerService` 或 `FLAG_SECURE` 的同类模块"
configPaths:
  - "/data/adb/lspd/"
features:
  - "解除应用窗口的 `WindowManager.LayoutParams.FLAG_SECURE` 安全标志限制，允许在受限页面正常截屏与录屏"
  - "屏蔽 Android 14+ 系统级截屏检测回调（防止应用收到截屏通知）"
  - "屏蔽 Android 15+ 系统级录屏检测回调（防止应用感知当前正在录屏）"
  - "深度适配 Android 12–16 主流原厂系统：AOSP、小米 HyperOS、OPlus 系（ColorOS / RealmeUI / OxygenOS）及三星 One UI"
  - "极致轻量化设计（`io.github.lsposed.disableflagsecure`，APK 仅约 20 KB），基于 libxposed API 101 并采用 `staticScope=true` 无后台界面架构"
faq:
  - question: "在 LSPosed 作用域中应该勾选哪些应用？"
    answer: "请**仅勾选**模块推荐的默认系统作用域（包括 `system`、`com.android.systemui` 及对应厂商截图服务如 `com.miui.screenshot`、`com.oplus.screenshot`、`com.oplus.appplatform`、`com.flyme.systemuiex`）。切勿手动勾选普通第三方应用，否则不仅无效还可能引发异常。"
  - question: "为什么作者明确提示不支持第三方 Custom ROM 或非官方 LSPosed？"
    answer: "该模块直接针对 AOSP 及主流原厂系统（HyperOS、ColorOS/RealmeUI/OxygenOS、One UI）的窗口管理与截屏服务实现 Hook；第三方魔改 ROM 与非官方 LSPosed 分支往往改动了内部类签名或 API 行为，因此官方仓库明确不予支持。"
  - question: "安装后桌面为什么找不到应用图标？"
    answer: "DisableFlagSecure（`io.github.lsposed.disableflagsecure`）是一款纯底层免配置模块（`app-release.apk` 体积仅约 20.8 KB），未包含独立图形设置界面。只需在 LSPosed 中启用并保持推荐作用域，重启后即可自动生效。"
---

## 概述

**Enable Screenshot**（仓库与社区常用名 **DisableFlagSecure**，托管于 `LSPosed/DisableFlagSecure`）是由 **LSPosed** 官方团队维护的系统级 Xposed 模块。

出于隐私或版权保护目的，许多金融、聊天与流媒体应用会在窗口属性中设置 `WindowManager.LayoutParams.FLAG_SECURE`，导致截屏报错或录屏画面全黑。此外，**Android 14** 引入了官方截屏检测 API，**Android 15** 进一步增加了录屏状态检测回调，使应用能够直接感知用户的截屏和录屏行为。

DisableFlagSecure 直接在系统框架与厂商截屏组件层拦截上述限制与检测回调，在 **Android 12 至 Android 16** 上同时实现解除截屏录屏限制与静默屏蔽检测通知。

---

## 技术架构与工作原理

### libxposed API 101 与系统/厂商作用域机制

通过检查 `v5.0.1` 安装包（`app-release.apk`，包名 `io.github.lsposed.disableflagsecure`）内部结构，可见其采用极其克制的系统级设计：

- **零冗余精简架构**：整个安装包体积仅约 20.8 KB，仅包含 `classes.dex`、`AndroidManifest.xml`、`resources.arsc` 及 `META-INF/xposed/*` 元数据，无任何原生 `.so` 库或常驻前台界面。
- **libxposed API 101 静态作用域**：`META-INF/xposed/module.prop` 声明了 `minApiVersion=101`、`targetApiVersion=101` 与 `staticScope=true`。
- **预设作用域清单（`META-INF/xposed/scope.list`）**：
  - `system`（系统框架 `system_server`，覆盖 `WindowManagerService` 与截屏/录屏检测分发逻辑）
  - `com.android.systemui`（系统界面截屏与最近任务缩略图处理）
  - `com.miui.screenshot`（小米 HyperOS / MIUI 截屏组件）
  - `com.oplus.screenshot` 与 `com.oplus.appplatform`（OPPO / 一加 / 真我 OPlus 系统截屏与平台服务）
  - `com.flyme.systemuiex`（魅族 Flyme 系统界面扩展）

通过直接挂钩系统框架与厂商截屏服务而非逐一注入第三方应用，模块无需用户手动维护应用黑名单即可全局生效。

---

## 系统兼容性范围

根据 `LSPosed/DisableFlagSecure` 官方文档说明：
- **支持系统版本**：Android 12 – 16 原厂固件（**明确不支持第三方 Custom ROM**）
- **专项适配厂商 OS**：
  - 小米 **HyperOS**
  - **OPlus OS**（**ColorOS** / **RealmeUI** / **OxygenOS**）
  - 三星 **One UI**
- **框架要求**：仅支持官方 **LSPosed**（不支持非官方分支或修改版 LSPosed）

---

## 安装与启用步骤

1. 从 `LSPosed/DisableFlagSecure` 官方发布页下载 `app-release.apk`。
2. 在已 Root 的设备上安装该 APK：
   ```bash
   adb install app-release.apk
   ```
3. 打开 **LSPosed 管理器** -> **模块** -> **Enable Screenshot / DisableFlagSecure**。
4. 打开模块开关，并**仅保留勾选**列表中的推荐系统作用域（切勿额外勾选普通第三方 App）。
5. **重启设备**，等待系统框架与 SystemUI 重新加载模块钩子。

---

## 常见问题与注意事项

- **在第三方类原生 ROM（Custom ROM）上无效或报错**：许多第三方 ROM 已自带或魔改了类似功能，导致窗口管理类签名与 AOSP/原厂固件不一致，上游已明确不受理 Custom ROM 问题。
- **流媒体加密视频画面仍为黑屏**：DisableFlagSecure 解除的是软件窗口层面的 `FLAG_SECURE` 与检测回调；部分依赖硬件级 Widevine L1 DRM 安全合成层（Protected Surface）的视频流在 SurfaceFlinger 硬件渲染阶段仍受硬件密钥保护，属于正常现象。
