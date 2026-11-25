---
id: "livebootmodule"
title: "LiveBoot：独立版开机实时日志与内核 DMESG 启动动画"
sidebarTitle: "LiveBoot"
description: "在设备开机过程中将传统启动动画替换为按级别着色的 Linux 内核 dmesg 与 Android logcat 实时滚动日志流。"
category: "system-environment"
tier: 1
searchQueries:
  - "LiveBoot Magisk 模块"
  - "Chainfire LiveBoot Magisk 版"
  - "Android 开机显示 dmesg logcat 日志"
  - "livebootmodule symbuzzer 下载"
  - "Android 类 Unix 详细开机动画"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "已在 Android 12、13、14、15 及 16 ROM 上验证可用"
conflicts:
  - "严格限定非标准 SurfaceFlinger 帧缓冲格式的个别定制 OEM 开机画面"
configPaths:
  - "/data/adb/modules/livebootmagisk/config"
  - "/data/adb/modules/livebootmagisk/loader.sh"
features:
  - "实时开机日志流：直接在屏幕上实时渲染内核 `dmesg` 与 `logcat` 输出信息"
  - "完全独立运行：内置全部渲染程序，无需安装 Chainfire 早期的配套 APK 即可自主运行"
  - "可定制视觉模式：支持深色、透明或默认背景样式，并可自定义显示行数与自动换行"
  - "日志自动保存：支持将完整的开机日志归档保存至 `/data/cache`，便于排查卡开机（Bootloop）问题"
  - "可调退出延迟：支持设置退出延迟时间，平滑衔接桌面启动器加载前的黑屏过渡间隙"
faq:
  - question: "还需要从 Play 商店安装 Chainfire 的 LiveBoot 应用吗？"
    answer: "不需要。本模块是 Chainfire 原版 LiveBoot 技术的现代化独立移植版本，已将渲染二进制文件与配置解析器直接内嵌在模块中，无需任何第三方 APK。"
  - question: "如何修改文字颜色或日志过滤级别等 LiveBoot 设置？"
    answer: "直接编辑纯文本配置文件 `/data/adb/modules/livebootmagisk/config` 即可。切勿在文件中添加注释或多余的空行格式，因为精简的 Shell 解析器仅识别严格的键值对标记。"
---

## 概述

由 **symbuzzer** 维护（基于 **Chainfire** 的开创性作品重构）的 **LiveBoot** 模块，能够在 Android 设备开机阶段将常规品牌启动动画替换为类 Unix 风格的实时滚动控制台，同步输出 `logcat` 与内核 `dmesg` 缓冲区日志。

对于内核开发者、ROM 编译者及极客玩家而言，原厂开机动画会遮盖关键的底层初始化过程。LiveBoot 直接在物理屏幕上实时打印硬件初始化、分区挂载操作、守护进程启动以及 SELinux 拒绝记录（Denials），使其成为极具价值的开机排错诊断工具。

---

## 技术架构与工作原理

### SurfaceFlinger 原生帧缓冲渲染

LiveBoot 在 Android Zygote 完全初始化之前便已介入工作：

1. **早期启动加载**：在 `post-fs-data` 阶段由 `loader.sh` 触发执行，拉起专为直接对接 Android `surfaceflinger` 合成器而编译的底层原生守护进程。
2. **缓冲区多路复用**：实时捕获来自 `/dev/kmsg`（或 `dmesg`）以及 Android 日志套接字（`/dev/socket/logd`）的原始输出流。
3. **硬件屏幕输出**：按照日志严重级别（Verbose、Debug、Info、Warning、Error、Fatal）对每行日志进行格式化并着色渲染至帧缓冲区，直至系统触发 `sys.boot_completed` 信号后执行退出序列。

---

## 安装与启用

1. 下载最新版 `LiveBoot-v*.zip` 发行包。
2. 在 Magisk、KernelSU 或 APatch 中刷入该模块。
3. 重启设备，即可立即看到实时滚动的开机日志控制台输出。

---

## 配置与参数说明

通过编辑以下配置文件自定义显示行为：
```bash
/data/adb/modules/livebootmagisk/config
```

### 可配置选项
- **背景样式**：支持 `transparent`（透明）、`dark`（深色）或默认背景。
- **Logcat 缓冲区**：选择需要监听的日志缓冲区（`M` 代表 Main、`S` 代表 System、`R` 代表 Radio、`C` 代表 Crash）。
- **日志留存**：配置 `save` 参数即可将本次开机日志保存至 `/data/cache/liveboot.log`。
- **退出时机**：自定义以毫秒为单位的自毁延迟（suicide delay），确保动画与桌面启动器之间的平滑过渡。

---

## 故障排查与常见问题

- **开机过程全程黑屏**：部分定制 OEM ROM 实施了严格的 DRM 显存表面限制，阻止外部进程向主显示层绘图。若在桌面加载完成前屏幕始终黑屏，请确认当前 ROM 的兼容性。
