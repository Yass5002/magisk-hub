---
id: "fas-rs"
title: "FAS-RS：基于 Rust 编写的 Android 帧感知调度守护进程"
sidebarTitle: "FAS-RS"
description: "由 shadow3aaa 使用 Rust 编写的用户态性能守护进程，依据实际帧渲染延迟动态升降 CPU/GPU 频率，实现稳帧与控温平衡。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "FAS-RS Magisk 模块"
  - "Android 帧感知调度下载"
  - "shadow3aaa fas-rs 下载"
  - "fas-rs games.toml 配置方法"
  - "安卓游戏稳帧降功耗 Root 模块"
prerequisites:
  - "Android 9.0（Pie）及以上系统"
  - "通过 KernelSU、APatch 或 Magisk 获取 Root 权限"
  - "支持调频驱动的多核 SoC（高通骁龙、联发科天玑、Google Tensor）"
conflicts:
  - "静态锁频或接管 cpufreq 的性能模块（如 Uperf、Scene 性能模式等会覆盖调度策略的工具）"
  - "会篡改 SurfaceFlinger 缓冲队列的激进厂商游戏助手"
configPaths:
  - "/sdcard/Android/fas-rs/games.toml"
  - "/data/adb/modules/fas-rs/"
features:
  - "SurfaceFlinger 帧耗时监控：直接从 Android 图形合成器采样渲染延迟"
  - "动态余量调度器：按 60/90/120 FPS 目标精细分配硬件算力，在稳帧的同时压低整机功耗"
  - "分游戏 TOML 配置：支持按应用包名自定义目标刷新率与性能档位"
  - "无需修改内核：完全运行于用户态，拥有极佳的跨平台 SoC 兼容性"
faq:
  - question: "FAS-RS 与传统的 schedutil 或 performance 调度器有何区别？"
    answer: "标准 Linux 调度器依据 CPU 负载百分比调节频率，无法感知画面是否真正流畅。例如部分优化欠佳的游戏可能在一个低效线程上跑满 100% CPU 占用，但画面早已稳定在 60 FPS，继续高频运行只会白白发热。FAS-RS 直接测量每一帧画面的实际渲染耗时：若帧输出在显示刷新周期预算内（如 60Hz 对应 16.6ms）保有充足余量，便会温和降频以减少发热。"
  - question: "FAS-RS 可以和 Scene 或 Uperf 同时使用吗？"
    answer: "不可以。运行 FAS-RS 前请关闭 Scene 中的性能调度脚本或卸载 Uperf。如果其他模块强制锁定 CPU 最高频率或接管了调度器策略，将会直接干扰 FAS-RS 的动态帧耗时计算。"
  - question: "如何为指定游戏单独配置目标 FPS？"
    answer: "使用任意文本编辑器打开 `/sdcard/Android/fas-rs/games.toml`，在 `[game]` 配置段下添加应用包名与目标帧率，例如：`\"com.miHoYo.GenshinImpact\" = 60`。保存文件后，FAS-RS 会自动热重载规则，无需重启手机。"
---

## 概述

传统移动端 CPU 调度器（如 `schedutil`、`interactive` 和 `ondemand`）仅依赖运行队列负载和任务等待时间来决定处理器频率。尽管这套机制在日常通用计算中行之有效，但在手游与重度图形渲染场景下却存在明显缺陷：

1. **功耗浪费**：游戏线程中的忙等待（Busy-Wait）循环可能让某个 CPU 核心占用率飙至 100%，诱使传统调度器拉满最高频率——此时画面其实早已稳定在 60 FPS，盲目升频只会徒增发热并加速触发温控。
2. **温控降频**：不必要的高频爆发会提前撞上设备温控墙，导致频率骤降和剧烈掉帧。
3. **瞬间卡顿**：相反，当复杂战斗或特效场景突然到来时，传统调度器往往反应滞后，无法及时提供满足帧截止时间所需的算力突发。

由 shadow3aaa 开发的 **FAS-RS**（Frame Aware Scheduling in Rust）彻底颠覆了这一思路。它不再依赖内核负载启发式猜测性能需求，而是从用户视角出发，直接监测 Android 图形合成器（**SurfaceFlinger**），判断每一帧是否按时送达屏幕。

---

## 技术架构与工作机制

FAS-RS 作为一个使用 Rust 编写的独立守护进程，以 Root 权限在后台运行：

```
┌────────────────────────────────────────────────────────┐
│                   Android 显示屏幕                      │
│              (例如 120Hz 目标周期 = 8.33ms)             │
└───────────────────────────▲────────────────────────────┘
                            │ 输出显示帧
┌───────────────────────────┴────────────────────────────┐
│                    SurfaceFlinger                      │
│  - 采集帧提交与 VSYNC 同步时间戳                         │
└───────────────────────────┬────────────────────────────┘
                            │ 实时帧延迟指标
┌───────────────────────────▼────────────────────────────┐
│                     fas-rs 守护进程                     │
│  - 计算帧交付时间余量：                                  │
│    * 若帧渲染 < 6.0ms：温和降频（降低发热）              │
│    * 若帧渲染 > 8.0ms：瞬时提频补充算力余量              │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│             内核 cpufreq 与 devfreq 节点                │
│  /sys/devices/system/cpu/cpufreq/policy*/              │
└────────────────────────────────────────────────────────┘
```

1. **指标采集**：FAS-RS 挂载读取 SurfaceFlinger 的缓冲队列与时间戳统计数据，精确计算 CPU 与 GPU 渲染每一帧所消耗的微秒级时长。
2. **余量计算**：当帧渲染大幅提前于 VSYNC 截止时间完成（余量充足）时，FAS-RS 会适当降低 CPU 与 GPU 频率档位。
3. **零抖动响应**：一旦帧渲染耗时逼近截止阈值，FAS-RS 会瞬间拉升频率，确保不发生掉帧卡顿。

---

## 安装与配置

### 前置要求
- KernelSU、APatch 或 Magisk。
- Android 9 及以上系统。

### 安装步骤
1. 从官方 GitHub 发布页下载 `fas-rs.zip`。
2. 在你的 Root 管理器（Magisk、KernelSU 或 APatch）中刷入该模块。
3. 重启设备。
4. 守护进程将在开机后自动初始化，并在 `/sdcard/Android/fas-rs/` 目录下生成默认配置文件。

---

## 配置文件说明：`games.toml`

FAS-RS 从 `/sdcard/Android/fas-rs/games.toml` 读取分游戏调优规则：

```toml
# 默认全局配置
[config]
mode = "balance" # 可选档位："powersave"、"balance"、"performance"、"fast"

# 各游戏包名对应的目标帧率
[game]
"com.miHoYo.GenshinImpact" = 60
"com.activision.callofduty.shooter" = 120
"com.pubg.imobile" = 90
```

- 启动列表中的应用时，FAS-RS 会自动接管调度。
- 退出应用后，FAS-RS 会立即释放频率限制，恢复系统默认调度状态。

---

## 故障排查与状态验证

### 检查守护进程运行状态
打开任意具备 Root 权限的终端模拟器执行：
```bash
su
# 检查运行中的进程：
ps -ef | grep fas-rs

# 查看实时运行日志：
cat /sdcard/Android/fas-rs/fas_log.txt
```

### 模块冲突排查
如果遇到偶发微卡顿或异常掉帧：
- 确认没有其他性能调度模块（如 Uperf、Scene 性能服务、温控修改模块）正在强行接管调频策略。
- 关闭会限制后台线程执行的激进省电类应用。

### 紧急卸载
```bash
rm -rf /data/adb/modules/fas-rs
rm -rf /sdcard/Android/fas-rs
reboot
```
