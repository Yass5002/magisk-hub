---
id: "swap-disabler"
title: "Swap Disabler：面向大内存设备彻底禁用 Swap 与虚拟内存"
sidebarTitle: "Swap 禁用器"
description: "在配备 8GB–16GB+ 物理内存的设备上，开机自动禁用 Android Swap 交换空间、虚拟内存扩展（RAM Plus、动态内存扩展）与冗余分页。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Swap Disabler Magisk 模块"
  - "rompelhd Swap Disabler 下载"
  - "关闭三星 RAM Plus 虚拟内存 Root"
  - "Android 禁用 Swap 分区 Magisk"
  - "关闭 ZRAM 虚拟内存扩展 Root"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
  - "配备充足物理运行内存的设备（建议 8 GB 及以上）"
conflicts:
  - "其他 Swap 交换分区管理模块（例如 magisk-swapspace 或 SwapBoost-Pro）"
configPaths:
  - "/data/adb/modules/Swap-Disabler/"
features:
  - "开机自动终止 Swap：在系统启动早期对所有活动交换设备与回环分区执行内核 swapoff 命令"
  - "保护闪存寿命：避免系统在后台持续向机身 UFS/eMMC 闪存芯片写入大量交换数据"
  - "消除微卡顿：防止应用线程在读取被换出到磁盘的内存页时因等待 I/O 而阻塞"
  - "专为现代旗舰优化：为配备 8 GB、12 GB、16 GB 或 24 GB 物理内存的机型免除不必要的 CPU 压缩开销"
  - "纯无侵入式执行：通过开机服务脚本下发指令，完全不破坏系统分区完整性"
---

## 概述

许多手机厂商热衷于宣传所谓的“虚拟内存”、“RAM Plus”或“动态内存扩展”，其本质是从机身内部闪存中划出数 GB 空间作为二级 Swap 交换分区。在早期仅配备 2GB–3GB 物理内存的老设备上，Swap 确实能减少内存不足（OOM）导致的闪退；但在如今普遍搭载 8GB、12GB、16GB 甚至更高容量高速 LPDDR 物理内存的现代智能手机上，Swap 不仅毫无必要，反而会拖累整机性能。

由于闪存的读写速度比物理内存慢出好几个数量级，频繁将内存数据换入换出闪存会引入明显的 I/O 延迟、导致切换应用时出现微卡顿，并加速机身内部闪存芯片的擦写损耗。

由 rompelhd 开发的 **Swap-Disabler** 是一款无侵入式（Systemless）Magisk 模块，可在系统启动阶段自动执行 `swapoff` 命令，彻底关闭活动的磁盘交换文件与虚拟内存机制。

## 大内存设备禁用 Swap 的优势

1. **消除闪存写入磨损**：在数月乃至数年的日常使用中，避免系统向机身 UFS 闪存执行数百 GB 的无效后台写入操作。
2. **应用切换更跟手**：驻留在高速物理内存中的应用可瞬间唤醒，无需等待内核从缓慢的闪存或压缩页中重新换入数据。
3. **降低 CPU 负载**：省去内核持续运行内存压缩算法以及维护交换页表所消耗的 CPU 算力。

## 安装与验证

1. 确认你的设备至少配备 8 GB 物理内存。
2. 从 GitHub Releases 下载最新的 `Swap-Disabler-v*.zip` 模块压缩包。
3. 在 **Magisk** 中刷入该模块。
4. 重启设备。
5. 在 Termux 或 ADB Shell 中执行以下命令，验证 Swap 是否已成功关闭：
   ```bash
   su -c free -m
   ```
   *（输出结果中 Swap 行的 total 与 used 均应显示为 `0`。）*
