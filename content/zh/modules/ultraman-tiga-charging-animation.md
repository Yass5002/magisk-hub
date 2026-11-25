---
id: "ultraman-tiga-charging-animation"
title: "Ultraman Tiga 迪迦奥特曼锁屏充电动画与音效模块：技术指南"
sidebarTitle: "迪迦充电特效"
description: "基于 Vendor RRO 机制的锁屏充电动画模块，将原生充电画面与提示音替换为迪迦奥特曼神光棒变身光效与音效。"
category: "customization-ui"
tier: 1
searchQueries:
  - "迪迦奥特曼充电动画 Magisk"
  - "MIUI 充电动画修改模块"
  - "澎湃 OS 充电特效 Root 替换"
  - "神光棒充电动画安卓模块"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "搭载原版锁屏框架的 MIUI 12、13、14 或 HyperOS（澎湃 OS）"
conflicts:
  - "其他修改厂商锁屏充电资源的覆盖层（Overlay）模块"
configPaths:
  - "/system/vendor/overlay/充电动画.apk"
  - "/data/adb/modules/ChargeChange/uninstall.sh"
features:
  - "定制神光棒能量光效动画，全面取代默认充电圆环气泡"
  - "接入电源瞬间自动触发经典的迪迦奥特曼变身激活音效"
  - "纯运行时资源覆盖（RRO）设计，零二进制字节码修改"
  - "自带完整卸载清理脚本，卸载即可彻底恢复原版锁屏充电效果"
faq:
  - question: "这个模块会影响小米快充或 Turbo Charge 功率标识显示吗？"
    answer: "不会。该模块仅替换锁屏界面覆盖层中的展示图形资源与音频触发器；底层电池充电协议握手与硬件快充功率协商完全不受影响。"
  - question: "支持哪些 ROM 系统？"
    answer: "该资源覆盖包专为小米 MIUI 与 HyperOS（澎湃 OS）锁屏资源标识符构建。不包含小米 SystemUI 锁屏资源的类原生 AOSP 第三方 ROM 会安全忽略此覆盖层。"
---

## 概述

**Ultraman Tiga Charging Animation & SFX**（由 Fu Chen Ran Xi 制作）为日常插入充电线的锁屏瞬间注入满满情怀，将系统常规充电界面替换为迪迦奥特曼标志性的变身光效与音效。

本模块利用 Android 原生的 **运行时资源覆盖（RRO）** 框架，在不破坏系统 APK 签名、也不修改核心系统库的情况下，干净利落地替换厂商原版充电动画资源与接通提示音。

---

## 技术架构与工作原理

### 1. 运行时资源覆盖（RRO）注入

Android 资源覆盖子系统允许在运行时动态替换应用资源而无需修改基础安装包。本模块会注入以下文件：

```text
/system/vendor/overlay/
└── 充电动画.apk
```

在 `充电动画.apk` 内部，清单文件声明了目标包名、覆盖目标名与优先级配置：

```xml
<overlay
    android:targetPackage="com.android.systemui"
    android:targetName="MiuiKeyguardChargeAnimation"
    android:priority="100"
    android:isStatic="true" />
```

### 2. 资源替换与动画机制

当底层电池驱动通过 `BatteryManager` 广播 `ACTION_POWER_CONNECTED` 事件时，SystemUI 会加载锁屏充电视图。此时覆盖层会接管并替换下列资源：

- **矢量与 Lottie 动画资源**：将原本的同心圆充电波纹替换为多阶段晶体闪烁的神光棒能量变身动画。
- **提示音效**：将系统默认的轻柔充电提示音替换为经典的奥特曼神光棒启动音效。

### 3. 无系统分区可逆清理

模块内置自动化 `uninstall.sh` 卸载脚本，在移除模块时会自动清理 `/data/resource-cache/` 中的临时资源覆盖缓存，防止画面残留错乱。

---

## 安装与验证

1. 通过 Magisk、KernelSU 或 APatch 刷入模块。
2. 重启手机。
3. 熄屏锁屏后插上充电线，屏幕即会点亮并播放迪迦变身动画及专属音效。
