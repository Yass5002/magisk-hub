---
id: "kernelsu"
title: "KernelSU：新一代基于 Linux 内核的 Android Root 方案"
sidebarTitle: "KernelSU"
description: "由 weishu/tiann 研发的革命性 Root 方案，直接运行于 Ring 0 内核空间，具备基于 UID 的凭据委派、App Profile 沙盒隔离与 OverlayFS 无侵入挂载能力。"
category: "root-management"
tier: 1
searchQueries:
  - "KernelSU APK 管理器下载"
  - "KernelSU GKI 刷入教程"
  - "KernelSU 和 Magisk 对比"
  - "KernelSU 修补 Boot 镜像刷机"
  - "KernelSU OverlayFS 模块挂载"
prerequisites:
  - "搭载 Linux 5.10、5.15 或 6.1 内核的 Android GKI 2.0 设备（4.14/4.19 等旧内核需自行编译定制内核）"
  - "已解锁 Bootloader 并配备 Fastboot 刷机工具"
conflicts:
  - "同一 Boot 镜像上不可与 Magisk `su` 守护进程共存"
  - "未启用 OverlayFS 或 `kprobes` 支持的第三方定制内核"
configPaths:
  - "/data/adb/ksu/"
  - "/data/adb/modules/"
  - "/data/adb/ksud"
features:
  - "内核级 `su` 委派：`su` 二进制仅对白名单 UID 可见，未获授权的应用完全探测不到任何 Root 痕迹"
  - "硬件级 App Profile：精细限制单个应用的 Root 权限，隔离 Linux Capabilities、挂载命名空间与 SELinux 域"
  - "原生 OverlayFS 挂载：以 Linux 内核态 OverlayFS 取代用户态 Magic Mount，实现更快、更纯净的无系统分区修改覆盖"
  - "GKI 2.0 通用修补：无需编译完整 ROM，即可直接刷入各类标准 Android 12、13、14 或 15 GKI 设备"
faq:
  - question: "如何确认我的设备是否受到 KernelSU 官方支持？"
    answer: "打开终端或运行 `uname -r`。如果内核版本号显示为 `5.10.x-android12-...`、`5.15.x-...` 或 `6.1.x-...`（带有 `-androidXX` GKI 标识），则说明设备属于官方开箱支持的 GKI 2.0 机型。较老的 4.14 与 4.19 内核设备则需要将 KernelSU 源码集成编译进定制内核中。"
  - question: "为什么 KernelSU 在隐蔽性上天然优于 Magisk？"
    answer: "Magisk 主要在用户态（Ring 3）运作，通过在文件系统中放置全局 `su` 二进制并运行后台守护进程，再借助列表隐藏去规避检测。KernelSU 则直接驻留于 Linux 内核态（Ring 0）：内核直接拦截系统调用，且仅为白名单内的 UID 修改进程凭据（`struct cred`）。未获授权的应用在系统中既看不到 `su` 文件，也观察不到异常挂载点或开放的套接字。"
  - question: "刷入不兼容的 KernelSU 模块导致卡米（Bootloop）该如何恢复？"
    answer: "KernelSU 内置硬件安全模式：开机出现厂商 Logo 时连续多次按动音量下键，KernelSU 会捕获按键事件并自动禁用全部第三方模块。除此之外，你也可以随时通过 Fastboot 刷回原厂 `boot.img` 或 `init_boot.img`，无损还原至未 Root 的官方状态。"
---

## 概述

近十年来，Magisk 凭借其“无系统分区修改（Systemless）”的用户态架构一直定义着 Android Root 的行业标准。然而，随着 Google 不断引入硬件级安全校验、收紧 SELinux 策略，以及银行类应用普遍部署启发式反 Root 检测，在 Ring 3 用户态隐藏常驻的 `su` 守护进程已逐渐沦为永无止境的猫鼠游戏。

由知名 Android 安全工程师 weishu（tiann）构想并开发的 **KernelSU**，通过将权限管控彻底迁入 **Linux 内核空间（Ring 0）**，重新定义了 Android Root 机制。

KernelSU 不再在用户态运行常驻的 `magiskd` 守护进程，而是直接将逻辑集成到内核之中。当应用请求获取超级用户权限时，内核会亲自核对内部的 UID 授权表，并就地修改进程的凭据结构（`uid`、`gid`、`capabilities`）。对于未被显式授予 Root 权限的应用而言，无论是文件系统扫描、套接字检查还是内存探测，均无法感知到 Root 的存在。

---

## 技术架构：Ring 0 vs Ring 3 Root

- **应用层（用户空间）**：
  - **已授权 Root 应用（UID）**：获得完整的 Root Shell 访问权限及专属的 App Profile 挂载命名空间。
  - **非 Root 应用（如银行类应用）**：看到的是完全原生的运行环境——文件系统中不存在 `su` 二进制，挂载表洁净且进程表毫无异常。
- **Linux 内核空间（Ring 0）**：
  - **KernelSU 核心引擎**：直接在内核代码中拦截 `sys_execve` 与提权相关的系统调用。
  - **凭据提升**：仅为白名单内的调用者 UID 覆写 `struct cred`。
  - **OverlayFS 无侵入分层**：在虚拟文件系统（VFS）层直接完成无系统分区修改的分层合并。

### 1. 文件系统零暴露
在 KernelSU 环境下，普通应用的 `/system/bin` 或标准 `PATH` 目录中根本不存在 `su` 二进制文件。当未授权应用尝试执行 `which su` 或 `stat("/system/xbin/su")` 时，内核会直接返回 `ENOENT`（文件或目录不存在）。

### 2. Linux 内核原生 OverlayFS
KernelSU 放弃了用户态繁琐的绑定挂载树（即“Magic Mount”），转而直接调用 Linux 内核原生的 **OverlayFS**。所有存放在 `/data/adb/modules/<id>/system/` 下的修改都会在 VFS（虚拟文件系统）层面直接与 `/system` 合并，带来极致的挂载速度与干净整齐的目录树。

### 3. App Profile 安全隔离
KernelSU 允许像“笼子”一样精准收束 Root 权限：
- 按应用限制可调用的具体 Linux Capabilities（例如 `CAP_NET_ADMIN`、`CAP_SYS_ADMIN`）。
- 在沙盒化的挂载命名空间内授予 Root，避免暴露全局存储。
- 强制执行特定的 SELinux 域转换规则。

---

## 安装指南（GKI 2.0 设备）

### 第一步：核对 GKI 兼容性
确认设备运行的是 Android 12、13、14 或 15 的 GKI 内核：
```bash
adb shell uname -r
# 预期输出示例：5.10.198-android12-9-g8a3...
```

### 第二步：修补并刷入 Boot 镜像
1. 下载并安装官方 **KernelSU 管理器**（`KernelSU_v*.apk`）。
2. 提取设备对应版本的原厂 `boot.img`（出厂为 Android 13+ 的设备通常为 `init_boot.img`）。
3. 将镜像传入手机并打开 KernelSU 应用。
4. 点击 **安装（Install）** -> 选择并修补一个文件 -> 选中原厂 Boot 镜像。
5. 将修补生成的镜像（`kernelsu_boot.img`）传回电脑。
6. 重启设备至 Bootloader 模式并通过 Fastboot 刷入：
   ```bash
   fastboot flash boot kernelsu_boot.img
   # （若为 init_boot 分区机型则执行）：
   fastboot flash init_boot kernelsu_boot.img
   fastboot reboot
   ```

---

## 模块管理与安全模式恢复

KernelSU 兼容遵循现代无系统分区修改目录规范的标准可刷入 Magisk 模块，所有模块均存放于 `/data/adb/modules/`。

### 内置硬件安全模式
若因故障模块导致 Android 无法正常完成开机：
1. 将设备彻底关机。
2. 按下电源键开机。
3. 当屏幕亮起并出现厂商开机 Logo 时，连续多次按动 **音量下键**，直至感受到机身震动反馈。
4. KernelSU 将捕获硬件按键事件，触发全局模块禁用标记，并禁用所有第三方模块进入安全模式。

### Fastboot 救砖恢复
如果安全模式仍无法解除故障，只需通过 Fastboot 重新刷回原厂未修改的 `boot.img`，即可在零数据丢失的前提下恢复纯净的未 Root 系统。
