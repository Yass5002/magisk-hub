---
id: "minecraft-boot-animation"
title: "Minecraft Pixel Boot Animation：复古像素方块合成开机模块"
sidebarTitle: "Minecraft 开机动画"
description: "面向 Magisk、KernelSU 与 APatch 的无侵入式开机动画替换模块，呈现复古 8-bit Minecraft 方块生成与合成启动序列。"
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "Minecraft 开机动画 Magisk"
  - "我的世界像素开机动画 安卓 Root"
  - "Minecraft 草方块 bootanimation zip"
  - "复古游戏开机动画 Root 模块"
prerequisites:
  - "Magisk 16.6+、KernelSU 或 APatch"
  - "任意分辨率的 Android 智能手机屏幕"
conflicts:
  - "其他修改 /system/media/bootanimation.zip 的模块"
configPaths:
  - "/system/media/bootanimation.zip"
features:
  - "等距像素风 Minecraft 方块合成与搭建动画"
  - "185 KB 超轻量体积，存储读取速度极快"
  - "系统初始化期间实现零电量与零 CPU 额外负担"
  - "广泛兼容各类 Android ROM 与 Root 环境"
faq:
  - question: "为什么这个模块的体积如此小巧（不足 200 KB）？"
    answer: "像素艺术资源具备极高的压缩效率。借助索引调色板技术，整套多帧动画在保持高视觉清晰度的同时，几乎不占用额外的存储与内存开销。"
---

## 概述

**Minecraft Pixel Boot Animation**（由 Wei Bin Guo 打包）为已获取 Root 权限的 Android 设备注入了怀旧的像素游戏气息。

该模块将厂商原厂开机画面替换为像素风 Minecraft 方块合成动画，在进入 Android 系统锁屏前逐块搭建起一个立体的泥土草方块模型。

---

## 技术架构与工作原理

模块向 `/system/media/` 挂载了一个精简高效的 `bootanimation.zip`：

```text
bootanimation.zip (185 KB)
├── desc.txt
├── part0/            # Pixel block assembly sequence
└── part1/            # Subtle animated pixel shimmer loop
```

得益于极小的文件体积，SurfaceFlinger 纹理缓冲区的内存分配开销低于 4 MB，非常适合老旧机型或注重启动性能的用户使用。
