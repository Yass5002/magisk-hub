---
id: "ezme-dex-space"
title: "ezme-dex-space：面向空间优化的 Android ART 预编译（AOT）调优"
sidebarTitle: "ezme-dex-space"
description: "将 Android dex2oat 编译器目标从 speed 重新配置为 space-profile，大幅降低 Dalvik 缓存存储占用与内存开销。"
category: "system-utilities"
tier: 1
searchQueries:
  - "ezme-dex-space Magisk 模块"
  - "Android dex2oat 节省内部存储空间"
  - "pm.dexopt.bg-dexopt space-profile 设置"
  - "Root 缩小 dalvik-cache 体积"
  - "Android AOT 编译空间优化模块"
prerequisites:
  - "Android 11、12、12L 或更高版本"
  - "通过 Magisk v24+ 或 KernelSU 获取 Root 权限"
  - "建议安装后清空 Dalvik 缓存以触发重新优化"
conflicts: []
configPaths:
  - "/data/adb/modules/ezme-dex-space/"
features:
  - "Systemless 属性调优：无侵入式配置安装、后台 dexopt 与 OTA 升级阶段的编译器参数"
  - "空间优化字节码编译：将 AOT 编译配置从激进的 speed 切换为紧凑的 space-profile"
  - "缓解低内存抖动：更小的应用编译体积有助于减少因内存不足（OOM）引发的杀后台"
  - "数 GB 级空间回收：在安装大量应用的设备上显著缩减 /data/dalvik-cache 空间占用"
faq: []
---

## 概述

Android Runtime（ART）的预编译（AOT）编译器（`dex2oat`）负责将 DEX 字节码编译为原生机器码 ELF 文件（`.odex` 与 `.vdex`）。现代 Android 版本默认采用激进的 `speed` 编译策略，尽管能为纯 CPU 运算带来微弱的执行速度提升，但会使编译产物体积急剧膨胀——在应用较多的设备上，`/data/dalvik-cache` 往往会吞噬 10GB 至 20GB 的内部存储空间。

由 ez-me 开发的 **ezme-dex-space** 以无系统分区修改（Systemless）方式重新调优 Android 内部包管理器的编译指令。通过将默认编译目标从 `speed` 切换为 `space-profile`，它引导 `dex2oat` 仅对高频热路径代码执行优化编译，其余部分保留紧凑字节码形态，从而释放可观的存储空间并降低内存压力。

## 已配置的系统属性指令

该模块以 Systemless 方式设置以下包管理器编译参数：

```ini
pm.dexopt.install=space-profile
pm.dexopt.install-bulk=space-profile
pm.dexopt.bg-dexopt=space-profile
pm.dexopt.ab-ota=space-profile
pm.dexopt.shared=space
```

### 各目标策略说明：
- **`space-profile`**：分析应用日常运行时的实时配置文件（Profile），仅编译实际被调用的方法。未使用的库代码保持未展开状态，大幅压缩二进制产物大小。
- **`space`**：为共享系统库生成最小占用体积的编译代码，避免多应用间产生重复编译开销。

## 重新优化现有应用

刷入模块后，新的编译指令将应用于后续所有新安装应用及后台维护周期。若要立即从已安装应用中回收存储空间：

1. 通过 **Magisk** 或 **KernelSU** 刷入 **ezme-dex-space**。
2. 使用第三方 Recovery 或终端命令清空 Dalvik/ART 缓存：
   ```bash
   su -c rm -rf /data/dalvik-cache/*
   ```
3. 重启设备。
4. Android 将在首次启动及随后的空闲充电周期中，依据新的 `space-profile` 目标重新编译所有应用包。

## 兼容性与验证

- **已验证系统**：确认在 LineageOS 18.1 与 19.1（Android 11 与 12L）直至现代 Android 14+ 系统上稳定运行。
- **验证方法**：在终端 Shell 中检查当前生效的包管理器编译属性：
   ```bash
   getprop | grep pm.dexopt
   ```
   所有返回条目均应显示为 `space-profile` 或 `space`。
