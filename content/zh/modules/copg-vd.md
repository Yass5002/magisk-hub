---
id: "copg-vd"
title: "COPG-VD：全局设备身份、指纹与系统框架属性伪装模块"
sidebarTitle: "COPG-VD"
description: "由 VD171 维护的基于 Zygisk 的全局设备指纹与 Build 属性伪装套件，支持 JSON 声明式配置、分进程覆盖、WebUI 管理与 VDLU 增量更新。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "COPG-VD 模块下载"
  - "VD171 COPG-VD 配置教程"
  - "Zygisk 全局机型指纹伪装"
  - "COPG-VD.json 怎么写"
  - "替代 PlayIntegrityFix Google 相册无限空间"
prerequisites:
  - "已通过 Magisk（20.4+）、KernelSU 或 APatch 获取 Root 权限"
  - "已启用 Zygisk 运行环境（内置 Zygisk、Zygisk Next、ReZygisk 或 NeoZygisk）"
  - "已准备好 `/data/adb/COPG-VD/COPG-VD.json` 配置文件"
conflicts:
  - "其他全局或 Play Integrity 属性伪装模块（COPG、PlayIntegrityFix、integrity-box）"
configPaths:
  - "/data/adb/COPG-VD/COPG-VD.json"
  - "/data/adb/COPG-VD/vdlu/config"
  - "/data/adb/modules/COPG-VD/"
features:
  - "全局与精细化作用域挂钩：支持 `scope_mode`、全局字段（如 `SECURITY_PATCH`）及分进程覆盖列表（`process_overrides`）"
  - "完整设备属性模拟：支持修改 `BRAND`、`DEVICE`、`MODEL`、`FINGERPRINT`、`BOOTLOADER`、`UUID`、`FIRST_API_LEVEL` 与 `DRM_SECURITY_LEVEL`"
  - "内置 WebUI 与指纹更新脚本：提供图形化配置界面与 `fingerprint-update.sh` 快速同步工具"
  - "VDLU 启动前增量更新：在 `post-fs-data` 阶段支持带签名校验的 `.so` 热替换，无需完整重刷模块"
  - "旧版路径自动迁移：启动时自动将旧版 `/data/adb/COPG-VD.json` 迁移至 `/data/adb/COPG-VD/`"
faq:
  - question: "在 `v6.18-vd` 中 `COPG-VD.json` 应该放在哪个路径？"
    answer: "新版统一将配置存放在 `/data/adb/COPG-VD/COPG-VD.json`（目录权限为 `0700`）。若你仍保留着旧路径 `/data/adb/COPG-VD.json`，`service.sh` 与 `fingerprint-update.sh` 会在运行过程中自动完成迁移。"
  - question: "COPG-VD 可以和 PlayIntegrityFix 同时开启吗？"
    answer: "不建议同时使用。COPG-VD 的安装脚本会主动检测 `COPG`、`playintegrity`/`playintegrityfix` 与 `integrity-box` 等冲突模块，避免多个 Zygisk 属性挂钩互相覆盖。"
---

## 概述

由 **VD171** 基于 AlirezaParsi 的 COPG 分支开发维护，**COPG-VD**（`v6.18-vd`）是一款支持 **Magisk**、**KernelSU** 与 **APatch** 的全局 Zygisk 设备身份与系统构建属性伪装模块。

常规伪装模块通常只对少数用户应用或 Play 服务注入钩子，容易在系统框架 API 与用户态属性交叉比对时露馅。COPG-VD 通过多架构原生 Zygisk 库（`zygisk/*.so`）配合 `etc/copgvd_scope.dex` 读取 `/data/adb/COPG-VD/COPG-VD.json`，并内置 WebUI 面板、`fingerprint-update.sh` 与 **VDLU** 签名增量更新引擎。

---

## 配置结构（`/data/adb/COPG-VD/COPG-VD.json`）

`"COPG-VD"` 对象内的所有字段均为可选项；未填写的属性将直接透传设备原始值。所有属性字符串必须使用双引号包裹。

### 配置示例（参考 `COPG-VD.json.example`）：
```json
{
  "scope_mode": "playstore",
  "motor_drm": false,
  "drm_targets": [],
  "global_fields": ["SECURITY_PATCH"],
  "process_overrides": [],
  "COPG-VD": {
    "BRAND": "google",
    "DEVICE": "tegu",
    "MANUFACTURER": "Google",
    "MODEL": "Pixel 9a",
    "FINGERPRINT": "google/tegu_beta/tegu:CANARY/ZP11.261016.008/16754936:user/release-keys",
    "PRODUCT": "tegu_beta",
    "BOOTLOADER": "unknown",
    "BOARD": "tegu",
    "HARDWARE": "tegu",
    "DISPLAY": "ZP11.261016.008",
    "ID": "ZP11.261016.008",
    "HOST": "e4df75f83a59",
    "INCREMENTAL": "16754936",
    "TIMESTAMP": "1793211232",
    "PREVIEW_SDK": "20261104",
    "USER": "android-build",
    "SDK_FINGERPRINT": "ee82a872870173d77e68050e21a2bcbf",
    "UUID": "FjWvtSORkI0sEwekaPz2s30gqV5vWP_EZHFtBiXzboc",
    "SECURITY_PATCH": "2026-11-05",
    "FIRST_API_LEVEL": "35",
    "DRM_SECURITY_LEVEL": "L1"
  }
}
```

---

## 技术架构与工作原理

1. **多架构 Zygisk 注入**：内置经过 `.sha256` 校验的 `arm64-v8a`、`armeabi-v7a`、`x86` 与 `x86_64` 原生库，在进程分化阶段拦截 `android.os.Build` 反射与原生 `__system_property_get` 调用。
2. **作用域与全局字段控制**：支持 `scope_mode`（如 `"playstore"`）、`global_fields`（如 `["SECURITY_PATCH"]`）、`drm_targets`、`process_overrides` 及 `COPG-VD-Settings` 运行开关。
3. **VDLU 启动前增量更新**：`post-fs-data.sh` 会在 Zygote 映射 `zygisk/<abi>.so` 前执行 `vdlu/update.sh`（配置位于 `/data/adb/COPG-VD/vdlu/config`），实现带签名验证的增量更新而无需二次重启。
4. **WebUI 与指纹同步脚本**：通过内置 `webroot/` 管理设备配置，或调用 `fingerprint-update.sh` 获取最新示例指纹配置。

---

## 安装与配置步骤

1. 确认已在 Magisk、KernelSU 或 APatch 中启用 **Zygisk**，并卸载冲突的伪装模块（如 `COPG`、`PlayIntegrityFix`、`integrity-box`）。
2. 在 Root 管理器中刷入 `COPG-VD-v6.18-vd.zip`（无交互环境或超时场景下安装脚本会自动回落默认选项）。
3. 通过 WebUI 或具备 Root 权限的编辑器生成并完善 `/data/adb/COPG-VD/COPG-VD.json`（可参考模块内置的 `COPG-VD.json.example`）。
4. 重启设备后，在终端或 ADB Shell 中验证伪装结果：
   ```bash
   getprop ro.product.model
   ```

---

## 常见问题与排查

- **配置文件未生效**：确认文件位于 `/data/adb/COPG-VD/COPG-VD.json`（旧版 `/data/adb/COPG-VD.json` 会在开机或更新时自动迁移至 `/data/adb/COPG-VD/`）。
- **JSON 语法解析失败**：修改后建议先用 `jq` 或校验工具检查括号、逗号与双引号转义，任何语法错误都会导致解析器跳过伪装规则。
