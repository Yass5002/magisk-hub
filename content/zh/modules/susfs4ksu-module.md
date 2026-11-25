---
id: "susfs4ksu-module"
title: "SUSFS：面向 KernelSU 与 APatch 的内核级挂载与 Root 隐藏方案"
sidebarTitle: "SUSFS"
description: "依托内核补丁扩展实现的内核态 Root 隐藏模块，从底层彻底抹除挂载记录、敏感路径与进程命名空间特征，全面抵御用户态扫描。"
category: "root-management"
tier: 1
searchQueries:
  - "SUSFS 模块 KernelSU 下载"
  - "SUSFS APatch 使用教程"
  - "SUSFS 如何隐藏挂载点"
  - "Momo 检测绕过 SUSFS"
  - "Android 内核级 Root 隐藏"
prerequisites:
  - "设备已刷入合入 SUSFS 补丁的自定义内核（需启用 `CONFIG_KSU_SUSFS=y`）"
  - "已安装 KernelSU 或 APatch 管理器"
conflicts:
  - "未打补丁的原厂内核（模块检测到内核不支持时会退出并提示警告）"
configPaths:
  - "/data/adb/susfs/"
  - "/data/adb/modules/susfs4ksu-module/"
features:
  - "内核空间挂载点隐藏：直接从 `/proc/[pid]/mountinfo` 输出中抹除 OverlayFS 与 Root 相关挂载记录"
  - "自定义路径隐藏（`susfs_add_sus_path`）：使 `readdir` 与 `stat` 系统调用无法探测自定义目录与 `su` 二进制文件"
  - "Kstat 元数据伪装：掩盖被修改系统文件的异常 `ctime`/`mtime` 时间戳及硬链接属性"
  - "无需用户态 `ptrace` 挂钩即可绕过主流强力检测工具（Momo、Native Alpha、Applist Detector）"
faq:
  - question: "标准版 Magisk 可以使用 SUSFS 吗？"
    answer: "不能。标准版 Magisk 完全运行在用户空间，仅通过修补 init 与 Ramdisk 工作，并不替换 Linux 内核。SUSFS 必须在内核源码层面打入专用补丁并重新编译内核。"
  - question: "如何确认当前内核已经成功启用了 SUSFS？"
    answer: "在终端执行 `su -c 'which ksu_susfs'` 或 `su -c 'cat /proc/sys/fs/susfs/version'`。如果内核已启用 SUSFS，命令会输出对应的版本号（例如 v1.5.x 或更高）。"
---

## 概述

由 **sidex15** 打造的 **SUSFS**（Super User Secret File System）标志着 Android Root 隐藏技术的一次代际跃迁。

传统的隐藏工具（如 Shamiko 或 Magisk DenyList）均运行在 **用户空间（Userspace）**，主要依靠 libc 函数挂钩、`ptrace` 调试拦截或在目标应用进程内卸载挂载命名空间来掩盖痕迹。然而，现代反 Root 检测引擎可以通过直接执行内联汇编系统调用（例如 ARM64 下的 `svc #0` 指令）绕过用户态挂钩，直连内核读取 `/proc/self/mountinfo` 或探测 `/data/adb` 目录。

SUSFS 将整套隐藏逻辑直接下沉至 **Linux 内核**。由于内核掌握所有文件系统与进程查询的最终裁决权，无论应用层采用何种原生系统调用手段，都无法突破内核级的过滤屏障。

---

## 技术架构与工作原理

### 内核空间文件系统拦截

1. **VFS 系统调用挂钩**：SUSFS 对 Linux 内核中的虚拟文件系统（VFS）核心函数实施补丁拦截：
   - `vfs_read` 与 `show_mountinfo`：在内核格式化输出 `/proc/[pid]/mounts` 或 `/proc/[pid]/mountinfo` 之前，自动过滤掉由 KernelSU 或 APatch 创建的挂载点条目。
   - `vfs_statx` / `vfs_getattr`：拦截文件属性查询请求。当普通应用探测 `/data/adb/ksu` 或 `/system/bin/su` 时，除非调用方为受信任的 Root 管理器，否则内核一律直接返回 `ENOENT`（文件或目录不存在）。
2. **Kstat 元数据伪装**：检测类应用常会校验 inode 元数据（如修改时间戳与硬链接计数）。SUSFS 可对 inode 时间戳进行内核态伪装，使被挂载替换的系统分区看起来与原厂未修改状态完全一致。
3. **用户态伴生模块**：`susfs4ksu-module` 充当用户空间与内核之间的控制桥梁，在系统启动时读取模块配置，并通过 `ioctl` 指令向内核注册需要隐匿的路径、Loop 设备及进程列表。

---

## 前置准备与安装步骤

### 第一步：刷入集成 SUSFS 补丁的内核
安装本模块前，设备必须正在运行包含 SUSFS 支持的内核：
1. 获取适配你机型的 SUSFS 内核（如 WildKSU、GKI SUSFS 或自行编译的内核构建）。
2. 通过 Fastboot 或第三方 Recovery 刷入内核镜像：
   ```bash
   fastboot flash boot boot.img
   ```

### 第二步：刷入 SUSFS 模块
1. 打开 **KernelSU** 或 **APatch**。
2. 进入 **模块（Modules）** → **安装（Install）** → 选择 `susfs4ksu-module-vX.zip`。
3. 重启设备。

### 第三步：验证内核状态
在 Root 终端执行以下诊断命令：
```bash
su -c "ksu_susfs show_version"
```
正常情况下将返回：`ksu_susfs version: v1.5.x (or newer)`。

---

## 配置与自定义路径隐藏

通过配套命令行工具 `ksu_susfs` 可动态管理隐藏规则：

```bash
# 向非信任应用隐藏指定自定义路径：
su -c "ksu_susfs add_sus_path /data/local/tmp/my_tool"

# 隐藏自定义的 Loop 挂载点：
su -c "ksu_susfs add_sus_mount /system/etc/hosts"

# 查看当前已隐藏的挂载列表：
su -c "ksu_susfs show_sus_mount"
```
