---
id: "shizuku"
title: "Shizuku：面向 Android 的直接系统 API 与 Binder IPC 代理服务"
sidebarTitle: "Shizuku"
description: "Rikka 开发的特权用户态服务，通过 ADB 无线调试或 Root su 向第三方应用开放系统服务 Binder 令牌，彻底消除进程 fork 开销。"
category: "root-management"
tier: 1
searchQueries:
  - "Shizuku APK 下载"
  - "Shizuku 无线调试配对教程"
  - "ADB 命令行启动 Shizuku"
  - "Shizuku Root 模式激活"
  - "Shizuku Binder IPC 原理"
prerequisites:
  - "Android 6.0（Marshmallow）及以上系统（无线调试模式需 Android 11+）"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限，或启用 ADB 调试桥（电脑连接或无线调试）"
conflicts:
  - "激进的 OEM 后台省电策略（如小米 HyperOS / MIUI 省电策略会强杀后台启动进程）"
  - "ColorOS、OxygenOS 及 HyperOS 上受限的 USB 调试安全权限开关"
configPaths:
  - "/sdcard/Android/data/moe.shizuku.privileged.api/start.sh"
  - "/data/user_de/0/moe.shizuku.privileged.api/"
features:
  - "高性能 Binder IPC：直接代理 AIDL 系统服务调用，无需反复派生缓慢的 `su` 子进程"
  - "免 Root 运行支持：依托 Android 11+ 无线调试配对机制，无需解锁 Bootloader 即可获得 ADB 级系统能力"
  - "细粒度安全令牌：通过用户授权的加密令牌校验机制，确保客户端应用仅在允许范围内访问系统 API"
  - "Rish 交互式终端：借助 Shizuku 现有 Binder 令牌直接在手机端提供高权限交互 Shell 环境"
faq:
  - question: "为什么在 HyperOS 或 MIUI 上息屏后 Shizuku 就会自动停止运行？"
    answer: "HyperOS 与 MIUI 的后台进程回收策略较为激进。要保持 Shizuku 守护进程常驻，请进入“设置 -> 应用设置 -> 应用管理 -> Shizuku -> 省电策略”，选择“无限制”。此外，还需确认开发者选项中的“USB 调试（安全设置）”保持开启。"
  - question: "每次重启手机都需要重新进行无线调试配对吗？"
    answer: "不需要。配对是一次性的加密握手过程。但 Android 在每次重启或重新连接 Wi-Fi 后都会随机分配无线调试端口，你只需重新开关一次无线调试，然后打开 Shizuku 点击“启动”即可重新绑定到新的动态端口。"
  - question: "在电脑上手动启动 Shizuku 的 ADB 命令是什么？"
    answer: "开启 USB 调试并将设备通过数据线连接电脑后，执行 `adb shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh`。Shizuku 守护进程便会立即拉起并完成绑定。"
---

## 概述

由 Rikka 开发并以 Apache-2.0 协议开源的 **Shizuku**，从架构层面革新了 Android 应用与系统底层特权接口的交互方式。

过去，需要高权限运行的工具类应用（如包管理器、应用冻结工具与文件管理器）普遍依赖反复派生交互式超级用户 Shell 进程（`su`）。每次操作都需要执行终端命令（例如 `pm disable-user <package>` 或 `dumpsys activity`），这种传统模式存在显著的工程缺陷：
1. **高延迟开销**：频繁派生 Shell 进程会带来可观的 CPU 消耗与 fork/exec 性能开销。
2. **文本解析脆弱**：命令输出必须序列化为纯文本后再通过正则解析，极易因 OEM 厂商改动输出格式而失效。
3. **能力范围受限**：应用只能调用系统镜像内预编译好的命令行工具。

Shizuku 直接在 Android 原生 Binder 框架之上建立跨进程通信（IPC）代理通道，彻底省去了 Shell 中间层。

---

## 技术架构与工作原理

Android 系统将核心能力封装在运行于 `system_server` 中的各类系统服务中（如 `PackageManagerService`、`ActivityManagerService`、`AppOpsService`）。普通应用需要获取 `IBinder` 句柄才能与这些服务通信：

- **客户端应用**（如 Canta、Hail、Material Files）：经用户授权后，通过 Shizuku IPC Binder 令牌完成鉴权。
- **Shizuku 服务端**（`app_process` 守护进程）：以 UID 2000（Shell）或 UID 0（Root）身份运行，负责代理高权限 Binder 句柄。
- **Android `system_server`**：接收 Shizuku 服务端代客户端应用转发的原生 AIDL 系统调用（PackageManager、ActivityManager、AppOps）。

1. **拉起守护进程**：Shizuku 借助 Android 原生 `app_process` 二进制文件启动一个独立 Java 进程，运行权限为 `shell` UID（ADB 模式下为 `2000`）或 `root` UID（`su` 模式下为 `0`）。
2. **Binder 权限委派**：守护进程就绪后，向系统服务端获取特权 Binder 接口句柄。
3. **IPC 代理转发**：当已授权的客户端应用（例如雹 Hail、Canta 或质朴文件管理器 Material Files）发起连接时，Shizuku 会对照用户授权列表校验客户端 UID，并返回一个代理封装对象（`ShizukuBinderWrapper`）。
4. **直接方法调用**：客户端应用即可在 Java/Kotlin 中以接近零延迟、类型安全的方式直接调用原生 AIDL 方法。

---

## 三种激活方式

Shizuku 根据设备是否具备 Root 权限，提供三种截然不同的启动模式：

### 1. Root 模式（Magisk / KernelSU / APatch）
如果设备已获取 Root 权限，无需执行任何手动 ADB 命令：
1. 下载并安装 `shizuku-v*.apk`。
2. 打开 Shizuku 应用。
3. 找到 **通过 Root 启动** 卡片并点击 **启动**。
4. 当 Root 管理器（Magisk、KernelSU 或 APatch）弹出授权提示时，选择永久授予超级用户权限。
5. Shizuku 将启动后台守护进程，并显示 `Shizuku 正在运行（root）`。

### 2. 无线调试模式（Android 11+ 免 Root）
适用于运行 Android 11 及以上版本的未 Root 设备：
1. 将手机连接至可用的 Wi-Fi 网络。
2. 前往 *设置 -> 关于手机*，连续点击 *版本号* 七次以开启 **开发者选项**。
3. 在开发者选项中开启 **无线调试**。
4. 打开 Shizuku，点击 *通过无线调试启动* 下方的 **配对**。
5. 使用分屏或小窗模式打开开发者选项，进入 *无线调试 -> 使用配对码配对设备*。
6. 将屏幕上显示的 6 位配对码填入 Shizuku 通知栏提示框中。
7. 返回 Shizuku 应用并点击 **启动**。Shizuku 将自动连接内部无线端口并初始化服务。

### 3. 电脑有线 ADB 模式
适用于 Android 10 及更早版本系统，或当前没有 Wi-Fi 网络的环境：
1. 开启 **USB 调试** 并通过数据线将手机连接至电脑。
2. 在电脑终端执行以下命令：
   ```bash
   adb shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh
   ```
3. 终端会输出 `app_process` 启动确认信息，随后 Shizuku 应用内即显示 `Shizuku 正在运行（adb）`。

---

## 使用 Rish（Root/Shell 交互式终端）

Shizuku 内置 `rish`（Rikka Shell）工具，可将 Shizuku 的 Binder 令牌直接转换为本机交互式 Root 或 ADB 终端会话，无需连接电脑：

1. 在 Shizuku 主界面点击 **在终端应用中使用 Shizuku**。
2. 点击 **导出文件**，将 `rish` 与 `rish_dex.jar` 保存到本地目录。
3. 打开 Termux 或你常用的 Android 终端模拟器，执行：
   ```bash
   chmod +x ./rish
   ./rish
   ```
4. 执行后即可直接获得 UID 2000（`shell`）或 UID 0（`root`）的交互式 Shell，方便运行各类自动化脚本。

---

## 厂商系统差异与故障排查

### 小米 HyperOS / MIUI
- **常见问题**：Shizuku 启动后自动退出，或权限请求立即超时。
- **解决方法**：打开开发者选项，同时启用以下两项：
  - **USB 调试（安全设置）** *（通常需要登录小米账号并插入 SIM 卡验证）*
  - **关闭权限监控** *（防止 MIUI 拦截运行时 Binder 校验）*
- 前往 *设置 -> 省电与电池 -> 应用智能省电*，找到 Shizuku 并设为 **无限制**。

### 三星 OneUI
- **常见问题**：断开 Wi-Fi 后 Shizuku 停止工作。
- **解决方法**：Samsung Knox 在设备断开已知 Wi-Fi 网络后会自动关闭无线调试。重新连网后，请在开发者选项中重新开启 *无线调试*。

---

## 紧急恢复与停止守护进程

若某个异常客户端应用占用了过多资源，或需要手动终止 Shizuku 守护进程，可执行：

```bash
# 通过 Root Shell 或 ADB 终止 Shizuku 守护进程：
pkill -f moe.shizuku.privileged.api

# 验证进程是否已终止：
ps -ef | grep shizuku
```
