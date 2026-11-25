---
id: "alterinstaller"
title: "AlterInstaller：应用包管理器安装来源与更新所有者伪装"
sidebarTitle: "AlterInstaller"
description: "由 chenxiaolong 开发的无侵入式工具模块，无需运行时 Zygisk 注入即可直接修改 Android 包管理数据库中的应用安装来源与更新所有者属性。"
category: "system-environment"
tier: 1
searchQueries:
  - "AlterInstaller Magisk 模块"
  - "chenxiaolong AlterInstaller"
  - "Root 伪装 Google Play 安装来源"
  - "Android packages.xml 修改更新所有者"
  - "Android 14 更改应用安装程序包名"
prerequisites:
  - "Android 12 及以上系统（Android 12、13、14、15、16）"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
conflicts:
  - "Android 11 及更早版本系统（明确不支持）"
configPaths:
  - "/data/local/tmp/AlterInstaller.json"
  - "/data/local/tmp/AlterInstaller.log"
  - "/data/system/packages.xml"
features:
  - "安装来源包名伪装：覆盖任意目标应用的 `installer`、`initiating installer` 与 `update owner` 属性"
  - "无 Hook XML 直接修改：在 PackageManagerService 初始化之前的开机早期直接修改 `/data/system/packages.xml`，带来零 Zygisk 性能开销"
  - "绕过反侧载安装检测：满足金融银行与企业级应用要求通过官方 Google Play 商店安装的安全校验"
  - "精确控制应用商店更新归属：将本地侧载安装的开源软件绑定至特定商店管理器（如 F-Droid、Droid-ify），防止 Google Play 误推送覆盖更新"
faq: []
---

## 概述

**AlterInstaller** 由知名 Android 软件工程师 chenxiaolong 开发，是一款专门用于在 Android 12 及更高版本上伪装包管理器应用来源元数据的 Root 实用工具。

如今，越来越多的 Android 应用加入了严格的防侧载检测机制。金融理财应用、受 DRM 保护的流媒体播放器以及部分游戏会调用 `PackageManager.getInstallSourceInfo()` 查询自身是由哪个安装程序安装的。如果系统记录显示该应用是通过本地 APK 安装器侧载而非从 Google Play（`com.android.vending`）下载，应用就可能限制部分功能甚至拒绝启动。此外，自 Android 14 起，系统强制实施了「更新所有者（Update Ownership）」机制，将应用的后续更新权限锁定给特定的应用商店。

AlterInstaller 能够同时解决这两项痛点。它在 Android 系统服务尚未启动的早期引导阶段直接修补 `/data/system/packages.xml`，从而安全、持久地修改包管理元数据，完全无需借助侵入式的运行时内存 Hook。

## 前置要求与兼容性

- **Android 版本**：**仅支持 Android 12 及更高版本**。Android 11 及更早系统缺少对应的更新所有权与安装来源分离字段，因此不受支持。
- **Root 环境**：同时兼容 Magisk 与 KernelSU。
- **无 Hook 设计**：无需安装 Zygisk、LSPosed 或 Xposed 框架。

目前暂无已知的模块冲突。

## 配置与使用方法

AlterInstaller 从位于 `/data/local/tmp/` 目录下的简洁 JSON 配置文件读取规则：

1. 在 Magisk 或 KernelSU 中刷入 `AlterInstaller-*.zip` 模块。
2. 使用任意具备 Root 权限的文件管理器或终端创建 `/data/local/tmp/AlterInstaller.json`：
   ```bash
   su
   cat << 'EOF' > /data/local/tmp/AlterInstaller.json
   {
       "org.videolan.vlc": {
           "installer": "com.android.vending",
           "updateOwner": "com.looker.droidify"
       },
       "com.example.bankingapp": {
           "installer": "com.android.vending"
       }
   }
   EOF
   ```
3. 设置合适的文件读取权限（`chmod 644 /data/local/tmp/AlterInstaller.json`）。
4. 重启设备。
5. 在系统早期启动阶段，AlterInstaller 会解析该 JSON 配置，修改 `/data/system/packages.xml` 中对应的软件包标签，并输出执行日志。

### 支持的配置属性

| 键名 | 说明 | 示例 |
| :--- | :--- | :--- |
| `installer` | 向上层报告的应用安装来源包名 | `com.android.vending`（Google Play） |
| `updateOwner` | 有权对该应用执行后续更新的商店包名 | `com.looker.droidify` 或 `org.fdroid.fdroid` |

## 故障排查与验证

- **验证规则是否生效**：重启后立即查看模块输出的日志文件：
  ```bash
  cat /data/local/tmp/AlterInstaller.log
  ```
- **直接向包管理器查询核验**：检查 Android 系统当前向目标应用报告的安装来源信息：
  ```bash
  su -c "dumpsys package com.example.bankingapp | grep -E 'installerPackageName|initiatingPackageName'"
  ```
- **卸载模块后修改依然保留**：由于 AlterInstaller 是将合法的 XML 标签直接写入持久化数据库文件 `/data/system/packages.xml`，即使随后禁用或卸载该模块，已修改的应用属性仍会保留。如需还原某个应用的安装来源，请从 `AlterInstaller.json` 中移除对应条目并重启，或使用原始安装器重新安装。
