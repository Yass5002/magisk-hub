---
id: "xiaomi-13pro-device-spoofer"
title: "小米 13 Pro 机型身份伪装模块（Xiaomi 13 Pro Device Identity Spoofer）"
sidebarTitle: "小米 13 Pro 机型伪装"
description: "无系统分区修改（Systemless）的设备身份伪装模块，将系统属性伪装为国行小米 13 Pro（2210132C），解锁 120 FPS 高帧率与旗舰游戏画质档位。"
category: "system-environment"
author: "Da Feng Mei Le Yun Bu Fei"
version: "v1.0"
updatedAt: "2026-10-04"
compatibility: ["Magisk", "KernelSU", "APatch"]
tier: 1
searchQueries: []
prerequisites: []
conflicts: []
configPaths: []
features: []
faq: []
---

## 概述与系统架构

**小米 13 Pro 机型身份伪装模块（Xiaomi 13 Pro Device Identity Spoofer）** 是由大风没了云不飞（Da Feng Mei Le Yun Bu Fei）开发的轻量级无系统分区修改（Systemless）属性注入模块。该模块通过修改 Android 产品识别属性，将设备身份伪装为搭载骁龙 8 Gen 2 的国行旗舰机型 **Xiaomi 13 Pro**（型号 `2210132C`）。

包括《王者荣耀》、《和平精英 / PUBG Mobile》与《原神》在内的现代大型手游均在服务端维护了硬件白名单。未被明确收录为顶级旗舰的机型通常会被限制在 60 FPS 或低画质预设。通过在开机阶段经由 `system.prop` 伪装机型身份，本模块可解锁极限高帧率模式（90 FPS、120 FPS）与超高画质档位。

## 注入的系统属性

拆包检查 `common/system.prop` 可见如下精确的旗舰机型伪装字段：

```properties
ro.product.manufacturer=Xiaomi
ro.product.brand=Xiaomi
ro.product.model=Xiaomi 13Pro
ro.product.name=2210132C
ro.product.device=2210132C
```

## 核心优势

1. **解锁游戏高帧率**：在腾讯系及网易系等主流手游中解锁 90Hz 与 120Hz 高刷新率画质选项。
2. **旗舰特性白名单**：解锁小米云电脑、相册 HDR 增强以及游戏加速（Game Turbo）中的高性能模式。
3. **纯净无侵入式运行**：在运行时动态修改系统属性，完全不触碰只读系统分区块设备，确保顺畅 OTA 升级并与 SafetyNet / Play Integrity 和谐共存。

## 安装与验证方法

### 第一步：刷入模块
通过 Magisk、KernelSU 应用或 APatch 管理器从本地安装并刷入模块。

### 第二步：验证注入属性
重启设备后，通过 ADB Shell 或手机本地终端执行以下验证命令：
```bash
getprop ro.product.model
# Output: Xiaomi 13Pro

getprop ro.product.name
# Output: 2210132C

getprop ro.product.device
# Output: 2210132C
```

### 第三步：清除游戏应用缓存
为确保游戏服务器重新拉取并识别更新后的机型名称，建议清除目标游戏应用的缓存：
```bash
pm clear-cache <package.name>
```

## 兼容性与安全说明

- **广泛设备兼容**：兼容各品牌设备（小米、一加、真我、三星、Google Pixel 等）上的 Magisk（v20.4+）、KernelSU 与 APatch 环境。
- **Play Integrity / SafetyNet 说明**：本模块不会改动安全补丁级别或 Bootloader 锁定状态。若同时配合 Play Integrity Fix 使用，请确保 Play Integrity Fix 按需正常加载设备指纹。
