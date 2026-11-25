---
id: "tencent-rog6-device-spoofer"
title: "腾讯 ROG 游戏手机 6 天玑版机型伪装模块：165Hz/120Hz 高帧率解锁"
sidebarTitle: "ROG 6 机型伪装"
description: "无系统分区修改硬件身份伪装模块，将设备属性配置为华硕 ROG 游戏手机 6 天玑至尊版（ASUS_AI2203_B），突破主流手游画质与帧率上限。"
category: "system-environment"
tier: 1
searchQueries:
  - "ROG 6 机型伪装 Magisk 模块"
  - "asus_ai2203_b build.prop Root"
  - "解锁手游最高画质 ROG Magisk"
  - "腾讯 ROG 游戏手机型号伪装"
prerequisites:
  - "Magisk 17.0+、KernelSU 或 APatch"
  - "配备 120Hz 及以上高刷新率屏幕的 Android 智能手机"
conflicts:
  - "其他全局 `build.prop` 机型伪装模块"
configPaths:
  - "/data/adb/modules/机型问题删我/system.prop"
features:
  - "将设备属性伪装为华硕 ROG 游戏手机 6 天玑至尊版（`ASUS_AI2203_B`）"
  - "在腾讯系与网易系热门手游中解锁极致画质与高帧率预设"
  - "纯 `system.prop` 属性注入，零后台进程常驻开销"
  - "全面兼容 Magisk、KernelSU 与 APatch"
faq:
  - question: "银行类应用会检测到这个机型修改吗？"
    answer: "该模块仅修改用户空间的设备型号（Product Model）属性。银行应用主要检测 Root 二进制特征（由 Play Integrity / SafetyNet 隐藏工具处理），而游戏引擎则通过读取这些型号属性来决定是否开放高刷新率选项。"
---

## 概述

**腾讯 ROG 游戏手机 6 天玑版机型伪装模块（Tencent ROG Phone 6 Dimensity Edition Device Spoofer）**（作者：时长两年半的坤 / Shi Chang Liang Nian Ban De Kun）通过模拟华硕旗舰电竞手机身份，帮助设备突破游戏厂商设定的画质与帧率限制。

---

## 技术架构与工作原理

该模块通过 Magisk 的 `resetprop` 框架注入以下系统属性：

```properties
ro.product.manufacturer=asus
ro.product.brand=asus
ro.product.marketname=腾讯ROG6天玑至尊版
ro.product.model=ASUS_AI2203_B
```
