---
id: "miui-stacked-recent-tasks"
title: "MIUI 堆叠最近任务桌面：类 iOS 卡片式多任务概览"
sidebarTitle: "MIUI 堆叠后台"
description: "将标准 MIUI 最近任务视图改造为类 iOS 风格横向重叠卡片堆叠界面，带来顺滑物理动效与快捷多任务切换体验。"
category: "customization-ui"
tier: 1
searchQueries:
  - "MIUI 堆叠最近任务 Magisk 模块"
  - "小米 MIUI 类 iOS 堆叠卡片后台"
  - "Xposeded 堆叠桌面 Magisk 下载"
  - "MIUI 横向堆叠多任务修改模块"
prerequisites:
  - "运行 MIUI 12.5、13、14 或 HyperOS 的小米、Redmi 或 POCO 设备"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他修改桌面 smali 或最近任务提供程序的模块"
configPaths:
  - "/system/priv-app/MiuiHome/MiuiHome.apk"
features:
  - "在最近任务界面启用横向重叠卡片堆叠布局"
  - "复刻上滑关闭应用时丝滑的 iOS 弹簧物理动画效果"
  - "保留清晰的内存状态显示栏与一键清理后台功能"
  - "完整兼容全面屏手势导航，切换过程中无手势卡顿"
faq:
  - question: "堆叠布局与 MIUI 原厂纵向双列后台有何区别？"
    answer: "MIUI 默认最近任务采用两列纵向网格排布；而堆叠布局则呈现大尺寸、横向交错重叠的单应用预览卡片，单手滑动浏览更顺手，窗口预览内容也更清晰直观。"
  - question: "如果重启后出现黑屏或桌面无法启动怎么办？"
    answer: "若遇到不兼容的桌面版本冲突，请进入第三方 Recovery（TWRP / OrangeFox）或使用 Magisk 安全模式，删除 /data/adb/modules/ppp 下的对应模块目录即可恢复。"
---

## 概述

**MIUI Stacked Recent Tasks Launcher（MIUI 堆叠最近任务桌面）**（由 Xposeded 引擎驱动，南橘北枳封装为 Magisk 模块）是一款专用的系统界面修改模块，可将小米纵向双列任务切换器替换为灵感源自 iOS 多任务的横向重叠堆叠卡片视图。

对于习惯横向切换后台或觉得双列小预览图难以辨识的用户，该模块通过重构 `MiuiHome.apk` 内部的布局管理器，提供大视野、高清晰度的应用预览窗口与跟手顺滑的手势惯性体验。

---

## 技术架构与工作原理

MIUI 的多任务切换逻辑直接集成在系统桌面应用包内：

### 1. 布局管理器替换

模块覆写了默认的 `RecentsView` 实现：

- 注入自定义横向布局计算逻辑，沿 Z 轴动态偏移每一张后台任务卡片的层叠位置。
- 当后台卡片远离中心焦点时，自动施加分级缩放比例（例如从 0.9x 递减至 0.7x），营造立体景深。

### 2. 手势过渡物理曲线

针对堆叠卡片的交互习惯重新调校触摸手势动画曲线：

- **上滑轻拂**：带惯性物理效果关闭当前焦点应用。
- **下滑操作**：将应用锁定在内存中，防止被一键清理或后台策略自动清除。
- **横向滑动搓动**：在卡片堆叠队列间快速切换，保证高帧率不丢帧。

---

## 故障排查与验证

- **切换布局选项**：请打开 **设置 > 桌面 > 最近任务样式**，确认布局选项已切换为 **横向**（Horizontally）。
- **卡顿或掉帧**：建议确保设备保留至少 3GB 可用运行内存；后台挂起过多重负载应用可能导致老旧处理器出现帧率波动。
