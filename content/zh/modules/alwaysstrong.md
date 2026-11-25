---
id: "alwaysstrong"
title: "AlwaysStrong：一体化 Strong Play Integrity 认证模块"
sidebarTitle: "AlwaysStrong"
description: "由 Evokerr 维护的一体化整合模块，将 TEESimulator-RS 与 PlayIntegrityFork 打包为单一模块，支持自动刷新 Keybox 与 WebUI 管理。"
category: "root-management"
tier: 1
searchQueries:
  - "AlwaysStrong 模块下载"
  - "Evokerr AlwaysStrong GitLab"
  - "Strong Integrity 一体化过检测"
  - "AlwaysStrong WebUI 配置"
  - "TEESimulator-RS PlayIntegrityFork 整合包"
prerequisites:
  - "Android 10+（API 29+），已安装 Magisk、KernelSU（verCode >= 10670）或 APatch"
  - "已启用独立的 Zygisk 引擎（推荐 ZygiskNext、ReZygisk 或 NeoZygisk）"
conflicts:
  - "独立安装的 TrickyStore、TEESimulator-RS 或 PlayIntegrityFix/Fork（AlwaysStrong 已内置两者并使用 tricky_store 模块 ID）"
  - "旧版 Universal SafetyNet Fix（安装脚本会自动将其标记移除）"
configPaths:
  - "/data/adb/tricky_store/alwaysstrong/config"
  - "/data/adb/tricky_store/alwaysstrong/state"
  - "/data/adb/tricky_store/alwaysstrong/apps.map"
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/modules/tricky_store/"
features:
  - "单包直刷整合：将基于 Rust 的 TEESimulator-RS 硬件证明模拟与 PlayIntegrityFork 设备指纹伪装合二为一"
  - "统一存储目录：将模块配置、内部循环状态与分应用映射集中存放于 `/data/adb/tricky_store/alwaysstrong/`"
  - "内置 WebUI 面板：支持定时自动刷新间隔、分应用 Keybox 映射、高级伪装开关（`spoof.conf`）与目标应用管理"
  - "Action 一键自动化：点击管理器 Action 按钮即可执行 Keybox 轮换、指纹拉取、目标清单重建与 GMS 缓存清理"
  - "多管理器兼容：适配 Magisk、KernelSU 与 APatch，并在 `action.sh` 中自动切换 BusyBox `ash` 执行环境"
faq:
  - question: "为什么 AlwaysStrong 使用 `tricky_store` 作为模块 ID？"
    answer: "AlwaysStrong 沿用 `tricky_store` 模块 ID，旨在与现有 Root 管理工具及社区脚本保持无缝兼容，确保各类工具仍可在 `/data/adb/tricky_store/` 下正常读写 `keybox.xml` 与 `target.txt`。"
  - question: "AlwaysStrong 把自身配置和状态保存在哪里？"
    answer: "自 v1.0.5 起，AlwaysStrong 将自身配置、运行状态与分应用密钥盒映射统一存放在 `/data/adb/tricky_store/alwaysstrong/{config,state,apps.map}`（同目录下还包含 `packages`、`spoof.conf`、`imported` 与 `logs/`），避免污染 `/data/adb/tricky_store/` 根目录。"
  - question: "使用 AlwaysStrong 时还需要保留 PlayIntegrityFix 吗？"
    answer: "不需要。AlwaysStrong 已内置经过路径修补的 PlayIntegrityFork（直接读取 `/data/adb/modules/tricky_store/`）与 TEESimulator-RS。刷入前请先卸载独立的 PlayIntegrityFix/Fork 或 TrickyStore 模块，避免双重属性劫持冲突。"
---

## 概述

由 **Evokerr** 开发并托管于 GitLab（**Evokerr/AlwaysStrong**）的 **AlwaysStrong**（`v1.0.6.1`）是一款面向已 Root Android 10+（SDK 29+）设备的一体化整合模块，专为通过 Google `MEETS_STRONG_INTEGRITY` 强完整性认证而设计。

在传统方案中，通过强完整性认证往往需要分别刷入、配置并维护多个独立模块——即硬件密钥证明模拟器（TEESimulator-RS）与系统指纹伪装模块（PlayIntegrityFork）。AlwaysStrong 将二者整合进单个即插即用的刷入包，并配备内置 WebUI、原生拉取工具（`asfetch` 与 `aswatcher`）及一键 Action 维护流程。

---

## 技术架构与工作原理

### 统一栈编排机制

AlwaysStrong 在单一模块目录（`/data/adb/modules/tricky_store/`）内协同运行系统框架伪装与硬件 Keystore 模拟：

1. **双引擎深度集成**：内嵌 **TEESimulator-RS** 原生组件（`libTEESimulator.so`、`libinject.so`、`libsupervisor.so`、`libcertgen.so`、`daemon` 与 `tee_classes.dex`）以及针对模块目录二进制重定位的 **PlayIntegrityFork**（读取模块内的 `custom.pif.prop`）。
2. **集中式数据布局**：模块自用的运行数据位于 `/data/adb/tricky_store/alwaysstrong/`，其中 `config` 保存 `auto_fp`、`interval_sec` 等键值对设置，`state` 记录引擎与后台循环状态，`apps.map` 存储分应用 Keybox 与模式映射，另有 `packages`、`spoof.conf`、`imported`、`logs/` 与 `tmp/`；而证明引擎核心文件（`keybox.xml`、`target.txt`）仍保留在 `/data/adb/tricky_store/`。
3. **Action 与开机自动化管线**：点击 **Action**（`action.sh`）会自动切换至管理器内置 BusyBox `ash`，依次刷新有效 Keybox 证书、拉取最新 Pixel 设备指纹、重建 `/data/adb/tricky_store/target.txt`、同步安全补丁日期并清理 Google Play 服务缓存。
4. **WebUI 可视化控制台**：在 KernelSU、APatch 及支持 WebUI 的 Magisk 管理器中提供内置 `webroot/` 界面，可直接调整自动刷新周期、导入 Keybox、修改高级伪装开关与勾选目标应用。

---

## 安装与配置步骤

1. 卸载设备中已有的独立版 TrickyStore、TEESimulator 或 PlayIntegrityFix/Fork 模块。
2. 确认已启用独立 Zygisk 实现（推荐 **ZygiskNext**、**ReZygisk** 或 **NeoZygisk**；若使用 Magisk，请保持 **遵守排除列表 / Enforce DenyList** 为关闭状态）。
3. 从 GitLab 官方仓库（`Evokerr/AlwaysStrong`）下载 `AlwaysStrong-v1.0.6.1.zip`。
4. 在 Root 管理器中从本地刷入该模块（不支持在 Recovery 模式下刷入）并重启设备。
5. 重启后在管理器中点击模块卡片上的 **Action** 按钮，完成首次初始化与凭证拉取。

---

## 日常使用与配置文件

- **WebUI 管理面板**：打开模块 WebUI 即可配置定时自动更新、覆盖高级伪装参数（`spoof.conf`）、导入本地 Keybox 并指定目标包名。
- **核心路径速查**：
  ```text
  /data/adb/tricky_store/keybox.xml
  /data/adb/tricky_store/target.txt
  /data/adb/tricky_store/alwaysstrong/config
  /data/adb/tricky_store/alwaysstrong/state
  /data/adb/tricky_store/alwaysstrong/apps.map
  ```
- **旧版自动迁移**：从 v1.0.5 之前的版本升级时，`post-fs-data.sh` 会自动调用 `as_migrate`，将 `/data/adb/tricky_store/` 下的零散标记文件无损导入 `/data/adb/tricky_store/alwaysstrong/`。

---

## 常见问题与排查

- **认证依然失败**：在 Root 管理器中再次点击 **Action** 按钮，拉取未吊销的最新证书与指纹并强制重置 Play 服务认证缓存，同时可查看 `/data/adb/tricky_store/alwaysstrong/logs/` 下的运行日志。
- **Zygisk 环境建议**：尽量避免使用 Magisk 自带 Zygisk，且在使用独立 Zygisk 加载器时不要开启 **Enforce DenyList**，以免阻断模块注入与隐藏逻辑。
