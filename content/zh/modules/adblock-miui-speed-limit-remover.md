---
id: "adblock-miui-speed-limit-remover"
title: "AdBlock & MIUI Download Speed Limit Remover：无侵入式去广告与限速解除指南"
sidebarTitle: "MIUI 去广告与解除限速"
description: "综合性去广告与网络优化模块，结合 42,000+ hosts 重定向、iptables 空路由、空壳 APK 替换与无侵入式 MIUI 下载限速绕过。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "miui 去广告 magisk 模块"
  - "小米解除下载限速 root 模块"
  - "analyticscore 替换去广告"
  - "安卓 systemless hosts 去广告"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "Android 9.0 至 Android 14（MIUI、HyperOS 或 AOSP）"
conflicts:
  - "若未开启 Systemless hosts 选项，可能与其他整块覆盖 hosts 的去广告模块冲突"
configPaths:
  - "/data/adb/modules/GGAT_10007/service.sh"
  - "/data/adb/modules/GGAT_10007/hosts"
  - "/data/adb/modules/GGAT_10007/mod/"
  - "/system/app/AnalyticsCore"
features:
  - "收录超过 42,390 条精选广告与遥测域名空路由规则，覆盖国内外主流广告平台"
  - "使用轻量级空壳 APK 与 .replace 标记替换 AnalyticsCore，彻底切断 MIUI 遥测"
  - "亮屏守护进程按需唤醒，针对特定应用执行专项广告 SDK 屏蔽脚本"
  - "对受保护的 DNS 与 hosts 配置应用 chattr 不可变属性，防止被系统篡改还原"
faq:
  - question: "该模块会屏蔽第三方浏览器中的文件下载吗？"
    answer: "不会。该模块专门用于解除 MIUI 系统下载器及应用商店内厂商施加的下载带宽限制，同时将广告追踪域名重定向至 0.0.0.0，不影响第三方浏览器的正常下载。"
  - question: "可以手动更新 hosts 规则文件吗？"
    answer: "可以。模块内置了 update.sh 更新脚本，并支持读取位于模块目录内的用户自定义规则配置文件。"
---

## 概述

**AdBlock & MIUI Download Speed Limit Remover**（作者：ZiXuan & MoLiRanRan）是一套专为小米 MIUI 与澎湃 HyperOS 环境深度打造的无侵入式网络过滤及系统精简套件，同时保持对通用 AOSP 固件的完整兼容。

在原厂 MIUI 系统中，小米在底层集成了主要依赖 `AnalyticsCore` 的系统级遥测与广告推送网络，并在系统应用安装器及内置浏览器中对未开通会员的用户施加了下载带宽限制。该模块在不修改物理 `/system` 块设备的前提下，通过无系统分区修改（Systemless）方式一并解决上述两项问题。

---

## 技术架构与工作原理

模块在系统早期初始化及运行时阶段协同部署了多层防护机制：

### 1. 通过空壳 APK 替换消除系统遥测

在 Magisk 挂载覆盖阶段，模块直接定位小米核心数据采集组件：

```text
/system/app/AnalyticsCore/Analytics.apk
/system/app/AnalyticsCore/.replace
```

通过放置空的占位 APK 并配合 `.replace` 指令，Android `PackageManager` 会将该系统包解析为无效占位符，从而在不引发系统崩溃或无限重启（Bootloop）的情况下彻底阻断后台遥测与下载限速策略。

### 2. 高效 Hosts 路由拦截

模块内置了 42,390 条经过验证的广告、追踪器及埋点域名规则，全部路由至本地回环地址（`0.0.0.0`）：

```text
0.0.0.0 ad.xiaomi.com
0.0.0.0 api.ad.intl.xiaomi.com
0.0.0.0 tracking.miui.com
0.0.0.0 sdkconfig.ad.xiaomi.com
```

脚本会通过 `sort | uniq` 校验规则唯一性，并严格设定 Unix 文件权限（`0644`）。

### 3. 亮屏触发守护进程

`service.sh` 不会在设备深度休眠时执行高耗电轮询，而是等待用户点亮屏幕交互后再触发执行：

```sh
until $(dumpsys deviceidle get screen); do
    sleep 5
done

for i in $MODDIR/mod/*.sh; do
    nohup $i >/dev/null 2>&1 &
done
```

检测到屏幕唤醒后，专项清理脚本（`killpangle.sh`、`ad.sh`、`aweme.sh`、`zhihu.sh`）会随之运行，利用精确的 `iptables` 规则与包管理器限制，精准拦截内嵌于第三方应用中的商业广告 SDK。

---

## 验证与常用运维命令

检查当前 hosts 重定向与空壳替换是否已生效：

```bash
# 测试小米追踪域名的 DNS 空路由是否生效
ping -c 1 ad.xiaomi.com

# 确认 AnalyticsCore 空壳挂载路径
pm path com.miui.analytics
```
