---
id: "xtreme-bs"
title: "Xtreme Battery Saver：事件驱动型 Root 电源控制模块"
sidebarTitle: "Xtreme Battery Saver"
description: "在已获取 Root 权限的 Android 设备上，以事件驱动方式精细管控 CPU、应用行为、Wi-Fi、Doze 与后台进程功耗。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Xtreme Battery Saver Magisk 模块"
  - "DethByte64 XtremeBS 下载"
  - "Android Root 事件驱动省电模块"
  - "XBSctl Magisk 命令行"
  - "XtremeBS WebUI 配置"
prerequisites:
  - "已通过 Magisk 或 KernelSU 获取 Root 权限的 Android 设备"
  - "适合用于测试系统电源管理策略变更的设备与 ROM 环境"
  - "具备 ADB 或 Recovery 环境，以便在错误配置导致异常时及时恢复"
  - "调整激进省电选项前请先备份 XtremeBS 配置文件"
conflicts:
  - "同时修改相同 CPU、应用策略、Doze、Wi-Fi 或进程参数的其他省电或性能模块"
  - "在未将关键应用加入白名单的情况下启用 `disable_cores`、`low_ram`、`doze` 或应用冻结等激进选项"
configPaths:
  - "/data/local/tmp/XtremeBS/XtremeBS.conf"
  - "/data/local/tmp/XtremeBS/XtremeBS.status"
  - "/sdcard/XtremeBS.log"
  - "/data/adb/modules/XtremeBS/"
features:
  - "事件驱动 v2 配置架构：支持针对 `boot`、`charging`、`screen_off`、`low_power`、`manual` 及自定义事件分别设定策略"
  - "CPU 核心与调度器控制：支持核心开关调整以及可定制的应用与进程处理机制"
  - "Doze、Wi-Fi、低内存（low-RAM）与 Google 移动服务（GMS）精细管控"
  - "提供 `XBSctl` 命令行工具，支持配置重载、暂停、恢复及安全模式等指令"
  - "上游 v1.0.6+ 文档提供可选的本地 WebUI 面板（监听 8081 端口）"
faq:
  - question: "XtremeBS 是开箱即用的模块吗？"
    answer: "不是。上游 README 明确将其定位为面向高阶用户的可配置模块。建议从默认配置起步，每次仅启用一项改动并观察效果，切勿直接开启激进选项。"
  - question: "设备出现卡顿或不稳定时该如何恢复？"
    answer: "若 ADB 仍可连接，请使用上游提供的安全模式命令 `adb shell XBSctl safe`。上游 README 还说明可在 Recovery 中修改配置文件添加 `safemode=1`，随后禁用风险选项并恢复先前的正常配置。"
  - question: "哪些配置项存在较高风险？"
    answer: "上游文档特别提示需谨慎使用 `disable_cores`、`low_ram`、`doze`、应用挂起（app suspension）、进程优先级重排以及禁用 Wi-Fi 等选项。此外明确建议三星设备避开 `disable_cores` 和 `handle_cores`，一加设备避开 `low_ram`。"
  - question: "修改配置后如何使其生效？"
    answer: "编辑配置文件后执行 `XBSctl reload` 或重启设备即可生效。使用 v2 格式时请核对事件名称与代码块语法；若使用 v1 格式，则沿用传统的 `key=value` 写法。"
  - question: "XtremeBS 能否保证固定的续航提升幅度？"
    answer: "不能。上游页面虽然提到有望延长续航，但也明确指出实际效果因机型与配置而异。Magisk Hub 不对具体续航提升作任何保证。"
---

## 概述

**Xtreme Battery Saver（XtremeBS）** 是一款高度可配置的 Root 电源管理模块，其文档记录的可控范围涵盖 CPU 核心、应用管控、进程优先级、Doze 休眠、Wi-Fi、低内存模式（low-RAM）以及 Google 移动服务（GMS）。根据上游 README 说明，该模块同时兼容 Magisk 与 KernelSU。

请注意，这是一款面向深度调校的激进省电工具，而非通用的“一键省电”方案。上游项目明确警告：不当的配置可能导致系统卡顿、通知或闹钟漏响、SystemUI 崩溃甚至系统不稳定。兼容性因设备与 ROM 而异，开发者注明其主要测试环境为运行 ProtonAOSP 的 Pixel 5。

## 安装步骤

1. 下载最新版本的 `XtremeBS.zip` 安装包。
2. 通过 Magisk 或 KernelSU 刷入模块。
3. 重启设备。
4. 在启用任何非默认策略前，先检查模块生成的初始配置文件。

模块会在 Android 启动完成后的 `late-start service` 阶段拉起守护进程。发行包内同时附带了 `XBSctl` 命令行实用工具以及可选的 WebUI 启动脚本。

## 配置说明

配置文件路径如下：

```text
/data/local/tmp/XtremeBS/XtremeBS.conf
```

上游项目支持两种配置格式：

- **v1**：由单一触发条件控制的传统 `key=value` 键值配置。
- **v2**：推荐使用的事件块结构，支持 `boot`、`charging`、`screen_off`、`low_power`、`manual` 以及自定义事件。

以下为上游文档给出的最小化 v2 配置示例：

```text
version=2
delay=3
log_file=/sdcard/XtremeBS.log
log_level=3

screen_off={
  handle_apps=nice
}
```

编辑完成后执行重载使配置立即生效：

```sh
su -c XBSctl reload
```

自定义事件可通过命令手动触发：

```sh
su -c "XBSctl start my_event"
```

上游文档指出多个事件块之间存在叠加效应，因此若规则作用范围有所重叠，需提前统筹规划。

## 控制项与安全须知

影响最为显著的核心控制项包括：

- `disable_cores`：关闭指定或由系统自动挑选的 CPU 核心。
- `handle_apps`：对应用执行查杀、降低优先级或挂起休眠操作。
- `handle_proc`：调整进程优先级，可能会延迟后台任务执行。
- `doze`：强制进入轻度或深度 Doze 模式，可能影响定时闹钟触发。
- `kill_wifi`：直接关闭 Wi-Fi。
- `low_ram`：启用 Android 低内存特性。
- `handle_gms`：调控 Google 服务；若强行查杀 GMS，可能导致 Google 系应用异常及 Play Integrity 认证失败。

启用应用挂起功能时务必配合白名单使用，测试前请先将输入法与终端等关键应用加入白名单。建议每次只调整一项参数、充分观察设备表现，并始终保留可行的应急恢复手段。

## WebUI 与日志查看

上游 README 记载 v1.0.6+ 版本内置了 WebUI，可通过模块动作脚本启动，访问地址为：

```text
http://127.0.0.1:8081
```

状态文件与日志文件的默认存放位置为：

```text
/data/local/tmp/XtremeBS/XtremeBS.status
/sdcard/XtremeBS.log
```

排查行为异常时可适当调高 `log_level` 等级，定位问题后再调回较低级别以减少日志写入。

## 恢复与故障排查

若设备仍可通过 ADB 响应指令，请执行：

```sh
adb shell XBSctl safe
```

按上游说明，该命令会停止 XtremeBS 运行并解除所有已挂起应用的限制。若 ADB 已无法连接，上游 README 建议重启进入 Recovery，在 `/data/local/tmp/XtremeBS/XtremeBS.conf` 中写入 `safemode=1` 后再次重启。

上游针对特定品牌的注意事项：

- **三星（Samsung）设备**：避免使用 `disable_cores` 与 `handle_cores`。
- **一加（OnePlus）设备**：避免开启 `low_ram`。
- **模块互斥**：禁用或协调其他省电/性能模块中功能重叠的选项。

## 参考来源

- [上游 README](https://github.com/DethByte64/Xtreme-Battery-Saver)
- [上游 Releases 发布页](https://github.com/DethByte64/Xtreme-Battery-Saver/releases)
- [上游源码仓库](https://github.com/DethByte64/Xtreme-Battery-Saver)
