---
id: "komodo-build-prop"
title: "Komodo Pixel Props：无侵入式 Google Pixel 9 Pro XL 机型伪装"
sidebarTitle: "Komodo Pixel Props"
description: "通过无系统分区修改的方式伪装构建属性、认证标志与系统配置，将设备识别为 Google Pixel 9 Pro XL（komodo）。"
category: "root-management"
tier: 1
searchQueries:
  - "komodo build prop magisk 模块"
  - "elcapitanoe komodo pixel props"
  - "magisk 伪装 pixel 9 pro xl"
  - "play integrity pif komodo pixel 9"
  - "trickystore target txt komodo 配置"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "Android 10 及以上系统"
conflicts:
  - "其他修改全局设备指纹属性的属性伪装模块（例如 Pixelify、MagiskHide Props Config）"
configPaths:
  - "/data/adb/modules/komodo-build-prop/"
  - "/data/adb/pif.json"
  - "/data/adb/tricky_store/target.txt"
features:
  - "多分区属性伪装：在 system、vendor、product、system_ext 与 odm 分区统一应用 Pixel 9 Pro XL（komodo）设备标识"
  - "Play Integrity Fix（PIF）集成：自动生成并与当前 Pixel 9 Pro XL 设备指纹同步的 pif.json"
  - "TrickyStore 集成：自动生成并维护 /data/adb/tricky_store/target.txt，支持硬件 TEE 异常自动检测"
  - "第三方 ROM 特征清理：清除泄露的测试与开发标识（如 test-keys、lineage 及 userdebug 前缀）"
  - "Pixel sysconfig 集成：内置 Google 自适应充电、轻敲背面（Quick Tap）与新一代谷歌助理所需的权限及配置文件"
faq: []
---

## 概述

在非 Pixel 设备或第三方 ROM 上通过 Google Play Integrity 认证并解锁 Google Pixel 专属功能，需要保证所有系统分区中的属性高度一致。一旦 `ro.system.build.fingerprint` 与底层 vendor 属性存在冲突，便会立即触发完整性校验失败。

**Komodo Pixel Props** 由 Elcapitanoe 维护，是一款无侵入式 Root 模块，通过修改系统构建属性、安全认证标志及 Google 框架 `sysconfig` 配置，将你的设备完整伪装为 **Google Pixel 9 Pro XL**（`komodo`）。

## 核心架构与生态联动

### 1. 统一的多分区设备身份
Komodo 并非简单地修补 `/system/build.prop`，而是在所有 Android 分区中同步应用一致的构建 ID、产品品牌、机型名称与设备指纹：
- `ro.product.model=Pixel 9 Pro XL`
- `ro.product.name=komodo`
- `ro.product.device=komodo`
- `ro.build.flavor=komodo-user`

### 2. Play Integrity 与密钥证明生态集成
- **PlayIntegrityFix (PIF)**：自动导出或更新包含已验证目标属性的 `/data/adb/pif.json`。
- **TrickyStore 集成**：自动向 `/data/adb/tricky_store/target.txt` 写入硬件认证目标应用列表。若模块检测到设备缺少可用的硬件 TEE Keybox 能力，会自动启用 `teeBroken=true`。
- **PropImitationHooks (PIHooks)**：在未安装外部 PIF 模块时，提供内置属性伪装回退机制。

### 3. 第三方 ROM 特征清理
第三方 ROM 发行版常带有容易导致银行应用风控失败的开发环境签名特征，Komodo 会自动清理以下标识：
- 将 `test-keys` 发布标签替换为 `release-keys`。
- 清理带有 `lineage_`、`aosp_` 或 `userdebug` 前缀的构建风味（Build Flavor）。
- 修正 Bootloader 锁定状态标志（`ro.boot.flash.locked=1`、`ro.boot.verifiedbootstate=green` 以及三星保修熔断标志位）。

## 安装与配置

1. 从 GitHub Releases 下载最新的 `Komodo_beta_*.zip` 模块压缩包。
2. 通过 **Magisk** 或 **KernelSU** 刷入该压缩包。
3. 重启设备。
4. 在 KernelSU 或 APatch 中，可以直接打开模块内置的 **WebUI** 控制面板，查看当前生效属性、管理 PIF 目标并验证认证状态。
