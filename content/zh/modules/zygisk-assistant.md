---
id: "zygisk-assistant"
title: "Zygisk Assistant：开源防检测与沙盒 Root 隐匿模块"
sidebarTitle: "Zygisk Assistant"
description: "专注于隐藏 Root 二进制文件、调试标志与挂载点的开源 Zygisk 模块，有效应对严苛的银行与金融风控框架检测。"
category: "root-management"
tier: 1
searchQueries:
  - "zygisk assistant 下载"
  - "zygisk assistant 对比 shamiko"
  - "银行 app 如何隐藏 root"
  - "开源 root 隐藏模块"
  - "zygisk assistant 配置教程"
prerequisites:
  - "Magisk 26.0+（开启 Zygisk）、KernelSU 或搭配 Zygisk Next 的 APatch"
conflicts:
  - "其他同时挂钩相同 libc 卸载跳板（unmount trampoline）且缺乏协同机制的模块"
configPaths:
  - "/data/adb/zygisk_assistant/config.json"
  - "/data/adb/modules/zygisk-assistant/"
features:
  - "100% 完全开源，可替代闭源的商业或私有 Root 隐藏模块"
  - "对文件系统扫描隐藏 `/system/bin/su`、`/system/xbin/su` 与 `/data/adb`"
  - "屏蔽异常进程环境变量与 `ptrace` 调试属性"
  - "直接联动 Magisk DenyList，无需编写复杂的白名单配置文件"
faq:
  - question: "Zygisk Assistant 与 Shamiko 有何区别？"
    answer: "Shamiko 由 LSPosed 团队开发且为闭源专有模块，其二进制文件经过了高强度混淆。而 Zygisk Assistant 完全 100% 开源，允许安全研究人员与隐私关注者审计在高权限下运行的每一行代码。"
  - question: "在 Magisk 中需要开启“遵守排除列表”（Enforce DenyList）吗？"
    answer: "请遵循对应版本的说明：Zygisk Assistant 会读取你在 DenyList（排除列表）中勾选的应用，但通常在 Magisk 中将“遵守排除列表”设为关闭（OFF）时效果最佳，这样才能保留 Zygisk 挂钩以执行动态卸载隐藏操作。"
---

## 概述

由 **snake-4** 开发的 **Zygisk Assistant** 旨在为已 Root 的 Android 设备提供一款现代、完全开源且可审计的 Root 隐藏伴侣模块。

随着企业级与银行风控安全套件（如 Promon SHIELD、AppSealing 与 ThreatMetrix）开始针对已知的闭源隐藏工具进行特征扫描，社区对透明、可审计的 Zygisk 模块需求日益增长。Zygisk Assistant 通过拦截文件系统、挂载表与系统环境查询，在无需黑盒闭源二进制组件的情况下提供稳健的 Root 隐匿能力。

---

## 技术架构与工作原理

### 用户态系统调用与 C 库拦截

1. **Zygote Fork 挂钩**：当沙盒应用从 Zygote 进程 Fork 启动时，Zygisk Assistant 会检查目标包名是否已被配置为需要隐藏。
2. **挂载表清理**：模块会拦截访问 `/proc/mounts`、`/proc/self/mountinfo` 与 `/proc/self/mountstats` 的 `read` 与 `fopen` 调用，动态过滤掉所有 Loop 挂载记录、Magisk 镜像目录及 OverlayFS 标识。
3. **系统属性伪装**：拦截与开发和调试相关的 Android 属性查询：
   - `ro.debuggable`：强制返回 `0`
   - `ro.secure`：强制返回 `1`
   - `ro.build.type`：强制返回 `user`
   - `persist.sys.usb.config`：移除 `adb` 字样
4. **二进制路径隐匿**：针对 `/system/bin/su`、`/data/adb/` 或 Root 管理器包名的文件系统查询请求会被重定向，直接返回标准的“文件不存在”错误码（`ENOENT`）。

---

## 安装与配置

1. 打开你的 Root 管理器（**Magisk**、**KernelSU** 或 **APatch**）。
2. 下载并刷入最新的 `Zygisk-Assistant-vX.zip`。
3. 在 Magisk 中前往 **设置** → **配置排除列表（Configure DenyList）** → 勾选需要对其隐藏 Root 权限的应用。
4. 确保关闭 **遵守排除列表（Enforce DenyList）** 开关（以便 Zygisk Assistant 能将伴侣库注入目标进程）。
5. 重启设备。
