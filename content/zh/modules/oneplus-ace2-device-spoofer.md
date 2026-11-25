---
id: "oneplus-ace2-device-spoofer"
title: "OnePlus Ace 2 机型伪装模块：手游高帧率解锁器"
sidebarTitle: "OnePlus Ace 2 机型伪装"
description: "无系统分区修改构建属性注入模块，将设备身份伪装为一加 Ace 2（PHK110），解锁竞技手游中的 90FPS 与 120FPS 高帧率选项。"
category: "system-environment"
tier: 1
searchQueries:
  - "一加 Ace 2 机型伪装 Magisk"
  - "和平精英解锁 120 帧 Root"
  - "PHK110 build.prop 伪装"
  - "一加 120Hz 游戏解锁 Magisk 模块"
prerequisites:
  - "Magisk 16.0+、KernelSU 或 APatch"
  - "Android 8.0 至 Android 14"
conflicts:
  - "其他全局单一机型伪装模块"
configPaths:
  - "/data/adb/modules/ONEPLUSACE2/common/system.prop"
features:
  - "注入完整有效的一加厂商与品牌系统属性定义"
  - "将硬件型号字符串伪装为 `PHK110`（一加 Ace 2）"
  - "在《和平精英》《PUBG Mobile》及《原神》中解锁 90 FPS 与 120 FPS 高帧率档位"
  - "纯无系统分区修改的构建属性注入方案，无需篡改任何 APK 文件"
faq:
  - question: "这个模块会改变我的系统语言或系统界面吗？"
    answer: "不会。该模块仅修改供游戏服务端检测画质支持档位的设备标识字符串，系统 UI 与语言设置均不受影响。"
---

## 概述

**OnePlus Ace 2 机型伪装模块（OnePlus Ace 2 Device Identity Spoofer）**（作者：游戏里解6）帮助手游玩家解锁原本被游戏厂商锁定给特定合作旗舰机型的超高帧率模式（90 FPS / 120 FPS）。

---

## 技术架构与工作原理

该模块通过 `/common/system.prop` 提供以下关键设备识别属性覆盖：

```properties
ro.product.manufacturer=ONEPLUA
ro.product.brand=ONEPLUS
ro.product.model=PHK110
```

当游戏客户端查询 `android.os.Build.MODEL` 与 `Build.BRAND` 时，系统运行时将返回一加 Ace 2 的硬件配置信息。
