---
id: "magisk-frida"
title: "Magisk-Frida：无系统分区 Frida Server 动态插桩模块"
sidebarTitle: "Magisk-Frida"
description: "自动打包并无系统运行官方 frida-server 守护进程的通用模块，支持 ARM/ARM64/x86/x86_64 架构识别、Action 一键启停与自定义监听端口。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "Magisk-Frida 模块下载"
  - "Android frida-server 开机自启"
  - "ViRb3 MagiskFrida 教程"
  - "KernelSU APatch Frida 配置"
  - "Android 应用动态分析插桩"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "电脑端已安装与模块 Frida 版本一致的 Python 与 `frida-tools`"
conflicts:
  - "手动在后台运行并占用 27042 端口的其他 `frida-server` 实例"
configPaths:
  - "/data/adb/modules/magisk-frida/"
  - "/data/adb/modules/magisk-frida/bin/frida-server"
  - "/data/adb/modules/magisk-frida/port"
  - "/data/adb/modules/magisk-frida/logs/"
features:
  - "紧跟官方上游版本：与 Frida 官方构建流程同步发布（当前 `17.27.5-1`）"
  - "全架构通用刷机包：单包内含 `arm`、`arm64`、`x86` 与 `x86_64` 官方 `frida-server` 二进制"
  - "Action 一键启停控制：无需重启手机，在 Root 管理器点击 Action 即可即时启动或终止 `frida-server`"
  - "实时运行状态回写：自动检测进程存活状态并更新 `module.prop` 描述（`active` / `failed`）"
  - "可选自定义本地端口：支持在模块 `port` 文件中指定端口（`1–65535`）绑定至 `127.0.0.1:<port>`"
faq:
  - question: "如何从电脑连接手机上的 Frida？"
    answer: "在手机开启 USB 调试并连接电脑，确保 PC 端 `frida-tools` 主次版本与手机端模块版本一致，然后在终端执行 `frida-ps -U` 即可列出当前运行中的进程。"
  - question: "平时不用时可以临时关闭 `frida-server` 吗？"
    answer: "可以。在 Magisk、KernelSU 或 APatch 中点击该模块的 **Action** 按钮，`action.sh` 会通过 `pgrep` 判断状态并一键停止或重新拉起 `frida-server`。"
  - question: "银行或高安全应用会检测到 `frida-server` 吗？"
    answer: "会的。官方标准 `frida-server` 默认监听 27042 端口且存在明显特征字符串与线程名。日常不用时建议通过 Action 停止服务；若需分析强对抗应用，可配合隐藏手段或使用 ZygiskFrida。"
---

## 概述

由 **ViRb3**（与 enovella 联合维护）发布的 **Magisk-Frida**（`17.27.5-1`）是面向 Android 安全研究员、渗透测试人员及逆向工程师的经典动态插桩辅助模块。

手动运行 `frida-server` 通常需要反复通过 ADB 推送对应架构的二进制至 `/data/local/tmp/`、赋予可执行权限并在交互式 Shell 中后台挂起。Magisk-Frida 将官方四种架构的 `frida-server` 封装进无系统模块（显式设置 `SKIPMOUNT=true` 以兼容 Magisk、KernelSU 与 APatch），在系统启动完成后自动以守护进程运行，并提供 Action 按钮即时启停。

---

## 技术架构与工作原理

### 守护进程启动与控制流程

1. **自动架构识别（`customize.sh`）**：安装时检测设备 ABI（`arm`、`arm64`、`x86`、`x86_64`），提取对应的 `frida-server` 至 `/data/adb/modules/magisk-frida/bin/frida-server`，同时生成 `skip_mount` 标记，不向 `/system` 挂载任何文件。
2. **延迟启动服务（`service.sh` + `utils.sh`）**：等待 `sys.boot_completed=1` 后读取可选的 `/data/adb/modules/magisk-frida/port` 文件，随后执行 `"$FRIDA_BIN" -D`（若配置了合法端口 `1–65535`，则附加 `-l 127.0.0.1:<PORT>` 参数）。
3. **状态校验与日志留存**：`check_frida_is_up` 通过 `busybox pgrep 'frida-server'` 检查进程状态并动态更新 `module.prop` 描述（`✅ (active)` 或 `❌ (failed)`），运行日志保存在 `/data/adb/modules/magisk-frida/logs/`（含 `service.log`、`action.log` 与 `utils.log`）。

---

## 安装与快速上手

### 第一步：刷入模块
1. 从 `ViRb3/magisk-frida` 下载 `MagiskFrida-17.27.5-1.zip`。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入该模块并重启设备。

### 第二步：工作站连接测试
1. 在电脑端安装与模块版本匹配的 `frida-tools`：
   ```bash
   pip install frida-tools
   ```
2. 通过 USB 连接设备（确保已开启 ADB 调试），验证进程列表：
   ```bash
   frida-ps -U
   ```
3. 注入脚本调试目标应用：
   ```bash
   frida -U -f com.example.targetapp -l hook.js
   ```

---

## 进阶配置与排查

- **自定义监听端口**：如需让 `frida-server` 仅监听 `127.0.0.1:<PORT>`，可将端口号（`1–65535`）写入 `/data/adb/modules/magisk-frida/port`，随后点击 **Action** 重启服务或重启设备。
- **版本不匹配报错**：若 `frida-ps -U` 提示协议或版本不兼容，请核对当前模块版本（`17.27.5-1`），并在电脑端同步升级或锁定对应的 `frida` 版本（`17.27.5`）。
- **Action 一键开关**：需要临时关闭端口避免风控探测或重新启动服务时，直接点击管理器中的 **Action** 按钮即可即时生效。
