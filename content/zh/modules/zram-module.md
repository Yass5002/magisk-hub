---
id: "zram-module"
title: "ZRAM Module：自定义内核压缩算法与容量管理器"
sidebarTitle: "ZRAM Module"
description: "在不修改系统分区的前提下，开机动态加载自定义内核压缩算法模块（如 lz4kd、zstdn）并重新配置 ZRAM 交换容量。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "ZRAM Module Magisk 模块"
  - "FurLC ZRAM-Module 下载"
  - "Android 加载自定义 ZRAM 算法"
  - "lz4kd zstdn ZRAM 内核模块"
  - "KernelSU 自定义 ZRAM 大小"
prerequisites:
  - "已通过 Magisk 或 KernelSU 获取 Root 权限"
  - "Android 内核已启用 ZRAM 支持及可加载内核模块支持（`CONFIG_MODULES=y`）"
conflicts: []
configPaths:
  - "/data/adb/modules/ZRAM-Module/"
features:
  - "动态加载内核模块：开机时自动探测并插入树外编译的压缩驱动模块（`.ko`），如 `lz4kd` 与 `zstdn`"
  - "自定义 ZRAM 容量分配：轻松按需设定内存压缩交换分区的总容量"
  - "降低解压开销：借助更高效的压缩算法提升内存页换入换出与检索速度"
  - "零分区修改：以无系统分区修改（Systemless）方式执行 `modprobe` 与 sysfs 参数绑定"
  - "双 Root 平台兼容：原生兼容 Magisk 与 KernelSU 环境"
---

## 概述

ZRAM 是 Linux 内核中至关重要的内存优化特性，能够在物理内存中划出一块虚拟压缩块设备。通过将非活跃内存页压缩存放而非写入速度较慢的闪存，ZRAM 能够有效扩展可用内存空间，显著提升后台应用的留存率。

然而，原厂 Android 内核通常将压缩算法锁定在标准的 `lz4` 或 `lzo-rle`，且若不重新编译整个 Boot 镜像，很难灵活调整固定的 ZRAM 容量。此外，编译了高性能树外压缩驱动（如 `lz4kd` 或 `zstdn`）的第三方内核开发者，也常常面临如何干净地分发这些驱动模块的问题。

由 FurLC 开发的 **ZRAM-Module** 是一款专为 Magisk 与 KernelSU 打造的实用性能模块。它能在开机早期自动加载自定义压缩内核模块（`.ko`），并以无侵入式方式完成自定义 ZRAM 块大小的设置。

## 核心能力

1. **自动插入 `.ko` 驱动**：模块会在开机早期扫描内置目录，并对打包的压缩算法驱动（如 `lz4kd.ko` 或 `zstdn.ko`）自动执行 `insmod` / `modprobe`。
2. **动态算法绑定**：当驱动成功注册至内核加密子系统（Crypto API）后，模块会将其直接绑定至 `/sys/block/zram0/comp_algorithm`。
3. **灵活的容量调节**：支持用户在执行 `swapon` 初始化前按需设定具体的 ZRAM 空间大小（例如 4GB、6GB、8GB）。
4. **第三方内核绝佳搭档**：尤其适合追求极致性能与低延迟游戏体验的第三方内核用户。

## 安装与配置

1. 从 GitHub Releases 下载最新的 `ZRAM-Module-v*.zip` 压缩包。
2. 在 **Magisk** 或 **KernelSU** 中安装该模块包。
3. 重启设备。
4. 在 Termux 中验证当前生效的压缩算法与 ZRAM 分配容量：
   ```bash
   su -c cat /sys/block/zram0/comp_algorithm
   su -c free -m
   ```
