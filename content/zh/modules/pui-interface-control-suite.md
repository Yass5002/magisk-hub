---
id: "pui-interface-control-suite"
title: "PUI System Interface & Control Suite：ColorOS 15 与 OxygenOS 15 界面控制中心美化套件"
sidebarTitle: "PUI 界面控制套件"
description: "专为 ColorOS 15 与 OxygenOS 15 固件打造的系统界面深度定制与控制中心主题覆盖模块。"
category: "customization-ui"
tier: 1
searchQueries:
  - "PUI for OS15 Magisk 模块"
  - "ColorOS 15 控制中心美化模块"
  - "OxygenOS 15 状态栏主题定制"
  - "PUI 主题定制 Root 模块下载"
prerequisites:
  - "运行 ColorOS 15 或 OxygenOS 15（Android 15）的 OnePlus、OPPO 或 Realme 设备"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他针对 ColorOS 15 的 SystemUI 界面覆盖（Overlay）模块"
configPaths:
  - "/system/product/overlay/PUIThemeCustomized.apk"
  - "/system/system_ext/overlay/PUIThemeCustomized.apk"
features:
  - "专为 Android 15 视觉层级与重构版快捷设置面板量身定制"
  - "重绘控制中心亮度条与音量滑块，呈现更精致的人体工学圆角曲线"
  - "深度定制通知卡片、状态栏图标以及快捷开关激活态视觉样式"
  - "采用无破坏性的 RRO（运行时资源覆盖）架构，无需修补系统框架二进制文件"
faq:
  - question: "可以在 ColorOS 13 或 14 等旧版系统上使用该模块吗？"
    answer: "不可以。本套件严格基于 ColorOS 15 与 OxygenOS 15 的资源 ID 与 XML 布局结构编译。若在旧版 Android 系统上强行刷入，可能导致主题无法生效，甚至引发 SystemUI 强制停止（FC）。"
  - question: "使用该模块需要依赖 Xposed 或 LSPosed 框架吗？"
    answer: "不需要。本模块通过 Magisk 无系统分区加载 Android 原生运行时资源覆盖（RRO）机制，全程无需任何代码挂钩（Hook）或 ART 运行时修补。"
---

## 概述

**PUI System Interface & Control Suite**（由 Tiansansha 与 PanL 创作）是一款专为搭载 ColorOS 15 与 OxygenOS 15 的新一代 OPPO、OnePlus 及 Realme 设备量身打造的定制化界面美化模块。

Android 15 对 SystemUI 布局层级与通知栏架构进行了大幅调整。PUI 套件引入了一套优雅统一的视觉方案，全面优化了 ColorOS 15 控制中心的毛玻璃通透感、滑块动效比例与快捷开关几何形态。

---

## 技术架构与工作原理

本模块通过 Android 原生的运行时资源覆盖（RRO，Runtime Resource Overlay）子系统无缝融入系统：

### 1. 资源覆盖注入

模块会无侵入挂载预编译的覆盖层 APK：

```bash
/system/product/overlay/PUIThemeCustomized.apk
```

这些覆盖层直接接入 `com.android.systemui` 与 `com.oplus.systemui` 的框架资源表，在不触及已编译 Java/smali 字节码的前提下，直接覆写界面尺寸、配色与 Drawable 图形资源。

### 2. 控制中心人体工学优化

- **滑块几何重调**：重新调校亮度条与音量滑块的宽高比和圆角半径，提供更宽裕舒适的触控热区。
- **微交互动画**：增强切换蓝牙、Wi-Fi 与蜂窝网络磁贴时的触控视觉反馈。

---

## 故障排查与生效验证

- **使修改生效**：刷入后必须完整重启系统，以便 Android 的 `idmap2` 守护进程重新注册并链接新的资源覆盖层。
- **主题冲突**：若当前启用了第三方 Substratum 主题或官方主题商店主题，请在系统设置中恢复默认主题后再激活本模块。
