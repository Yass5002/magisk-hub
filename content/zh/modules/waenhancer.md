---
id: "waenhancer"
title: "WaEnhancer：基于 LSPosed 的 WhatsApp 隐私增强、防撤回与主题定制模块"
sidebarTitle: "WaEnhancer"
description: "基于 YukiHookAPI 与 DexKit 构建的 WhatsApp 开源 Xposed 模块（com.wmods.wppenhacer），在不篡改原版安装包的前提下于内存中注入隐私隐藏、消息防撤回与 CSS 主题定制功能。"
category: "xposed-runtime-hooks"
tier: 1
searchQueries:
  - "WaEnhancer 下载安装"
  - "WhatsApp LSPosed 增强模块"
  - "WhatsApp 消息防撤回模块"
  - "WhatsApp 隐藏已读蓝勾与输入状态"
  - "WaEnhancer 怎么配置"
prerequisites:
  - "已激活官方 LSPosed（支持 libxposed API 101）的 Magisk、KernelSU 或 APatch 设备"
  - "已安装官方原版 WhatsApp（`com.whatsapp`）或 WhatsApp Business（`com.whatsapp.w4b`）"
conflicts:
  - "第三方魔改/重打包版 WhatsApp（WaEnhancer 仅对官方正版在内存层注入，切勿与篡改版客户端混用）"
  - "其他同时 Hook 相同 WhatsApp 混淆方法的 Xposed 模块"
configPaths:
  - "/data/adb/lspd/"
  - "/data/data/com.wmods.wppenhacer/"
features:
  - "基于 YukiHookAPI 1.5.0 与原生 `libdexkit.so`（支持 arm64-v8a 与 armeabi-v7a）动态解析字节码，兼容 WhatsApp 版本迭代"
  - "全维度隐私控制：支持冻结最后上线时间、隐藏状态查看、隐藏已读蓝勾、隐藏送达回执、隐藏正在输入与语音录制状态，以及回复时才发送蓝勾"
  - "消息与媒体留存：支持消息防撤回、动态/状态防撤回、查看已编辑消息历史记录、解除阅后即焚限制并隐藏阅后即焚与语音已听回执"
  - "聊天与转发增强：支持隐藏转发标签、移除转发人数限制、解除置顶会话上限、移除长消息折叠按钮以及对所有消息执行双方删除"
  - "内置可视化 CSS 主题编辑器（`assets/css_editor.html`）与通话录音配置页面（`CallRecordingSettingsActivity`），全程不修改原版 APK 文件"
faq:
  - question: "WaEnhancer 会提供修改版的 WhatsApp 安装包吗？"
    answer: "不会。`Dev4Mod/WaEnhancer` 官方免责声明明确指出，仓库不包含任何 WhatsApp 或 Meta 专有代码，也不分发任何修改版 WhatsApp APK。它本身是一个纯正的 Xposed 模块（`com.wmods.wppenhacer`），仅通过框架在设备内存中动态挂钩官方客户端。"
  - question: "使用 WaEnhancer 是否存在封号风险？"
    answer: "存在。上游项目明确警告：通过客户端 Hook 改变 WhatsApp 行为可能违反第三方服务条款并导致账号受限或封禁，所有使用风险需由用户自行承担。"
  - question: "WhatsApp 频繁更新并混淆代码后，WaEnhancer 如何保持可用？"
    answer: "模块内置了原生 `libdexkit.so`（支持 `arm64-v8a` 与 `armeabi-v7a`），可在运行时扫描 WhatsApp 的 DEX 字节码并自动定位混淆后的方法签名，从而显著降低小版本更新导致的 Hook 失效概率。"
---

## 概述

**WaEnhancer**（仓库 `Dev4Mod/WaEnhancer`，包名 `com.wmods.wppenhacer`）是一款面向官方 **WhatsApp**（`com.whatsapp`）与 **WhatsApp Business**（`com.whatsapp.w4b`）的开源 Xposed 增强模块。

与早期需要卸载正版并信任第三方重打包 APK 的所谓“修改版 WhatsApp”不同，WaEnhancer 不修改磁盘上的任何原版安装包，而是通过 **LSPosed** 在应用运行时的内存中动态注入功能，兼顾原版签名安全性与高度可定制性。

> **风险提示与项目声明**：根据上游文档声明，WaEnhancer 仅用于技术研究与教育目的，不包含任何 Meta/WhatsApp 专有代码，也不破解任何付费订阅或服务端加密。使用任何客户端增强模块均存在触发 WhatsApp 账号风控或封禁的风险，请自行评估后谨慎使用。

---

## 技术架构与工作原理

### YukiHookAPI + libxposed API 101 + DexKit

通过分析 `WaEnhancer-1.6.6.0352170C.apk`（`1.6.6-0352170c`）安装包结构，可以看到其核心架构如下：

1. **YukiHookAPI 与 libxposed 服务桥梁**：
   - `META-INF/xposed/module.prop` 由 **YukiHook 1.5.0** 生成，声明 `minApiVersion=101`、`targetApiVersion=101`、`staticScope=false`，入口类为 `com.wmods.wppenhacer.WppXposed_YukiHookXposedInit`。
   - 模块同时声明了 `com.wmods.wppenhacer.XposedService`、`io.github.libxposed.service.XposedProvider`，以及自定义的 `PrefsProvider`、`HookProvider` 和 `BridgeService`，确保界面开关调整能可靠同步至宿主进程。
2. **原生 DexKit 动态寻址（`libdexkit.so`）**：
   - 面对 WhatsApp 每次发版后的高度代码混淆，WaEnhancer 内置了 `arm64-v8a` 与 `armeabi-v7a` 架构的 `libdexkit.so`，在运行时动态检索类与方法特征，同时配套 `libaudio_opus_converter.so` 处理音频编码转换。
3. **目标作用域（`META-INF/xposed/scope.list`）**：
   - 默认涵盖 `com.whatsapp`（WhatsApp）、`com.whatsapp.w4b`（WhatsApp Business）与 `system`。
4. **内置扩展界面**：
   - 自带基于 Prism 语法高亮的 CSS 编辑器（`assets/css_editor.html` 与 `assets/www/`）以及通话录音设置页（`CallRecordingSettingsActivity`）。

---

## 核心功能清单

根据 `Dev4Mod/WaEnhancer` 上游功能说明：
- **隐私隐身**：冻结最后上线时间（Freeze Last Seen）、隐藏状态查看记录、隐藏已读蓝勾、隐藏阅后即焚与语音消息已读状态、隐藏送达双勾、隐藏正在输入与正在录音提示，以及“仅在回复后发送蓝勾”。
- **防撤回与消息留存**：聊天消息防撤回、动态/状态防撤回、显示已编辑消息的修改历史、解除阅后即焚媒体查看限制。
- **消息与聊天增强**：隐藏转发标签（Hide Forwarded Tag）、移除转发人数限制、解除置顶聊天数量上限、移除长文本“查看更多”折叠、对任意消息执行“为所有人删除”。
- **界面与音频定制**：通过内置 CSS 编辑器微调界面样式，并支持通话录音相关设置。

---

## 安装与配置步骤

1. 确保设备上已安装官方原版 **WhatsApp**（`com.whatsapp`）或 **WhatsApp Business**（`com.whatsapp.w4b`），并激活支持 **libxposed API 101** 的 **LSPosed**。
2. 下载官方发布的 `WaEnhancer-1.6.6.0352170C.apk` 并安装：
   ```bash
   adb install WaEnhancer-1.6.6.0352170C.apk
   ```
3. 打开 **LSPosed 管理器** -> **模块**，启用 **WaEnhancer**，并在作用域中勾选 `com.whatsapp`（及/或 `com.whatsapp.w4b`）。
4. 启动 **WaEnhancer** 主应用（`MainActivity`），按提示授予所需存储与通知权限，开启需要的隐私或主题开关后强行停止并重启 WhatsApp（也可点击应用内 `ForceStartActivity` 快捷重启）即可生效。

---

## 常见问题与排查

- **WhatsApp 更新后部分功能失效**：先打开 WaEnhancer 应用刷新并重建 DexKit 特征缓存，强行停止 WhatsApp 后重新进入；若 WhatsApp 为大版本架构升级，请关注 `Dev4Mod/WaEnhancer` 仓库更新。
- **勾选过多功能后出现闪退**：建议逐项排查近期新开启的实验性功能开关，在重置缓存后重启 WhatsApp 测试稳定性。
