---
id: "miui-camera-feature-expansion"
title: "MIUI 相机功能扩展：完整特性标志与解锁能力指南"
sidebarTitle: "MIUI 相机功能扩展"
description: "无侵入式（Systemless）相机增强模块，为小米设备开启受限摄影功能、480FPS 慢动作、超级月亮、Vlog 与多摄同开录制。"
category: "customization-ui"
tier: 1
searchQueries:
  - "MIUI 相机功能补全扩展 Magisk 模块"
  - "小米手机 Root 开启超级月亮模式"
  - "MIUI 解锁 480fps 慢动作模块"
  - "小米 10 多摄同开导演模式修改版"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "运行官方 MIUI 或 HyperOS 的小米、Redmi 或 POCO 设备"
conflicts:
  - "其他替换 MiuiCamera.apk 的模块"
configPaths:
  - "/system/priv-app/MiuiCamera/MiuiCamera.apk"
  - "/data/adb/modules/MIUI_MiuiCamera/install.sh"
features:
  - "为所有受支持机型开启超级月亮、长曝光、魔法分身、电影画幅与 Vlog 模式"
  - "为小米 10 与小米 10S 解锁 480 FPS 慢动作视频录制"
  - "开启多摄同开并发录制（支持最多 3 个取景画面同时录制的导演模式）"
  - "解锁超级防抖 Pro、录音变焦以及自定义专业模式摄影配置文件"
faq:
  - question: "如果我的手机传感器不支持某项模式，开启后会导致相机闪退吗？"
    answer: "对于依赖特定硬件能力的模式（例如依赖高倍长焦的超级月亮，或依赖多 ISP 吞吐量的三摄同录），如果底层传感器 ISP 无法支持请求的图像流，相机应用会自动优雅隐藏或回退至标准处理逻辑。"
  - question: "该模块会修改相机 HAL 或厂商底层驱动文件吗？"
    answer: "不会。它仅以无侵入方式替换用户态特权系统应用 /system/priv-app/MiuiCamera/MiuiCamera.apk，从而开启 OEM 开发者在中低端机型的原厂 ROM 中屏蔽的软件特性开关。"
---

## 概述

**MIUI Camera Feature Completion & Expansion（小米相机功能补全与扩展）**（由晓晨同学 & xing1225 制作）能够解锁小米在部分中端机型及地区版 ROM 中人为隐藏的丰富影像与视频录制算法。

小米相机的代码库在旗舰机与中低端机型之间共用同一套统一引擎，高级功能仅通过设备特性配置表进行选择性开关。该模块提供经过完整修补的 `MiuiCamera.apk`，可在受支持的骁龙（Snapdragon）与联发科（MediaTek）硬件平台上激活高阶影像功能。

---

## 技术架构与工作原理

### 1. 特权应用叠加覆盖

模块将修改后的 `MiuiCamera`（v4.3.001951.0，版本号 211030）直接挂载至特权系统应用目录：

```text
/system/priv-app/MiuiCamera/
└── MiuiCamera.apk
```

由于挂载位置处于 `/system/priv-app/`，该应用能够完整保留所需的系统私有权限，包括：

- `android.permission.CAMERA`
- `android.permission.CONTROL_CAMERA_SESSION`
- 访问厂商专有相机 HAL 扩展接口（`vendor.xiaomi.hardware.camera.provider`）。

### 2. 已解锁的影像能力

修改版应用覆写了设备特性检测字段（`support_camera_*`），从而解锁以下功能：

- **超级月亮模式（Super Moon Mode）**：AI 月球纹理合成与长焦曝光优化。
- **魔法分身模式（Clone Mode）**：分身创意拍照与视频分段合成。
- **电影画幅（Movie Frame）**：2.39:1 电影宽银幕比例遮罩。
- **录音变焦（Audio Zoom）**：长焦录像过程中的波束成形定向收音变焦。
- **480 FPS 慢动作**：在小米 10 与小米 10S 上开启高帧率传感器读出。
- **多摄同开导演模式（Multi-Camera Director）**：在旗舰平台上实现三颗镜头同步录像。

---

## 验证与故障排查

1. 安装完成后先清除相机应用数据：**设置 -> 应用设置 -> 应用管理 -> 相机 -> 清除数据**。
2. 启动相机并向右滑动进入 **更多** 菜单，即可查看新激活的拍摄模式。
