---
id: "hail"
title: "Hail（雹）：基于 Shizuku、Root 与 Device Owner 的高阶应用冻结工具"
sidebarTitle: "Hail（雹）"
description: "由 aistra 开发的开源（FOSS）应用生命周期管理工具，利用 Android 原生停用、隐藏与暂停接口按需冻结后台进程。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Hail 雹 APK 下载"
  - "Hail Shizuku 冻结软件教程"
  - "Android 免 Root 冻结后台应用"
  - "Hail 设备所有者 ADB 激活命令"
  - "Android pm suspend 暂停冻结"
prerequisites:
  - "Android 6.0（Marshmallow）及更高版本（暂停模式需 Android 7.0+）"
  - "通过 Shizuku、Root（Magisk/KernelSU/APatch）或 Android 设备所有者（Device Owner）模式授予特权"
conflicts:
  - "未设置共同应用排除列表时，与其他自动冻结工具同时启用"
  - "冻结关键通话或身份验证系统核心包（如 com.android.phone、系统桌面/UI）"
configPaths:
  - "/data/data/com.aistra.hail/"
features:
  - "三种原语冻结模式：自由选择停用（pm disable-user）、隐藏（pm hide）或暂停（pm suspend）"
  - "零守护进程开销：不驻留后台轮询服务，仅在执行冻结或解冻操作时唤醒"
  - "多权限后端支持：兼容 Shizuku Binder IPC、Root su Shell 以及标准 Android Device Owner"
  - "桌面快捷方式一键启动：点击冻结应用图标即可自动解冻并打开，锁屏后支持自动重新冻结"
faq:
  - question: "Hail 中的“停用（Disable）”、“隐藏（Hide）”和“暂停（Suspend）”有什么区别？"
    answer: "“停用”（`pm disable-user`）会彻底禁用软件包并从桌面启动器移除图标；“隐藏”（`pm hide`）会将应用标记为对当前用户未安装，同时完整保留应用数据；“暂停”（`pm suspend`，需 Android 7+）则让应用图标以灰阶状态保留在桌面上，屏蔽一切通知与后台闹钟并立即终止后台进程，同时不改变软件包启用状态。"
  - question: "如何在免 Root 情况下将 Hail 配置为设备所有者（Device Owner）？"
    answer: "在系统 **设置 -> 账号** 中移除所有 Google 及用户账号，开启 USB 调试后连接电脑，执行命令：`adb shell dpm set-device-owner com.aistra.hail/.receiver.DeviceAdminReceiver`。配置完成后即可重新登录账号。"
  - question: "如何快速启动已冻结的应用？"
    answer: "在 Hail 中长按任意应用并选择“创建快捷方式”。点击桌面上的快捷方式时，Hail 会自动解冻并启动该应用，还可在设置中开启锁屏后自动重新冻结。"
---

## 概述

现代 Android 应用频繁注册后台广播接收器、Firebase 推送任务与常驻遥测服务，即便极少打开，依然会持续消耗 CPU 周期、内存与电量。

尽管原生 Android 内置电池优化机制，但流氓应用常借助唤醒锁（Wakelock）与高优先级闹钟绕过限制。对于银行客户端、打车软件或外卖平台等偶尔必须使用的应用，直接卸载并不现实。

由 aistra 开发的 **Hail（雹）** 是一款简洁、现代的开源 Android 应用，提供按需“冻结”能力。通过调用原生 Android 框架 API，Hail 无需常驻后台守护进程或内存清理循环，即可彻底阻断后台运行。

---

## 技术冻结机制

Hail 提供三种不同的底层原语来冻结应用：

- **Hail 界面**：负责管理应用列表、分组标签与一键冻结/解冻操作。
- **调度通道**：
  - **Shizuku**：无需持久 Root 权限的特权 ADB Shell 执行通道。
  - **Root（`su`）**：通过 Magisk、KernelSU 或 APatch 直接以超级用户身份执行。
  - **设备所有者（Device Owner）**：通过 Dhizuku 或 Knox 实现企业级权限管理。
- **Android PackageManagerService 接口**：
  - **停用（Disable）**：`setApplicationEnabledSetting()`（标准组件停用）
  - **隐藏（Hide）**：`setApplicationHiddenSettingAsUser()`（使应用在启动器与系统设置中完全不可见）
  - **暂停（Suspend）**：`setPackagesSuspendedAsUser()`（Android 7+ 冻结模式；图标变灰并暂停执行）

### 1. 暂停模式（`setPackagesSuspendedAsUser`）
- **现代 Android（7.0+）首选方案**：最为干净且响应迅速。
- 应用图标仍保留在桌面启动器中，但会呈 **灰阶** 显示。
- Android 系统会拦截该应用发送通知、拉起后台 Activity、播放音频或获取唤醒锁。
- 点击灰阶图标时，系统会弹出已暂停提示或触发 Hail 快速解冻跳转。

### 2. 停用模式（`setApplicationEnabledSetting`）
- 等效于在 Android 系统设置中点击“停用”。
- 应用在当前用户下被标记为停用状态（`COMPONENT_ENABLED_STATE_DISABLED_USER`）。
- 在解冻之前，应用图标会从桌面启动器彻底消失。

### 3. 隐藏模式（`setApplicationHiddenSettingAsUser`）
- 对所有用户态包查询请求隐藏该软件包。
- `/data/data/<package>` 下的应用数据与缓存完好无损。

---

## 工作模式与权限配置

配合 Shizuku 或 Device Owner 使用时，Hail 无需 Root 权限：

### 模式 A：Shizuku（推荐 Root 及无线 ADB 用户使用）
1. 安装并启动 **Shizuku**。
2. 打开 Hail -> 设置 -> **工作模式** -> 选择 **Shizuku**。
3. 在弹出的 Shizuku 授权框中允许 Hail 访问。

### 模式 B：Root 模式（Magisk / KernelSU / APatch）
1. 打开 Hail 设置 -> **工作模式** -> 选择 **Root**。
2. 在 Magisk、KernelSU 或 APatch 弹窗中授予超级用户权限。

### 模式 C：设备所有者（免 Root 且无需 Shizuku）
若设备未 Root 且不希望每次重启都重新开启无线调试：
1. 确保设备中不存在任何用户账号（暂时移除 Google、WhatsApp 等账号）。
2. 开启 USB 调试并连接电脑，运行：
   ```bash
   adb shell dpm set-device-owner com.aistra.hail/.receiver.DeviceAdminReceiver
   ```
3. 重新登录原有账号。此后 Hail 即拥有持久的系统级包管理权限。

---

## 工作流自动化与自动冻结

Hail 支持将应用归入自定义标签（如 *银行*、*社交*、*游戏*）并配置自动化生命周期规则：

1. **锁屏自动冻结**：在设置中启用该开关后，每次熄屏锁屏时都会自动冻结所有已标记应用。
2. **桌面快捷方式**：为已冻结应用创建桌面快捷方式，点击即可自动解冻并无缝打开。
3. **关键应用白名单**：切勿冻结关键系统组件、输入法、桌面启动器或短信管理应用，以免引发系统异常。

---

## 紧急解冻与恢复

如果误冻结了重要应用导致无法打开 Hail：

### 通过 ADB 恢复（电脑或 Termux Rish）
```bash
# To unsuspend an app:
adb shell pm unsuspend com.example.app

# To enable a disabled app:
adb shell pm enable com.example.app

# To unhide a hidden app:
adb shell pm unhide com.example.app
```
