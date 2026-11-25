---
id: "hyperos-theme-manager"
title: "HyperOS Theme Manager Mod：解锁主题商店、MTZ 导入与超级图标"
sidebarTitle: "HyperOS Theme Manager"
description: "由 Kashi 修改的 HyperOS 主题壁纸 V6 模块，为全系澎湃 OS 设备解锁第三方 MTZ 主题导入、多区域主题服务器、付费资源及超级图标。"
category: "customization-ui"
tier: 1
searchQueries:
  - "HyperOS 主题商店修改版 Magisk"
  - "Kashi HyperOS Theme Manager V6"
  - "澎湃 OS 导入第三方 MTZ 主题"
  - "小米澎湃免费解锁付费主题"
  - "Apk Protection Patch 国行澎湃 OS"
prerequisites:
  - "运行澎湃 OS（HyperOS）的 Xiaomi、Redmi 或 POCO 设备"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "国行原版（CN）ROM 用户必须预先刷入 Apk Protection Patch 模块"
  - "建议配合修改版负一屏（App Vault）模块使用，以确保桌面高端小部件正常显示"
conflicts:
  - "非澎湃 OS 设备及标准 AOSP 类 ROM"
  - "Magisk Delta（存在已知的兼容性问题）"
configPaths:
  - "/data/adb/modules/"
features:
  - "第三方主题自由导入：绕过官方签名校验，直接导入社区分享的 `.mtz` 主题安装包"
  - "多区域服务器切换：同时浏览并下载国际服、印度服与国行主题商店中的丰富资源"
  - "付费资源免费解锁：移除收费主题、字体与图标包的付费门槛与广告限制"
  - "超级图标与小部件集成：在旗舰及中低端机型上同步开启炫酷超级图标与自定义小部件形态"
  - "AI 壁纸集成：解锁隐藏的 AI 生成壁纸与景深壁纸调节控制项"
faq: []
---

## 概述

由 Kashi 在 Mods-Center 组织下维护的 HyperOS Theme Manager Mod，将限制重重的小米原厂主题壁纸应用替换为深度定制的 V6 修改版。原版澎湃 OS 主题商店拥有严格的版权保护（DRM）限制：禁止用户导入第三方 `.mtz` 主题包、屏蔽跨区主题资源库、对优质主题收取米币费用，并在入门机型上禁用超级图标功能。

这款无系统分区修改（Systemless）模块能够绕过上述限制。通过以无侵入方式替换主题管理器 APK，在保障底层系统安全完整性的同时，充分释放澎湃 OS 的个性化视觉定制潜力。

## 前置条件与兼容性

- **设备与系统**：严格仅限运行澎湃 OS 的小米、Redmi 及 POCO 机型。不兼容 AOSP、LineageOS 或其他品牌定制系统。
- **Root 方案**：支持 Magisk 或 KernelSU。
  - **不兼容说明**：Magisk Delta（狐狸面具）的 APK 替换机制存在已知冲突，不建议使用。
- **国行原版（CN）ROM 必读**：如果你使用的是官方国行版系统，在安装本模块前**必须先刷入 [Apk Protection Patch](https://github.com/Mods-Center/Apk-Protection-Patch)** 模块，否则小米系统完整性校验会拦截并丢弃修改后的系统 APK。
- **搭配 App Vault 负一屏**：为确保主题附带的高级桌面小部件能够正常加载并运行，强烈建议搭配使用兼容的修改版 App Vault 负一屏模块。

## 核心功能与特性

- **无限制 MTZ 导入**：直接在主题商店内导入任意第三方 `.mtz` 主题文件，不再弹出“不支持第三方来源主题”的拦截提示。
- **解除商业化付费限制**：无需观看广告或兑换积分，即可直接免费应用高级图标包、动态锁屏与正版付费字体。
- **多区主题商店目录**：支持切换并拉取多个区域服务器数据，畅享原本仅限特定亚洲或欧洲市场供应的海量主题。
- **全机型支持超级图标**：为原本被官方固件屏蔽该特性的中低端手机解锁 2x1、1x2 与 2x2 动态超级图标。

## 安装与使用

1. 若使用国行原版澎湃 OS，请先刷入 `Apk Protection Patch` 模块并重启一次。
2. 从官方仓库发布页下载 `HyperOS_ThemeManagerV6*.zip`。
3. 通过 Magisk 或 KernelSU 刷入该模块。
4. 重启设备。
5. 打开桌面上的**主题壁纸**应用：
   - 进入 **我的 > 主题 > 从 SD 卡导入**（Profile > Themes > Import）即可导入本地 `.mtz` 文件。
   - 自由浏览在线商店并一键应用各类主题与字体。

## 故障排查与验证

- **应用第三方主题几分钟后自动恢复默认**：若第三方主题在短暂使用后被重置为默认主题，请检查是否已关闭小米主题授权守护进程，或确认前置签名破解模块处于激活状态。
- **桌面小部件缺失**：若导入的主题无法在桌面正确显示交互式小部件，请安装配套的修改版 App Vault 模块，并确认已授予系统桌面相关权限。
