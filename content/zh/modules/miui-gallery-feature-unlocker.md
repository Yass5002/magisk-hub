---
id: "miui-gallery-feature-unlocker"
title: "MIUI Gallery AI 功能解锁模块：小米相册旗舰修图套件"
sidebarTitle: "MIUI Gallery+"
description: "为全系小米机型解锁小米相册中受机型限制的旗舰摄影与神经网络编辑功能，涵盖 AI 魔法消除、魔法抠图与动态换天滤镜。"
category: "system-utilities"
tier: 1
searchQueries:
  - "MIUI 相册 AI 功能解锁 Magisk"
  - "小米相册魔法抠图模块下载"
  - "MIUI 相册解锁证件照与魔法换天"
  - "HyperOS 相册 AI 编辑 Magisk 模块"
prerequisites:
  - "运行 MIUI 12+ 或 HyperOS 的小米、Redmi 或 POCO 设备"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他同样覆盖修改 /system/priv-app/MiuiGallery/ 目录的模块"
configPaths:
  - "/system/priv-app/MiuiGallery/MiuiGallery.apk"
features:
  - "绕过硬件与 SoC 机型白名单校验，开启旗舰级神经网络修图功能"
  - "在相册编辑器中解锁魔法抠图与 AI 路人/杂物消除算法"
  - "启用影棚级智能证件照生成及纯色背景替换功能"
  - "激活风景照片的动态魔法换天滤镜与天气动画效果"
  - "开启文档拍摄去摩尔纹增强与几何透视畸变矫正"
faq:
  - question: "使用这些 AI 修图功能需要联网吗？"
    answer: "部分高阶计算摄影功能（例如神经网络魔法换天或高精度杂物消除）在首次启动时需要从小米服务器下载对应的离线 AI 插件模型。"
  - question: "该模块可以刷入非小米的第三方 AOSP 类原生系统吗？"
    answer: "不可以。修改后的 APK 高度依赖小米专有系统框架（MiuiFramework.jar），仅严格兼容 MIUI 或小米 HyperOS 固件。"
---

## 概述

**MIUI Gallery AI 功能解锁模块**（由 Xiao Chen Tongxue 制作）是一款无侵入式（Systemless）增强模块，通过对小米原厂相册应用进行修补，解除其中的设备分级限制与特定处理器功能屏蔽。

小米长期将魔法抠图、神经网络杂物消除、动态魔法换天以及文档防反光去摩尔纹等高阶计算摄影编辑功能限制在高端旗舰机型上。本模块通过提供预先修补的相册安装包，让中端及入门级 Redmi 与 POCO 设备也能完整体验这些旗舰修图特性。

---

## 技术架构与工作原理

小米相册通过客户端侧的设备能力标志位（`DeviceFeature` 以及 `Build.DEVICE` / `Build.MODEL` 校验）来控制功能入口的显隐：

### 1. 功能开关覆写

修补后的相册二进制文件直接覆写了内部能力判定方法：

- `isSupportMagicErase()` -> `return true`
- `isSupportIdPhoto()` -> `return true`
- `isSupportSkyFilter()` -> `return true`
- `isSupportDocumentDeMoire()` -> `return true`

### 2. Systemless 特权覆盖挂载

模块将增强后的相册安装包部署至：

```bash
/system/priv-app/MiuiGallery/MiuiGallery.apk
```

借助 Magisk 的 overlayfs / 绑定挂载机制，原始系统镜像保持完好无损。应用在保留系统签名权限的同时无缝替换原厂内置相册，既不会清除用户原有相册照片，也不会破坏本地媒体库索引。

---

## 故障排查与验证

- **更新 AI 插件**：首次使用魔法消除或魔法换天时，点击对应滤镜后应用会提示下载离线 AI 组件（约 50–150 MB），请保持 Wi-Fi 网络畅通。
- **缓存未刷新问题**：若新功能菜单未立即出现，请前往 **设置 > 应用设置 > 应用管理 > 相册**，强行停止相册并清除应用缓存后重新打开。
