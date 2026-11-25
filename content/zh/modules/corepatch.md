---
id: "corepatch"
title: "CorePatch：禁用安卓 APK 签名校验与降级安装限制（核心破解）"
sidebarTitle: "CorePatch"
description: "现由 LSPosed/CorePatch 官方接管维护的 Xposed 模块（org.lsposed.corepatch），基于 libxposed API 101 禁用签名校验、允许保留数据降级与跨签名覆盖安装。"
category: "xposed-runtime-hooks"
tier: 1
searchQueries:
  - "CorePatch 核心破解下载"
  - "LSPosed CorePatch 教程"
  - "安卓禁用 APK 签名验证"
  - "安卓保留数据降级安装"
  - "不同签名覆盖安装 APK"
prerequisites:
  - "Android 9.0 及以上系统，已部署 Magisk、KernelSU 或 APatch"
  - "支持 libxposed API 101 的官方 LSPosed 框架"
conflicts:
  - "旧版幸运破解器（Lucky Patcher）静态修改 `services.jar` / `core.jar` 的补丁（与运行时 ART Hook 叠加易导致 `system_server` 崩溃）"
  - "早期 `coderstory/CorePatch` 旧包名或不同签名版本"
configPaths:
  - "/data/adb/lspd/"
  - "/data/data/org.lsposed.corepatch/"
features:
  - "由官方 `LSPosed/CorePatch` 仓库维护的 CorePatch N（`org.lsposed.corepatch`），原生接入 libxposed API 101（`XposedService` 与 `XposedProvider`）"
  - "绕过 APK 签名校验：允许在官方正版应用之上直接覆盖安装重新签名、修改版或未签名的 APK"
  - "保留数据降级安装：屏蔽 `PackageManagerService` 的 `INSTALL_FAILED_VERSION_DOWNGRADE` 拦截，无需清除应用数据即可回退旧版本"
  - "跨签名覆盖安装：支持使用测试/调试证书签名的 APK 直接覆盖生产环境正式版应用"
  - "屏蔽摘要校验：绕过新版 Android 的安装包清单摘要比对限制"
faq:
  - question: "在 LSPosed 中需要为 CorePatch 勾选哪个作用域？"
    answer: "CorePatch（`org.lsposed.corepatch`）在配置中声明了 `staticScope=true`，且 `scope.list` 目标固定为系统框架 `system`。请在 LSPosed 模块页勾选 **系统框架**（`system`）并重启手机，以确保 Hook 注入 `system_server` 进程。"
  - question: "为什么 CorePatch 现在的仓库变成了 LSPosed/CorePatch？"
    answer: "CorePatch 最初由 coderstory 开发，现已正式移交至 **LSPosed/CorePatch** 组织接管维护并升级为 CorePatch N（`N-1.0`+），全面迁移至现代 libxposed API 101 架构（`org.lsposed.corepatch.XposedService`），以保持对高版本 Android 的良好兼容性。"
  - question: "开启 CorePatch 后仍提示 `INSTALL_FAILED_DUPLICATE_PERMISSION` 怎么办？"
    answer: "CorePatch 仅放行签名校验与版本号降级限制，但 Android 对自定义权限树仍有唯一归属校验：若目标 APK 声明的自定义权限已被设备上另一个不同签名的应用占用，系统仍会拒绝安装。请先卸载或冻结声明了冲突权限的应用。"
---

## 概述

在原生 Android 系统中，`PackageManagerService`（PMS）会在安装与更新应用时严格校验 `/data/system/packages.xml` 中记录的数字签名与版本信息：

1. **签名不一致**：若新旧 APK 签名证书不同，系统会报错 `INSTALL_FAILED_UPDATE_INCOMPATIBLE` 并中止安装。
2. **版本号降级拦截**：当待安装 APK 的 `versionCode` 低于已安装版本时，系统会返回 `INSTALL_FAILED_VERSION_DOWNGRADE`。
3. **完整性摘要校验**：新版 Android 还会比对 APK 签名块与清单摘要信息。

**CorePatch（核心破解）** 最初由 **coderstory** 发起，现已正式移交至 **LSPosed/CorePatch** 组织维护并演进为 CorePatch N（包名 `org.lsposed.corepatch`）。它基于 **libxposed API 101** 在 Android 运行时内存中动态挂钩 `system_server`，无需静态修改 `/system/framework/services.jar` 分区文件即可解除上述安装限制。

---

## 技术架构与工作原理

### libxposed API 101 与 `system_server` 运行时挂钩

通过分析 `LSPosed/CorePatch` 发布的 `N-1.0`（`app-release.apk`）载荷可见，新版模块采用了极为精简的现代架构：

- **标准 libxposed 服务接入**：`org.lsposed.corepatch` 在清单中声明了 `io.github.libxposed.service.XposedProvider` 与 `org.lsposed.corepatch.XposedService`，并在 `META-INF/xposed/module.prop` 中指定 `minApiVersion=101`、`targetApiVersion=101`。
- **静态系统作用域（`staticScope=true`）**：模块通过 `META-INF/xposed/scope.list` 明确锁定作用域为 `system`（即承载 `PackageManagerService`、`KeySetManagerService` 与 `SigningDetails` 的 `system_server` 进程）。
- **核心验证拦截**：在用户通过系统安装器或 `adb install` 发起安装请求时，CorePatch 动态拦截 `SigningDetails.checkCapability()`、`PackageManagerService.checkDowngrade()` 及证书解析逻辑，使其直接放行跨签名覆盖、未签名或低版本 APK。

---

## 安装与配置指南

### 前置要求
- 已通过 **Magisk**、**KernelSU** 或 **APatch** 获取 Root 权限的 Android 设备。
- 已安装支持 **libxposed API 101** 的 **LSPosed** 框架。

### 第一步：安装模块 APK
1. 从 `LSPosed/CorePatch` 官方发布页下载 `app-release.apk`。
2. 直接在设备端安装（若此前安装过早期 `coderstory` 签名版本导致冲突，请先卸载旧版）。

### 第二步：启用作用域并配置开关
1. 打开 **LSPosed 管理器** -> **模块**。
2. 开启 **CorePatch** 开关，并确认作用域中已勾选 **系统框架**（`system`）。
3. 从桌面或 LSPosed 模块设置打开 **CorePatch**（`org.lsposed.corepatch.MainActivity`），按需启用对应开关：
   - 允许降级安装（Allow downgrade installation）
   - 禁用签名校验（Disable signature verification）
   - 禁用包摘要检查（Disable package digest checks）
   - 允许不同签名覆盖安装（Allow overwrite across different signatures）
4. **重启设备**，使 `system_server` 在系统启动阶段完成 Hook 注入。

---

## 典型使用场景

### 1. 保留数据回退应用版本
当常用应用新版出现严重 Bug 或耗电异常时，可保留本地数据库与登录状态直接降级回旧版：
```bash
# 通过 Root Shell 或 ADB 直接执行降级安装：
pm install -d /sdcard/Download/app-older.apk
```

### 2. 直接覆盖安装调试版或修改版 APK
开发者与玩机用户在测试本地编译的 Debug 包或开源分支构建时，无需先卸载正式版即可原地覆盖更新。

---

## 常见问题与排查

### 启用后安装仍提示签名冲突
1. 确认 **CorePatch** 在 LSPosed 中处于启用状态，且 **系统框架**（`system`）已被勾选。
2. 更改设置或首次启用后务必完整重启设备，因为 `system_server` 钩子仅在系统早期启动阶段挂载。
3. 检查系统中是否残留其他静态修改过 `services.jar` 的补丁或冲突模块。

### 极端情况卡开机（Bootloop）恢复
若在魔改幅度较大的第三方 ROM 上导致 `system_server` 启动异常，可通过 ADB 临时禁用 LSPosed 恢复开机：
```bash
adb wait-for-device shell touch /data/adb/modules/zygisk_lsposed/disable
adb reboot
```
进入系统后卸载或更新 CorePatch 即可。
