---
id: "pikachu-boot-animation"
title: "Pikachu Animated Boot Sequence：皮卡丘高帧率开机动画模块"
sidebarTitle: "皮卡丘开机动画"
description: "无侵入式高清 60 FPS 皮卡丘动态开机动画模块，以生动的电光粒子特效替换默认厂商启动画面。"
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "皮卡丘开机动画 Magisk"
  - "宝可梦开机动画 安卓 Root"
  - "60帧皮卡丘 bootanimation zip"
  - "自定义动漫开机动画 Magisk"
prerequisites:
  - "Magisk 17.0+、KernelSU 或 APatch"
  - "配备 1080x1920 及以上分辨率屏幕的 Android 智能手机"
conflicts:
  - "任何挂载至 /system/media/bootanimation.zip 的模块"
configPaths:
  - "/system/media/bootanimation.zip"
features:
  - "鲜活细腻的 1080x1920 60 FPS 皮卡丘动态序列帧"
  - "采用无压缩 PNG 帧归档，确保 SurfaceFlinger 高速解码"
  - "内置持续循环段落，无缝播放直至 Zygote 完成初始化"
  - "全面兼容 Magisk、KernelSU 与 APatch 等主流 Root 管理器"
faq:
  - question: "这个动画会在开机时消耗大量电量吗？"
    answer: "不会。开机动画仅在内核初始化完毕至显示管理器启动之间的数秒内运行，一旦系统 UI 加载完成便会立即终止。"
  - question: "在 20:9 或超宽带鱼屏手机上会出现拉伸变形吗？"
    answer: "SurfaceFlinger 在缩放开机动画时会保持原始纵横比，通过黑边适配或自适应居中裁剪的方式渲染，在现代修长屏幕上依然保持画面清晰。"
---

## 概述

**Pikachu Animated Boot Sequence**（由 Ao Jiao Xiao Zheng Tai 制作）是一款充满活力的视觉美化模块，以流畅的 60 FPS 皮卡丘释放十万伏特电光动画替换单调的厂商开机 Logo。

---

## 技术架构与工作原理

### 1. `/system/media/bootanimation.zip` 内部结构

该动画采用 Android 原生 `bootanimation` 程序所需的标准无压缩（`STORE` 仅存储模式）ZIP 封装结构：

```text
bootanimation.zip
├── desc.txt          # Configuration: 1080 1920 60
├── part0/            # Introduction frames: Pikachu charging electricity
└── part1/            # Infinite loop: lightning spark oscillation
```

### 2. 执行流程

1. **内核初始化**：Linux 内核启动并挂载 rootfs 与 vendor 分区。
2. **覆盖挂载**：Magisk 或 KernelSU 将自定义 `bootanimation.zip` 挂载覆盖至 `/system/media/bootanimation.zip`。
3. **启动 SurfaceFlinger**：`/system/bin/surfaceflinger` 启动并拉起 `/system/bin/bootanimation`。
4. **画面渲染**：程序读取 `desc.txt`，将帧纹理预加载至 GPU 显存，并以 60 FPS 帧率输出渲染。
5. **交接桌面**：当 `sys.boot_completed=1` 触发时，动画终止并显现 Android SystemUI 锁屏界面。

---

## 安装与验证

通过你常用的 Root 管理器刷入 `pikachu-boot-animation-v1.0.zip` 后重启设备，即可在开机时体验动态闪电视觉效果。
