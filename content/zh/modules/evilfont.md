---
id: "evilfont"
title: "EvilFont：无侵入式阿拉伯语/波斯语字体与 Apple Emoji 定制模块"
sidebarTitle: "EvilFont"
description: "支持音量键交互安装的字体定制模块，以无侵入式方式替换 Android 默认阿拉伯语与波斯语字体，并集成高清 Apple Emoji。"
category: "customization-ui"
tier: 1
searchQueries:
  - "EvilFont Magisk 模块"
  - "dedeadend EvilFont 下载"
  - "安卓 Root 替换阿拉伯语波斯语字体"
  - "苹果 iOS Emoji Magisk 模块"
  - "音量键交互字体安装模块"
prerequisites:
  - "Android 8.0 及以上系统"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "用于安装菜单导航的实体音量按键"
conflicts:
  - "其他已启用的系统字体或 Emoji 覆盖模块（会引发 fontconfig XML 与 NotoColorEmoji 冲突）"
configPaths:
  - "/data/adb/modules/evilfont/"
  - "/system/fonts/"
features:
  - "交互式音量键安装：直接在 Root 管理器刷入终端中逐步选择字体与 Emoji 组合"
  - "精选阿拉伯语与波斯语字库：将生硬的系统回退字体替换为优雅易读的中东风格字体"
  - "高清 Apple Emoji：将完整且最新的 iOS Emoji 字形集注入 Android 字体渲染管线"
  - "灵活的模块化部署：支持仅安装阿拉伯语字体、仅安装 Apple Emoji 或两者同时安装"
  - "零分区改动：干净地覆盖挂载至 /system/fonts/，完全不触碰系统物理分区"
faq: []
---

## 概述

尽管 Android 默认的排版引擎近年来不断改进，但其对非拉丁文字——尤其是阿拉伯语和波斯语（Farsi）——的渲染仍常常依赖简陋的通用回退字体，存在字形度量不均、基线对齐不佳及字距调整生硬等问题。此外，许多用户相比厂商自带的 Emoji 图标，更青睐视觉风格统一和谐的 iOS Emoji。

由 dedeadend 开发的 **EvilFont** 是一款面向已 Root Android 设备的精致交互式字体定制模块。EvilFont 通过干净的无侵入式（Systemless）挂载机制，让用户能够从精选的阿拉伯语与波斯语字库中自由挑选美观字体，并按需整合原生 Apple iOS Emoji。

## 交互式音量键安装程序

EvilFont 直接在 Magisk、KernelSU 或 APatch 的刷入终端中提供交互式文本菜单，免去了手动预先修改配置文件的繁琐：

1. **分类选择**：安装脚本会提示选择仅刷入**字体（Fonts Only）**、仅刷入**Apple Emoji（Apple Emojis Only）**，或**两者同时刷入（Both）**。
2. **字体浏览与选定**：按 **[VOL+]** 在精选的阿拉伯语/波斯语字体列表中循环切换，按 **[VOL-]** 确认选择。
3. **Emoji 配置**：选择是否使用苹果高分辨率 Emoji 资源包替换 Android 原生的 `NotoColorEmoji.ttf`。
4. **自动生成 XML 配置**：安装脚本会自动生成所需的 `fonts.xml` 声明，并将修改后的文件挂载覆盖到 `/system/fonts/`。

## 为什么无侵入式字体覆盖至关重要

过去手动替换字体通常需要将 `/system` 挂载为可读写（`rw`）并直接覆盖系统文件——在采用只读动态分区（`erofs`/`ext4`）和 dm-verity 加密校验的现代 Android 设备上，这种操作极易引发系统异常甚至无法开机。

EvilFont 以无侵入式（Systemless）方式部署所有 `.ttf` 资源：
- 100% 保持系统分区完整性。
- 在 Root 管理器中禁用或卸载该模块后，即可立即恢复原厂字体与 Emoji。

## 安装操作步骤

1. 确认未启用其他字体或 Emoji 模块，以免发生挂载冲突。
2. 下载 `EvilFont` `.zip` 发布包。
3. 打开你的 Root 管理器，选择**从本地安装**（Install from storage）。
4. 留意刷入终端屏幕提示：
   - 按提示按下 **[VOL+]** 滚动切换选项。
   - 按下 **[VOL-]** 确认当前选择。
5. 待终端提示 `Done!` 完成安装后，重启手机。
6. 打开常用的聊天或社交应用，即可体验焕然一新的字体排版与 Apple Emoji。
