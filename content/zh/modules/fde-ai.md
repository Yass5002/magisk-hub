---
id: "fde-ai"
title: "FDE.AI (FeraDroid Engine)：自适应无系统分区修改（Systemless）Android 优化工具"
sidebarTitle: "FDE.AI"
description: "独立运行的 Root 系统优化应用（com.feravolt.fdeai），在不修改系统分区的前提下提供自适应 AI 内核、虚拟内存、CPU/GPU 调度器、温控冷却与电源管理。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "FDE.AI 下载"
  - "FeraDroid Engine Magisk KernelSU"
  - "安卓 AI 内核虚拟内存优化"
  - "FDE.AI 旁路供电与温控设置"
  - "Root 性能省电调度软件"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取超级用户权限（亦支持免 Root 的 Shizuku 模式，但内核级调优能力受限）"
  - "支持 ARM64（`arm64-v8a`）或 ARMv7（`armeabi-v7a`）架构的 Android 设备"
conflicts:
  - "其他同时修改内核/调度参数的工具或脚本（如各类性能调度脚本、温控修改模块等）"
  - "FDE.AI 内部互斥功能：不能同时开启「旁路供电（Charging Bypass）」与「电池寿命延长（Battery Life Cycle Extender）」"
configPaths:
  - "/data/data/com.android.system.optimizer/"
  - "/data/adb/fdeai/"
features:
  - "实时 AI 进程负载识别：自动区分前台重负载与轻负载应用，动态切换 CPU/GPU 调度器（Governor）、DDR/L3/UFS 总线加速与预读参数"
  - "内置 `CooldownService`、`DownscaleService`、`SoundService` 与 `AutorunService` 等独立后台服务，并提供快捷设置磁贴与悬浮性能监视窗"
  - "支持动态虚拟内存（VM）调优、8GB+ 内存设备专属动态预读（Dynamic Read-Ahead）、熄屏充电期间自动触发 ART 与文件系统优化，并内置精简（Debloat）清单"
  - "提供可自定义温度上限的温控降频控制、强制 Doze、熄屏后台清理、充电上限保护（下降 6% 恢复）及直通旁路供电功能"
faq:
  - question: "使用 FDE.AI 是否需要刷入 ZIP 模块或修改 `/system` 分区？"
    answer: "不需要。FDE.AI 以独立 APK 形式发布（`FDE.AI-v26.08.1.apk`，应用核心命名空间为 `com.feravolt.fdeai`，清单包名为 `com.android.system.optimizer`）。所有内核参数、sysfs 节点、虚拟内存与调度策略均在运行时以无侵入式（Systemless）方式动态写入，完全不触碰 `/system` 分区。"
  - question: "FDE.AI 的 Root 模式与 Shizuku 模式有何区别？"
    answer: "在 Root 模式下（通过 `libsu` 配合 Magisk、KernelSU 或 APatch 授权），FDE.AI 可调用内置原生二进制库（`libfcore.so`、`libfdeinit.so`、`libfbusybox.so`、`libprofilehelper.so`）直接读写内核 sysfs 节点、CPU/GPU 频率表、DDR/L3/UFS 总线、VM 参数与硬件充电开关；而 Shizuku 模式仅能在用户态与 `WRITE_SECURE_SETTINGS` 权限范围内执行受限优化。"
---

## 概述

由 **feravolt** 开发的 **FDE.AI**（**FeraDroid Engine**）是一款跨平台、无系统分区修改（Systemless）的 Android 综合性能优化工具。它不同于对所有机型套用同一套死板参数的传统 `init.d` 或 `sysctl` 脚本，而是根据设备的实时硬件特性与当前运行状态，为每台设备独立生成并动态切换平衡的性能与功耗配置。

当设备熄屏时，所有性能加速策略会自动关闭，以尽可能降低待机功耗。

---

## 技术架构与核心组件

通过分析 `FDE.AI-v26.08.1.apk` 安装包，其内部采用基于 `libsu`、Shizuku（`rikka.shizuku.ShizukuProvider`）、AndroidHiddenApiBypass 的多进程 Kotlin/Compose 架构，并同时包含 `arm64-v8a` 与 `armeabi-v7a` 双架构原生执行库：

- **原生执行层**：
  - `libfcore.so` 与 `libfdeinit.so`：核心原生调优引擎与初始化例程。
  - `libfbusybox.so`：内置 BusyBox 二进制（`Brutal_busybox`，GPL-2.0），确保在不同 ROM 上执行 Shell 与 sysfs 操作时的行为一致性。
  - `libprofilehelper.so`：硬件信息与配置档案探测组件。
- **独立后台服务与进程**：
  - `:CooldownService`（`com.feravolt.fdeai.services.main.CooldownService`）：降温冷却服务，可通过快捷磁贴 `TileServiceCooldown` 快速触发。
  - `:DownscaleService`（`com.feravolt.fdeai.services.main.DownscaleService`）：分辨率缩放与刷新率调节服务（清单元数据包含 `60, 90, 120, 144` Hz 支持）。
  - `:SoundService`（`com.feravolt.fdeai.services.main.SoundService`）：音频子系统调节服务与广播接收器（`SoundReceiver`）。
  - `AutorunService` 与 `BootReceiver`：在系统启动完成（`BOOT_COMPLETED`）或应用更新替换（`MY_PACKAGE_REPLACED`）后自动恢复 AI 配置。
  - `OverlayServiceMainFloating` / `OverlayServiceTopFloating`：实时帧率与状态悬浮窗。

### 自适应 AI 与内核调度能力

1. **进程检测与机器学习**：实时分析前台应用，自动识别重负载（大型游戏/渲染）或轻负载（聊天/浏览）场景，在 AI 自动模式下动态调整策略，也支持手动指定特定应用的负载分级。
2. **CPU Turbo、GPU Turbo 与总线加速**：在高负载下结合设备温度动态调整 CPU/GPU 调度器（Governor）及最低频率下限；在支持的 SoC 上，性能模式还会提升 **DDR / L3 缓存 / UFS 闪存** 频率。
3. **温控降频管理（Throttling Control）**：可选关闭系统的部分温控降频策略以维持持续高帧率，同时允许用户设定安全温度阈值；当设备过热或正在充电时会自动回退保护。
4. **动态 VM 与磁盘预读**：依据实时内存占用动态调节 Linux 虚拟内存（`vm.*`）参数；在 **8 GB 及以上内存** 设备上，会在重负载期间自动增大块设备预读（`read_ahead_kb`），退出后恢复默认值。
5. **熄屏省电与电池寿命管理**：
   - **强制 Doze / 系统省电 / 流量节省 / 熄屏杀后台**：在屏幕关闭后立即介入降低待机耗电。
   - **ART 与文件系统优化**：支持手动或自动以 `max` 过滤级别编译优化 ART 缓存，并在熄屏充电时触发文件系统优化。
   - **充电上限保护与旁路供电**：可将最大充电电量限制在设定百分比（低于设定值 6% 后恢复充电），或在玩重负载游戏时启用直通旁路供电减少电池发热。上述两项功能互斥，不可同时启用。

---

## 安装与配置指南

1. 下载并安装 `FDE.AI-v26.08.1.apk`。
2. 首次启动时在 **Magisk**、**KernelSU** 或 **APatch** 中授予超级用户权限（若使用免 Root 模式则授权 **Shizuku**）。
3. 阅读并同意最终用户许可协议（EULA），选择初始预设（均衡、性能或省电），如需使用快捷磁贴（`TileServiceAiMode`、`TileServiceCooldown`、`TileServiceMainOverlay`）或悬浮窗请授予通知及悬浮窗权限。
4. 按需在设置中调整温度安全上限、单应用重/轻负载名单及电池保护选项。

---

## 验证与状态检查

可通过具备 Root 权限的终端或 ADB Shell 检查 FDE.AI 进程状态及内核参数生效情况：

```bash
# 查看 FDE.AI 相关进程与服务是否正常运行
su -c "ps -ef | grep -E 'fdeai|optimizer'"

# 检查当前虚拟内存与块设备预读参数
su -c "cat /proc/sys/vm/swappiness; cat /sys/block/sda/queue/read_ahead_kb 2>/dev/null"

# 启用强制 Doze 后检查深度睡眠状态
dumpsys deviceidle get deep
```

> **提示**：FDE.AI 为闭源专有软件（Proprietary）。请勿将其与同样频繁写入 `/sys/devices/system/cpu/` 或 `/proc/sys/vm/` 的其他内核调度模块同时使用，以免参数互相覆盖。
