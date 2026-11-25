---
id: "leica-camera-port"
title: "Leica Camera MIUI Port & Color Profiles：小米徕卡相机移植指南"
sidebarTitle: "Leica Camera Port"
description: "无系统分区修改的小米相机特权应用移植模块，为小米及 Redmi 设备解锁官方徕卡经典与徕卡生动色彩风格、徕卡水印及进阶 ISP 调优。"
category: "customization-ui"
tier: 1
searchQueries:
  - "徕卡相机 Magisk 模块"
  - "MIUI 徕卡相机移植版"
  - "小米解锁徕卡经典和徕卡生动"
  - "徕卡水印相机 APK Root"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "运行官方 MIUI 或澎湃 OS（HyperOS）的 Xiaomi、Redmi 或 POCO 设备"
conflicts:
  - "其他替换 MiuiCamera 的相机模块"
configPaths:
  - "/system/priv-app/MiuiCamera/MiuiCamera.apk"
  - "/data/adb/modules/LeicaCamera/service.sh"
features:
  - "解锁正统“徕卡经典”（高对比度德味影调）与“徕卡生动”双画质调校模式"
  - "支持在拍摄照片底部自动生成官方徕卡联名品牌水印框"
  - "内置预编译的 Dalvik/ART oat 运行时优化缓存，确保相机冷启动零卡顿"
  - "广泛适配小米 10 至尊纪念版、小米 11 Ultra、Redmi K40、K50 及更新系列机型"
faq:
  - question: "刷入后会覆盖我原有的相册照片或相机设置吗？"
    answer: "该模块仅以 Systemless 方式替换系统相机应用包，不会影响相册照片。首次打开新版相机时参数设置可能会重置为默认，重新配置你偏好的水印和画幅比例即可。"
  - question: "首次开机后相机闪退怎么解决？"
    answer: "请前往 设置 -> 应用设置 -> 应用管理 -> 相机 -> 清除全部数据，然后重新授予相机与存储读写权限。"
---

## 概述

**Leica Camera MIUI Port & Color Profiles**（由 晚风秋词 移植打包）将小米备受赞誉的徕卡影像联名体验带到了出厂未获徕卡授权的机型上。

---

## 技术架构与工作原理

本模块在 `/system/priv-app/MiuiCamera/` 目录下以无系统分区修改方式挂载定制版 `MiuiCamera.apk`（v4.3.04750.0）：

```text
/system/priv-app/MiuiCamera/
├── MiuiCamera.apk
├── lib/arm64/
└── oat/arm64/
    ├── base.art
    ├── base.odex
    └── base.vdex
```

通过随包附带预编译的 ART 字节码缓存（`.odex`、`.vdex`），大幅降低了相机应用的冷启动延迟；修改版安装包同时向小米相机图像处理管线注入了徕卡色彩校准查找表（LUT）。
