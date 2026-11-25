---
id: "knoxpatch"
title: "KnoxPatch：在已 Root 的三星 One UI 上恢复 Knox 专属功能"
sidebarTitle: "KnoxPatch"
description: "全面的系统级修复补丁，用于在已 Root 的三星 Galaxy 设备上恢复失效的安全文件夹、Samsung Pass 与三星健康等 Knox 功能。"
category: "system-environment"
tier: 1
searchQueries:
  - "KnoxPatch Magisk 模块下载"
  - "三星 Root 修复安全文件夹"
  - "One UI Root 后修复 Samsung Pass"
  - "salvogiangri KnoxPatch 教程"
  - "三星健康绕过 Knox 0x1 熔断"
prerequisites:
  - "运行官方 One UI 固件的三星 Galaxy 设备（Android 9 至 Android 15）"
  - "已获取 Root 权限（Magisk、KernelSU 或 APatch）并激活 LSPosed 或 Vector 框架"
conflicts:
  - "原生 AOSP 或非三星 ROM（仅适用于三星 One UI 系统）"
configPaths:
  - "/data/adb/modules/knoxpatch/"
  - "/data/user/0/io.github.salvogiangri.knoxpatch/"
features:
  - "恢复失效的三星专有服务：安全文件夹、Samsung Pass、私密分享与三星健康"
  - "在内存中动态修补 Knox 安全守护进程（`keystorage`、`sem_personamanager`）"
  - "支持动态 WSM Hook 注入，无需手动解包系统分区或反编译合并（Deodex）"
  - "提供配套管理应用，便于按需开关单应用补丁及查看运行诊断状态"
faq:
  - question: "KnoxPatch 能否把物理熔断的 Knox 状态从 0x1 还原回 0x0？"
    answer: "不能。三星 Knox 保修熔断位是主板上的一颗一次性可编程物理电子熔丝（OTP e-fuse），在解锁 Bootloader 的瞬间即已永久熔断。KnoxPatch 无法修改硬件熔丝状态，而是通过 Hook 系统框架与 Knox API，向三星应用伪造返回结果，使其认为设备完整且 Knox 验证已通过。"
  - question: "为什么刷入 KnoxPatch 后安全文件夹依然无法完成初始化设置？"
    answer: "安全文件夹（Secure Folder）必须同时依赖 KnoxPatch（Xposed 模块端）与 KnoxPatch Enhancer（Magisk 模块端）协同工作。Enhancer 负责在开机早期修补 Knox 底层守护进程，而 Xposed 组件负责拦截运行时框架调用，请确保两者均已安装并正常激活。"
---

## 概述

由 **salvogiangri** 开发的 **KnoxPatch** 是所有为三星 Galaxy 手机或平板（运行 One UI）获取 Root 权限玩家的必备工具。

当三星设备解锁 Bootloader 时，硬件安全逻辑会永久熔断 Knox 电子熔丝（`0x1`）。作为响应，三星系统软件会立即封锁一系列专有安全应用：**安全文件夹（Secure Folder）**、**Samsung Pass**、**三星健康（Samsung Health）**、**安全 Wi-Fi（Secure Wi-Fi）** 以及 **私密分享（Private Share）**。KnoxPatch 通过挂钩（Hook）三星专有框架服务并伪造安全完整性校验结果，系统性地恢复这些应用的正常功能。

---

## 技术架构与工作原理

### 三星框架与守护进程拦截

1. **Knox 守护进程修补（Enhancer 模块）**：
   - 在开机早期阶段，三星专有安全守护进程（`sec_keystorage`、`ss_conn_daemon`）会通过内核 sysfs 读取并核验 Knox 保修熔断状态。
   - KnoxPatch Enhancer 模块通过注入库补丁绕过这些守护进程校验，确保凭据密钥库能够顺利初始化。
2. **框架服务挂钩（Xposed 组件）**：
   - 当安全文件夹或 Samsung Pass 启动时，会调用 `SemPersonaManager` 与 `KnoxVpnEngineService` 接口。
   - KnoxPatch 在内存中拦截这些 API 调用，直接返回 `STATUS_SUCCESS` 并将 Knox 保修位伪装为 `0x0`。
3. **密钥库软件降级回退**：
   - 由于 Samsung Pass 依赖 Knox 熔断后即被禁用的硬件级生物识别密钥校验，KnoxPatch 会将加密签名请求重定向至修补后的软件密钥库（Keystore），从而恢复无缝指纹/人脸认证体验。

---

## 安装与配置指南

### 第一步：安装 KnoxPatch Enhancer（Root 模块）
1. 下载 `KnoxPatch-Enhancer-vX.zip`。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入该模块。
3. 暂不重启设备。

### 第二步：安装 KnoxPatch Manager（APK）
1. 在设备上安装 `KnoxPatch.apk`。
2. 打开 **Vector Manager** 或 **LSPosed Manager**。
3. 在模块列表中启用 **KnoxPatch**，并确保其作用域（Scope）中已勾选 **系统框架（System Framework）**。
4. 重启手机。

### 第三步：配置修复服务
1. 从应用抽屉打开 **KnoxPatch** 应用。
2. 查看状态指示灯：**Xposed 模块** 与 **KnoxPatch Enhancer** 均应显示绿色对勾。
3. 按需开启需要修复的服务（安全文件夹、Samsung Pass、三星健康）。
4. 启动安全文件夹并按常规引导流程完成初始化设置即可。
