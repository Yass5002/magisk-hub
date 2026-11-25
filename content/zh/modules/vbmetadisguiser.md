---
id: "vbmetadisguiser"
title: "VBMeta Disguiser：Android Verified Boot (AVB)、Boot Hash 与安全属性伪装引擎"
sidebarTitle: "VBMeta Disguiser"
description: "通过伪装 Android Verified Boot 属性、VBMeta 分区参数与 Bootloader 状态标志，绕过硬件认证检测与 Root 环境扫描。"
category: "system-environment"
tier: 1
searchQueries:
  - "VBMeta Disguiser Magisk 模块"
  - "Astoritin VBMetaDisguiser 下载"
  - "Android 伪装 VBMeta Boot Hash"
  - "AVB 2.0 Bootloader 属性隐藏"
  - "Native Detector VBMeta 过检测"
prerequisites:
  - "已通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "已从 Key Attestation 或 Native Detector 中复制设备 Boot Hash"
  - "需使用 Root 文件管理器或文本编辑器修改 /data/adb/vbmeta_disguiser/vbmeta.conf"
conflicts: []
configPaths:
  - "/data/adb/vbmeta_disguiser/vbmeta.conf"
  - "/data/adb/vbmeta_disguiser/slain_prop.prop"
  - "/data/adb/modules/vbmetadisguiser/"
features:
  - "已验证启动参数伪装：将 AVB 版本（2.0）与 VBMeta 分区大小（4096）伪装为与官方出厂镜像一致"
  - "加密 Boot Hash 替换：支持将官方正式版 Boot Hash 写入 `ro.boot.vbmeta.*` 属性"
  - "属性清除器（props_slay）：在开机阶段彻底移除会暴露 Bootloader 解锁状态的特定系统属性"
  - "安全补丁日期同步：支持与 Tricky Store 的 TEE 配置联动对齐系统安全补丁日期"
  - "Bootloader 与构建类型伪装：将 Bootloader 状态伪装为已锁定，并将 ROM 构建类型伪装为 user/release-keys"
faq: []
---

## 概述

现代防篡改检测应用（如 Native Detector、Momo 以及部分银行客户端）不再仅仅依赖 SafetyNet 或 Play Integrity 认证结果。为了揪出已解锁 Bootloader 的设备，它们会直接扫描系统属性表中的 Android Verified Boot（AVB）标志位——重点检查 `ro.boot.vbmeta.device_state`、`ro.boot.vbmeta.avb_version`、分区大小以及加密 Boot Hash。在 Bootloader 已解锁的手机上，这些标志位会直接暴露未验证状态。

由 Astoritin 开发的 **VBMeta Disguiser** 是一款全面的系统属性掩码引擎。它全面支持 Magisk、KernelSU 与 APatch，允许用户在不修改物理闪存分区的前提下，将设备暴露出来的 AVB 属性调整为与原厂未解锁的正式版设备完全一致。

> [!NOTE]
> VBMeta Disguiser 作用于**系统属性层**（`resetprop` / 用户态反射）。建议将其与 **Tricky Store** 等负责处理 TEE 级密钥证明（Key Attestation）响应的模块配合使用，以实现完整防护。

## 核心配置指令（`vbmeta.conf`）

所有配置均通过 `/data/adb/vbmeta_disguiser/vbmeta.conf` 文件进行管理。请使用 Root 权限编辑该文件以启用对应功能：

### 1. Boot Hash 与分区校验伪装
```ini
# Android Verified Boot version (defaults to 2.0)
avb_version=2.0

# VBMeta partition byte size (defaults to 4096)
vbmeta_size=4096

# Paste your genuine Boot Hash copied from Native Detector / Key Attestation
boot_hash=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

### 2. 加密状态与 Bootloader 伪装
```ini
# Force Data partition state: encrypted, unencrypted, or unsupported
crypto_state=encrypted

# Spoof bootloader properties as locked (ro.boot.flash.locked=1, etc.)
bootloader_props_spoof=true

# Spoof ROM build type to production user/release-keys
build_type_spoof=true
```

### 3. 属性剥离（`props_slay`）
环境检测应用通常会扫描第三方 ROM 或早期 Root 模块遗留的调试属性来识别 Root 环境。
```ini
# Enable property removal
props_slay=true

# Space-separated list of properties to purge on boot
props_list="persist.sys.phh.no_magisk ro.debuggable persist.service.adb.enable"
```
*说明*：被清除的属性会自动备份至 `/data/adb/vbmeta_disguiser/slain_prop.prop`。将 `props_slay` 改回 `false` 后即可恢复原始属性值。

### 4. 安全补丁日期同步
若同时安装了 **Tricky Store**，VBMeta Disguiser 会自动优先沿用 Tricky Store 的配置文件（`/data/adb/tricky_store/security_patch.txt`）。如需独立配置，请使用以下选项：
```ini
security_patch_disguise=true
all=20260705
```

## 分步安装指南

1. 通过 Magisk、KernelSU 或 APatch 刷入 **VBMeta Disguiser** `.zip` 模块包。
2. 在设备上打开 **Key Attestation** 或 **Native Detector**，复制目标设备对应的有效 Boot Hash。
3. 使用具备 Root 权限的文本编辑器打开 `/data/adb/vbmeta_disguiser/vbmeta.conf`。
4. 将复制的 Boot Hash 填入 `boot_hash=`，并按需开启相应的伪装开关。
5. 重启设备，使系统启动早期阶段的属性伪装脚本正式生效。

## 常见问题排查

- **Native Detector 提示 Property Modified (10)**：首次配置 `props_slay` 后重启出现该提示属于正常现象。由于 `resetprop` 需要挂载并修改 Android 属性服务树，通常需要再重启一次即可使属性节点恢复正常状态。
- **开启构建类型伪装后出现 Bootloop（无限重启）**：在部分带有严格内部完整性校验的厂商魔改 ROM 上开启 `build_type_spoof=true` 可能会导致系统框架崩溃。如遇无法开机问题，请进入安全模式（Safe Mode）或卸载该模块以还原修改。
