---
id: "pixelupdater"
title: "Pixel Updater：面向已 Root Google Pixel 设备的原生 A/B OTA 更新引擎"
sidebarTitle: "Pixel Updater"
description: "专为已 Root Google Pixel 设备打造的无缝 OTA 更新工具，直接通过原生 update_engine 将系统更新流式写入非活动 A/B 槽位，同时自动保留 Magisk Root 权限。"
category: "system-environment"
tier: 1
searchQueries:
  - "pixelupdater Magisk 下载"
  - "Pixel Root 设备 OTA 更新工具"
  - "Google Pixel 自动 OTA 保留 Root"
  - "update_engine pixel updater 模块"
  - "pixelupdater SELinux 策略"
prerequisites:
  - "支持 A/B 或虚拟 A/B 分区架构的 Google Pixel 智能手机"
  - "Android 13 及以上版本"
  - "Magisk Root 环境"
conflicts:
  - "非 Google Pixel 硬件（三星、小米、一加、摩托罗拉等品牌机型）"
  - "KernelSU 与 APatch（由于依赖 Magisk 专属的 Boot 修补挂钩机制，目前暂不支持）"
configPaths:
  - "/system/priv-app/com.github.pixelupdater.pixelupdater/"
  - "/sdcard/Android/com.github.pixelupdater.pixelupdater/files/"
  - "/data/local/tmp/pixelupdater_selinux.log"
features:
  - "直接集成 `update_engine`：将官方 Google 月度安全更新及大版本系统升级直接流式写入非活动槽位"
  - "自动保留 Magisk：在 OTA 刷写过程中自动修补更新后的非活动槽位，确保重启后持续拥有 Root 权限"
  - "定向 SELinux 域隔离：在开机时建立隔离的 `pixelupdater_app` 策略域以通信调用 `update_engine`，避免暴露过高的系统特权权限"
  - "回滚索引校验：检查 OTA 元数据（`metadata.pb`、`payload_metadata.bin`），防止因意外降级触发 Android Verified Boot（AVB）变砖"
  - "高级维护控制：隐藏调试选项支持同指纹系统重装、日志提取以及重启前撤销已完成的更新"
---

## 概述

Pixel Updater 是一款专为已 Root Google Pixel 设备打造的开源无系统分区修改（Systemless）OTA 更新工具。过去，在已 Root 的 Pixel 手机上安装 Google 月度安全更新需要繁琐的手动流程：暂停系统更新、在电脑端下载完整工厂镜像或 OTA 包、通过 Magisk 手动修补 `init_boot` 或 `boot` 分区，再借助 Fastboot 刷回设备。

Pixel Updater 将整个升级生命周期自动化并集成至手机端本地完成。它以系统特权应用形式配合 Magisk 启动挂钩运行，直接与 Android 原生 `update_engine` 守护进程交互：检测官方 Google OTA 更新包，将分区载荷流式写入并校验至非活动 A/B 槽位，自动将 Magisk Root 修补注入新槽位，随后提示用户无缝重启。

## 前置要求与兼容性

- **硬件设备**：官方 Google Pixel 机型（Pixel 6 系列、Pixel 7 系列、Pixel 8 系列、Pixel 9 系列及更新机型）。
- **Android 版本**：Android 13 及以上版本。
- **Root 方案**：**Magisk**。由于 Pixel Updater 高度依赖 Magisk 的槽位修补集成机制，目前暂不支持 KernelSU 与 APatch。

### 不兼容说明

Pixel Updater 围绕 Google 官方 Pixel OTA 分发架构与元数据规范构建。在其他品牌厂商设备（如三星、小米或一加）上刷入该模块将会失败且无法获取更新。

## 技术架构与安全模型

为了在不引发系统安全漏洞的前提下与 Android 底层 `update_engine` 交互，Pixel Updater 采用了最小特权原则的安全架构：

1. **自定义 SELinux 域**：在开机早期阶段（`post-fs-data.sh`），原生二进制程序 `pixelupdater_selinux` 会基于受限的 `untrusted_app` 配置文件创建名为 `pixelupdater_app` 的专用 SELinux 域，而非直接授予宽泛的 `priv_app` 权限。
2. **上下文绑定**：模块在 `/dev/selinux/apex_seapp_contexts` 中将包名 `com.github.pixelupdater.pixelupdater` 绑定至 `pixelupdater_app` 安全上下文。
3. **载荷校验**：在将更新提交给 `update_engine` 之前，Pixel Updater 会先下载 `metadata.pb` 与 `payload_metadata.bin`，校验文件头摘要、设备指纹兼容性以及安全补丁时间戳，从而拦截不兼容镜像或意外降级操作（避免触发 AVB 回滚索引导致变砖）。

## 安装与使用流程

1. 通过 Magisk 刷入 `PixelUpdater-*-release.zip` 安装包并重启设备。
2. 在应用抽屉中启动 **Pixel Updater** 应用。
3. 点击 **Check for updates**（检查更新）向 Google 官方更新服务器轮询新版本。
4. 检测到可用更新后点击 **Install**（安装）。Pixel Updater 会将更新载荷流式写入非活动槽位、校验分区摘要，并将 Magisk Root 自动修补至新槽位。
5. 完成后点击通知栏提示或应用内重启按钮，即可重启进入更新后的系统。

## 诊断日志与调试菜单

Pixel Updater 内置完善的日志记录与调试功能：

- **开启调试模式**：在应用设置界面中长按版本号即可显示隐藏的调试开关。
- **撤销未重启的更新**：若更新已安装完成但尚未重启，可开启调试模式并选择 **Revert completed update**，取消 Bootloader 的槽位切换。
- **日志文件路径**：
  - 运行操作日志（`check.log`、`install.log`、`revert.log`、`crash.log`）保存在：
    ```bash
    /sdcard/Android/com.github.pixelupdater.pixelupdater/files/
    ```
  - 开机早期 SELinux 策略修改日志保存在：
    ```bash
    /data/local/tmp/pixelupdater_selinux.log
    ```
  - 若需在电脑端实时追踪 `update_engine` 运行状态，可执行：
    ```bash
    adb logcat '*:S' update_engine
    ```
