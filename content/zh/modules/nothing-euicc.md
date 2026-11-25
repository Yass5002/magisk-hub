---
id: "nothing-euicc"
title: "Nothing EUICC 启用器：在 Nothing 设备上强制开启 eSIM 与系统级 LPA"
sidebarTitle: "Nothing EUICC Enabler"
description: "通过搭配 eSTK.me 或 5ber 等实体可编程 eSIM 卡，在 Nothing OS 设备上强制启用 eSIM 功能与系统本地配置文件助手（LPA）。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "nothing euicc force enabler Magisk"
  - "reindex-ot nothing-euicc 下载"
  - "Nothing Phone 1 2 开启 eSIM"
  - "Nothing OS 系统 LPA eSTK 教程"
  - "5ber eSIM Nothing 手机 Magisk 模块"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
  - "搭载高通处理器的 Nothing Phone (1) 或 Nothing Phone (2)"
  - "实体可编程 eSIM 卡贴/写卡器（例如 eSTK.me 或 5ber）"
conflicts: []
configPaths:
  - "/data/adb/modules/nothing-euicc/"
features:
  - "系统级 LPA 激活：启用 Android 原生本地配置文件助手（Local Profile Assistant）框架，实现流畅的 eSIM 配置文件下载与切换"
  - "可插拔智能 eSIM 卡集成：完整支持放入 SIM 卡槽的 eSTK.me 与 5ber 实体 eSIM 芯片"
  - "系统原生管理：直接在 Nothing OS 网络设置中管理 eSIM 配置文件，无需完全依赖第三方配套 App"
  - "高通基带适配优化：专门针对高通调制解调器与无线电接口层（RIL）配置进行调整"
  - "Systemless 无侵入部署：注入电信框架配置而不修改物理系统分区"
faq: []
---

## 概述

尽管现代智能手机在国际漫游与多卡配置上越来越普及 eSIM 技术，部分 Nothing 机型在出厂时并未提供原生 eSIM 支持，或未开放通过系统层面直接管理数字蜂窝配置文件所需的本地配置文件助手（LPA）。

由 reindex-ot 开发的 **nothing-euicc**（Nothing EUICC Force Enabler）是一款专用 Magisk 模块，用于在搭配可插拔实体 eSIM 智能卡（如 eSTK.me 与 5ber）时，为 Nothing OS 设备强制启用 eSIM 服务与系统级 LPA 功能。

## 硬件兼容性与局限

### 已测试与支持的机型
- **Nothing Phone (1)**：完整支持系统级 LPA 以及配置文件下载与切号。
- **Nothing Phone (2)**：完整支持系统级 LPA 以及配置文件下载与切号。
- **Nothing Phone (2a) 与 CMF Phone 1**：硬件采用联发科（MediaTek）处理器；**系统级 LPA 在联发科芯片平台上无法工作**。
- **Nothing Phone (3)**：系统级 LPA 可正常运行，但卡槽 2 的内置嵌入式 eSIM 会被基带优先识别。

### 支持的实体 eSIM 卡
- **eSTK.me**：同时支持直接下载配置文件与切换配置文件。请在 SIM 卡工具包（STK）菜单中确保开启 ATR 模式下的 “Announce as eUICC” 或 “eUICC Mark” 选项，以允许系统 LPA 执行下载操作。
- **5ber eSIM**：支持已写入 eSIM 配置文件的切换管理。

## 安装与配置步骤

1. 将实体可编程 eSIM 卡插入 Nothing 设备的 SIM 卡槽中。
2. 从 GitHub 发布页下载最新的 `nothing-euicc.zip`。
3. 在 **Magisk** 中刷入该模块。
4. 重启手机。
5. 打开 **设置 > 网络和互联网 > SIM 卡**，此时即可看到原生的 Android eSIM 设置与二维码扫描界面。
