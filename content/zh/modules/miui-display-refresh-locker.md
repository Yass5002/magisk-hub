---
id: "miui-display-refresh-locker"
title: "MIUI Display Refresh Rate Locker：禁用动态降频实现全局锁定高刷"
sidebarTitle: "MIUI 全局高刷锁定"
description: "内核与 SurfaceFlinger 属性调优模块，在小米 MIUI 与澎湃 OS 上永久锁定 120Hz/144Hz 高刷新率，彻底屏蔽自动降频。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "MIUI 全局高刷 Magisk 模块"
  - "锁定 120Hz MIUI 澎湃 OS 模块"
  - "禁用 MIUI SmartFPS 模块下载"
  - "解决小米看视频自动降频 60Hz"
prerequisites:
  - "支持高刷新率屏幕并运行 MIUI 或澎湃 OS（HyperOS）的小米、红米或 POCO 设备"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "其他同样修改屏幕刷新率规则的厂商覆写脚本"
configPaths:
  - "/system/etc/system.prop"
features:
  - "禁用 MIUI 私有 SmartFPS 与基于显示内容的动态刷新率自适应"
  - "在视频播放、浏览器滚动及电子书阅读场景下保持满血高刷"
  - "覆盖厂商 Joyose 与 SurfaceFlinger 的频率降档策略"
  - "无需改动物理系统分区，即可维持顺滑无卡顿的全局界面动效"
faq:
  - question: "为什么 MIUI 会把我的屏幕刷新率从 120Hz 降到 60Hz？"
    answer: "小米 MIUI 与澎湃 OS 内置了激进的省电策略（SmartFPS 与 Joyose），当系统检测到画面静止、正在播放视频流或打开特定包名的应用时，会自动将显示控制器降至 60Hz。本模块正是用于关闭此类自动降频检测。"
  - question: "长期锁定高刷对屏幕面板安全吗？"
    answer: "安全。本模块仅让屏幕维持在厂商出厂硬件官方支持的 120Hz/144Hz 刷新率档位内运行，不会超频或突破面板设计上限。"
---

## 概述

**MIUI Display Refresh Rate Locker**（由 key 基于 kevmck、Liangmisanxing 与 kakathic 的研究成果开发）是一款专门解决小米 MIUI 与澎湃 OS（HyperOS）固件中频繁自动降刷新率问题的定向优化模块。

尽管小米手机配备了流畅的 120Hz 与 144Hz OLED 屏幕，原厂系统在播放视频、阅读电子书或使用部分第三方应用时仍会频繁将刷新率压低至 60Hz。这种反复横跳的刷新率切换在滑动列表或切换应用时会带来明显的视觉微卡顿，而本模块可彻底稳定全局刷新率。

---

## 技术架构与工作原理

该模块通过 `system.prop` 注入多条系统属性，从底层屏蔽 MIUI 的刷新率降档逻辑：

### 1. SurfaceFlinger 属性覆写

```ini
# Disable dynamic smart fps adaptation
persist.sys.smartfps=0

# Disable vendor default fps downclocking switch
ro.vendor.fps.switch.default=false

# Disable content-aware refresh rate scaling in SurfaceFlinger
ro.surface_flinger.use_content_detection_for_refresh_rate=false
```

### 2. 框架合成器协调

通过指示 Android SurfaceFlinger 显示合成器忽略视频播放帧率元数据，无论前台媒体源本身是 24 FPS、30 FPS 还是 60 FPS，显示控制器都将始终维持最高扫描刷新率。

---

## 故障排查与验证

- **实时刷新率显示**：前往 **设置 > 更多设置 > 开发者选项**，开启 **显示刷新率** 开关，即可直观确认屏幕已稳定锁定在 120Hz/144Hz。
- **机身温度保护**：在极端高温环境下，设备内核仍可能触发硬件级热安全降频；这属于底层内核硬件保护机制，与软件层面的 SmartFPS 降频彼此独立。
