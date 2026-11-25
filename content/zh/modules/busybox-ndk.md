---
id: "busybox-ndk"
title: "Busybox for Android NDK：全架构静态编译 BusyBox 模块"
sidebarTitle: "Busybox NDK"
description: "由 osm0sis 使用 Android NDK 静态编译的 BusyBox 1.36.1 安装包，覆盖 ARM、ARM64、x86、x86_64 与 MIPS 全架构，支持 SELinux 版本及无系统分区修改（Systemless）符号链接管理。"
category: "system-utilities"
tier: 1
searchQueries:
  - "BusyBox NDK 下载"
  - "osm0sis BusyBox 1.36.1 模块"
  - "Magisk KernelSU BusyBox 安装包"
  - "BusyBox NDK nolinks noselinux 用法"
  - "Android 全架构静态 BusyBox"
prerequisites:
  - "支持 Magisk、KernelSU、APatch、SuperSU 或第三方 Recovery（TWRP / OrangeFox）"
  - "支持的处理器架构：ARM、ARM64、x86、x86_64、MIPS 或 MIPS64"
conflicts:
  - "其他同时在 `/system/bin` 或 `/system/xbin` 写入同名工具链的旧版 BusyBox 安装器（如 Stericson BusyBox）"
configPaths:
  - "/data/adb/modules/busybox-ndk/system/xbin/busybox"
  - "/data/adb/modules/busybox-ndk/system/bin/busybox"
features:
  - "内置 10 份 NDK 静态编译的 BusyBox 1.36.1 二进制文件（涵盖 `arm`、`arm64`、`x86`、`x86_64`、`mips`、`mips64` 及其 `-selinux` 变体）"
  - "采用 Diffusion Installer Core（`customize.sh` + `diffusion_config.sh`），同时支持开机后 Root 管理器刷入与 Recovery 模式安装/卸载"
  - "支持通过修改 ZIP 文件名选项（`nolinks`、`noselinux`）免改脚本灵活控制是否创建 Applet 符号链接及是否使用 SELinux 版本"
  - "安装前自动清理历史 `busybox` 残留符号链接，并在安装至 `bin` 目录时避开 `/system/bin` 原生命令以防冲突"
faq:
  - question: "如何在不生成 Applet 符号链接或不启用 SELinux 版本的情况下安装？"
    answer: "该模块在 `diffusion_config.sh` 中启用了 `USE_ZIP_OPTS=true`。只需在刷入前重命名压缩包文件名即可：文件名包含 `nolinks`（不区分大小写）将设置 `NOLINKS=1` 仅安装主程序而不生成符号链接；包含 `noselinux` 则会安装不含 `-selinux` 后缀的常规静态版本（MIPS 架构默认不带 `-selinux`）。"
  - question: "在 Magisk、KernelSU 或 APatch 中，BusyBox 会被安装到哪个路径？"
    answer: "安装脚本会检查设备是否存在 `/system/xbin`（或兼容路径）。若存在 `/system/xbin`，则以无系统分区修改（Systemless）方式挂载至 `/data/adb/modules/busybox-ndk/system/xbin/busybox`；在无 `xbin` 的现代 SAR 分区设备上则会回退安装至 `$MODPATH/system/bin/busybox`，且自动跳过 `/system/bin` 中已有的原生命令以防覆盖系统二进制。"
---

## 概述

由知名开发者 **osm0sis**（`xda-developers`）维护的 **Busybox for Android NDK** 提供了基于 Android NDK 静态链接编译的 **BusyBox 1.36.1** 工具集（最初源于其 `AIK-mobile` 项目需求）。许多 Root 自动化脚本、系统调试工具以及模块安装脚本需要标准 POSIX/GNU 风格的命令行工具（如 `awk`、`sed`、`grep`、`tar`、`unzip`、`nc`、`vi` 等），而 Android 原生精简的 `toybox` 与 `mksh` 在参数兼容性上往往有所欠缺。

该压缩包将全架构静态二进制封装于一体，可自动识别设备架构、清理旧版残留符号链接，并安全地建立新的命令映射。

---

## 技术架构与安装脚本机制

检查 `UPDATE-Busybox.Installer.v1.36.1-ALL-signed.zip` 内容可知，其核心安装逻辑由 **Diffusion Installer Core**（`customize.sh` 与 `diffusion_config.sh`）驱动：

### 1. 内置静态编译二进制文件
压缩包包含来自 `osm0sis/android-busybox-ndk` 构建的 10 个静态 ELF 可执行文件：
- **ARM / ARM64**：`busybox-arm`、`busybox-arm-selinux`、`busybox-arm64`、`busybox-arm64-selinux`
- **x86 / x86_64**：`busybox-x86`、`busybox-x86-selinux`、`busybox-x86_64`、`busybox-x86_64-selinux`
- **MIPS / MIPS64**：`busybox-mips`、`busybox-mips64`（`custom_install` 会在 `mips*` 架构下取消 `SELINUX` 后缀）

### 2. 核心安装与链接逻辑（`diffusion_config.sh`）
1. **ZIP 文件名参数识别（`custom_zip_opts`）**：
   - 默认安装带 `-selinux` 后缀的二进制（ARM/x86 架构）并生成全套 Applet 符号链接。
   - 文件名含 `nolinks` 时置位 `NOLINKS=1`，跳过符号链接创建。
   - 文件名含 `noselinux` 时取消 `-selinux` 后缀选择。
2. **安装目录与权限**：
   - 在 Magisk、KernelSU 与 APatch 环境下安装到模块挂载目录（优先 `system/xbin`，若无则使用 `system/bin`），设置权限 `0755` 及 SELinux 上下文 `u:object_r:system_file:s0`。
3. **旧链接清理（`custom_cleanup`）**：
   - 扫描目标目录（及早期迁移路径）中所有指向 `*busybox` 的符号链接并预先清除，防止无效链接残留。
4. **安全符号链接生成（`custom_postinstall`）**：
   - 调用 `$XBIN/busybox --list` 遍历所有受支持小程序（Applet）并执行 `busybox ln -sf busybox $applet`。
   - 当部署路径为 `*/bin` 时，会与 `ls /system/bin` 列表比对，避免直接覆盖系统自带二进制文件。

---

## 安装与验证

1. 下载 `UPDATE-Busybox.Installer.v1.36.1-ALL-signed.zip`（如需启用 `nolinks` 或 `noselinux` 选项可先重命名压缩包）。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中选择 **从本地安装** 刷入，或通过第三方 Recovery 刷入。
3. 重启设备使系统挂载生效。

### 命令行验证

```bash
# 查看当前生效的 busybox 路径
which busybox

# 确认版本与静态编译信息
busybox | head -n 2

# 统计可用 Applet 数量
busybox --list | wc -l

# 查看 SELinux 安全上下文
ls -Z "$(which busybox)"
```

---

## 卸载说明

在 Root 管理器中卸载 **Busybox for Android NDK** 并重启即可移除系统挂载。若是在无 Systemless 支持的 Recovery 模式下直接刷入 `/system` 分区，再次刷入相同 ZIP（或使用脚本卸载模式）会触发 `customize.sh` 的 `ACTION=uninstall` 分支，调用 `custom_uninstall` 与 `custom_cleanup` 彻底清除 `busybox` 及全部相关符号链接。
