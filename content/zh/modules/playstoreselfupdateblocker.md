---
id: "playstoreselfupdateblocker"
title: "PlayStoreSelfUpdateBlocker：实时拦截 Google Play 商店静默自更新"
sidebarTitle: "Play 商店防自更新"
description: "阻止 Google Play 商店在后台静默自动更新，帮助已 Root 设备锁定特定版本以维持 Play Integrity 认证状态。"
category: "system-environment"
tier: 1
searchQueries:
  - "play store self update blocker Magisk"
  - "pusblocker himanshujjp 下载"
  - "Root 禁止 Google Play 商店自动更新"
  - "Play Integrity 锁定 Play 商店版本"
  - "KernelSU 阻止 Play 商店静默更新"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/playstoreselfupdateblocker/"
features:
  - "主动后台守护监测：以 30 秒为周期监控 Google Play 商店软件包变动，CPU 占用极低"
  - "自动回滚触发机制：检测到未经授权的后台静默更新后，立即恢复预设锁定的版本"
  - "Play Integrity 认证防护：防止新版 Play 商店强制启用更严苛的硬件级密钥证明校验"
  - "广泛支持主流 Root 管理器：在 Magisk、KernelSU 与 APatch 环境下均能稳定运行"
  - "纯净无系统分区修改架构：在暂存与安装阶段拦截更新事务，不改动底层系统分区"
---

## 概述

对于致力于维持 Google Play Integrity 认证（`MEETS_DEVICE_INTEGRITY` / `MEETS_STRONG_INTEGRITY`）的已 Root Android 用户而言，将 Google Play 商店（`com.android.vending`）锁定在特定版本往往至关重要。Google 会定期向 Play 商店客户端推送静默无感更新，引入更严格的服务端完整性校验逻辑，从而在毫无预警的情况下使定制设备指纹或 PlayIntegrityFix 挂钩失效。

由 himanshujjp 开发的 **PlayStoreSelfUpdateBlocker**（简称 PUSBlocker）是一款采用无系统分区修改（Systemless）机制的后台守护模块，旨在永久阻止 Google Play 商店在后台自行静默更新。

## PUSBlocker 工作原理

1. **轻量级轮询监控**：运行一个低资源占用的后台服务，约每隔 30 秒检查一次 `com.android.vending` 的已安装版本号与 APK 哈希值。
2. **即时拦截暂存更新**：当 Google Play 服务将新版 Play 商店 APK 下载至暂存缓存目录时，PUSBlocker 会拦截该更新事务或清理暂存安装包。
3. **自动回滚恢复**：若 Google 在设备休眠期间成功完成了更新推送，守护进程会在唤醒后检测到版本不匹配，并自动执行清理回滚，将 Play 商店还原为你指定的锁定版本。

## 兼容性与安装步骤

- **Root 兼容性**：全面兼容 **Magisk**、**KernelSU** 与 **APatch**。
- **安装步骤**：
  1. 先将 Google Play 商店降级或安装为你希望锁定的目标 APK 版本。
  2. 从 GitHub Releases 页面下载最新版 `PlayStoreSelfUpdateBlocker-v*.zip`。
  3. 在 Root 管理器中刷入该模块并重启设备。
  4. 后台守护服务随即生效，并将当前 Play 商店版本锁定到位。
