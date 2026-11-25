---
id: "google-pixel-boot-animation-dark"
title: "Google Pixel Boot Animation (Dark)：纯黑开机动画视觉定制"
sidebarTitle: "Pixel 纯黑开机动画"
description: "无侵入式替换原厂开机画面为 Google Pixel 官方深色开机动画，呈现流畅 60 FPS 四色几何粒子动态效果与 OLED 纯黑背景。"
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "Google Pixel 开机动画 Magisk"
  - "Pixel 深色开机动画 zip"
  - "Pixel 60帧开机动画 Root"
  - "谷歌开机动画 Magisk 模块"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他修改 /system/media/bootanimation.zip 或 product 分区媒体资源的模块"
configPaths:
  - "/system/media/bootanimation.zip"
  - "/system/product/media/bootanimation.zip"
features:
  - "将厂商原厂启动画面替换为简洁的 Google Pixel 字体与动画"
  - "以流畅的 60 FPS 帧率渲染，确保开机过渡丝滑无卡顿"
  - "专为 OLED 与 AMOLED 屏幕优化的 #000000 纯黑背景"
  - "支持多挂载目标，兼容各品牌机型下的 /system/media 与 /system/product/media 路径"
faq:
  - question: "为什么开机动画未能正确适配我的屏幕分辨率？"
    answer: "该动画已在 desc.txt 中内置标准的 1080p 与 1440p 自适应缩放参数。现代 Android 系统的 bootanimation 二进制程序会自动按设备屏幕分辨率缩放帧画面。"
  - question: "这会修改 Bootloader 阶段的第一屏开机 Logo 吗？"
    answer: "不会。开机动画仅负责启动流程的第二阶段（即 Linux 内核将控制权移交至用户空间 init 进程之后）。初始厂商 Splash Logo 存储在只读的 bootloader 或 splash 分区中。"
---

## 概述

**Google Pixel Boot Animation (Dark)**（由 Kuku de RCOL 打包）是一款精致的视觉定制模块，可将 Google 极简风格的深色模式 Pixel 开机动画引入任意已获取 Root 权限的 Android 设备。

Samsung、Xiaomi、Oppo 等厂商的原生开机动画往往采用高对比度的刺眼白底画面和冗长的品牌展示。该模块将这些资源替换为纯黑背景上的经典 Google 四色变形几何动画，既能减轻夜间重启时的视觉疲劳，又能带来原生态的 Google 视觉体验。

---

## 技术架构与工作原理

Android 通过由 `init` 进程拉起的 `/system/bin/bootanimation` 守护进程来渲染开机画面：

### 1. 文件覆盖目标解析

根据不同 OEM 厂商的分区布局以及 Android 版本（Android 10 至 15），开机动画位于不同目录中：

- `/system/media/bootanimation.zip`：传统 AOSP 及早期 OEM 厂商的默认路径。
- `/system/product/media/bootanimation.zip`：Android 11+ 动态分区（Dynamic Partition）设备的现代目标路径。

该模块会以无系统分区修改（Systemless）的方式将高帧率 `bootanimation.zip` 同时绑定挂载到上述两个目标路径，无论 ROM 从 `/system` 还是 `/product` 加载资源都能确保兼容。

### 2. 动画包内部结构

ZIP 压缩包内部由以下部分组成：

- `desc.txt`：定义视口分辨率（例如 1080 2400）、目标帧率（60 fps）及循环逻辑。
- `part0/`：开场序列，展示 Google 粒子汇聚动画。
- `part1/`：无限循环序列，持续播放直至系统框架发出 `sys.boot_completed=1` 信号。

---

## 故障排查与验证

- **免重启直接预览**：可通过 Root Shell 直接测试开机动画效果：
  ```bash
  su -c "bootanimation"
  ```
  *（按 Ctrl+C 或终止该进程即可退出预览）。*
- **高速启动设备**：在搭载超高速 UFS 4.0 闪存的设备上，系统可能在完整动画播放完毕前即完成启动。一旦锁屏界面就绪，Android 会立即终止动画守护进程，这属于正常行为。
