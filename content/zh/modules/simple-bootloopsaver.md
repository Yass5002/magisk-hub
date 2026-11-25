---
id: "simple-bootloopsaver"
title: "Simple Bootloop Saver：Magisk Zygote 崩溃循环自动检测与救砖模块"
sidebarTitle: "Simple Bootloop Saver"
description: "在系统启动后期监测 Android Zygote 进程 PID 稳定性，一旦检测到处于加密存储环境下的模块引发 Bootloop 无限重启循环，自动禁用全部已安装模块并重启手机。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Simple Bootloop Saver Magisk 模块"
  - "ez-me Simple_BootloopSaver 下载"
  - "Magisk 加密分区防卡米救砖模块"
  - "Zygote 崩溃无限重启自动禁用模块"
  - "HuskyDG 轻量防变砖模块"
prerequisites:
  - "Magisk v20.4 或更高版本"
  - "已加密或未加密的 /data 分区（兼容文件级加密 FBE）"
  - "需要防范因刷入模块导致无法开机的设备"
conflicts: []
configPaths:
  - "/data/adb/modules/simple_bootloopsaver/"
  - "/data/adb/modules/*/disable"
features:
  - "加密存储无忧救砖：无需通过第三方 Recovery（TWRP/OrangeFox）解密访问 /data/adb/modules 即可完成系统自救"
  - "无侵入式 Zygote 轮询：在 late_start 阶段以 15 秒为间隔监测 Zygote 进程标识符"
  - "启发式崩溃确认：要求连续多次检测到 PID 变化才触发防御机制，有效避免启动瞬间的误判"
  - "故障自动解除：自动为所有已激活模块写入 disable 禁用标记，随后重启进入纯净的原厂用户空间"
---

## 概述

尝试各种 Magisk 模块时，最大的风险莫过于遭遇开机无限重启（Bootloop / 卡米）。现代 Android 设备普遍强制启用了文件级加密（FBE），一旦新刷入的模块导致 system_server 或 Zygote 进程崩溃，第三方 Recovery（如 TWRP 或 OrangeFox）往往无法在不开机解锁的情况下解密用户存储，没有可用 Recovery 的用户甚至只能被迫恢复出厂设置并丢失全部数据。

**Simple Bootloop Saver** 源自 HuskyDG 的早期技术研究，并由 ez-me 精简为极致轻量的单脚本守护方案，扮演着系统自救看门狗的角色。它在系统启动后期静默运行，持续追踪 Android Zygote 进程的运行稳定性。一旦发现 Zygote 陷入崩溃重启死循环，模块会立即介入，自动禁用所有已安装模块并触发安全重启。

## 看门狗检测原理

由框架修改模块、错误叠加层或冲突 Zygisk 二进制组件引发的 Bootloop，几乎都会表现为 32 位或 64 位 Zygote 守护进程的反复崩溃。

该模块的具体工作流程如下：

1. **后期启动执行**：看门狗脚本在 Magisk 的 `late_start` 服务阶段（基础文件系统挂载完成后）作为后台任务启动。
2. **PID 采样记录**：查询并记录主 `zygote` 守护进程的进程号（PID）。
3. **多轮状态校验**：
   - 脚本以 15 秒为间隔，连续三次检查 Zygote 的 PID。
   - 若两次检查之间的 PID 发生变化，说明 Zygote 发生了崩溃并被 `init` 进程重新拉起。
   - 为避免开机初期部分系统服务正常重启引发误判，脚本还会额外等待一个 15 秒窗口进行第四次确认检测。
4. **自动执行救砖**：
   - 一旦确认为 Zygote PID 持续异常，脚本会在 `/data/adb/modules/` 下的每个模块目录中写入 `disable` 禁用标记文件。
   - 紧接着执行系统重启命令（`/system/bin/reboot`）。
5. **纯净恢复进入系统**：手机将在禁用所有模块的状态下正常启动进入 Android 桌面，随后即可打开 Magisk 定位并卸载引发故障的模块。

## 安装与部署

1. 从官方仓库下载 `simple_bootloopsaver` 的 `.zip` 安装包。
2. 通过 **Magisk** 应用刷入该模块。
3. 重启设备以完成安装生效。
4. 此后每次开机时，看门狗都会在后台自动守护系统启动过程。

## 触发救砖后如何重新启用模块

当某个异常模块触发故障保护并禁用全部模块后：

1. 设备会安全重启并正常进入锁屏界面。
2. 打开 **Magisk** 应用并切换至 **模块** 标签页。
3. 此时所有模块均显示为已关闭状态。
4. 找到并移除导致本次启动崩溃的问题模块。
5. 逐一重新启用你信任的正常模块，每开启一个后重启验证系统稳定性即可。
