---
id: "copg"
title: "COPG：自带 WebUI 的分应用机型与 GPU 信息伪装模块"
sidebarTitle: "COPG"
description: "基于 Zygisk 的高级分应用设备、CPU 与 GPU 伪装模块，通过本机 WebUI 为特定游戏解锁 90/120fps 高帧率与高画质档位。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "copg Magisk 模块下载"
  - "Magisk 解锁游戏 90 120 帧"
  - "alirezaparsi copg 使用教程"
  - "Zygisk 分应用机型伪装"
  - "Android GPU 型号伪装模块"
prerequisites:
  - "Magisk（开启 Zygisk）、KernelSU 或 APatch"
  - "Android 9.0 至 Android 15"
conflicts:
  - "会全局修改 `ro.product` 系统属性的通用机型伪装模块"
configPaths:
  - "/data/adb/copg/"
  - "/data/adb/modules/copg/"
  - "/data/adb/modules/COPG/COPG.json"
features:
  - "分应用独立伪装：仅针对指定游戏伪装为小米 14 Ultra 或 ROG Phone 8 等旗舰机型，系统其他应用保持原厂信息"
  - "内置交互式 WebUI：可直接通过 Root 管理器打开可视化界面选择预设机型模板"
  - "解锁受限画质帧率：支持在《PUBG Mobile》《使命召唤手游》《原神》与《英雄联盟手游》中开启 90Hz、120Hz 与极限 HDR"
  - "OpenGL 与 Vulkan 渲染器伪装：支持伪装 Adreno 750 / Mali-G720 等旗舰 GPU 渲染器字符串"
faq:
  - question: "为什么硬件性能明明足够，很多游戏还是锁死了高帧率选项？"
    answer: "不少手游开发商会与特定手机品牌（如 ASUS ROG、黑鲨或一加）合作开放独占的 90fps 或 120fps 模式，而把白名单之外的机型硬性限制在 60fps，即便其硬件性能更强。COPG 可以让游戏误认为当前设备属于官方适配的旗舰机型。"
  - question: "使用 COPG 会影响 Google Wallet 或银行应用吗？"
    answer: "不会。与全局篡改 `build.prop` 的传统模块不同，COPG 通过 Zygisk 严格按应用进程生效。你的银行应用与 Google Play 服务读取到的依然是经过认证的原厂设备指纹。"
---

## 概述

由 **AlirezaParsi** 开发的 **COPG**（Custom OEM Profile Generator）是一款基于 Zygisk 的现代分应用硬件信息伪装模块，并配备了完整的本机 WebUI 控制面板。

在手游生态中，诸多热门竞技游戏（如《PUBG Mobile》《使命召唤：战区手游》《原神》与《荒野乱斗》）会根据设备上报的厂商型号与 GPU 渲染器字符串限制画质档位、粒子特效密度及 90Hz/120Hz 高刷新率开关。COPG 允许你按单个应用粒度分配旗舰硬件配置模板，同时完全不干扰系统整体稳定性。

---

## 技术架构与工作原理

### 定向 Zygisk 属性与 OpenGL 拦截

1. **进程级精准匹配**：当某个应用进程启动时，COPG 会检查 `/data/adb/copg/profiles.json` 中是否为该包名分配了自定义配置。
2. **Build Prop 属性模拟**：在目标进程内部挂钩 `__system_property_get`，按需返回伪装后的 `ro.product.model`、`ro.product.brand` 与 `ro.product.manufacturer` 字符串。
3. **OpenGL / Vulkan 查询挂钩**：拦截 `glGetString(GL_RENDERER)` 与 `glGetString(GL_VENDOR)` 调用，使 3D 渲染引擎识别到诸如骁龙 8 Gen 3 Adreno 750 等顶级 GPU 型号。
4. **作用域严格隔离**：未在 COPG 中配置的应用不受任何影响，直接读取操作系统原生的系统属性。

---

## 安装与配置

1. 打开 **Magisk**、**KernelSU** 或 **APatch**。
2. 下载并刷入最新版的 `COPG-vX.zip`。
3. 重启设备。
4. 直接从 Root 管理器的模块列表中打开 **COPG WebUI**（若已启用端口监听，也可访问 `http://127.0.0.1:8080`）。
5. 在应用列表中搜索目标游戏，选择一个旗舰预设模板（例如 *ASUS ROG Phone 8 Pro*），然后点击 **Apply**。
6. 启动游戏并进入画面设置，即可开启高帧率模式。
