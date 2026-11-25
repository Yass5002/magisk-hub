---
id: "canta"
title: "Canta：基于 Shizuku 的免 Root 系统应用精简工具"
sidebarTitle: "Canta"
description: "由 samolego 开发的开源 Android 精简工具，结合 Shizuku 与 Universal Debloat List 为用户 0 安全移除厂商与运营商预装应用。"
category: "system-utilities"
tier: 1
searchQueries:
  - "canta 精简工具 apk 下载"
  - "canta shizuku 卸载系统应用"
  - "免 root 卸载安卓预装软件"
  - "canta 恢复已卸载系统应用"
  - "cmd package install-existing 恢复应用"
prerequisites:
  - "Android 9.0（Pie）或更高版本"
  - "通过无线调试 ADB 或 Root（Magisk/KernelSU/APatch）激活 Shizuku 服务"
conflicts:
  - "卸载核心操作系统组件（如 SystemUI、默认拨号器、Android 框架）"
  - "部分 OPPO/一加 ColorOS 系统包存在固件级卸载锁定限制"
configPaths:
  - "/data/data/io.github.samolego.canta/"
features:
  - "集成 Universal Debloat List：将软件包划分为 Recommended、Advanced、Expert 与 Unsafe 四个安全等级，防止误删变砖"
  - "无需 Root 权限：通过 Shizuku Binder 令牌为主用户干净卸载应用包"
  - "一键即时恢复：直接在 Trash（回收站）标签页中恢复任何误卸载的应用"
  - "支持 Web ADB 客户端：可选通过浏览器 WebUSB 进行精简，无需安装 APK"
faq:
  - question: "在 Canta 中卸载系统应用会从设备中永久删除它吗？"
    answer: "不会。在 Android 中，如果不解锁 Bootloader 并修改系统镜像，只读系统分区（`/system`、`/product`、`/system_ext`）中的文件是无法物理删除的。Canta 执行的是用户态卸载（`pm uninstall -k --user 0 <package>`），仅为主配置文件停用该软件包并清除用户数据，原始 APK 仍完整保留在出厂系统镜像中。"
  - question: "如果无法打开 Canta，该如何恢复已卸载的系统应用？"
    answer: "由于出厂 APK 仍保存在只读系统分区内，你随时可以通过 ADB 或终端运行 `cmd package install-existing <package_name>` 恢复任何已移除的应用，应用将按出厂默认设置重新安装回来。"
  - question: "为什么部分一加 / OPPO 系统应用无法卸载？"
    answer: "ColorOS 与 Oplus 框架固件在 PackageManagerService 中加入了自定义安全校验，会拦截针对特定预装系统应用的 `pm uninstall` 调用。对于这类顽固应用，建议改用 Hail（雹）进行冻结或挂起。"
---

## 概述

各手机厂商（Samsung、Xiaomi、OPPO、Motorola、Transsion 等）出厂的商用 Android 设备通常会预装数十个无法直接卸载的应用：专有应用商店、遥测后台守护进程、冗余浏览器内核、预装社交软件以及运营商推广服务。

过去，移除这些预装应用往往需要获取完整 Root 权限、将系统分区挂载为可读写（`rw`）并物理删除 APK 文件——这种侵入式操作会破坏 SafetyNet / Play Integrity 认证、触发三星 Knox 熔断，甚至导致设备无法开机。

**Canta** 是由 samolego 开发的开源 Android 精简工具，彻底革新了这一流程。通过将 **Shizuku** 的特权 Binder 访问能力与社区协作维护的 **Universal Debloat List（UAD）** 相结合，Canta 让用户无需 Root 权限即可在手机本地安全移除预装冗余应用。

---

## 技术机制：User-0 用户态精简原理

Canta 移除应用时不会执行破坏性的文件系统删除操作，而是通知 Android 的 `PackageManagerService` 仅针对主用户配置文件（`UserHandle.USER_SYSTEM` / `0`）移除该软件包：

- **Canta 界面层**：查询 Universal Debloat List 数据库并展示软件包安全评级（`[Recommended]`、`[Advanced]`、`[Expert]`、`[Unsafe]`）。
- **Shizuku 代理层**：无需 Root，通过特权 Binder 向 Android 的 `IPackageManager` 接口派发调用请求。
- **PackageManagerService 执行层**：
  - 通过 `pm uninstall -k --user 0 <package_name>` 执行软件包移除
  - 终止该应用进程并清除用户状态数据
  - 将软件包标记为对 User 0 已卸载，同时保留 `/system/app/` 下不可变的原始 APK 以便安全恢复

这种架构具备三大优势：
1. **高安全性**：由于出厂 APK 完好无损地留在只读系统分区中，恢复出厂设置即可重新找回所有原装应用。
2. **不影响官方 OTA**：系统分区完整性未被破坏，官方在线升级（OTA）可顺利安装而不报错。
3. **无需解锁 Bootloader**：借助无线调试激活 Shizuku 即可在免 Root 环境下运行。

---

## 安全分级标准（Universal Debloat List）

Canta 基于社区众包调研成果，将设备中的每个软件包划分至以下四个安全等级：

- **[Recommended]（推荐移除）**：完全可安全移除。移除此类应用（如 Facebook 后台服务、诊断日志工具、推广游戏）不会造成任何功能退化。
- **[Advanced]（进阶移除）**：若你不使用其对应的特定功能，则可安全移除（例如使用 Google 日历时移除系统自带日历）。
- **[Expert]（专家谨慎）**：需谨慎操作。移除此类包可能会影响部分子系统功能（例如移除语音合成引擎或打印后台服务）。
- **[Unsafe]（危险勿动）**：核心系统组件（如 SystemUI、Android 框架、TelephonyProvider）。Canta 会将其标红并警告移除后将立即引发无限重启（Bootloop）。

---

## 分步使用指南

### 1. 前置准备
1. 安装并启动 **Shizuku**（可通过无线调试或 Root 方式启动）。
2. 从 Canta 官方发布页下载并安装 `androidApp-release.apk`。

### 2. 精简应用
1. 打开 Canta，在弹窗中授予 Shizuku 授权。
2. Canta 将扫描所有已安装的用户应用与系统应用，并按安全等级分类展示。
3. 使用搜索栏或筛选标签（如 *Recommended*）查看可安全卸载的目标。
4. 勾选需要移除的冗余预装应用复选框。
5. 点击右下角的**垃圾桶（Trash）**悬浮按钮，批量卸载所有选中应用。

### 3. 恢复已卸载的应用
如果你之后需要重新使用某个已卸载的应用：
1. 在 Canta 顶部切换至 **Trash** 标签页。
2. 此处列出了所有此前为 User 0 卸载的软件包。
3. 点击目标应用旁的恢复图标，即可立即重新安装启用。

---

## 通过 ADB 紧急恢复

如果你误删了关键系统组件，导致设备进入 Bootloop 或无法加载系统桌面：

将手机通过 USB 连接至已开启 USB 调试的电脑，执行以下命令：
```bash
# Reinstall the package for User 0 from the factory system image:
adb shell cmd package install-existing <package_name>

# Example: restoring stock launcher:
adb shell cmd package install-existing com.miui.home

# Example: restoring Google Play Services:
adb shell cmd package install-existing com.google.android.gms

# Reboot the device:
adb reboot
```
目标应用将立即重新恢复，所有系统级绑定关系也会随之还原。
