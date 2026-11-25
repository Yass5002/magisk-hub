---
id: "magicalprotection"
title: "MagicalProtection：零配置 Systemless Hosts 去广告模块"
sidebarTitle: "MagicalProtection"
description: "提供全自动、零配置的无系统分区修改（Systemless）hosts 广告与追踪拦截方案，无需安装配套应用或开启 Systemless Hosts 开关。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "MagicalProtection Magisk 模块"
  - "programminghoch10 MagicalProtection 下载"
  - "Magisk 零配置去广告模块"
  - "Android Systemless hosts 去广告"
  - "EnergizedProtection 替代去广告方案"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
conflicts:
  - "其他 Systemless hosts 管理工具（例如处于 Root hosts 模式的 AdAway 或 EnergizedProtection）"
configPaths:
  - "/data/adb/modules/MagicalProtection/"
features:
  - "零配置开箱即用：刷入并重启即可生效，无需设置向导、终端命令或配套应用"
  - "自包含 hosts 挂载：直接将精选拦截表挂载覆盖至 `/system/etc/hosts`，无需手动开启 Magisk 的 Systemless Hosts 开关"
  - "自动化 CI/CD 构建发布：通过 GitHub Actions 流水线自动拉取并整合最新过滤规则"
  - "双组件版本追踪：同时记录模块核心脚本版本（`mv`）与底层 hosts 规则库修订版本（`hv`）"
  - "全面域名防护：拦截广告联盟网络、第三方统计追踪器、遥测上报端点及已知恶意域名"
faq: []
---

## 概述

虽然 EnergizedProtection 和 AdAway 等工具提供了强大的广告拦截能力，但它们通常需要手动在终端中交互操作、授予配套应用权限或依赖外部服务。

由 programminghoch10 开发的 **MagicalProtection** 提供了一种精简、一劳永逸的全局去广告方案。借鉴了 EnergizedProtection 的便利性与 Magisk Magic Mount 架构，MagicalProtection 直接在模块内部打包了经过预编译与高度优化的 hosts 文件。它无需任何配置或配套 APK，完全以无系统分区修改（Systemless）方式运行。

## 架构优势

- **不依赖 Systemless Hosts 开关**：不同于需要在 Magisk 设置中启用内置 Systemless Hosts 开关的 AdAway，MagicalProtection 会在开机时直接将精选文件绑定挂载至 `/system/etc/hosts`。
- **双维度版本追踪**：发布版标签采用明确的双层格式（如 `mv19-hv121`），其中 `mv` 代表模块脚本版本号，`hv` 代表 hosts 规则库修订版本号。
- **上游规则自动同步**：模块仓库利用 GitHub Actions 自动化流水线，定期拉取、校验并对权威拦截列表执行去重合并。
- **符合 POSIX 标准的 Shell 逻辑**：简洁且符合规范的 Shell 脚本可避免在不同 Android Toybox 与 BusyBox 环境下出现开机卡顿或语法报错。

## 安装步骤

1. 从 GitHub 发布页下载最新的 `MagicalProtection-mv*-hv*.zip` 安装包。
2. 打开 **Magisk Manager**，进入 **模块 > 从本地安装**，选择该 zip 压缩包。
3. 重启 Android 设备。
4. 重启后，广告与追踪拦截将立即在所有浏览器、WebView 及原生应用中生效。

## 卸载方法

如需恢复系统原生的域名解析，只需在 Magisk Manager 中停用或移除 MagicalProtection 并重启即可。原始 `/system/etc/hosts` 文件全程保持完全未被修改的状态。
