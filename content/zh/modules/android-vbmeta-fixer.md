---
id: "android-vbmeta-fixer"
title: "Android-VBMeta-Fixer：已验证启动哈希与 VBMeta 摘要还原模块"
sidebarTitle: "VBMeta Fixer"
description: "通过在开机早期执行密钥证明提取真实已验证启动哈希，并还原 ro.boot.vbmeta.digest 系统属性，从而修复已解锁设备上的 VBMeta 环境检测。"
category: "system-environment"
tier: 1
searchQueries:
  - "Android-VBMeta-Fixer Magisk 模块"
  - "reveny VBMeta Fixer 下载"
  - "修复 ro.boot.vbmeta.digest 属性"
  - "Android 绕过 VBMeta 检测"
  - "密钥证明获取 vbmeta 哈希"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "已解锁 Bootloader 且因 VBMeta 摘要属性缺失或不匹配导致完整性校验失败的设备"
conflicts:
  - "无已知模块冲突"
configPaths:
  - "/data/adb/modules/vbmeta-fixer/"
features:
  - "自动化摘要计算：在本地执行硬件密钥证明以推导真实的已验证启动哈希"
  - "动态系统属性赋值：在早期 post-fs 初始化阶段自动设置 `ro.boot.vbmeta.digest`"
  - "满足反作弊合规校验：轻松应对会检查底层原始 VBMeta 属性的银行及企业级安全检测"
  - "零配置开箱即用：刷入安装后即可全自动运行，无需手动调整任何参数"
  - "广泛框架兼容性：全面适配 Magisk、KernelSU 与 APatch Root 管理器"
faq:
  - question: "为什么部分银行应用会检测 `ro.boot.vbmeta.digest` 属性？"
    answer: "在 Bootloader 锁定且开启了已验证启动（Verified Boot）的设备上，Android 引导加载程序会将 vbmeta 分区的密码学摘要传入 `ro.boot.vbmeta.digest` 属性中。一旦用户解锁 Bootloader 或刷入第三方 ROM，该属性往往会被置空或损坏，进而暴露设备异常状态。"
  - question: "Android-VBMeta-Fixer 是如何获取正确摘要值的？"
    answer: "该模块会在系统早期启动阶段在设备本地发起一次密钥证明查询，直接从硬件密钥库签发的证书中提取 `verifiedBootHash`（已验证启动哈希），并将其写入对应系统属性值。"
---

## 概述

由 **reveny** 开发的 **Android-VBMeta-Fixer** 是一款针对性的无系统分区修改（Systemless）工具模块，专门用于解决已 Root 设备面临的 VBMeta 属性检测问题。

如今的高级 Root 检测库已不再局限于排查编译标签（Build Tags）或 `su` 二进制文件，它们还会深入核查 Android 的底层引导加载程序属性。具体而言，现代安全风控 SDK 会检测 `ro.boot.vbmeta.digest` 是否存在、格式是否有效，以及其数值是否与硬件密钥证明记录一致。Android-VBMeta-Fixer 可通过密钥证明推导出真实的已验证启动哈希，并自动将其赋给系统属性。

---

## 技术架构与工作原理

### 硬件密钥证明与属性注入

该模块在系统早期启动阶段执行以下流程：

1. **发起证明质询**：在早期的 `post-fs-data` 阶段，模块调用 Android Keystore 子系统生成一份临时证明证书。
2. **提取哈希摘要**：解析生成的 ASN.1 证书扩展字段，从中提取出由硬件出具的 `verifiedBootHash`。
3. **设置系统属性**：借助 Root 属性修改工具（`resetprop`），将提取出的哈希值注入 `ro.boot.vbmeta.digest` 及相关引导加载程序摘要属性中，向检测应用呈现一致且合规的已验证启动环境状态。

---

## 安装与配置指南

1. 从项目仓库下载最新版本的 `Android-VBMeta-Fixer-*.zip` 安装包。
2. 使用 Magisk、KernelSU 或 APatch 刷入该模块。
3. 重启设备。
4. 打开终端模拟器执行以下命令验证属性是否成功写入：
   ```bash
   getprop ro.boot.vbmeta.digest
   ```

---

## 配置与使用说明

本模块无需任何手动配置。每次系统启动时，模块都会自动检测设备硬件架构并应用对应的系统属性。

---

## 故障排查与常见问题

- **首次重启后属性仍为空**：如果 `getprop ro.boot.vbmeta.digest` 返回空白，请确认设备的 Keystore HAL 服务工作正常，且没有其他模块阻塞了 `post-fs-data` 阶段脚本的执行。
