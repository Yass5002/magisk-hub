---
id: "yurikey"
title: "YuriKey Manager：自动化 TrickyStore Keybox 部署工具"
sidebarTitle: "YuriKey"
description: "无系统分区修改（Systemless）自动化辅助模块，为 TrickyStore 提供自动获取 Keybox、同步目标列表以及配置安全补丁级别等功能。"
category: "root-management"
tier: 1
searchQueries:
  - "yurikey magisk 模块"
  - "yurikey manager 下载配置"
  - "trickystore keybox 自动更新模块"
  - "yurikey 通过 strong integrity 认证"
  - "yurikey action 按钮一键配置"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "已在 `/data/adb/modules/tricky_store` 安装 TrickyStore 模块"
  - "已安装 Play Integrity Fix 或 Play Integrity Fork 模块"
  - "若 Keybox 脚本解码失败，需安装 BusyBox（`busybox-ndk`）"
conflicts:
  - "明确说明：与其他模块无已知冲突；必须依赖 TrickyStore 才可运行"
configPaths:
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/modules/yurikey/"
  - "/data/adb/Yurikey/"
features:
  - "一键 Action 按钮部署：运行自动化脚本获取、解码并备份 `keybox.xml`"
  - "动态目标同步：更新 `target.txt`，涵盖 Google Play 服务、Key Attestation 与各类银行风控检测包名"
  - "TEE 状态检测：解析 `/data/adb/tricky_store/tee_status`，当硬件 TEE 异常时自动调整目标策略"
  - "Keybox 自动备份：应用远程更新前自动为现有的 `keybox.xml` 创建安全副本"
  - "进程清理自动化：自动终止缓存的 Google 进程以立即刷新认证状态"
faq:
  - question: "为什么安装时提示“ERROR: Tricky Store module not found!”？"
    answer: "YuriKey 是管理伴侣模块，而非独立的 Keystore 挂钩工具。它完全依赖 TrickyStore 来执行底层的 Keystore HAL 拦截，因此在运行 YuriKey 前必须先安装 TrickyStore。"
  - question: "如果 Keybox 更新失败并报错该怎么办？"
    answer: "若 Keybox 解码失败，请在你的 Root 管理器中安装 `busybox-ndk` 模块。YuriKey 需要完整的 `ash` Shell 环境（支持 `base64` 及标准 UNIX 工具集）来处理加密的 Keybox 数据包。"
---

## 概述

由 **Yurii0307** 开发的 **YuriKey Manager** 是一款专为简化 **TrickyStore** 配置与日常维护而设计的自动化工具模块。

要通过 Google 的 `MEETS_STRONG_INTEGRITY` 认证，通常需要配置有效的未吊销硬件 `keybox.xml`、在 `target.txt` 中声明目标应用，并同步安全补丁级别。YuriKey 将这些繁琐的多步骤终端工作流封装为自动化 Shell 脚本，直接通过 Root 管理器的 **Action** 按钮或 WebUI 即可一键触发。

---

## 技术架构与工作原理

### TrickyStore 自动化编排脚本

通过 Action 按钮或 WebUI 触发后，YuriKey 会按顺序执行一系列编排脚本：

1. **`kill_google_process.sh`**：优雅终止后台运行的 Google Play 服务（`com.google.android.gms`）、Google 服务框架（`com.google.android.gsf`）以及 Play 商店守护进程，清除已缓存的认证令牌。
2. **`target_txt.sh`**：扫描 `/data/adb/tricky_store/tee_status` 以评估设备 TEE 健康状态，并向 `/data/adb/tricky_store/target.txt` 写入经过强化的目标列表，包含 Google 服务、密钥证明验证工具及常见银行检测组件。
3. **`yuri_keybox.sh`**：将当前 Keybox 文件备份至 `/data/adb/tricky_store/keybox.xml.bak`，从项目镜像下载最新加密的 Keybox 载荷，调用本地加密工具解码后部署到 `/data/adb/tricky_store/keybox.xml`。
4. **`pif.sh`**：将伪装的设备指纹与 Play Integrity Fix / Fork 配置对齐，确保安全补丁日期与整体认证环境一致。

---

## 安装与配置

### 1. 安装前置依赖
安装 YuriKey 前，请确保已在 Root 管理器中刷入并启用以下核心组件：
- **TrickyStore**：用于实现 Keystore 2.0 / Keymaster HAL 拦截。
- **Play Integrity Fix**（或 **Play Integrity Fork**）：与硬件密钥证明配合以满足 `MEETS_DEVICE_INTEGRITY` 认证。

### 2. 刷入 YuriKey Manager
1. 从项目官方发布页下载最新的 `Yurikey-v*.zip`。
2. 在你的 Root 管理器（Magisk、KernelSU 或 APatch）中刷入模块。
3. 点击 Root 管理器中的 **Action** 按钮（或在 Root Shell 中执行 `/data/adb/modules/yurikey/action.sh`）以运行自动化配置流水线。
4. 重启设备。

---

## 配置与日常使用

YuriKey 管理的所有配置文件均直接写入 TrickyStore 的配置目录中：
- **当前生效 Keybox**：查看 `/data/adb/tricky_store/keybox.xml` 以检查生成的证书链。
- **目标应用声明**：在 `/data/adb/tricky_store/target.txt` 中查看或自定义需要拦截的包名。
- **WebUI 界面**：在运行 KernelSU 或 APatch 的设备上，YuriKey 提供了内置 WebUI，方便直接查看设备认证状态、更新 Keybox 配置文件及切换特定应用规则。

---

## 故障排查与常见问题

- **Keybox 更新失败**：如果 Action 脚本提示 `ERROR: Keybox updated failed!`，请安装 **busybox-ndk**。标准 AOSP 精简版 Shell 工具链有时缺少解码 `base64` 载荷与文本流过滤所需的参数支持。
- **认证状态失效回退**：若 Google 吊销了当前部署的 Keybox，只需再次运行 Action 按钮，即可从 YuriKey 维护者源拉取最新的有效 Keybox 载荷。
