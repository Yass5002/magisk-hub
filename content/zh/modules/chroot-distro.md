---
id: "chroot-distro"
title: "chroot-distro：适用于 Android 的 GNU/Linux 发行版管理器"
sidebarTitle: "chroot-distro"
description: "功能强大的终端工具，用于在 Android 原生 chroot 环境中安装并运行完整的 GNU/Linux 发行版（Debian、Arch、Ubuntu、Alpine）。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "chroot-distro Magisk 模块"
  - "Android Root 原生 chroot 运行 Linux"
  - "手机 chroot 安装 Debian Ubuntu"
  - "chroot-distro 终端容器管理"
  - "proot-distro 原生 Root 替代方案"
prerequisites:
  - "已获取 Root 权限的 Android 设备（支持任意 Root 方案）"
  - "BusyBox for Android NDK（推荐使用 v1.36.1，请勿使用 v1.32.1）"
  - "终端环境：Termux、MT 管理器、MiXplorer 或 ADB Shell"
conflicts:
  - "说明：与其他模块暂无已知冲突；但依赖正常的 BusyBox NDK 二进制工具以下载并解压 rootfs 镜像"
configPaths:
  - "/data/local/chroot-distro/"
  - "/data/local/chroot-distro/.config/"
features:
  - "原生 chroot 执行：直接以内核原生性能运行 Linux 二进制程序，彻底消除 PRoot 带来的 ptrace 性能开销"
  - "多发行版目录支持：通过简单命令即可一键安装 Debian、Ubuntu、Arch Linux、Alpine、Fedora 与 Kali Linux"
  - "自动化文件系统隔离：自动将 `/dev`、`/dev/pts`、`/proc`、`/sys` 与存储分区挂载至容器内部"
  - "内存盘优化：支持将容器 rootfs 绑定到 RAM disk，实现极低 I/O 延迟"
  - "备份与恢复机制：内置归档工具，可导出或还原已安装的 Linux 发行版环境"
faq:
  - question: "chroot-distro 与 Termux 的 proot-distro 有何区别？"
    answer: "PRoot 无需 Root 权限，但需要通过 ptrace 拦截系统调用，会带来显著的 CPU 性能损耗。chroot-distro 直接调用 Linux 原生 chroot 系统调用，让 Linux 进程以零转换开销直接运行在内核之上，并拥有完整的 Root 能力。"
  - question: "为什么必须搭配 BusyBox for Android NDK 使用？"
    answer: "chroot-distro 脚本依赖标准 GNU/Linux 命令参数（如 `tar`、`wget`、`grep` 与 `mount`），而 Android 默认的 toybox/toolbox 并不支持这些参数。由 osm0sis 维护的 BusyBox NDK 可提供完整的 POSIX 命令兼容性。"
---

## 概述

由 **Magisk-Modules-Alt-Repo** 维护的 **chroot-distro** 是一款进阶发行版部署工具，可将原生 GNU/Linux 操作系统引入已获取 Root 权限的 Android 设备。

受 PRoot Distro 工作流的启发并专为 Root 用户重新设计，chroot-distro 直接利用 Linux 原生的 `chroot` 系统调用。这使得开发者能够在 Android 旁以接近裸机的运行速度，直接跑通完整的 Linux 服务端技术栈、编译器、网络分析工具乃至桌面环境。

---

## 技术架构与工作原理

### 原生容器化与挂载命名空间

chroot-distro 将容器化环境统一管理在 `/data/local/chroot-distro/` 目录下：

1. **Rootfs 引导构建**：直接从上游镜像源下载所选 Linux 发行版的精简官方 rootfs 压缩包。
2. **系统节点绑定**：将虚拟文件系统挂载至发行版根目录：
   - `/proc` 与 `/sys`：用于内核状态检查与系统信息读取。
   - `/dev` 与 `/dev/pts`：用于伪终端处理与硬件设备访问。
   - `/sdcard` 或 `/data/media/0`：用于跨环境共享访问内部存储。
3. **Android 环境桥接**：在 Android 宿主与 Linux 容器之间桥接 DNS 配置（`/etc/resolv.conf`）及用户权限映射。

---

## 安装与配置

1. 刷入 **BusyBox for Android NDK** 模块（推荐使用 1.36.1 版本）。
2. 下载 `chroot-distro-*.zip` 模块并在你的 Root 管理器中刷入。
3. 打开 **Termux** 或任意 Root 终端应用并执行：
   ```bash
   su
   chroot-distro help
   ```

---

## 配置与使用

### 安装 Linux 发行版
```bash
# List available distributions
chroot-distro list

# Install Debian or Ubuntu
chroot-distro install debian
```

### 进入 Linux 环境
```bash
chroot-distro login debian
```
进入容器后，即可直接使用完整的标准 APT 包管理器：
```bash
apt update && apt install python3 git build-essential htop
```

---

## 故障排查与常见问题

- **下载或解压失败**：请确认已安装 BusyBox NDK。使用 Android 自带的 Toybox `tar` 命令在处理发行版符号链接与硬链接时会报错。
- **访问 Android 存储提示 Permission Denied**：若需在 chroot 容器内启用手机内部存储访问权限，请在 `/data/local/chroot-distro/.config/` 中配置 `android_bind`。
