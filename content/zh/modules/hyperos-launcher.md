---
id: "hyperos-launcher"
title: "HyperOS Launcher Mod：解锁桌面网格、动效与手势增强"
sidebarTitle: "HyperOS Launcher"
description: "修改版小米澎湃 OS 系统桌面，解锁更多桌面图标网格、文件夹布局、动画参数调优以及全面屏手势优化。"
category: "customization-ui"
tier: 1
searchQueries:
  - "HyperOS Launcher 修改版 Magisk"
  - "Kashi HyperOS 桌面模块"
  - "澎湃 OS 桌面解锁网格布局"
  - "小米澎湃桌面个性化定制"
  - "澎湃系统桌面 APK 修改版 Root"
prerequisites:
  - "小米澎湃 OS（HyperOS）ROM（Android 14 及以上）"
  - "Magisk 或 KernelSU"
conflicts:
  - "AOSP、Pixel、LineageOS 或其他非 MIUI/HyperOS 系统（严格仅适用于小米澎湃 OS）"
configPaths:
  - "/data/adb/modules/HyperOS-Launcher/"
features:
  - "扩展桌面网格布局：突破原厂限制，解锁更多桌面排列规格（如 5x7、6x7、7x8）"
  - "自定义文件夹维度：支持调整大文件夹及普通文件夹的图标行列数"
  - "增强手势动画：针对高刷新率屏幕精细调校应用启动与退出的物理曲线"
  - "Systemless APK 挂载：安全替换原厂 `com.miui.home`，不破坏系统分区完整性"
  - "图标文字标题控制：自由开关桌面图标文字显示、调整标题大小与字体缩放"
faq:
  - question: "可以把这个模块刷入 AOSP 或 Pixel 类原生设备吗？"
    answer: "不可以。HyperOS 桌面严重依赖小米私有框架库（MIUI/HyperOS 框架、主题服务与物理动画引擎）。在非小米系统上刷入会导致启动器立即崩溃闪退。"
  - question: "刷入后如果系统桌面持续报错闪退怎么办？"
    answer: "请进入 设置 > 应用设置 > 应用管理 > 系统桌面，清除全部数据与缓存后重启手机。若不慎引发 Bootloop（卡开机），请通过 Root 管理器的安全模式或 TWRP 移除该模块。"
---

## 概述

由 **kakashi1v1** 与 **Mods-Center** 共同维护的 **HyperOS Launcher Mod**，为小米旗舰级 **澎湃 OS 系统桌面**（`com.miui.home`）带来了功能全面解锁的增强版本。

尽管原版澎湃 OS 已具备流畅的动画与简洁布局，但小米仍在国际版或部分机型固件中限制了桌面网格尺寸、文件夹排布及动画曲线等高阶定制项。本模块通过 Systemless 方式挂载经过优化的桌面安装包，解除上述隐藏限制。

---

## 技术架构与工作原理

### 框架覆盖与包绑定机制

该模块采用无系统分区修改的 APK 替换方式运行：

1. **Systemless 挂载**：设备开机阶段，模块会将修改后的 `MIUIHome.apk` 覆盖挂载至 `/system/priv-app/` 或 `/product/priv-app/` 下的系统桌面目录。
2. **特性标志解锁**：直接修补内部 Smali 字节码以绕过区域及硬件分级限制，在桌面设置中暴露出隐藏的高级配置选项。
3. **硬件加速保留**：完整保留与小米私有物理动效引擎及底层毛玻璃模糊着色器的兼容集成。

---

## 安装与配置

1. 确认设备正在运行 **小米澎湃 OS（HyperOS）**（Android 14+）。
2. 下载最新版 `HyperOS-Launcher-*.zip` 发布包。
3. 在 Magisk 或 KernelSU 中刷入模块。
4. 重启设备。
5. 长按桌面空白处，点击 **设置 > 更多设置** 即可访问所有已解锁的桌面定制选项。

---

## 配置与使用

进入“桌面设置”后，你可以配置：
- **桌面布局**：选择高密度网格比例，如 `5x7`、`6x7` 或 `6x8`。
- **文件夹列数**：自定义大文件夹内的图标排布密度。
- **隐藏应用名称**：关闭图标下方文字标签，打造极简无字桌面风格。

---

## 故障排查与常见问题

- **首次开机后桌面略有卡顿**：小米系统桌面需要重建图标数据库索引。初次重启后请静待 1–2 分钟待后台索引完成，如有需要可手动清理桌面缓存。
