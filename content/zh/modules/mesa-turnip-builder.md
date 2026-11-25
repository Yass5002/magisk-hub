---
id: "mesa-turnip-builder"
title: "Mesa Turnip Builder：高通 Adreno GPU 无系统修改开源 Vulkan 驱动模块"
sidebarTitle: "Mesa Turnip Builder"
description: "基于 Android NDK r30 编译的 Freedreno Turnip 开源 Vulkan 驱动可刷入模块，在 Android 14+ 设备上安全替换 /system/vendor/lib64/hw/vulkan.adreno.so 并自动清理着色器缓存。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Mesa Turnip Builder 下载"
  - "Turnip Vulkan 驱动 Magisk 模块"
  - "vulkan.adreno.so Android 14 15 替换"
  - "Adreno 6xx 7xx 8xx 开源驱动模块"
  - "v3kt0r-87 Mesa Turnip Builder"
prerequisites:
  - "搭载高通骁龙 Adreno 6xx、7xx 或 8xx GPU 的设备"
  - "Android 14+（强制要求 `ro.build.version.sdk >= 34`；完整支持 Vulkan 1.4 建议使用 Android 15 / SDK 35+）"
  - "Magisk v25.2+、KernelSU 或 APatch"
conflicts:
  - "其他同时替换 `/system/vendor/lib64/hw/vulkan.adreno.so` 的 GPU 驱动模块"
  - "Android 13 及以下版本（`SDK < 34` 会在安装阶段直接中止）"
  - "非高通平台设备（联发科 Mali/Immortalis、三星 Exynos Xclipse、Pixel Tensor）"
configPaths:
  - "/data/adb/modules/turnip-mesa/"
  - "/system/vendor/lib64/hw/vulkan.adreno.so"
features:
  - "以无系统修改（Systemless）方式将系统 Adreno Vulkan 驱动替换为基于 Android NDK r30 构建的 Mesa 26.3.1 Freedreno Turnip"
  - "刷入时显式设置 `u:object_r:same_process_hal_file:s0` SELinux 上下文，确保满足 Android SP-HAL 链接器命名空间权限要求"
  - "安装与卸载阶段均自动递归清理各用户及应用缓存目录下的 `*shader*`、`*graphitecache*` 与 `*gpucache*` 残留"
  - "显著改善模拟器（Dolphin、PPSSPP、EggNS）、ANGLE 及现代 Vulkan 游戏的扩展兼容性与渲染准确性"
faq:
  - question: "为什么 `customize.sh` 要专门为 `vulkan.adreno.so` 设置 `same_process_hal_file` SELinux 上下文？"
    answer: "自 Android 8.0 引入 Treble 架构起，Vulkan ICD 驱动属于同进程 HAL（SP-HAL），会被直接加载进非特权普通应用进程的内存空间中。如果挂载后的 `.so` 缺少 `u:object_r:same_process_hal_file:s0` 标签，SELinux 会直接拦截应用的 `mmap` 与执行请求，导致所有调用 Vulkan 的应用闪退或黑屏。"
  - question: "为什么在 Android 13 或更低版本上无法刷入该模块？"
    answer: "`customize.sh` 会读取 `ro.build.version.sdk`（并回退检查 `ro.system.build.version.sdk`），若低于 `34` 将立即中止安装（`Android 14 is now required!`）。此外，上游说明指出完整支持新版 Mesa Turnip 的 Vulkan 1.4 特性需要 Android 15（SDK 35）系统环境。"
  - question: "刷入或卸载 Turnip 模块后需要手动清除游戏和模拟器的着色器缓存吗？"
    answer: "不需要。无论是 `customize.sh` 还是 `uninstall.sh`，都会通过 `find` 扫描 `/data/user/*/*/*cache`、`/data/data/*/*cache` 与 `/data/user_de/*/*/*cache`，自动删除 `*shader*`、`*graphitecache*` 和 `*gpucache*` 目录，防止闭源 Adreno 与开源 Turnip 之间的缓存格式不兼容引发花屏或崩溃。"
---

## 概述

高通官方随 OEM 固件分发的闭源 Adreno Vulkan 驱动往往长期停留在旧版本，缺乏现代 Vulkan 扩展支持，在各类主机模拟器与图形转译层中容易出现贴图错误或特性缺失。**Mesa Turnip Builder**（`v3kt0r-87/Mesa-Turnip-Builder`，模块 ID `turnip-mesa`）利用 **Android NDK r30** 编译上游 **Mesa Freedreno Turnip** 开源驱动，并打包为标准可刷入的 `Turnip-26.3.1-MAGISK-KSU.zip` 模块。

---

## 技术架构与模块内部机制

查看 `Turnip-26.3.1-MAGISK-KSU.zip` 的包内结构，可以看到其严格遵循 Treble SP-HAL 规范的精简设计：

| 文件 | 作用说明 |
| --- | --- |
| `system/vendor/lib64/hw/vulkan.adreno.so` | 基于 Mesa 26.3.1 编译的 64 位 Freedreno Turnip ICD 驱动，无侵入覆盖原厂 Vulkan 实现 |
| `customize.sh` | 校验 SDK >= 34，配置 `0644` 权限与 `u:object_r:same_process_hal_file:s0` 标签，并清理旧 GPU 缓存 |
| `uninstall.sh` | 模块卸载时同步清理着色器/图形缓存，防止切回原厂驱动时产生二进制缓存冲突 |
| `module.prop` | 声明 `id=turnip-mesa`、`version=v26.3.1`，并关联 `stable` 分支的 `updateJson` 更新源 |

### 核心实现细节

1. **Android 14+ 版本校验**：`customize.sh` 检查 `ro.build.version.sdk` 与 `ro.system.build.version.sdk`，低于 SDK 34 的系统将拒绝安装；若需完整启用 Vulkan 1.4 能力，建议在 Android 15（SDK 35+）上使用。
2. **SP-HAL SELinux 权限标签**：在递归赋予 `$MODPATH/system` 基础权限（`0755`/`0644`）后，脚本显式执行：
   ```sh
   set_perm $MODPATH/system/vendor/lib64/hw/vulkan.adreno.so 0 0 0644 u:object_r:same_process_hal_file:s0
   ```
   确保所有 64 位系统服务与第三方应用均可通过 `sphal` 链接器命名空间正常加载驱动。
3. **自动着色器缓存清理**：由于高通闭源驱动生成的着色器缓存与 Mesa Turnip 的 NIR/IR3 编译器不兼容，安装和卸载脚本均会自动清除 `/data/data/`、`/data/user/` 及 `/data/user_de/` 下的 `*shader*`、`*graphitecache*` 与 `*gpucache*`。

---

## 安装与配置指南

1. 确认设备搭载 **高通 Adreno 6xx、7xx 或 8xx** GPU 且系统版本为 **Android 14+**（SDK 34+）。
2. 建议提前确认 Root 管理器安全模式（Safe Mode）触发方式或准备 Recovery 救砖手段（全局替换系统 Vulkan 驱动在部分启用 SkiaVk / ANGLE 渲染的固件上可能影响系统界面）。
3. 在 **Magisk**（v25.2+）、**KernelSU** 或 **APatch** 中刷入 `Turnip-26.3.1-MAGISK-KSU.zip`。
4. 等待 `Cleaning GPU Cache` 流程执行完毕后**重启设备**。
5. 可通过 **3DMark**、**Vulkan Hardware Capability Viewer** 或 Dolphin、PPSSPP 等模拟器的图形信息页验证当前已切换为 Turnip 驱动。

---

## 常见问题与排查

- **部分机型刷入后系统界面闪烁或无法进入桌面**：个别较新的 Adreno 8xx 步进版本或深度定制了 SkiaVk 管线的系统可能与全局 Turnip 存在兼容性回退。进入 Root 安全模式或通过 Recovery/ADB 删除 `/data/adb/modules/turnip-mesa` 即可无损恢复；若在系统内卸载，`uninstall.sh` 会自动清理解析残留的缓存。
- **更新驱动后个别游戏贴图异常或闪退**：强制停止对应游戏或模拟器，并手动清理该应用的全部缓存，以防应用将 Vulkan 管线缓存存放在自定义非标准目录中。
- **32 位老旧应用仍调用原厂驱动**：当前发布包仅替换 64 位 `lib64/hw/vulkan.adreno.so`。主流 64 位游戏与模拟器均会加载 Turnip，而纯 32 位 `armeabi-v7a` 应用仍会回落至设备原有的 32 位驱动。
