---
id: "hydro-br-leur"
title: "Hydro-Brûleur：面向联发科与骁龙小米设备的定制内核及显示增强模块"
sidebarTitle: "Hydro-Brûleur"
description: "专为搭载第三方内核（Yuni、AngelBeats、Pandora）的小米及红米设备打造的硬件级性能优化模块，集成联发科 fpsgo 与 Iris 独显处理器调校。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "Hydro-Brûleur Magisk 模块下载"
  - "红米 K60 至尊版 corot 内核优化"
  - "联发科 fpsgo 帧率调度模块"
  - "iris_configs.xml 独显配置模块"
  - "Yuni AngelBeats Pandora 内核优化"
prerequisites:
  - "受支持的小米、红米（如 Corot / K60 至尊版）或部分一加、真我骁龙机型"
  - "第三方内核环境（Yuni Kernel、AngelBeats Kernel、Pandora Kernel）或兼容的官方原厂内核"
  - "Magisk 26300+ 或 KernelSU"
conflicts:
  - "上述联发科天玑与骁龙硬件分支以外的未适配 OEM 机型"
  - "会覆盖联发科 fpsgo 或 Iris 独显芯片配置的第三方帧率增强模块"
configPaths:
  - "/data/adb/modules/scene_systemless/settings.txt"
  - "/data/adb/modules/scene_systemless/"
features:
  - "智能内核识别：刷入时自动检测 uname 字符串，针对 Yuni、AngelBeats 或 Pandora 内核定制系统属性与功耗表"
  - "联发科 fpsgo 与 perfmgr 调校：重映射 DDR 频率表并针对 48、60、90、120 FPS 目标优化帧时间稳定性"
  - "Pixelworks Iris 独显芯片校准：注入调优后的 `iris_configs.xml` 与辅助脚本，优化 MEMC 运动补偿及显示引擎管线"
  - "动态云端模式路由：依据检测到的内核构建时间戳与版本标识自动切换增强配置 JSON 文件"
faq: []
---

## 概述

Hydro-Brûleur 由 AestasBritannia 联合社区内核贡献者（Shadow3、Mly、M7recRAB、Ski 与 Hamjin）共同开发，是一款面向小米、红米及部分欧加系（BBK）设备的硬件级性能优化模块。与跨机型套用通用 Linux VM sysctl 参数的做法不同，Hydro-Brûleur 专注于特定机型（例如 Redmi K60 至尊版，代号 `"corot"`）及配套小米平台。

该模块会在刷入阶段检测当前运行的 Linux 内核构建字符串，自动重构负载策略以适配第三方内核——具体支持 **Yuni Kernel**、**AngelBeats Kernel** 与 **Pandora Kernel**，并针对联发科 `mtk_fpsgo` 帧调度及 Pixelworks Iris 独显协处理器等底层子系统进行精细调校。

## 前置要求与兼容性

Hydro-Brûleur 严格限定在兼容的硬件与内核环境中运行：

1. **硬件平台**：搭载受支持 SoC 的小米 / 红米机型（尤其是 Redmi K60 至尊版所用的联发科天玑 9200+ 等天玑平台，以及部分一加、真我适配机型）。
2. **内核环境**：
   - 支持联发科 `fpsgo` 与 `perfmgr` 接口的官方原厂内核。
   - 或第三方内核：**Yuni Kernel**、**AngelBeats Kernel** 或 **Pandora Kernel**（涵盖 Open 与 Beta 分支）。
3. **Root 框架**：Magisk v26.3（26300）及以上版本，或 KernelSU。

### 已知不兼容说明

明确不支持将 Hydro-Brûleur 刷入其他无关 OEM 品牌机型（如三星、Google Pixel、摩托罗拉）或通用 AOSP GSI 系统。其安装脚本会直接针对 Vendor 功耗配置文件（`powercontable.xml`）及 Vendor 显示配置执行修改，在非目标硬件平台上无法正常生效。

## 内部架构与工作原理

在部署阶段（`customize.sh`），模块会执行深度的硬件环境探测：

- **内核探测**：读取 `uname -r` 识别第三方内核特征标识（`Yuni`、`AngelBeats` 或 `Pandora`）。若检测到第三方内核，会自动修补 `/data/adb/modules/<kernel_id>/service.sh` 中的活动服务脚本，取消冲突的触控空闲计时器并对齐频率上下限节点。
- **Iris 独显芯片管理**：部署 `iris_helper.sh` 与定制的 `iris_configs.xml` 配置树，调用硬件显示协处理器实现插帧与刷新率稳定控制。
- **联发科帧调度优化**：将传统 `perfmgr_mtk` sysfs 引用转换至现代 `mtk_fpsgo` 目标节点，针对 48、60、90 与 120 FPS 渲染管线动态调整 DDR 总线频率重映射表。

## 配置文件与路径

Hydro-Brûleur 将配置文件及运行状态保存在以下目录：
```bash
/data/adb/modules/scene_systemless/
```
模块运行标志位与历史用户配置则从以下文件解析：
```bash
/data/adb/modules/scene_systemless/settings.txt
```

## 故障排查与验证

- **内核特征不匹配**：若在安装 Hydro-Brûleur 后更换或更新了第三方内核，请在 Root 管理器中重新刷入本模块。安装脚本生成的配置路径与刷入时的内核字符串严格绑定。
- **显示不同步或画面卡顿**：请确保未同时启用强制锁定刷新率的应用或第三方锁帧工具，以免干扰 Iris 独显辅助脚本与联发科 DDR 频率重映射逻辑。
