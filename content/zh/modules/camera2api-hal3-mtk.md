---
id: "camera2api-hal3-mtk"
title: "Camera2API HAL3 Enabler - Universal MTK：联发科通用 HAL3 开启模块"
sidebarTitle: "Camera2API MTK"
description: "适用于 Android 8–14 联发科（MediaTek）设备的通用 Camera2 API HAL3 与 EIS 开启模块，结合 system.prop、post-fs-data.sh 与按品牌匹配的持久化守护进程防止厂商重置。"
category: "system-environment"
tier: 1
searchQueries:
  - "联发科开启 Camera2API 模块"
  - "MTK HAL3 Magisk 模块下载"
  - "联发科谷歌相机 Camera2API EIS"
  - "camera2api_mtk_universal"
  - "persist.vendor.camera.HAL3.enabled"
prerequisites:
  - "搭载联发科（MediaTek）芯片且运行 Android 8.0 至 Android 14 的设备"
  - "Magisk v19.0+（`minMagisk=1900`）、KernelSU 或 APatch"
conflicts:
  - "其他同时修改 `persist.vendor.camera.HAL3.enabled` 等相机属性的模块"
configPaths:
  - "/data/adb/modules/camera2api_mtk_universal/system.prop"
  - "/data/adb/modules/camera2api_mtk_universal/permission_trigger.sh"
  - "/data/adb/camera2api_mtk.log"
features:
  - "通过 `system.prop` 与早期 `post-fs-data.sh` 阶段执行 `resetprop`，全面启用 Camera2 HAL3 与电子防抖（EIS）属性"
  - "后台 `service.sh` 守护进程每隔 20 秒检测 `ro.product.brand`，为三星、小米/Redmi/POCO、OPPO/realme、vivo、Infinix/Tecno 及类原生（AOSP）设备下发差异化属性防止厂商服务重置"
  - "内置 `permission_trigger.sh` 辅助脚本，可为谷歌相机、系统相机及 Snap 相机一键授予 `CAMERA` 与 `RECORD_AUDIO` 权限"
  - "全程记录品牌识别与属性注入状态至 `/data/adb/camera2api_mtk.log`，便于快速排查"
faq:
  - question: "为什么刷入模块后 Camera2 API Probe 仍显示 `LEGACY` 或 `LIMITED`？"
    answer: "该模块通过系统属性与每 20 秒轮询的 `resetprop` 守护进程强制开启 HAL3 与 EIS，但部分厂商（例如某些三星、OPPO、vivo 联发科机型）会在闭源相机 HAL 动态库或底层固件中硬性屏蔽 HAL3。若底层固件已硬锁，仅靠属性覆盖无法将支持级别提升至 `FULL` 或 `LEVEL_3`。"
  - question: "`service.sh` 每 20 秒循环检查一次是否会明显耗电？"
    answer: "每次循环仅执行一次轻量级的 Shell `case` 分支判断与 `resetprop` 调用，随后休眠 20 秒，CPU 唤醒开销极低；但每次循环都会向 `/data/adb/camera2api_mtk.log` 追加状态日志。"
---

## 概述

**Camera2API HAL3 Enabler - Universal MTK**（模块 ID：`camera2api_mtk_universal`）是由 **AnasBex** 开发的开源（Apache-2.0）模块，专门针对运行 **Android 8 至 Android 14** 的 **联发科（MediaTek / MTK）** 平台设备。许多联发科机型在出厂固件中默认将 Camera2 API 限制为 `LEGACY` 或 `LIMITED`，导致无法正常使用手动曝光、RAW 拍摄或安装第三方谷歌相机（GCam）。

该模块融合了静态 `system.prop` 配置、早期 `post-fs-data.sh` 注入以及按厂商品牌自适应的 `service.sh` 持久化守护进程，确保开机后属性不被系统相机服务重置。

---

## 技术架构与工作原理

解压检查 `Camera2API-MTK-v2026.0102.0421.zip` 可确认其包含以下核心脚本与配置：

### 1. 安装清理（`META-INF/com/google/android/update-binary`）
安装过程中脚本会自动清理旧版 `/data/adb/modules/Camera2API-MTK` 残留目录，释放 `module.prop`、`system.prop`、`post-fs-data.sh`、`service.sh` 与 `permission_trigger.sh`，并为所有脚本赋予 `0755` 可执行权限。

### 2. 静态系统属性（`system.prop`）
在模块挂载阶段预设核心 HAL3 与 EIS 开关：
```ini
persist.vendor.camera.HAL3.enabled=1
ro.vendor.camera.HAL3.enabled=1
persist.camera.HAL3.enabled=1
camera.hal3.enabled=1

persist.vendor.camera.eis.enable=1
persist.vendor.camera.is_mode=4
persist.vendor.camera.enableBusDC=1
persist.vendor.camera.stats.test=5
```

### 3. 早期启动注入（`post-fs-data.sh`）
在 Zygote 启动前重建 `/data/adb/camera2api_mtk.log` 日志，记录 `ro.product.brand`、`ro.product.model` 与 `ro.product.vendor.manufacturer`，并使用 `resetprop` 强制写入基础 HAL3 与 EIS 属性。

### 4. 分品牌持久化守护进程（`service.sh`）
系统启动后，`service.sh` 将 `ro.product.brand` 转为小写并进入间隔 20 秒的守护循环，按设备品牌追加专属参数：
- **`samsung`**：持续强化 `persist.vendor.camera.HAL3.enabled`、`ro.vendor.camera.HAL3.enabled` 与 `persist.vendor.camera.eis.enable`。
- **`xiaomi` | `redmi` | `poco`**：补充设置 `persist.vendor.camera.manufacturer_id=1` 与 `persist.vendor.camera.enableBusDC=1`。
- **`oppo` | `realme`**：额外启用 `persist.vendor.cam.hal3.enabled=1` 及辅助摄像头白名单 `vendor.camera.aux.packagelist "*"`。
- **`vivo`**：强制维持 `persist.vendor.camera.HAL3.enabled` 与 `persist.camera.HAL3.enabled`。
- **`infinix` | `tecno` | `itel`**：维持 HAL3 与 `persist.vendor.camera.eis.enable`。
- **其他通用联发科 / AOSP 设备**：持续守护通用 HAL3 属性。

### 5. 权限辅助脚本（`permission_trigger.sh`）
模块目录内附带 `permission_trigger.sh`，检测到 `com.google.android.GoogleCamera`、`com.android.camera` 或 `org.cyanogenmod.snap` 时，可通过 `pm grant` 自动授予 `CAMERA` 与 `RECORD_AUDIO` 运行时权限。

---

## 安装与效果验证

1. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入 `Camera2API-MTK-v2026.0102.0421.zip`。
2. 重启设备使 `post-fs-data.sh` 与 `service.sh` 生效。
3. 使用 Root 终端或 ADB 检查日志与属性状态：

```bash
# 查看模块运行日志
su -c "tail -n 30 /data/adb/camera2api_mtk.log"

# 检查 Camera2 HAL3 与 EIS 属性值
getprop persist.vendor.camera.HAL3.enabled
getprop ro.vendor.camera.HAL3.enabled
getprop persist.vendor.camera.eis.enable
```

4. 打开 **Camera2 API Probe** 验证硬件支持等级：`LEVEL_3` 或 `FULL` 代表完整支持 HAL3；若仍显示 `LIMITED` 或 `LEGACY`，则说明该机型存在底层厂商固件硬性限制。
