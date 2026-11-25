---
id: "gphotosunlimited"
title: "GPhotosUnlimited：面向 Google 相册的无侵入式 Pixel 机型伪装"
sidebarTitle: "GPhotosUnlimited"
description: "通过专门针对 Google 相册应用伪装 Google Pixel 硬件型号，解锁无限量原画质与节省空间画质云端备份。"
category: "customization-ui"
tier: 1
searchQueries:
  - "GPhotosUnlimited Magisk 模块"
  - "Google 相册无限备份 Root"
  - "Rev4N1 GPhotosUnlimited 下载"
  - "仅针对 Google 相册伪装 Pixel"
  - "Magisk 解锁谷歌相册无限存储"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "官方版 Google 相册应用（`com.google.android.apps.photos`）"
conflicts:
  - "暂无与其他模块的已知冲突记录；但修改系统全局 build 属性的全局机型伪装模块可能会覆盖本模块设置"
configPaths:
  - "/data/adb/modules/gphotosunlimited/"
features:
  - "定向单应用伪装：仅针对 Google 相册修改设备属性，其余所有应用均保留真实机型标识"
  - "无限云端存储空间：解锁无限量原画质或高画质照片与视频备份"
  - "降低账号风控风险：精确模拟初代 Pixel（marlin）或 Pixel 5 特性，符合 Google 服务器校验规则"
  - "交互式终端安装程序：可在刷入模块过程中按提示选择偏好的备份配置档案"
  - "无系统分区修改（Systemless）：保持 `/system` 分区完整，支持干净卸载"
faq:
  - question: "GPhotosUnlimited 会更改我在其他应用或游戏中的机型显示吗？"
    answer: "不会。不同于直接全局编辑 `/system/build.prop` 的旧式机型伪装模块，GPhotosUnlimited 将属性覆盖严格隔离在 `com.google.android.apps.photos` 进程内部。"
  - question: "该模块解锁的是原画质还是节省空间画质的无限备份？"
    answer: "这取决于你在刷入时选择的设备配置文件（Pixel 1 或 Pixel 5）：模拟初代 Pixel 可解锁终身无限原画质备份，选择 Pixel 5 则解锁无限节省空间画质备份。"
---

## 概述

由 **Rev4N1** 开发的 **GPhotosUnlimited** 是一款无系统分区修改（Systemless）定制模块，用于在 **Google 相册** 中免费开启无限量照片与视频备份。

Google 曾为早期 Pixel 系列机型提供终身无限云端存储权益。GPhotosUnlimited 会在 Google 相册启动时向其应用进程注入定向构建属性覆盖，使 Google 服务器判定媒体上传来自符合条件的 Pixel 设备，同时完全不改动系统全局设备标识。

---

## 技术架构与工作原理

### 定向应用属性注入

该模块通过限定作用域的属性挂钩（Hook）机制工作：

1. **进程识别**：监测 `com.google.android.apps.photos` 进程的启动。
2. **属性替换**：在目标应用的内存空间内覆盖运行时构建属性（`ro.product.model`、`ro.product.manufacturer`、`ro.product.brand`），将其模拟为合法的 Pixel 硬件（例如 Pixel XL `marlin`）。
3. **全局隔离**：系统应用、银行类应用与手机游戏仍读取真实的 OEM 设备属性。

---

## 安装与配置

1. 下载最新版本的 `GPhotosUnlimited-*.zip` 发布包。
2. 在 Magisk、KernelSU 或 APatch 中刷入该模块。
3. 根据终端交互提示选择所需的 Pixel 配置档案。
4. 重启设备。
5. 打开 **Google 相册 > 设置 > 备份**，确认无限存储空间状态已生效。

---

## 配置与使用

如果重启后 Google 相册未能立即显示无限备份状态：
- 前往 **设置 > 应用 > Google 相册 > 存储**，执行**清除缓存**与**清除数据**。
- 重新打开应用并完成初始配置。

---

## 故障排查与常见问题

- **备份仍消耗存储配额**：请确保在安装模块后已清除 Google 相册应用缓存，以便应用重新向 Google 服务器校验设备的备份权益。
