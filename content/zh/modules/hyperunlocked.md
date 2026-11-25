---
id: "hyperunlocked"
title: "HyperUnlocked：面向小米澎湃 OS 与 MIUI 的无侵入系统特性解锁器"
sidebarTitle: "HyperUnlocked"
description: "专为小米、红米与 POCO 设备打造的系统特性解锁套件，通过 WebUI 无侵入启用旗舰级高级模糊质感、景深锁屏、相机特性与高刷新率选项。"
category: "system-environment"
tier: 1
searchQueries:
  - "HyperUnlocked Magisk 模块"
  - "ukriu HyperUnlocked 下载"
  - "小米澎湃 OS 解锁旗舰特性 Root"
  - "小米开启高级模糊质感 Magisk"
  - "HyperUnlocked WebUI 元模块配置"
prerequisites:
  - "运行官方或第三方澎湃 OS / MIUI 的小米、Redmi 或 POCO 设备"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "KernelSU 环境需先安装可用的元模块（Metamodule，建议优先选用 Magic Mount 而非 OverlayFS）"
  - "在 Root 管理器设置中关闭“默认卸载模块（Umount modules by default）”"
  - "具备 WebUI 运行环境（KernelSU 内置支持，Magisk 用户需搭配 WebUI X 或 MMRL）"
conflicts:
  - "非小米系品牌设备（Google Pixel、三星 One UI、一加、摩托罗拉等）"
  - "缺少澎湃 OS / MIUI 框架基础的原生 AOSP 或 LineageOS ROM"
configPaths:
  - "/data/adb/modules/hyperunlocked/"
features:
  - "视觉渲染引擎解锁：为入门及中端小米机型开启实时高级窗口模糊与系统材质纹理"
  - "丰富锁屏个性化：启用景深效果壁纸、进阶时钟字体排版与旗舰版澎湃 OS 锁屏样式"
  - "相机与相册增强：开放旗舰机型专属拍摄模式、超清画质及 AI 修图工具"
  - "屏幕与性能调校：解锁高刷新率自由切换与扩展电池性能模式"
  - "控制中心升级：为低配机型配置文件补充摄像头与麦克风硬件隐私总开关"
faq: []
---

## 概述

**HyperUnlocked** 由 ukriu 开发，是一款专为运行澎湃 OS（HyperOS）或 MIUI 的小米、Redmi 与 POCO 智能手机设计的无侵入式（Systemless）特性解锁与定制模块。小米出厂固件常会依据机型定价档位人为屏蔽部分软件特性——即使硬件性能完全足以流畅渲染，中低端芯片机型仍会被屏蔽高斯模糊、景深锁屏、高刷新率选项以及进阶相机算法。

HyperUnlocked 通过无系统分区修改的方式调整供应商覆盖层（Vendor Overlays）、系统特性 XML 声明与框架属性，并配备交互式 WebUI 管理面板，让用户无需改动只读系统分区即可按需开关各类旗舰特性。

## 前置要求与兼容性

- **目标硬件与 ROM**：严格限定运行 MIUI 或澎湃 OS 的小米、Redmi 与 POCO 设备。在原生 Android、AOSP 或其他厂商定制系统上强行刷入会导致无法开机或框架服务崩溃。
- **Root 方案**：兼容 Magisk、KernelSU 与 APatch。
- **元模块（Metamodule）要求（KernelSU）**：
  - 使用 KernelSU 或其分支版本的用户必须预先安装元模块。强烈推荐使用基于 **Magic Mount** 的元模块；虽然 OverlayFS 也可工作，但部分框架资源文件可能无法干净挂载。
  - 在 KernelSU 设置中务必 **关闭“默认卸载模块（Umount modules by default）”**，以确保系统框架进程能够正常读取解锁后的覆盖资源。
- **WebUI 宿主环境**：
  - KernelSU 用户可直接在模块卡片中点击打开 WebUI。
  - Magisk 用户需额外安装 [WebUI X](https://github.com/MMRLApp/WebUI-X-Portable) 或 [MMRL](https://github.com/MMRLApp/MMRL)。

## 已解锁功能一览

通过 WebUI 管理界面，用户可分类配置以下系统特性：

1. **系统界面与模糊质感**：将通知栏、控制中心与音量滑块的纯灰背景替换为动态高斯模糊效果。
2. **锁屏景深效果**：启用支持前景人物/物体动态遮挡锁屏时钟的多图层景深壁纸。
3. **控制中心升级**：在低配机型的配置文件中恢复缺失的硬件隐私开关（相机禁用开关、麦克风隐私指示器）与媒体控制卡片。
4. **相机与相册增强**：解锁被屏蔽的拍摄模式、文档扫描模式与相册 AI 魔法消除功能。
5. **负一屏与桌面小部件**：解锁自定义桌面超级图标与交互式小部件。

## 安装与配置流程

1. 从项目发布页下载最新版本的 `HyperUnlocked.zip`。
2. 使用你的 Root 管理器刷入该模块。
3. 重启设备。
4. 打开模块 WebUI，逐项浏览并启用所需的特性分组。
5. 应用更改，若界面提示重建 Android 资源缓存请配合重启设备。
6. 模块文件与配置状态持久化保存于：
   ```bash
   /data/adb/modules/hyperunlocked/
   ```

## 故障排查与注意事项

- **界面卡顿或掉帧**：在入门级 GPU（如低端骁龙 600 系列或联发科 Helio 芯片）上开启“高级材质（Advanced Textures）”或高强度实时模糊可能引发动画掉帧。如遇卡顿，请在 WebUI 中关闭高级材质，仅保留锁屏样式与控制中心等轻量特性。
- **Magisk 下无法打开 WebUI**：请确认已安装 MMRL 或 WebUI X Standalone，并在弹窗请求时授予其 Root 权限。
