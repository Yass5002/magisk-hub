---
id: "miui-perfect-icons"
title: "MIUI Perfect Icons HD Suite：2K 统一矢量图标套件"
sidebarTitle: "MIUI 完美图标"
description: "专为小米 MIUI 桌面打造的图标统一美化套件，将杂乱且低分辨率的第三方应用图标替换为锐利的 2K 矢量超椭圆图标并清除广告角标。"
category: "customization-ui"
tier: 1
searchQueries:
  - "MIUI Perfect Icons 完美图标 Magisk"
  - "小米桌面 2K 高清矢量图标模块"
  - "MIUI 统一超椭圆图标 Root"
  - "去除小米桌面图标广告角标 Magisk"
prerequisites:
  - "运行 MIUI 12+ 或 HyperOS 的小米、Redmi 或 POCO 设备"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他覆盖 /system/media/theme/default/icons 的模块"
configPaths:
  - "/system/media/theme/default/icons"
features:
  - "2K 高清纹理渲染，在 WQHD+ 与 120Hz 高分高刷屏幕上彻底消除图标发虚"
  - "为系统应用与第三方安装包强制统一超椭圆（Squircle）几何轮廓"
  - "清除商业应用图标上烦人的促销角标与广告丝带装饰"
  - "无侵入式叠加覆盖默认桌面图标缓存，不修改 /system 分区"
faq:
  - question: "如果重启后部分图标没有立即变化，该如何刷新？"
    answer: "请进入 设置 -> 应用设置 -> 应用管理 -> 系统桌面，点击强制停止后清除桌面缓存；或者在主题壁纸中切换一次系统默认主题以重建图标缓存。"
  - question: "这套图标包支持后续从 Play 商店新安装的应用吗？"
    answer: "支持。套件内置了自动背景遮罩规则，能够动态将未单独适配的第三方应用图标规范框选进统一风格的超椭圆容器中。"
---

## 概述

**MIUI Perfect Icons HD Suite（MIUI 完美图标高清套件）**（由 Move.p 整理制作）是一款无侵入式（Systemless）视觉美化模块，专为解决小米 MIUI 与 HyperOS 桌面常见的图标风格割裂问题而设计。

尽管小米为自家系统应用配备了精致的原厂图标，但通过 Google Play 或国内应用商店安装的第三方应用，往往会渲染出边框不齐、位图分辨率偏低甚至带有促销广告横幅的图标。Perfect Icons 通过叠加精选 2K 高清矢量资源库与动态遮罩滤镜，呈现出整洁统一的高级桌面美感。

---

## 技术架构与工作原理

小米系统桌面通过系统主题引擎解析应用图标资源：

### 1. 主题资源绑定挂载

模块通过无侵入绑定挂载方式，将统一图标包覆盖至以下路径：

```bash
/system/media/theme/default/icons
```

当桌面启动或 `ThemeManager` 编译桌面图标缓存时，系统会直接从该路径读取矢量可绘制资源（Drawable）及预渲染的 2K 位图。

### 2. 几何遮罩与广告角标剥离

- **自适应超椭圆遮罩**：对于尚未提供专属矢量替换图标的应用，内置的 `transform_config.xml` 会自动套用经过校准的超椭圆蒙版与投影效果，使其与小米官方图标几何曲率保持一致。
- **角标清除**：许多商业软件会在安装包图标内硬编码节日大促或周年庆丝带角标。该模块会直接用干净纯粹的品牌原标予以替换。

---

## 故障排查与验证

- **清理图标缓存**：如果个别图标仍停留在低分辨率旧缓存状态，可在终端执行以下指令重启桌面：
  ```bash
  killall com.miui.home
  ```
- **恢复出厂图标**：在 Root 管理器中禁用该模块并重启设备，即可瞬间还原标准 MIUI 原厂图标。
