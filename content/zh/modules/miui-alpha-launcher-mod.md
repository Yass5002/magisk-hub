---
id: "miui-alpha-launcher-mod"
title: "MIUI Alpha Launcher Mod：流畅动画与深度桌面定制"
sidebarTitle: "MIUI 内测桌面修改版"
description: "经过精修的小米 Alpha 系统桌面版本，提供自定义主屏幕网格、隐藏应用、文件夹展开特效以及系统级模糊物理效果。"
category: "customization-ui"
tier: 1
searchQueries:
  - "MIUI Alpha 桌面修改版 Magisk"
  - "小米桌面双击空白处锁屏模块"
  - "MiuiHome 修改版 Root 模块"
  - "小米桌面文件夹高斯模糊 Magisk"
prerequisites:
  - "运行 MIUI 13、MIUI 14 或 HyperOS 的小米、Redmi 或 POCO 设备"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他覆盖 /system/priv-app/MiuiHome/ 目录的模块"
configPaths:
  - "/system/priv-app/MiuiHome/MiuiHome.apk"
features:
  - "支持在桌面空白处双击熄屏并锁定屏幕"
  - "解锁高自由度桌面网格密度选项（4x6、4x7、5x6、5x7、6x7）"
  - "开启原生文件夹展开弹性动画与高斯背景模糊效果"
  - "支持直接在桌面设置中安全隐藏指定应用图标"
  - "优化滑动手势响应速度以及应用启动/退出动画曲线"
faq:
  - question: "安装或更新后，现有的桌面布局和小组件位置会被重置吗？"
    answer: "不会。由于模块完整保留了位于 /data/data/com.miui.home/ 的底层 com.miui.home 数据库，更新后原有的应用快捷方式与桌面小组件布局都会完好保留。"
  - question: "Android 12 到 Android 14 系统上都能开启文件夹背景模糊吗？"
    answer: "高端 SoC（如骁龙 870、888、8 Gen 1 及以上平台）均完整支持文件夹模糊效果；在部分中低端机型上，小米硬件渲染策略可能会出于节省 GPU 带宽的考虑禁用实时高斯着色器。"
---

## 概述

**MIUI Alpha Launcher Mod**（由 Hanhan Hatsune 编译修改，并融合 Sipollo 与 Xposeded 的上游贡献）将小米原厂桌面升级为功能丰富、响应迅捷的高性能系统桌面。

小米通常会将诸如高密度网格布局、流体文件夹模糊、手势快捷操作以及应用图标隐藏等实验性特性限制在内测通道或特定旗舰机型中。该模块通过无侵入方式挂载经过优化的 Alpha 内测桌面版本，为所有受支持设备解锁这些隐藏定制开关。

---

## 技术架构与工作原理

小米系统桌面作为特权系统组件（`MiuiHome.apk`）运行：

### 1. 无侵入二进制挂载

模块将修改后的安装包绑定挂载至以下路径：

```bash
/system/priv-app/MiuiHome/MiuiHome.apk
```

通过保留 OEM 签名对齐以及正确的 SELinux 安全上下文（`u:object_r:system_file:s0`），Android 包管理器会将其无缝识别为合法的系统应用更新。

### 2. 自定义能力覆写

经过修补的 smali 代码解锁了多项隐藏特性：

- `isSupportDoubleTapSleep()`：将桌面手势监听器绑定至 `PowerManager.goToSleep()`。
- `getGridRowColumnList()`：向桌面设置注入最高支持 6 列 × 7 行的灵活网格选项。
- `isSupportBlur()`：重新启用文件夹与搜索栏的硬件加速 RenderEffect 高斯模糊。

---

## 故障排查与最佳实践

- **手势短暂卡顿**：若刚安装完成时手势略显迟滞，建议再重启一次手机，让 ART 运行时完成 JIT 编译优化。
- **卸载还原**：如需恢复出厂原版桌面，只需在 Magisk 或 KernelSU 中禁用该模块并重启设备，系统分区内置的原版桌面将自动接管控制权。
