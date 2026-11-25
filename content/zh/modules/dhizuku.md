---
id: "dhizuku"
title: "Dhizuku：向第三方应用共享 Android 设备所有者（DPM）权限"
sidebarTitle: "Dhizuku"
description: "由 iamr0s 开发的开创性 Android 系统服务守护进程，以设备所有者（Device Owner）身份运行，并将 DevicePolicyManager 企业级 API 委派给已授权的客户端应用。"
category: "system-utilities"
softwareType: "standalone-app"
tier: 1
searchQueries:
  - "Dhizuku APK 下载"
  - "Dhizuku Device Owner ADB 激活命令"
  - "Android 共享设备所有者权限"
  - "Dhizuku 与 Shizuku 区别"
  - "设置设备所有者提示已有账号解决方法"
prerequisites:
  - "Android 8.0（Oreo）至 Android 15+"
  - "通过 Root、Shizuku 或免 Root ADB Shell 激活"
  - "设备尚未配置其他 Device Owner"
conflicts:
  - "已注册的企业 MDM 管理服务（如 Microsoft Intune、VMware Workspace ONE）"
  - "作为冲突设备管理员运行的工作资料管理器"
configPaths:
  - "/data/system/device_owner_2.xml"
  - "com.rosan.dhizuku/.server.DhizukuDAReceiver"
features:
  - "DevicePolicyManager 多路复用：允许多个第三方应用同时调用企业级管理 API"
  - "静默软件包操作：支持 App Manager、雹（Hail）、Canta 等客户端无需确认弹窗即可安装、卸载或冻结应用"
  - "免 Root 运行：在未获取 Root 权限的设备上可通过 ADB Shell 命令完整激活使用"
  - "精细化权限管控：向客户端应用授予 Device Owner API 访问权限前会弹出用户确认提示"
faq:
  - question: "Dhizuku 与 Shizuku 有什么区别？"
    answer: "Shizuku 通过提权后的系统 Shell 守护进程共享 ADB / Shell 权限（如 `android.permission.DUMP`、`pm`、`am`、`appops`）。而 Dhizuku 则注册为 Android 系统官方的 **设备所有者（Device Owner）**（`DevicePolicyManager`），开放诸如静默安装应用、后台冻结/隐藏应用（`setApplicationHidden`）、锁定任务模式及状态栏限制等企业级 API。"
  - question: "提示“Not allowed to set the device owner because there are already some accounts on the device”该如何解决？"
    answer: "Android 安全策略严禁在存在活跃用户账号的情况下设置 Device Owner。请前往系统 **设置 -> 密码与账号**，暂时退出并移除所有 Google、WhatsApp、三星及各类云端账号，随后执行 ADB 命令 `adb shell dpm set-device-owner com.rosan.dhizuku/.server.DhizukuDAReceiver`，激活成功后再重新登录账号即可。"
  - question: "如何在不恢复出厂设置的情况下彻底移除 Dhizuku？"
    answer: "打开 Dhizuku -> 设置 -> 点击 **停用设备所有者（Deactivate Device Owner）**。也可通过 ADB 执行命令取消授权：`adb shell dpm remove-active-admin com.rosan.dhizuku/.server.DhizukuDAReceiver`。停用后即可像普通 APK 一样直接卸载。"
---

## 概述

由 iamr0s 开发的 **Dhizuku** 解决了 Android 操作系统最古老的架构限制之一：**Device Owner（设备所有者）独占性**。

在 Android 企业框架（`android.app.admin.DevicePolicyManager`）下，整个系统仅允许指定单个应用作为“设备所有者”。Device Owner 拥有极高的系统管理权限：
- 无需用户手动确认即可静默安装或卸载应用
- 立即冻结（隐藏）后台软件包，消除额外耗电
- 限制网络策略、相机调用与通知横幅
- 管理硬件按键与信息亭（Kiosk）模式

由于 Android 严格执行单一所有者规则，用户过去只能在某个特定冻结工具（如 Island 或冰箱 Ice Box）之间二选一，无法与其他同类工具共存。Dhizuku 充当 **Device Owner 代理服务器**：由它占用唯一的设备所有者席位，并通过标准化的 Binder IPC 接口，让已授权的客户端应用（如 Hail、Canta、App Manager、Install with Options）安全共享这些管理权限。

---

## 技术架构与 Binder 代理机制

- **Android 系统框架**：托管 `android.app.admin.DevicePolicyManager`（DPM），提供企业级管理接口。
- **Dhizuku 服务端**：
  - 通过 `DeviceAdminReceiver` 持有官方 Device Owner 身份。
  - 对每个应用实施权限令牌校验与访问控制策略。
  - 在非特权客户端与 DPM 之间多路复用 IPC Binder 请求。
- **受托客户端应用**：
  - **Hail（雹）**：无需 Root 即可调用 Device Policy Manager API 冻结、隐藏或停用应用。
  - **App Manager / Canta**：高效管理用户策略与系统软件包生命周期。

---

## 激活方式

根据设备环境不同，可通过以下三种方式激活 Dhizuku：

### 方式一：Root 激活（Magisk、KernelSU、APatch）
若设备已获取 Root 权限，打开 Dhizuku 并选择 **Root 激活**，在 Root 管理器弹窗中点击授权即可。Dhizuku 会自动将其组件写入 `/data/system/device_owner_2.xml` 并重载策略缓存。

### 方式二：Shizuku 激活
若设备已在运行 Shizuku：
1. 打开 Dhizuku。
2. 选择 **通过 Shizuku 激活**。
3. 批准 Shizuku 权限请求。

### 方式三：免 Root ADB Shell 激活（无需 Root）
适用于完全未修改的官方系统设备：
1. 在手机上开启 **开发者选项** 与 **USB 调试**。
2. 将设备连接至已安装 Android SDK Platform-Tools 的电脑。
3. 打开终端并执行：
   ```bash
   adb shell dpm set-device-owner com.rosan.dhizuku/.server.DhizukuDAReceiver
   ```
4. 若执行成功，终端会返回 `Success: Device owner set to package...`。

> **注意**：如果遇到 `java.lang.IllegalStateException: Not allowed to set the device owner because there are already some accounts on the device` 报错，请前往 **设置 -> 密码与账号** 暂时移除所有 Google、Telegram 及企业账号，执行上述命令后再重新添加。

---

## 生态协同

激活后，Dhizuku 可为一系列免 Root 开源工具提供底层权限支撑：
- **Hail（雹）**：利用 `DevicePolicyManager.setApplicationHidden()` 一键冻结臃肿预装软件与后台游戏。
- **Canta**：深度精简系统冗余应用，安全移除 OEM 预装包而不触发 Bootloop。
- **Install with Options**：支持静默降级安装、绕过低目标 SDK 版本限制以及免手动点击安装拆分 APK。
