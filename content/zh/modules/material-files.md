---
id: "material-files"
title: "Material Files（质感文件）：开源 Android Root 与 Shizuku 文件管理器"
sidebarTitle: "Material Files"
description: "由 zhanghai 开发的纯净、注重隐私的 Material Design 文件管理器，直接基于 Linux 系统调用构建，支持 Root su 访问、Shizuku 绕过存储隔离以及各类网络存储协议。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Material Files APK 下载"
  - "Material Files Root 文件管理器"
  - "质感文件 Shizuku 访问 Android data"
  - "zhanghai MaterialFiles GitHub"
  - "开源 Android Root 管理器推荐"
prerequisites:
  - "Android 5.0（Lollipop）及更高版本"
  - "通过 Magisk/KernelSU/APatch 获取 Root 权限，或启用 Shizuku 服务以获得高权限存储访问"
conflicts:
  - "Android 11+ 未启用 Shizuku 或 Root 时受分区存储（Scoped Storage）限制"
configPaths:
  - "/data/data/me.zhanghai.android.files/"
features:
  - "原生 Linux 系统调用后端：摆脱脆弱的 ls 命令文本解析，精准读取文件权限、符号链接与 SELinux 上下文"
  - "Root 与 Shizuku 深度集成：自由编辑 Root 分区文件（/system、/data/adb）或浏览受限的 /sdcard/Android/data 目录"
  - "全能压缩包管理：原生浏览、打包与解压 ZIP、7Z、TAR、GZ 及 XZ 格式归档文件"
  - "内置网络协议客户端：无需第三方插件即可直连 SMB（Windows 共享）、SFTP、FTP 与 WebDAV 服务器"
faq:
  - question: "如何在 Android 11+ 上访问 `/sdcard/Android/data` 和 `/sdcard/Android/obb`？"
    answer: "Android 11 及更新版本禁止文档提供程序访问 `Android/data`。在 Material Files 中打开侧边导航栏 -> 添加存储 -> 选择“Shizuku”，在弹窗中授予权限，即可立即获得对所有应用数据与 obb 目录的完整读写访问权。"
  - question: "为什么 Material Files 比闭源 Root 文件管理器更安全？"
    answer: "向闭源管理器授予 Root 权限意味着允许不透明的专有二进制文件以 UID 0 身份在你的私人数据分区执行任意脚本。Material Files 采用 GPL-3.0 协议 100% 开源，支持可复现构建（Reproducible Builds），且不含任何追踪器或远程遥测统计。"
  - question: "如何在 Material Files 中修改文件权限（chmod）与所有者（chown）？"
    answer: "在 Root 模式下定位到目标文件，点击右上角三点菜单 -> 选择“属性” -> “权限”。你可以直接勾选所有者（Owner）、用户组（Group）与其他用户（Others）的读、写、执行权限位，或手动输入八进制数值（例如 0644 或 0755）。"
---

## 概述

对于任何已获取 Root 权限的 Android 设备而言，一款可靠且值得信赖的文件管理器都是不可或缺的基础工具。进阶玩家经常需要查看模块配置、修改 `/data/adb/` 中的系统属性、调整文件权限（`chmod`）、创建符号链接，以及访问被现代 Android 严格限制的分区存储目录（`/sdcard/Android/data/`）。

然而，大多数老牌 Root 文件管理器（如 Root Explorer 或 Solid Explorer）均为闭源商业软件。将超级用户（`su`）权限交给闭源软件，意味着设备的高度敏感数据将暴露给不可审计的二进制程序。此外，不少传统开源管理器依赖解析命令行工具 `ls` 的文本输出——这种架构在面对不同版本的 Android toybox/toolbox 或非 UTF-8 文件名时极易损坏或出错。

由开发者张海（zhanghai）打造的 **Material Files（质感文件）** 同时解决了这两大痛点：它是一款 100% 开源、严格遵循 Material Design 设计规范、并完全基于 **原生 Linux 系统调用** 驱动的高品质文件管理器。

---

## 技术架构：Linux 系统调用 vs `ls` 文本解析

传统 Android 文件管理器通常通过执行 Shell 命令与 Root 交互：
```bash
su -c "ls -la /data/adb"
```
随后再对返回的纯文本进行字符串分割和正则匹配，从中提取文件名、权限和文件大小。这种陈旧架构存在严重缺陷：
1. **文件名解析损坏**：包含空格、转义字符或本地化字符的文件名极易导致解析器崩溃。
2. **元数据缺失**：标准 `ls` 解析器难以准确处理符号链接目标、硬链接以及 SELinux 安全上下文。
3. **高延迟开销**：反复派生 Shell 进程并解析输出会带来可观的 CPU 延迟。

Material Files 实现了 **Java NIO2 文件 API**，并直接绑定原生 Linux 系统调用（`stat`、`openat`、`readdir`、`readlink`、`chmod`、`chown`），从而实现毫秒级目录浏览、原子化文件操作以及零解析错误。

---

## Root 与 Shizuku 权限能力

Material Files 支持多种提权后端：

- **本地存储提供程序**：基于 Java NIO2 文件系统 API 的高性能本地文件操作。
- **Root 超级用户提供程序**：通过 Magisk / KernelSU / APatch 的 `su` 直接读写受保护分区（`/system`、`/data/adb`、`/data/data`）。
- **Shizuku 提供程序**：在免 Root 环境下绕过 Android 分区存储限制，访问 `/Android/data` 与 `/Android/obb`。
- **网络存储提供程序**：原生内置 SMB（v1/v2/v3）、SFTP、FTP 与 WebDAV 客户端。

### 1. Root 模式（Magisk / KernelSU / APatch）
- 打开 Material Files -> 从侧边栏点击 **根目录**（`/`）。
- 在 Magisk、KernelSU 或 APatch 弹窗中授予超级用户权限。
- 随后即可自由浏览与编辑系统分区、查看 Magisk 模块目录（`/data/adb/modules/`）并修改配置脚本。

### 2. Shizuku 存储提供程序（免 Root 访问分区存储）
Android 11 至 Android 15 限制普通文件管理器访问 `/sdcard/Android/data` 和 `/sdcard/Android/obb`：
- 启动 **Shizuku**。
- 在 Material Files 左侧抽屉栏点击 **添加存储** -> 选择 **Shizuku**。
- 无需完整 Root 权限，即可获得 `/sdcard/Android/data` 目录的完整复制、移动与编辑权限。

---

## 网络存储与归档管理

### 远程存储客户端
Material Files 内置支持以下网络协议：
- **SMB / CIFS**：直连 Windows 网上邻居共享、TrueNAS 或本地路由器存储。
- **SFTP / SSH**：通过加密 SSH 隧道安全管理远程 Linux 服务器文件。
- **FTP / FTPS**：兼容传统服务器文件传输。
- **WebDAV**：连接 Nextcloud、ownCloud 或各类远程网盘服务。

### 高性能压缩包管理
无需预先解压到磁盘即可原生浏览与创建压缩包：
- 查看并编辑 `.zip`、`.tar`、`.tar.gz`、`.tar.bz2`、`.tar.xz` 与 `.7z` 内部文件。
- 支持解压分卷压缩包及采用 AES-256 加密的密码保护 ZIP/7Z 归档文件。

---

## 安全性与权限校验

编辑系统脚本或 `/data/adb/modules/` 中的模块文件时，确保正确的 Linux 文件权限对于防止系统卡开机（Bootloop）至关重要：

```bash
# Verify permissions directly in Material Files Properties or terminal:
chmod 0755 /data/adb/modules/<module_id>/post-fs-data.sh
chmod 0755 /data/adb/modules/<module_id>/service.sh
```
Material Files 可在“属性”面板中直观核对文件权限位（`rwxr-xr-x`）及 SELinux 文件上下文（`u:object_r:system_file:s0`）。
