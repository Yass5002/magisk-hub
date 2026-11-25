---
id: "uperf-game-turbo"
title: "Uperf Game Turbo：用户态性能与调度控制器"
sidebarTitle: "Uperf Game Turbo"
description: "动态用户态性能守护进程，直接读取 Linux 原始触控事件并挂钩 SurfaceFlinger，实时调节 CPU/GPU 频率与 cpuset 线程亲和性。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Uperf Game Turbo Magisk 模块下载"
  - "Uperf Android 调度优化"
  - "Uperf powercfg.sh 均衡模式"
  - "yinwanxi Uperf Game Turbo"
  - "Android 用户态性能控制器"
prerequisites:
  - "Android 6.0 及以上系统"
  - "64 位架构（arm64-v8a）"
  - "Magisk 20.4+ 或用于手动部署的直接 Root Shell 访问权限"
  - "受支持的 SoC 硬件平台（已为常见高通、联发科、Exynos 与 Google Tensor 芯片预调校配置文件）"
conflicts:
  - "自动触控模拟或屏幕连点器应用（可能导致输入读取器出现触控上报丢帧）"
  - "开启 sfanalysis 时 MIUI 12 桌面可能无响应（解决方法：删除 `/data/adb/modules/uperf/enable_sfanalysis`）"
  - "存在冲突的第三方内核调频升频模块（应予以禁用，避免调度策略互相干扰）"
configPaths:
  - "/sdcard/Android/yc/uperf/cur_powermode.txt"
  - "/sdcard/Android/yc/uperf/uperf_log.txt"
  - "/data/powercfg.sh"
  - "/data/adb/modules/uperf/"
  - "/data/adb/modules/uperf/enable_sfanalysis"
features:
  - "直读 Linux 输入事件轮询：直接从内核输入子系统读取硬件触控原始信号，即时捕捉点击与滑动操作"
  - "SurfaceFlinger 帧率挂钩：通过 `sfanalysis` 钩子追踪渲染启动、卡顿与完成时间点，提前规避掉帧"
  - "动态线程迁移：滑动屏幕时自动将活跃的 UI 渲染线程绑定至大核或超大核"
  - "精细化功耗模式：支持在 `auto`、`balance`、`powersave`、`performance` 与 `fast` 模式间切换"
  - "Scene 工具箱联动：完全兼容 Scene 按应用独立切换性能配置"
faq:
  - question: "Uperf 会增加设备待机时的耗电量吗？"
    answer: "不会。Uperf 在设计上保持了极低的待机开销。在休眠状态下，其配置会减少后台定时唤醒所激活的 CPU 核心数，并采用更为保守的升频曲线，甚至能够略微改善待机续航。"
  - question: "在 MIUI 12 上遇到触屏无响应怎么办？"
    answer: "这是 MIUI 12 专属桌面与 SurfaceFlinger 钩子之间的已知兼容性问题。只需删除 `/data/adb/modules/uperf/enable_sfanalysis` 文件并重启设备即可解决。"
---

## 概述

**Uperf Game Turbo** 由 **yinwanxi** 基于 **Matt Yang** 的原版项目分叉并持续现代化重构，是一款面向 Android 的用户态调度器（Governor）与性能控制器。

原厂 Linux 内核调度器面对突发的用户交互往往响应滞后，容易导致应用冷启动或高负载游戏过程中出现微卡顿。Uperf 以智能的用户态场景识别替代了传统的被动式内核升频逻辑：通过直接监听原始触控输入事件、SurfaceFlinger 帧步调与 cpuset 状态切换，在负载攀升的瞬间精准拉高频率并绑定线程。

---

## 技术架构与工作原理

### 用户态遥测与 Sysfs 节点管理

Uperf 绕过 Android 上层框架，以极低延迟直接监测硬件负载：

1. **直连触控轮询**：直接从 `/dev/input/event*` 读取事件数据包。当检测到手指接触或滑动手势时，Uperf 会在 Android UI 渲染管线尚未请求新帧之前，立即指令 CPU 调度器提升主频。
2. **SurfaceFlinger 渲染分析（`sfanalysis`）**：挂钩 Android 的 `surfaceflinger` 合成器进程，追踪帧生成截止时间，一旦捕捉到渲染延迟或缓冲区阻塞便立刻调高 GPU 与 CPU 目标频率，避免掉帧。
3. **Cpuset 与线程亲和性优化**：自动将当前活跃应用的 UI 线程与渲染线程绑定至高性能或超大核簇（大核/超大核），同时将后台任务隔离到小核上运行。
4. **Sysfs 节点抽象**：针对不同 SoC 架构（骁龙、天玑、Google Tensor、Exynos）内置专属 JSON 配置文件，动态调控频点表、能量感知调度（EAS）参数与温控降频裕量。

---

## 安装与部署

### 方式一：Magisk / KernelSU / APatch
1. 下载最新的 `Uperf-Game-Turbo-*.zip` 发布包。
2. 通过你的 Root 管理器刷入模块并重启设备。
3. 重启完成后，查看 `/sdcard/Android/yc/uperf/uperf_log.txt`，确认守护进程已正常初始化并成功识别当前 SoC 平台。

### 方式二：独立 Shell 运行
Uperf 并不强制依赖 Magisk，同样适用于定制嵌入式环境或已获取 Root 权限的原厂系统：
1. 将压缩包解压至 `/data/uperf`。
2. 赋予脚本可执行权限（`chmod 755 *.sh`）。
3. 依次运行 `sh /data/uperf/setup_uperf.sh` 与 `sh /data/uperf/run_uperf.sh`。

---

## 配置与日常使用

### 功耗模式切换

Uperf 提供五种运行功耗配置：
- `auto`：依据当前前台应用负载需求动态调节性能释放。
- `balance`：在保证比原厂 OEM 调度更顺滑的前提下兼顾功耗控制。
- `powersave`：在维持基本界面流畅度的同时最大限度压低能耗。
- `performance`：采用激进的调频策略，专为高强度竞技游戏优化。
- `fast`：面向极限触控响应速度的高灵敏度配置方案。

#### 修改默认功耗模式
编辑以下路径的文本文件：
```bash
/sdcard/Android/yc/uperf/cur_powermode.txt
```
将其中的内容替换为目标模式（例如 `balance` 或 `auto`）后重启生效。

#### 实时动态切换模式
在 Root 终端中执行以下命令即可免重启切换模式：
```bash
sh /data/powercfg.sh balance
```
*（同样完全兼容 Scene / Omarea VTools，可实现分应用自动切换调度模式）。*

---

## 故障排查与常见问题

- **MIUI 12 触屏锁死无响应**：若 MIUI 12 设备桌面出现触控失效，请删除 `/data/adb/modules/uperf/enable_sfanalysis` 并重启，以禁用 SurfaceFlinger 钩子并保留其余用户态调度功能。
- **硬件平台不受支持**：若安装时提示 `unsupported` 平台警告而中止，说明你的设备 SoC 在 `/data/uperf/config/` 目录下尚无预编译的 JSON 配置文件。
