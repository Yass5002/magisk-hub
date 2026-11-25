---
id: "lsposed"
title: "LSPosed：现代 Android ART 运行时 Hook 框架"
sidebarTitle: "LSPosed Framework"
description: "由 LSPosed Developers 开发的现代 Xposed 框架继任者，注入 Android Zygote 进程以提供纯内存级运行时方法 Hook 与按应用作用域隔离。"
category: "root-management"
tier: 1
searchQueries:
  - "lsposed 模块下载"
  - "lsposed zygisk 安装教程"
  - "lsposed 管理器 apk 下载"
  - "magisk 怎么安装 lsposed"
  - "lsposed 拨号代码 5776733"
prerequisites:
  - "Android 8.1（Oreo MR1）至 Android 14（Android 15+ 需使用 JingMatrix LSPosed 等更新的社区分支）"
  - "通过 Magisk（v24+ 且开启 Zygisk）、KernelSU（搭配 Zygisk-Next）或 APatch（搭配 Zygisk-APatch）获取 Root 权限"
conflicts:
  - "旧版 EdXposed 或基于 Riru 的 Xposed 引擎（刷入 LSPosed Zygisk 前必须彻底卸载）"
  - "不带应用作用域过滤机制的全局 Zygote Hook 模块"
configPaths:
  - "/data/adb/modules/zygisk_lsposed/"
  - "/data/adb/lspd/"
  - "/data/system/users/0/lspd/"
features:
  - "无侵入式 ART 方法 Hook：在内存中动态修补已编译的 ART dex 方法，无需修改系统分区或破坏 APK 签名"
  - "白名单作用域管理：模块仅在用户指定的目标应用中生效，避免系统级额外耗电与应用崩溃"
  - "寄生模式 SystemUI 集成：通过系统通知或拨号盘暗码直接调起管理界面，无需常驻前台后台服务"
  - "完整 Xposed API 兼容：100% 向后兼容经典 Xposed、EdXposed 及现代 LSPlant 引擎 API"
faq:
  - question: "为什么桌面上找不到 LSPosed 管理器应用图标？"
    answer: "LSPosed 默认以「寄生管理器」形式嵌入系统框架运行。如果系统通知被清除或被厂商省电策略拦截，可打开系统拨号盘输入 `*#*#5776733#*#*`（即 `*#*#LSPosed#*#*`）直接启动界面；也可从官方 LSPosed 发布页下载安装独立版 `manager.apk`。"
  - question: "为什么已经安装的 Xposed 模块没有生效？"
    answer: "不同于旧版 Xposed 对所有应用全局生效的机制，LSPosed 强制采用严格的白名单作用域模型。你必须打开 LSPosed 管理器，点击对应模块，开启顶部开关并在「作用域（Scope）」列表中勾选目标应用，随后强行停止并重启目标应用。"
  - question: "如果某个不兼容的 Xposed 模块导致无限重启（Bootloop），该如何恢复？"
    answer: "LSPosed 模块运行在用户应用与系统服务进程中。若模块引发卡开机，可在开机过程中长按音量减键进入安全模式（Safe Mode）以禁用所有第三方模块；也可通过 Root Shell 或 ADB 执行：`touch /data/adb/modules/zygisk_lsposed/disable && reboot`。"
---

## 概述

**LSPosed Framework** 是经典的 Android Xposed 框架的现代化高性能继任者。该框架由 LSPosed Developers 团队研发，将 Android Runtime（ART）与动态插桩技术结合，支持开发者实时挂钩（Hook）Java 与原生方法。

在早期的 Android 系统修改工作流中，调整系统行为往往需要反编译系统框架、使用 Apktool 等工具修补 APK，或刷入庞大的第三方 ROM。Xposed 通过注入 Zygote 进程并在内存中挂钩类方法，彻底改变了这一流程。

然而，初代 Xposed 与 EdXposed 等早期框架存在明显缺陷：它们会全局挂钩每一个应用进程，导致性能明显下降、电量消耗加剧以及频繁崩溃。LSPosed 基于 **Zygisk** 与**按应用作用域（Scope）隔离**重构了底层架构，彻底解决了上述问题。

---

## 技术架构与 Hook 机制

LSPosed 在 Android 开机早期通过 Magisk 或 KernelSU 的 **Zygisk**（Zygote 注入）生命周期运行：

- **init (PID 1)**：系统初始化启动操作系统并拉起核心系统守护进程。
- **app_process / Zygote**：加载 `libart.so` 与运行时类库；Zygisk 动态加载 LSPosed 核心库（`zygisk_lsposed`）。
- **选择性进程孵化（Fork）**：
  - **目标应用（在作用域内）**：激活 LSPosed 挂钩，直接将模块 DEX 加载至内存，并通过 LSPlant 执行方法 Hook。
  - **普通应用（不在作用域内）**：零 Hook 注入，保持原生执行速度且无任何额外开销。

1. **Zygisk 注入**：当 Android 拉起 `zygote`（以及 `zygote64`）守护进程时，LSPosed 注入其核心 Hook 库（`liblspd.so`）。
2. **Fork 前评估**：在 Zygote 孵化子进程运行应用之前，LSPosed 会查询 `/data/adb/lspd/`，检查目标应用包名是否位于模块的作用域数据库中。
3. **选择性 ART Hook**：
   - 若包名**不在作用域内**，Zygote 直接干净地完成进程孵化，不初始化 Hook 引擎，应用以 100% 原生性能运行。
   - 若包名**在作用域内**，LSPosed 初始化 LSPlant，将目标方法入口替换为动态跳板挂钩，并触发模块的 `IXposedHookLoadPackage` 回调。

---

## 安装与配置

### 前置要求
1. 运行 **Android 8.1 至 Android 14** 的已 Root 设备。
2. 现代化的 Root 管理器：
   - **Magisk v24+**：进入设置 -> 开启 **Zygisk**，然后重启设备。
   - **KernelSU**：在 KernelSU 中刷入 **Zygisk-Next** 模块，然后重启设备。
   - **APatch**：刷入 **Zygisk-APatch** 模块，然后重启设备。

### 分步安装指南
1. 下载 `LSPosed-v1.9.2-7024-zygisk-release.zip`。
2. 打开 Root 管理器（Magisk / KernelSU / APatch），进入**模块**标签页。
3. 点击**从本地安装**，选择 LSPosed 压缩包并等待刷入完成。
4. 重启设备。
5. 开机后下拉通知栏查看 **LSPosed 管理器**配置通知，点击即可在桌面创建管理器快捷方式。

---

## 寄生模式管理器与拨号盘暗码

为保持极简体积并防止第三方应用检测到设备上的独立管理器包名，LSPosed 采用了**寄生管理器**架构：

- 管理器界面基于系统资源动态合成。
- 若系统通知被误删或桌面启动器隐藏了快捷方式，可打开系统自带的拨号盘输入以下暗码立即调起 LSPosed 界面：
  ```
  *#*#5776733#*#*
  ```
  *（在数字九宫格键盘上，5776733 恰好对应字母 L-S-P-O-S-E-D）。*

- 如果你的厂商定制拨号盘不支持解析暗码，也可通过 Root 终端直接拉起：
  ```bash
  su -c am start -n org.lsposed.manager/.ui.MainActivity
  ```

---

## 作用域配置与模块管理

LSPosed 中的每个模块均需用户显式授权并绑定作用范围：

1. 安装任意兼容的 Xposed 模块 APK（例如 CorePatch、Bootloader Spoofer、HookVip）。
2. 打开 **LSPosed 管理器** -> 进入**模块**页面（拼图图标）。
3. 新安装的模块默认处于灰显状态并标记为「未激活」。
4. 点击该模块，打开顶部的**启用模块**开关。
5. 在**作用域（Scope）**列表中勾选模块需要修改的目标应用（例如状态栏美化模块勾选 `com.android.systemui`，或勾选特定目标应用以实现功能增强）。
6. 强行停止并重新打开所选应用以使修改生效。

---

## 无限重启恢复与紧急卸载

如果某个激进或不兼容的 Xposed 模块导致系统卡死或开机循环（Bootloop）：

### 方法一：ADB 安全禁用（推荐）
通过 USB 数据线将手机连接至电脑并执行：
```bash
# 仅停用 LSPosed 而不卸载模块数据
adb wait-for-device shell touch /data/adb/modules/zygisk_lsposed/disable
adb reboot
```

### 方法二：实体按键进入安全模式
在设备开机出现厂商启动动画时，持续长按**音量减**键，直至锁屏界面左下角显示「安全模式（Safe Mode）」。安全模式会阻止加载所有第三方模块，进入桌面后即可打开 Magisk/KernelSU 关闭问题模块。

### 方法三：彻底清除
在第三方 Recovery（TWRP/OrangeFox）终端或 Root Shell 中执行：
```bash
rm -rf /data/adb/modules/zygisk_lsposed
rm -rf /data/adb/lspd
```
