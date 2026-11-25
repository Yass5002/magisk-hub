---
id: "tricky-addon-enhanced"
title: "Tricky Addon Enhanced：基于 Rust 守护进程的 TrickyStore / TEESimulator 自动化管理模块"
sidebarTitle: "Tricky Addon Enhanced"
description: "采用全新 Rust 原生守护进程与多语言 WebUI 的增强型伴侣模块，为 TrickyStore 与 TEESimulator 提供双源 Keybox 轮换、安全补丁同步、VBHash 提取与冲突清理。"
category: "root-management"
tier: 1
searchQueries:
  - "Tricky Addon Enhanced 下载"
  - "TA Enhanced TrickyStore WebUI"
  - "TrickyStore 自动获取 Keybox 与安全补丁"
  - "Enginex0 tricky-addon-enhanced"
  - "TEESimulator 自动化增强模块"
prerequisites:
  - "Magisk v20.4+、KernelSU v32234+ 或 APatch v11159+"
  - "已在 `/data/adb/modules/tricky_store/` 安装可用的 TrickyStore 或 TEESimulator 模块"
  - "Magisk 用户需配合 KSU WebUI Standalone（`io.github.a13e300.ksuwebui`，点击 Action 按钮可自动拉取安装）"
conflicts:
  - "旧版 Tricky Addon（`TA_utl`、`.TA_utl`）、`tsupport-advance` 自动列表（自动暂停）、`PlayIntegrityFork`、`safetynet-fix`、`integrity_box`、`vbmeta-fixer`、`Reset_BootHash`、`Yurikey`、`Yamabukiko`、`ShamikoManager` 及内含 `com.lingqian.appbl` / `com.topmiaohan.hidebllist` 的模块"
configPaths:
  - "/data/adb/tricky_store/ta-enhanced/"
  - "/data/adb/tricky_store/enhanced.conf"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/security_patch_auto_config"
  - "/data/adb/boot_hash"
features:
  - "单进程原生 Rust 守护进程（`ta-enhanced`）取代传统多层 Shell 轮询脚本，大幅降低常驻开销"
  - "双源 Keybox 自动拉取与轮换，当本地缺失 `keybox.xml` 时在开机阶段执行指数退避重试（30s/60s/120s/240s）"
  - "内置 `SecurityPatchTask` 自动拉取 Android 安全公告日期，并结合独立打包的 `resetprop-rs` 伪装启动与锁定状态属性"
  - "安装期主动清理已知冲突模块，支持热安装、VBHash 自动提取（`vbhash_extractor.apk`）及 23 国语言 WebUI"
faq:
  - question: "为什么刷入后在 Magisk 或 KernelSU 模块列表中找不到 Tricky Addon Enhanced？"
    answer: "这是该模块的主动隐身设计。`service.sh` 会先将 `module.prop` 备份到 `/data/adb/tricky_store/ta-enhanced/module.prop` 供 WebUI 显示版本号，随后删除模块目录内的 `module.prop`（在 Magisk 下还会将自身镜像至隐藏目录 `/data/adb/modules/.TA_enhanced`）。同时它会将 `webroot`、`action.sh` 与 `banner.png` 软链接到 `/data/adb/modules/tricky_store/`，直接点击 TrickyStore 卡片即可打开控制面板。"
  - question: "刷入 Tricky Addon Enhanced 时为什么会清理其他隐藏或完整性模块？"
    answer: "由于该模块支持热安装（`MODULE_HOT_INSTALL_REQUEST=true`）并全面接管属性伪装、VBHash 与 `target.txt` 维护，`customize.sh` 会在安装时直接移除 `/data/adb/modules/` 下的已知冲突模块目录（如 `TA_utl`、`PlayIntegrityFork`、`integrity_box`、`vbmeta-fixer`、`Reset_BootHash`、`Yurikey` 等）；若检测到 `tsupport-advance`，则会写入 `/storage/emulated/0/stop-tspa-auto-target` 防止两者互相覆盖。"
  - question: "如果我想自行管理设备属性或 Boot Hash，如何关闭模块内置的伪装？"
    answer: "`prop.sh` 在执行 `resetprop-rs` 修改前会检查控制标记：创建 `/data/adb/disable_prop_handler` 可完全禁用系统属性伪装，创建 `/data/adb/disable_vbmeta_digest_spoof` 则仅跳过向 `ro.boot.vbmeta.digest` 写入 `/data/adb/boot_hash`。"
---

## 概述

由 **Enginex0** 开发的 **Tricky Addon Enhanced**（模块 ID `TA_enhanced`）是面向 **TrickyStore** 与 **TEESimulator** 的全自动增强伴侣模块。项目秉承 *“Flash once. Forget forever.”* 的零人工干预理念，彻底重构了传统 Shell 脚本组合方案，改为以单一原生 Rust 守护进程（`ta-enhanced`）驱动核心任务，并附带支持 23 种语言（含简体中文 `zh-CN`）的现代 WebUI。

---

## 技术架构与模块内部机制

`TA_enhanced-v5.53.1.zip` 内置了完整多架构二进制文件（`arm64-v8a`、`armeabi-v7a`、`x86_64`、`x86`），并贯穿 Root 模块生命周期的各个阶段：

| 组件 | 路径与核心职责 |
| --- | --- |
| `bin/<abi>/ta-enhanced` | 原生 Rust 守护进程，负责双源 Keybox 获取与轮换、`SecurityPatchTask` 安全补丁同步、`target.txt` 自动化、Xposed 扫描及冲突检测 |
| `bin/<abi>/resetprop-rs` | 每次开机同步至 `/data/adb/tricky_store/ta-enhanced/bin/resetprop-rs`，供 `prop.sh` 执行高性能属性伪装 |
| `post-fs-data.sh` | 最长等待 9 秒直至 `/data/adb/modules/` 就绪；若缺失 `/data/adb/modules/tricky_store` 则标记自卸载，并识别 Magisk/KSU/APatch 环境 |
| `service.sh` | 后台启动 `prop.sh`、在 Magisk 下合并 `--denylist`（启用 `target_from_denylist` 时）、隐藏模块本体、挂载 WebUI 软链、提取 VBHash 并拉起 `ta-enhanced daemon` |
| `hotinstall.sh` | 响应 `MODULE_HOT_INSTALL_REQUEST="true"`，使刷入后无需立即重启即可触发初始化与后台服务 |
| `common/vbhash_extractor.apk` | 开机完成后由 `ta-enhanced vbhash extract` 调用，自动提取并维护 `/data/adb/boot_hash` |

### 隐身机制与属性加固

- **管理器列表隐藏**：在 Magisk 环境下，`service.sh` 会将模块复制至带点前缀的隐藏路径 `/data/adb/modules/.TA_enhanced`，并将 `module.prop` 快照保存至 `/data/adb/tricky_store/ta-enhanced/module.prop` 后删除原文件。
- **WebUI 无缝挂载**：`service.sh` 会向 TrickyStore 模块目录创建 `webroot`、`action.sh` 与 `banner.png` 软链接，将配置入口直接集成至 TrickyStore 卡片中。
- **系统属性伪装（`prop.sh`）**：通过 `resetprop-rs` 统一修正 `ro.boot.vbmeta.device_state=locked`、`ro.boot.verifiedbootstate=green`、`ro.boot.flash.locked=1`、`ro.boot.veritymode=enforcing`、`ro.debuggable=0`、`ro.build.type=user`、`ro.build.tags=release-keys`，并涵盖小米/Realme 锁状态属性及 LineageOS 特征清理。

---

## 安装与配置指南

1. 请先刷入并启用 **TrickyStore** 或 **TEESimulator**，确保 `/data/adb/modules/tricky_store` 目录已存在。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入 `TA_enhanced-v5.53.1.zip`。
3. 刷入过程中根据终端提示按音量键选择模式（**音量上键**启用自动化托管，**音量下键**切换为手动模式；若已存在 `target.txt` 或超过 10 秒未按键将自动择优选择）。
4. 从 **TrickyStore** 模块卡片打开 **WebUI**（Magisk 用户直接点击模块卡片上的 **操作 / Action** 按钮，若尚未安装 `io.github.a13e300.ksuwebui` 会自动下载安装并拉起面板）。
5. 如需排查运行状态，可查看 `/data/adb/tricky_store/ta-enhanced/logs/` 目录下的 `boot.log`、`main.log` 与 `conflict.log`。

---

## 常见问题与排查

- **重启后模块自动消失并被卸载**：`post-fs-data.sh` 检测到 `/data/adb/modules/tricky_store/` 不存在或已被标记移除时会自动创建 `remove` 标记。请先安装 TrickyStore 或 TEESimulator，再重新刷入本模块。
- **全新刷入后 `keybox.xml` 未立即生成**：若开机时不存在 `/data/adb/tricky_store/keybox.xml`，`service.sh` 会在后台按 `30s`、`60s`、`120s`、`240s` 指数退避间隔调用 `ta-enhanced keybox fetch`。请确认设备已联网，或在 WebUI 中手动触发拉取。
- **彻底卸载**：执行卸载时，`uninstall.sh` 会依次停止 `ta-enhanced` 守护进程、清理 `/data/adb/modules/.TA_enhanced`、移除 `/data/adb/boot_hash` 与状态配置文件，并恢复 TrickyStore 原本的 `module.prop` 描述。
