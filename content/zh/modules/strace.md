---
id: "strace"
title: "Strace：在已 Root 的 Android 设备上进行系统调用追踪"
sidebarTitle: "Strace"
description: "通过 Magisk 以无系统分区修改（Systemless）方式安装 strace 诊断工具。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "strace magisk 模块下载"
  - "evdenis strace 安卓"
  - "安卓 Root 系统调用追踪"
  - "strace v6.19 android 编译版"
prerequisites:
  - "已通过 Magisk 获取 Root 权限的 Android 设备"
  - "具备执行已安装二进制文件权限的 Shell 或终端环境"
  - "支持发布包所提供的 ARM64、ARM、x86_64 或 x86 架构之一"
conflicts:
  - "上游文档未记录已知模块冲突；但启用追踪仍会给目标进程带来额外性能开销。"
configPaths:
  - "/system/bin/strace"
features:
  - "通过无系统分区修改（Systemless）的 Magisk 挂载层安装 strace v6.19"
  - "内置适用于 ARM64、ARM、x86_64 与 x86 架构的预编译二进制文件"
  - "安装模块时自动根据设备架构选择对应二进制文件"
faq:
  - question: "该模块会安装什么内容？"
    answer: "上游发布包内置了静态链接且经过 strip 精简的 strace v6.19 二进制文件，安装时会通过 Magisk 的 Systemless 挂载机制将匹配当前设备架构的可执行文件部署至 /system/bin/strace。"
  - question: "为什么安装时提示不支持的架构并中止？"
    answer: "发布包仅包含 ARM64、ARM、x86_64 与 x86 目录。当 Magisk 上报的设备架构没有对应的预编译二进制文件时，安装脚本会主动中止。"
  - question: "模块会自动追踪应用吗？"
    answer: "不会。该模块仅负责安装 strace 命令行工具。你需要自行在具有 Root 权限的 Shell 中指定目标进程及追踪参数；请注意，追踪过程可能产生大量日志输出与运行时开销。"
  - question: "如何卸载该模块？"
    answer: "在 Magisk 模块管理器中禁用或移除 Strace，随后按 Magisk 提示重启设备即可。"
---

## 概述

Strace 是一款用于记录进程所执行的系统调用（System Call）与接收信号的系统诊断工具。`evdenis/strace` 项目将 strace v6.19 打包为 Magisk 模块，无需直接修改只读的 Android 系统分区即可部署使用。

发布包 ZIP 内分别提供了面向 `arm64`、`arm`、`x86_64` 与 `x86` 的预编译二进制文件。安装脚本 `customize.sh` 会依据 Magisk 上报的设备架构选择对应目录；若无匹配文件，则会中止安装。

## 安装与验证

1. 从上游发布页下载最新的 `strace-v2.zip`。
2. 在 Magisk 中打开 **模块**，选择 **从本地安装** 并选中该 ZIP 压缩包。
3. 根据 Magisk 提示重启设备。
4. 在具备 Root 权限的 Shell 中验证命令是否就绪：

   ```sh
   su -c 'command -v strace && strace -V'
   ```

上游模块通过 Magisk 的无系统分区修改（Systemless）挂载层将命令安装至 `/system/bin/strace`。项目并未声明支持 KernelSU 或 APatch，因此本指南仅列出 Magisk 兼容性。

## 安全使用建议

建议先从生命周期较短的命令开始测试，并将输出重定向至可写目录：

```sh
su -c 'strace -f -o /data/local/tmp/trace.log -- ls /data'
```

追踪长期运行或频繁发起系统调用的进程会生成体积庞大的日志文件，并可能影响目标进程的时序行为。切勿仅凭追踪日志断定某个进程是否安全或存在恶意行为，应结合应用程序自身逻辑及 Android 权限模型综合研判。

## 局限性与异常恢复

该模块仅定位为二进制分发打包项目，而非完整的 Android 系统调用追踪教程。上游 README 提供了 strace 官方项目及 XDA 讨论帖链接供进阶参考，但未声明具体的 Android 版本兼容矩阵。

若模块导致设备无法正常开机或管理器异常，可通过 Magisk 的安全模式（Safe Mode）恢复，或在兼容的第三方 Recovery 环境中手动删除该模块目录。模块本身仅提供可执行文件，不包含任何驻留后台的守护进程。

## 参考来源

- [上游 README](https://github.com/evdenis/strace)
- [上游发布页](https://github.com/evdenis/strace/releases/tag/v2)
- [上游源码仓库](https://github.com/evdenis/strace)
