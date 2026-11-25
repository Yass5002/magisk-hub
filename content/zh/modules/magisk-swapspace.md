---
id: "magisk-swapspace"
title: "Magisk SwapSpace：Android 持久化虚拟内存与 Swap 交换空间管理工具"
sidebarTitle: "SwapSpace Manager"
description: "在 Android 内部存储中分配、配置并管理持久化 Swap 虚拟交换内存，支持自定义 swappiness 与交换优先级。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "magisk-swapspace 模块下载"
  - "chkndrp magisk-swapspace"
  - "Android Root 创建持久化 Swap 文件"
  - "magiskswap 终端命令用法"
  - "KernelSU 虚拟内存扩容模块"
prerequisites:
  - "通过 Magisk 27.0+ 或 KernelSU v0.9.4+ 获取 Root 权限"
  - "内部存储需具备足够可用空间以存放指定大小的 Swap 文件"
conflicts: []
configPaths:
  - "/data/adb/modules/magisk-swapspace/"
features:
  - "持久化 Swap 分配：生成并挂载专用 swapfile 交换文件，设备重启后依然自动生效"
  - "可调 Linux swappiness：支持调整 vm.swappiness（0–200），灵活平衡匿名页换出与内存压力"
  - "交互式 CLI 工具（magiskswap）：直接在 Termux 中查看状态、启用、停用或调整 Swap 空间"
  - "优先级串联调度：可设置自定义 Swap 优先级，与 zRAM 协同组建分层分页机制"
  - "文件保留开关：支持在不删除或重写底层存储块的前提下临时关闭或重新启用 swapfile"
faq: []
---

## 概述

在 Android 上执行高内存占用任务时——例如在 Termux 中编译源码、运行 chroot Linux 容器、开启大型模拟器或在内存紧张的机型上进行多任务切换，有限的物理 RAM 与 zRAM 很容易迅速耗尽，进而触发低内存杀手（LMK）强行终止前台或后台进程。

由 chkndrp 开发的 **magisk-swapspace** 是一款无侵入式（Systemless）的 Swap 交换空间管理工具。它提供了简洁直观的命令行接口（`magiskswap`），方便用户在内部闪存上分配、格式化、激活并管理持久化虚拟交换空间。

## 命令参考：`magiskswap`

请在 Termux 或 ADB Shell 中获取 Root 权限后执行相关命令：

```bash
su
magiskswap <COMMAND> <VALUE> [OPTIONS]
```

### 常用命令示例

- **创建 Swap 空间**：
  ```bash
  # 创建一个 4 GB 的 swapfile，激活 swapon 并设置开机自动挂载
  magiskswap create 4
  ```
- **查看当前状态**：
  ```bash
  magiskswap status
  ```
  输出当前激活的交换路径、总分配容量以及已使用的 Swap 字节数。
- **调节 Swappiness**：
  ```bash
  # 查看当前内核 swappiness 值
  magiskswap swappiness show

  # 将内核 swappiness 设为 60（有效范围 0-200）
  magiskswap swappiness 60
  ```
- **移除 Swap**：
  ```bash
  # 关闭交换并删除 swapfile 文件
  magiskswap remove

  # 仅关闭交换但保留磁盘上已分配的文件
  magiskswap remove preserve
  ```

## 闪存寿命注意事项

> **重要提示**：现代 Android 设备普遍采用 UFS 或 eMMC 闪存颗粒。长时间、高频度地向存储介质上的 swapfile 执行分页写入会加速闪存磨损。建议保持适中的 `swappiness` 数值，仅在确实需要大内存缓冲的特定场景下启用 swapfile，避免系统持续剧烈换页。

## 安装步骤

1. 从 GitHub Releases 页面下载 `magiskswapspace.zip`。
2. 在 **Magisk**（v27.0+）或 **KernelSU**（v0.9.4+）中刷入该模块。
3. 重启设备。
4. 打开 Termux，运行 `su -c magiskswap create <size_GB>` 创建交换空间，并通过 `free -m` 验证是否生效。
