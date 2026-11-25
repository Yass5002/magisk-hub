---
id: "supl-replacer"
title: "SUPL Replacer：基于 GrapheneOS 代理的 A-GPS 定位隐私保护模块"
sidebarTitle: "SUPL Replacer"
description: "将 gps.conf 中默认的 Google SUPL（安全用户面定位）A-GPS 服务器替换为注重隐私保护的 GrapheneOS 代理服务器，阻止定位时的 IMSI 追踪。"
category: "system-utilities"
tier: 1
searchQueries:
  - "supl-replacer Magisk 下载"
  - "Android Root 替换 Google SUPL 服务器"
  - "gps.conf 隐私 GrapheneOS SUPL 代理"
  - "防止 A-GPS 定位泄露手机 IMSI"
  - "Android 辅助定位隐私保护模块"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/supl-replacer/"
features:
  - "A-GPS 隐私加固：将硬编码的 Google SUPL 服务器（supl.google.com）替换为隐私优先的 GrapheneOS SUPL 代理"
  - "阻断 IMSI 泄露：防止移动运营商与 Google 在设备进行 GPS 定位时收集你的 SIM 卡唯一 IMSI 与基站标识"
  - "保留秒级搜星速度：继续享受辅助 GPS 快速首次定位时间（TTFF）的星历下载加速"
  - "双分区叠加覆盖：无侵入式同时覆盖 /system/etc/gps.conf 与 /vendor/etc/gps.conf"
  - "全芯片平台兼容：支持高通（Qualcomm）、联发科（MediaTek）及三星 Exynos GNSS 定位硬件栈"
---

## 概述

当智能手机获取卫星定位时，Android 会通过 **安全用户面定位（SUPL）** 协议启用 **辅助 GPS（A-GPS）**，快速下载卫星轨道预测信息（星历数据），从而将首次定位时间（TTFF）从数分钟大幅缩短至数秒。

然而，标准 Android 系统默认使用 `supl.google.com`。每当应用请求 GPS 定位时，系统都会发送未加密或保护极弱的数据包，其中往往携带你 SIM 卡的唯一 **IMSI**（国际移动用户识别码）以及当前所在基站的编号。这会向 Google 持续且静默地泄露你的设备身份与位置遥测信息。

**supl-replacer** 是一款无系统分区修改的隐私保护模块，通过修改 `gps.conf` 将所有 SUPL 请求重定向至 **GrapheneOS** 项目维护的隐私保护代理服务器。

## 隐私保护机制

1. **接入 GrapheneOS 代理**：将配置文件中的 `SUPL_HOST=supl.google.com` 替换为 GrapheneOS 提供的安全代理服务器（`supl.grapheneos.org`）。
2. **剥离 IMSI 标识**：GrapheneOS 代理会在向上游中继星历查询请求前，剥离数据包中的 SIM 卡 IMSI 与本地基站标识符，在不记录任何个人硬件识别信息的前提下返回最新卫星星历数据。
3. **不损失搜星速度**：在导航应用（如 Google Maps、OsmAnd、Waze）中依然能够获得亚秒级快速卫星定位，同时不再上传多余的隐私遥测数据。

## 安装步骤

1. 从 GitHub Releases 下载最新版的 `supl-replacer-v*.zip` 压缩包。
2. 在 **Magisk** 中安装该模块。
3. 重启设备。
4. 打开任意 GPS 测试应用（例如 GPSTest），验证 A-GPS 卫星定位是否能够快速完成锁定。
