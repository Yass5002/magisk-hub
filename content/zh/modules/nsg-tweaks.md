---
id: "nsg-tweaks"
title: "NSG Tweaks：Network Signal Guru（网络信号大师）LSPosed 增强模块"
sidebarTitle: "NSG Tweaks"
description: "基于 MIT 协议开源的 LSPosed 模块（com.nsgmod.band），为 Network Signal Guru（com.qtrun.QuickTest v4.8.14）扩展 16 行基站表、ARFCN 与带宽列、信令搜索及回放控制。"
category: "xposed-runtime-hooks"
tier: 1
searchQueries:
  - "NSG Tweaks 下载"
  - "Network Signal Guru LSPosed 模块"
  - "网络信号大师增强插件"
  - "com.nsgmod.band com.qtrun.QuickTest"
  - "NSG 16行基站表 ARFCN 带宽显示"
prerequisites:
  - "Android 6.0 及以上系统（`minSdkVersion 23`）"
  - "支持 Xposed API 102 的 **LSPosed** 框架（`minApiVersion=102`）"
  - "必须搭配 **Network Signal Guru (`com.qtrun.QuickTest`) qtrun v4.8.14** 版本使用"
conflicts:
  - "除 qtrun v4.8.14 之外的任何 NSG 版本（含 Google Play 商店版 `gplay` 及 v4.8.12 等旧版）"
  - "其他同时挂钩（Hook）`com.qtrun.QuickTest` 基站表或信令界面的 Xposed 模块"
configPaths:
  - "/data/adb/lspd/"
  - "/data/data/com.qtrun.QuickTest/shared_prefs/"
features:
  - "将 NR-NSA 与 LTE 服务/邻区基站表由 8 行扩展至最多 16 行，内联注入 `Band`（ARFCN）与 `BW`（下行信道带宽 MHz）列并压缩冗余子行高度"
  - "支持同站 NR 邻区高亮（`CellIdMatchHook`），可选显示 NR-NSA gNB-ID 表头、NR-SA 路径损耗（Pathloss）列、NR PDSCH SINR 行及以 CellID 替代 PCI 显示"
  - "增强信令分析与回放体验，提供信令导航、搜索与分享（`SignalingNavHook`、`SignalingSearchHook`、`SignalingShareHook`），以及 `RT-Play` 实时回放按钮和精细进度条"
  - "在 **NSG → Settings → Experiments** 页面底部内置 11 项独立功能开关（`SettingsToggleHook`）"
faq:
  - question: "为什么 NSG Tweaks v12.0 在 Google Play 版或旧版 Network Signal Guru 上无法生效？"
    answer: "从 v12.0 起，NSG Tweaks 移除了运行时版本探测逻辑以及对 Google Play 版（`gplay`）和 v4.8.12 及更早版本的兼容支持，转而使用针对 **qtrun v4.8.14** 混淆类名与方法签名精确校准的单一符号表。如需兼容旧版需回退至 v11.1。"
  - question: "在 LSPosed 启用后，如何在应用内单独开启或关闭各项增强功能？"
    answer: "在 LSPosed 中勾选 `com.qtrun.QuickTest` 作用域并强行停止重启 NSG 后，进入 **NSG → Settings → Experiments**，页面最下方会出现 11 个以 `NSGMod:` 开头的功能开关，可按需逐项启用或关闭。"
---

## 概述

**NSG Tweaks**（包名 `com.nsgmod.band`）是由 **henrik** 开发的开源（MIT）LSPosed 模块，专为使用 **Network Signal Guru (`com.qtrun.QuickTest`)** 进行蜂窝网络路测与射频分析的工程师及玩家设计。原版 NSG 默认将邻区基站表限制在 8 行以内，将 ARFCN 与信道带宽折叠在额外子行中占据纵向空间，且在信令搜索与日志回放操控上存在不便。

**v12.0** 版本在 `META-INF/xposed/module.prop` 中声明 `staticScope=true` 并锁定作用域为 `com.qtrun.QuickTest`，要求 **LSPosed API 102**（`minApiVersion=102`、`targetApiVersion=102`），且严格适配 **qtrun v4.8.14** 构建。

---

## 技术架构与 Hook 模块拆解

通过检查 `nsg_tweaks_lsposed_v12-0.apk` 的 `META-INF/xposed/java_init.list`（入口为 `com.nsgmod.band.MainHook`）及 DEX 内部实现，其挂钩逻辑分为四大子系统：

### 1. 基站表与射频指标扩展
- **NR-NSA / LTE 16 行基站表（`NrNsaExtCellsHook`、`CellRowHeightHook`、`CellTableRowDispatcher`）**：隐藏每行下方的冗余子行（每行节省约 22 dp 纵向空间；在 NR-SA 表格中将首行高度由 28 dp 压紧至 22 dp、子行由 26 dp 压紧至 21 dp），并将显示容量从 8 行扩展至最多 16 行。
- **内联 ARFCN 与带宽列（`BandColumnHook`、`NrNsaBandwidthColumnHook`、`LteBandwidthColumnHook`、`NrSaCellColumnsHook`）**：向 NR-NSA（`Serving | Band | BW | PCI | Beam | RSRP | RSRQ | SINR`）与 NR-SA 表格注入 **Band**（ARFCN）与 **BW**（下行 MHz 带宽）列。
- **NR-SA 与载波聚合矩阵扩展**：包含 `NrSaHeaderPathlossHook`（路径损耗列）、`NrSaCsiSnrRowHook`（PDSCH SINR 行）、`NrNsaGnbIdHeaderHook`（表头显示 gNB-ID）、`NrSaBwpIdHook`（`BWP-ID`）、`BwpUlBwDedicatedModeHook`、`CaMatrixDlHook`、`SACAMatrixDLHook`、`LteCaMatrixUlInNsaHook`、`LteCaMatrixUlQpskHook`、`NrSaMimoFormatHook`、`NrSaModUsageRowHook`、`NrSaPucchTxRowHook`、`NrSaThputPerPrbHook` 与 `RenamePuschTxLabelHook`。

### 2. 邻区匹配高亮与刷新率优化
- **同站邻区高亮（`CellIdMatchHook`、`NrSaCellColorHook`、`LteCellColorHook`、`MapDotColorHook`）**：自动对比 PCI 与 ARFCN，对与当前主服务小区同站的 NR 邻区进行高亮标识。
- **快速刷新与标识切换（`RefreshIntervalHook`、`PerSimFormatHook`、`PlmnOperatorToastHook`）**：提升界面数据刷新速度，并支持以 CellID 替代 PCI 显示。

### 3. 信令分析与日志回放工具
- **信令增强（`SignalingNavHook`、`SignalingSearchHook`、`SignalingShareHook`）**：为信令列表添加快速跳转、关键字搜索与导出分享功能。
- **回放控制（`RtPlayHook`、`ReplayStatusBarHook`、`GranularSeekBarHook`、`PageDotJumpHook`、`ScrollBarHook`）**：增加 `RT-Play` 按钮与高精细度进度条拖拽，便于逐帧回看测试日志。

### 4. 实验性设置开关（`SettingsToggleHook`）
在 **NSG → Settings → Experiments** 底部提供以下 11 项开关：
- `NSGMod: Cell table mods`
- `NSGMod: NR-NSA 16-cell table`
- `NSGMod: LTE 16-cell table`
- `NSGMod: Collapse empty cell rows`
- `NSGMod: Highlight same-site NR neighbours`
- `NSGMod: NR-NSA gNB-ID in header`
- `NSGMod: NR-SA Pathloss column`
- `NSGMod: Show NR PDSCH SINR`
- `NSGMod: Use CellID instead of PCI`
- `NSGMod: Fast refresh`
- `NSGMod: RT-Play button`

---

## 安装与验证步骤

1. 确认设备已安装 **Network Signal Guru qtrun v4.8.14**（`com.qtrun.QuickTest`）。
2. 安装 `nsg_tweaks_lsposed_v12-0.apk`。
3. 打开 **LSPosed 管理器 → 模块 → NSG Tweaks**，启用模块并确认作用域（Scope）已勾选 `com.qtrun.QuickTest`。
4. 强制停止并重新打开 Network Signal Guru：
```bash
su -c "am force-stop com.qtrun.QuickTest"
```
5. 进入 **NSG → Settings → Experiments** 滑到底部，确认可见 `NSGMod:` 系列开关及由 `TweaksVersionFooterHook` 注入的版本页脚。

---

## 常见问题排查

- **开启后闪退或表格列缺失**：请通过 `dumpsys package com.qtrun.QuickTest | grep versionName` 核对版本号是否为 **4.8.14**（非 Google Play 商店版本）。
- **模块未生效**：检查所用 LSPosed 框架是否支持 **API 102**，并在 LSPosed 日志中查看 `MainHook` 或 `BWHook` 输出以定位异常。
