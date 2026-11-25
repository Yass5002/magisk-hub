---
id: "ih8securelock"
title: "ih8SecureLock：Zygisk 截屏限制与截屏检测绕过模块"
sidebarTitle: "ih8SecureLock"
description: "由 j-hc 开发的 Zygisk 模块，通过拦截 Android FLAG_SECURE 窗口标志与截屏检测 Binder 调用，实现受限应用截图与录屏功能，支持 Android 10 至 17。"
category: "security-certificates"
tier: 1
searchQueries:
  - "ih8securelock magisk 模块"
  - "j-hc ih8securelock zygisk 下载"
  - "android 15 绕过 flag_secure 截图"
  - "root 阻止应用检测截屏"
  - "zygisk 受限应用强行截屏录屏"
prerequisites:
  - "Android 10 至 Android 17"
  - "启用 Zygisk 的 Magisk 或 KernelSU"
  - "目标应用绝对不能被加入任何 DenyList（排除列表）或隔离列表"
  - "必须为目标应用关闭“取消挂载模块”（Unmount modules）选项"
conflicts: []
configPaths:
  - "/data/adb/modules/ih8SecureLock/"
features:
  - "屏蔽 `FLAG_SECURE` 窗口标志：移除防截屏标记，恢复受保护应用内的正常截图与屏幕录制"
  - "阻断截屏事件监听：拦截 Android IPC Binder 接口，防止应用感知或上报用户的截屏操作"
  - "跨代系统广泛兼容：持续维护，支持从 Android 10 直至 Android 17 的系统版本"
  - "独立 Zygisk 运行：无需依赖厚重的 Xposed 或 LSPosed 框架，仅通过轻量级 C++ Binder 挂钩实现"
faq: []
---

## 概述

由 `j-hc` 开发的 **ih8SecureLock** 是一款开源 Zygisk 模块，专门用于绕过 Android 的 `WindowManager.LayoutParams.FLAG_SECURE` 窗口保护限制与系统截屏检测 API。在原生 Android 机制下，银行应用、流媒体客户端、阅后即焚聊天软件与身份认证应用常会将其显示窗口标记为安全界面，导致系统截屏直接黑屏、禁止屏幕共享，甚至在用户触发截图时向开发者上报事件通知。

ih8SecureLock 在 Zygisk 层运行，于目标进程创建时直接挂钩其 Binder 跨进程通信事务。它会剥离显示窗口的安全标记并废除截屏监听回调，在不修改应用安装包也不依赖臃肿 Xposed 框架的前提下，将完整的屏幕捕获控制权交还给用户。

## 前置要求与关键配置规则

- **Android 版本**：Android 10 至 Android 17。
- **Root 框架**：启用 **Zygisk** 的 Magisk 或 KernelSU。

### ⚠️ 强制配置规范

由于 ih8SecureLock 必须在目标应用进程启动时注入其底层原生挂钩库：
1. **切勿将目标应用放入 Root 管理器的 DenyList（排除列表）、Shamiko 列表或隐藏列表中。** 一旦应用被列入 DenyList，Zygisk 就会从该进程脱离，导致 ih8SecureLock 无法修改其窗口标志。
2. 在 KernelSU 或 APatch 中，务必为需要截图的目标应用**关闭“取消挂载模块”（Unmount modules）**开关。

目前没有已知的模块冲突。

## 架构与工作原理

ih8SecureLock 依赖底层 Binder 拦截机制（`binder.cpp` 与 `module.cpp`）：
- **窗口标记抹除**：当应用向 Android 的 `WindowManagerService` 提交包含 `FLAG_SECURE` 的窗口参数时，挂钩逻辑会拦截该 IPC 事务并屏蔽对应标志位。
- **监听回调阻断**：Android 14 引入了原生的截屏检测回调接口（`Activity.ScreenCaptureCallback`）。ih8SecureLock 会拦截这些注册调用，使应用无法获知用户是否按下了截屏组合键或启动了录屏软件。

## 安装与验证

1. 从项目发布页下载最新的 `ih8SecureLock-*.zip`。
2. 通过 Magisk 或 KernelSU 刷入模块。
3. 重启设备。
4. 打开受截屏限制的应用（例如银行 App 或隐私聊天软件）。
5. 尝试使用标准物理按键截屏（`电源键 + 音量减`）。
6. 此时系统将正常截取清晰的可见界面，不再输出全黑图片。

## 故障排查

- **截屏依然黑屏**：请再次检查确认目标应用未被加入 Magisk 的 DenyList，且 Shamiko 未对该应用屏蔽 Zygisk。执行强行停止（`am force-stop <package>`）后重新打开应用再试。
- **银行应用因未进 DenyList 而检测到 Root**：若银行应用因为移出排除列表而触发 Root 检测，请使用不分离 Zygisk 的隐匿方案（如搭配 Zygisk Next 或针对性的命名空间隔离方案），确保在保留 Zygisk 挂钩的同时隐藏 Root 特征。
