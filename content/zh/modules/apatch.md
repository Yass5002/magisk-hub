---
id: "apatch"
title: "APatch：基于 KernelPatch 的 Android 内核与 Boot 镜像级 Root 方案"
sidebarTitle: "APatch"
description: "bmax121 推出的内核级 Root 方案，利用 KernelPatch 直接修补原厂 Boot 镜像，支持 SuperKey 密钥隔离、KPM 内核内联挂钩及兼容 Magisk 的 APM 模块。"
category: "root-management"
softwareType: "standalone-app"
tier: 1
searchQueries:
  - "APatch APK 下载"
  - "APatch Root 刷入教程"
  - "KernelPatch APatch 使用指南"
  - "APatch SuperKey 忘记怎么办"
  - "APatch KernelSU Magisk 对比"
prerequisites:
  - "ARM64 架构设备"
  - "Linux 内核版本位于 3.18 至 6.12 之间"
  - "内核编译时已开启 `CONFIG_KALLSYMS=y`"
  - "已解锁 Bootloader，并能提取对应版本的原厂 `boot.img` 或 `init_boot.img`"
conflicts:
  - "与其他 Root 方案冲突（不可在同一 Boot 镜像上同时安装 Magisk 或 KernelSU）"
  - "未做对应绕过的原厂三星 Knox 安全保护机制"
configPaths:
  - "/data/adb/ap/"
  - "/data/adb/modules/"
  - "/data/adb/ap/superkey"
features:
  - "原厂 Boot 镜像直接修补：无需编译内核源码，直接对 `boot.img` 内的内核二进制进行修补"
  - "SuperKey 密钥鉴权：内核强制校验加密口令，即使恶意应用直接调用原始 `su` 命令也无法越权提权"
  - "KPM（Kernel Patch Modules）：直接向内核内存注入动态 C 代码模块，支持内联挂钩与系统调用表挂钩"
  - "APM（APatch Modules）：全面兼容基于 OverlayFS 的无系统分区修改（Systemless）模块"
  - "内核态 SELinux 绕过：避免修改用户态 SELinux 策略，防止触发企业或金融应用的安全检测守护进程"
faq:
  - question: "APatch 与 Magisk、KernelSU 有何区别？"
    answer: "Magisk 完全运行在用户空间，通过修改 Ramdisk 中的 init 二进制实现接管；KernelSU 运行在内核空间，但传统上要求从源码编译第三方内核或使用 GKI（通用内核镜像）设备。APatch 融合了二者的优势：它既像 KernelSU 一样扎根于内核空间，又通过 KernelPatch 直接修补原厂 `boot.img` 来落地，完全无需自行编译内核。"
  - question: "什么是 APatch SuperKey？为什么必须设置它？"
    answer: "SuperKey 是在修补 Boot 镜像时设定的私有口令。在 APatch 中，`su` 二进制会通过特权 `ioctl`/系统调用与内核驱动通信。若请求进程无法通过内核存储的 SuperKey 哈希校验，内核将静默拒绝授予 Root 权限。即便处于宽松环境下，这一机制也能杜绝恶意软件滥用 `su`。"
  - question: "刷入 APM 模块后手机卡米（Bootloop）该如何救砖？"
    answer: "APatch 内置了安全模式（Safe Mode）恢复机制。重启设备并在开机画面出现的瞬间连续按动音量下键，APatch 检测到按键后会自动取消挂载所有已启用的模块（`/data/adb/modules/`）。此外，也可以随时通过 Fastboot 刷回未修补的原厂 `boot.img`，立即移除 APatch 且完全保留用户数据。"
---

## 概述

由 bmax121 与开源 AndroidPatch 团队打造的 **APatch** 是一款新一代 Android Root 实现方案，成功打通了 Magisk 的低门槛安装体验与 KernelSU 的深度内核级隐蔽性。

传统的用户空间 Root 方案（如 Magisk）通过劫持 Boot Ramdisk 中的 `/init` 并动态修改 SELinux 规则来运作。如今的银行类应用以及 Play Integrity 硬件认证机制，会持续扫描用户空间进程树以及 SELinux 策略篡改痕迹。

KernelSU 虽然将 Root 权限收归内核空间（`task_struct->cred`），但往往要求用户要么根据厂商源码自行编译内核，要么拥有运行 Google 标准化 GKI（通用内核镜像，Linux 5.10+）的设备。

APatch 借助 **KernelPatch** 巧妙化解了这一难题：该工具能够直接解析并修补原厂 `boot.img` 或 `init_boot.img` 中的内核二进制文件，从而让几乎所有搭载 Linux 3.18 至 6.12 内核的 ARM64 设备，都能享受到内核态 Root、内联内核挂钩与无侵入式叠加挂载能力。

---

## 架构对比：Magisk vs. KernelSU vs. APatch

```
┌────────────────────────────────────────────────────────────────────────┐
│                            用户空间 (Userspace)                         │
├───────────────────────┬────────────────────────┬───────────────────────┤
│        Magisk         │        KernelSU        │        APatch         │
│  - 修补 /init         │  - KernelSU App (UI)   │  - APatch App (UI)    │
│  - magiskd 守护进程   │  - 极简 su 存根        │  - 鉴权后的 su        │
│  - 修改 SELinux       │                        │  - 强制校验 SuperKey  │
├───────────────────────┴────────────────────────┴───────────────────────┤
│                           内核空间 (Kernel Space)                       │
├───────────────────────┬────────────────────────┬───────────────────────┤
│        Magisk         │        KernelSU        │        APatch         │
│  - 原厂内核保持未改   │  - 源码树内编译        │  - KernelPatch 挂钩   │
│                       │  - Hook sys_read/exec  │  - 内联挂钩 (Inline)  │
│                       │  - 需 GKI 或源码编译   │  - 支持 KPM 模块      │
└───────────────────────┴────────────────────────┴───────────────────────┘
```

---

## 核心技术解析

### 1. KernelPatch 二进制修补
KernelPatch 会对原厂 `boot.img` 内嵌的内核二进制进行静态反汇编，通过扫描内核符号表（`kallsyms`）精确定位内存管理、进程凭据与系统调用分发的入口地址，并在不修改内核头文件或重新编译的情况下，将控制流无缝重定向至 KernelPatch 的微挂钩引擎。

### 2. SuperKey 加密隔离
在常规 Root 环境下，任何执行 `su` 的进程都会触发 Root 管理器弹窗或接入本地套接字。APatch 则在内核层引入了基于私有 **SuperKey** 的权限闸门：
- 在 APatch 应用内首次修补镜像时，由你设定一组私有口令（SuperKey）。
- 该密钥的哈希值会被直接写入修补后的 Boot 镜像中。
- 当应用请求 Root 权限时，APatch 管理器必须凭此密钥向内核驱动完成鉴权。
- 若无法提供正确的 SuperKey，内核挂钩引擎会将发起进程视作完全无特权的普通进程，令常见 Root 探测启发式规则彻底失效。

### 3. 双层模块架构：KPM 与 APM
APatch 引入了双层级模块化架构：
- **APM（APatch Modules）**：基于 OverlayFS 实现的传统无系统分区修改文件系统模块。其结构与 Magisk 及 KernelSU 模块完全一致，无需改动底层存储块即可将文件挂载覆盖至 `/system` 与 `/vendor`。
- **KPM（Kernel Patch Modules）**：编译后直接运行于内核空间的底层 C 模块。开发者可借助 KPM 对内核内部函数进行内联挂钩、改写系统调用行为或实时操控网络套接字缓冲区。

---

## 分步安装指南

### 第一步：提取原厂 Boot 镜像
1. 下载与你设备当前系统版本号完全一致的官方原厂固件包。
2. 提取对应的启动镜像：
   - 出厂搭载 Android 13 及更新系统的机型：提取 `init_boot.img`。
   - 出厂搭载 Android 12 及更早系统的机型：提取 `boot.img`。

### 第二步：使用 APatch 管理器修补镜像
1. 下载并安装最新官方 `APatch` APK。
2. 打开 APatch，点击 **修补 Boot 镜像（Patch Boot Image）**。
3. 选中刚刚提取出的 `boot.img` 或 `init_boot.img`。
4. 设定你的 **SuperKey**。请务必牢记该口令，进入应用内解锁超级用户管理功能时必须校验。
5. 点击 **开始（Start）**。应用将调用 KernelPatch 修补内核偏移量，并在 `Download/` 目录下生成 `apatch_patched_*.img`。

### 第三步：刷入修补后的镜像
将手机连接至电脑，并重启进入 Bootloader（Fastboot）模式：

```bash
# 若修补的是 init_boot：
fastboot flash init_boot apatch_patched_*.img

# 若修补的是 boot：
fastboot flash boot apatch_patched_*.img

# 重启设备
fastboot reboot
```

6. 进入 Android 桌面后打开 APatch 应用，输入 SuperKey 解锁并按需授予超级用户权限。

---

## 安全模式与紧急救砖

若因 APM 模块异常导致设备陷入无限重启（卡米）：
1. 长按 **电源键 + 音量下键** 强制重启设备。
2. 当屏幕出现厂商开机 Logo 时，反复连续点按 **音量下键**。
3. APatch 将捕获安全模式硬件按键中断，并在启动早期自动禁用所有 APM 模块。
4. 若因实验性 KPM 模块引发严重的内核恐慌（Kernel Panic），只需通过 Fastboot 刷回未修补的原厂 `boot.img`：
   ```bash
   fastboot flash boot stock_boot.img
   fastboot reboot
   ```
   即可在不影响任何应用、照片或系统设置的前提下立刻恢复原厂内核运行。
