---
id: "tricky-addon-update-target-list"
title: "Tricky Addon - Update Target List：Tricky Store 与 TEESimulator 图形化配置管理"
sidebarTitle: "Tricky Addon"
description: "由 KOWX712 开发的综合性 WebUI 配置伴侣模块，通过一键开关直观管理 Tricky Store、TEESimulator 与 OhMyKeymint 的 target.txt 应用伪装规则。"
category: "security-certificates"
softwareType: "flashable-module"
tier: 1
searchQueries:
  - "Tricky Addon Update Target List 下载"
  - "Tricky Store target.txt WebUI 配置"
  - "Tricky Store 感叹号叶证书模式"
  - "Tricky Addon KernelSU 模块"
  - "TEESimulator WebUI 图形化配置"
prerequisites:
  - "通过 KernelSU、APatch 或 Magisk 获取 Root 权限"
  - "已安装并启用至少一个密钥证明伪装模块：Tricky Store、TEESimulator 或 OhMyKeymint"
  - "KernelSU / APatch 原生内置 WebUI 支持，或 Magisk 搭配 KSUWebUIStandalone"
conflicts:
  - "无直接冲突（仅作为界面配置辅助插件运行）"
configPaths:
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/modules/TA_utl/"
features:
  - "原生 WebUI 深度集成：无缝嵌入 KernelSU 与 APatch 模块管理界面"
  - "一键勾选目标应用：支持搜索、筛选并在所有已安装用户应用与系统应用间快速切换伪装状态"
  - "高级目标语法支持：轻松切换包名末尾的感叹号（!），自由切换仅叶证书模式与完整证书链生成模式"
  - "自动备份与同步：防止 target.txt 目标列表意外损坏，并支持本地或云端配置导出"
faq:
  - question: "在列表中填写 `com.example.app` 与 `com.example.app!` 有什么区别？"
    answer: "在 Tricky Store 和 TEESimulator 中，包名末尾附加感叹号（`!`) 会指示 Keystore Hook 仅伪装叶证书（Leaf Certificate），而非合成整条硬件证明证书链。对于部分会交叉校验中间 CA 指纹与已知根证书库的银行类及高安全校验应用而言，这一选项至关重要。"
  - question: "该模块在 Magisk 环境下可以使用吗？"
    answer: "可以。在 Magisk 环境中，Tricky Addon 会自动配置 KSUWebUIStandalone 或 WebUI X，并在 Magisk 应用的模块卡片上提供操作（Action）触发按钮，点击即可打开配置界面。"
  - question: "卸载此模块会清除我已配置好的目标应用列表吗？"
    answer: "不会。实际的目标规则文件独立保存在 `/data/adb/tricky_store/target.txt` 中。更新或卸载 Tricky Addon 模块不会影响你现有的目标列表以及 Keybox 证书配置。"
---

## 概述

由 KOWX712 开发的 **Tricky Addon - Update Target List**，是目前针对 **Tricky Store**、**TEESimulator** 及 **OhMyKeymint** 等现代 Android 密钥库伪装框架不可或缺的配套工具模块。

如今，越来越多的反作弊系统、Play Integrity 以及手机银行应用都会通过 Android 硬件密钥库（`KeyStore2` / `KeyMint`）的加密证明机制，核验设备 Bootloader 是否锁定及系统是否处于未篡改状态。Tricky Store 等框架通过在 `keystore2` 层拦截这些证明请求，注入合法的硬件级证书。

然而，Tricky Store 依赖纯文本文件 `/data/adb/tricky_store/target.txt` 来决定对哪些软件包下发伪装证明。在手机触屏上使用 Root 文本编辑器手动增删包名既繁琐又容易出错。Tricky Addon 提供了响应迅速的原生 WebUI 界面，让你能够实时搜索应用、切换伪装规则并检查密钥库路由状态。

---

## 技术机制与 Keystore 拦截流程

- **目标应用**：发起密钥生成或硬件证明请求（例如 Google Play 服务、Google Wallet 或各类银行应用）。
- **Android Keystore 2.0（`keystore2`）**：由 Tricky Store 在 HAL Binder 通信层进行拦截。
- **Tricky Store 目标匹配判定**：
  - **命中匹配**（包名位于 `target.txt` 中）：注入有效的硬件证明证书链与 Keybox 凭据。
  - **未命中匹配**（包名不在 `target.txt` 中）：将请求直接放行至设备原生的 TEE / KeyMint 硬件处理。

Tricky Addon 直接读写 `/data/adb/tricky_store/target.txt` 文件：

```
com.google.android.gms
com.google.android.apps.walletnfcrel
com.target.bank.app!
```

- 当你在 WebUI 中勾选某个应用时，Tricky Addon 会安全地将其包名写入 `target.txt`。
- 当你切换开启 **叶证书模式（Leaf Mode）** 时，Tricky Addon 会在包名末尾自动追加 `!` 标记。
- 模块采用原子文件写入机制，确保 `keystore2` 在应用冷启动读取配置时绝不会读到写入了一半的残缺列表。

---

## WebUI 兼容性矩阵

| Root 方案 | 界面呈现方式 | 所需操作 |
| :--- | :--- | :--- |
| **KernelSU** | KernelSU 应用内原生 WebUI 标签页 | 零配置开箱即用；打开 KernelSU -> 模块 -> Tricky Addon -> WebUI |
| **APatch** | APatch 应用内原生 WebUI 标签页 | 零配置开箱即用；点击模块卡片上的 WebUI 按钮 |
| **Magisk** | KSUWebUIStandalone / 便携版 WebUI X | 自动部署便携版独立宿主，或通过模块卡片的 Action 按钮启动 |

---

## 目标配置最佳实践

1. **避免全量通配覆盖**：切勿将设备上所有已安装应用一股脑加入 `target.txt`。无差别伪装可能导致普通社交应用或云服务出现意外的证书校验不匹配问题。
2. **常见标准目标**：
   - `com.google.android.gms`（Google Play 服务，实现 `MEETS_DEVICE_INTEGRITY` / `MEETS_STRONG_INTEGRITY` 认证所必需）
   - `com.android.vending`（Google Play 商店）
   - 明确要求硬件密钥证明的金融、银行或企业办公类应用
3. **按需启用叶证书模式（`!`）**：若某款银行应用在加入 `target.txt` 后出现闪退或提示证书颁发机构无效，请在 Tricky Addon 中为其开启末尾 `!` 标记，将伪装范围严格限定在叶证书层级。
