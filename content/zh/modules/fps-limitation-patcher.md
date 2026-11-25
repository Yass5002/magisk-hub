---
id: "fps-limitation-patcher"
title: "FPS Limitation Patcher：HyperOS / MIUI 无侵入式 PowerKeeper 温控与高刷解锁"
sidebarTitle: "FPS Limitation Patcher"
description: "安装时自动反编译并修补小米 PowerKeeper（电量和性能）应用，消除激进温控锁帧，解锁真正的 90Hz/120Hz 游戏高刷。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "FPS Limitation Patcher Magisk"
  - "Mods-Center FPS Limitation Patcher"
  - "解除小米 PowerKeeper 60 帧限制"
  - "HyperOS MIUI 游戏 120Hz 解锁 Root"
  - "修补电量和性能解除温控降帧"
prerequisites:
  - "运行官方或第三方 MIUI / HyperOS（澎湃 OS）的小米、Redmi 或 POCO 手机"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "系统框架分区中存在 com.miui.powerkeeper 组件"
conflicts:
  - "非小米系设备及原生类 AOSP ROM（不包含 MIUI PowerKeeper 组件）"
configPaths:
  - "/data/adb/modules/fps-limitation-patcher/"
features:
  - "本机自动动态修补：安装过程中直接提取、反编译并修改设备原装 PowerKeeper APK"
  - "绕过温控锁帧：移除省电模式或机身升温时强制触发的 60 FPS 硬编码降帧上限"
  - "全局高刷新率：在游戏及第三方应用中强制释放 90Hz、120Hz 与 144Hz 屏幕刷新率"
  - "零系统分区篡改：以无系统分区修改（Systemless）方式将修补后的 PowerKeeper 挂载覆盖至 /system/app/ 或 /product/app/"
faq: []
---

## 概述

在运行 MIUI 或 HyperOS（澎湃 OS）的小米、Redmi 及 POCO 智能手机上，系统内置的 **PowerKeeper** 组件（电量和性能，包名 `com.miui.powerkeeper`）严格控制着功耗策略与温控降频规则。即便手机配备了 120Hz 或 144Hz 高刷屏与旗舰级处理器，一旦电池温度超过 38°C，PowerKeeper 仍会强制将大型游戏（如《原神》《PUBG》《使命召唤手游》等）锁定在 60 FPS 甚至 45 FPS。

由 Mods-Center 开发的 **FPS Limitation Patcher** 是一款全自动本机修补工具。刷入安装时，模块会直接提取你当前系统版本自带的 PowerKeeper 安装包，反编译其字节码以剔除温控锁帧表与刷新率限制器，再将修补后的 APK 无侵入式挂载回原位置。

## 本机实时修补原理

市面上许多直接替换预编译 APK 的方案在面对不同地区或不同版本的 MIUI/HyperOS 固件时，极易引发签名校验不匹配甚至卡米重启（Bootloop）。该模块直接针对你设备上的原厂包体进行修补：

1. **提取原包**：安装脚本自动从 `/system/app/`、`/system_ext/app/` 或 `/product/app/` 定位当前生效的 `PowerKeeper.apk`。
2. **字节码修改**：调用内置 DEX 工具，精准改写 PowerKeeper 温控策略类中负责执行 `fps_limit` 限制的条件判断分支。
3. **无侵入式挂载**：将修补后的新 APK 直接挂载覆盖至原系统路径，确保签名体系与系统框架完全兼容。
4. **解除帧率枷锁**：游戏及各类应用得以按照屏幕面板支持的最高刷新率渲染输出，不再受后台电量服务守护进程的强制压制。

## 安装与配置

1. 确认设备为运行 MIUI 或 HyperOS 的小米、Redmi 或 POCO 手机。
2. 从 GitHub 发布页下载 `FPS-Limitation-Patcher` 的 `.zip` 压缩包。
3. 打开 **Magisk** 或 **KernelSU** 刷入该模块。
   - *提示*：由于安装过程需要在设备本地执行 APK 反编译、修补与重打包，耗时将比常规模块略长。
4. 重启设备。
5. 启动目标游戏，并在开发者选项中开启“显示刷新率”，确认屏幕已可稳定维持 90Hz/120Hz 渲染。
