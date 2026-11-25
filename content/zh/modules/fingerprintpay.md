---
id: "fingerprintpay"
title: "FingerprintPay：为第三方及类原生 ROM 解锁生物识别指纹支付"
sidebarTitle: "FingerprintPay"
description: "在已 Root 的类原生及 AOSP 第三方 ROM 上，将 Android 标准 BiometricPrompt API 桥接至支付宝、微信支付、QQ 等专有支付安全服务。"
category: "customization-ui"
tier: 1
searchQueries:
  - "FingerprintPay Magisk 模块"
  - "类原生 ROM 支付宝指纹支付"
  - "安卓 Root 微信指纹支付恢复"
  - "eritpchy FingerprintPay 配置教程"
  - "安卓 IFAA Soter 服务桥接模块"
prerequisites:
  - "Android 8.0 至 Android 15"
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "已启用 LSPosed 或 Vector 框架"
conflicts:
  - "已内置原厂 IFAA/Soter 组件的中国大陆 OEM 官方系统（如 MIUI/ColorOS）"
configPaths:
  - "/data/adb/modules/fingerprintpay/"
  - "/data/user/0/org.sugar.fingerprintpay/"
features:
  - "模拟 OEM 厂商专有的 IFAA（互联网金融身份认证联盟）与腾讯 Soter 安全守护服务"
  - "将支付宝与微信支付的私有生物识别握手请求转换为标准 Android KeyStore 与 BiometricPrompt 调用"
  - "在 AOSP、LineageOS 与 Pixel Experience 等系统上恢复金融支付应用的指纹及人脸验证功能"
  - "内置配套辅助应用，用于密钥生成诊断与服务可用性校验"
faq:
  - question: "为什么支付宝等支付应用在第三方 ROM 上会拒绝开启指纹支付？"
    answer: "部分地区的支付服务商强制校验嵌入在厂商原厂 vendor 分区中的硬件签名安全令牌（IFAA / 腾讯 Soter）。刷入 AOSP 或 LineageOS 后，这些专有厂商服务会缺失。FingerprintPay 通过模拟 IFAA 接口，将认证请求路由至原生 Android 生物识别 API。"
  - question: "使用该模块安全吗？"
    answer: "FingerprintPay 完全依托 Android 自身安全的 BiometricPrompt 与 KeyStore 硬件加密体系运行。它不会绕过指纹验证流程，只是在厂商专有协议与标准 Android 系统安全框架之间充当桥接翻译层。"
---

## 概述

由 **eritpchy** 开发的 **FingerprintPay** 是第三方类原生 ROM（如 LineageOS、PixelOS、crDroid 或 Paranoid Android）用户不可或缺的功能模块，专为恢复**支付宝**、**微信支付**、**QQ 钱包**等亚洲主流移动支付平台的指纹支付而设计。

小米、一加、OPPO、vivo 等厂商的官方固件通常预置了用于签名生物识别支付交易的专有硬件认证守护服务（IFAA 与腾讯 Soter）。一旦设备刷入基于 AOSP 的第三方 ROM，这些厂商闭源服务便不复存在，导致支付应用永久禁用指纹识别选项。FingerprintPay 提供了一套软件协议转换桥梁，使这些支付网关能够直接调用标准 Android 生物识别能力。

---

## 技术架构与工作原理

### IFAA 与 Soter 协议模拟

1. **服务模拟**：模块向 Android 系统服务进程注入模拟服务，向应用声明 `org.ifaa.android.manager.IFAAManager` 与 `com.tencent.soter.core.model.SoterCore` 的可用状态。
2. **KeyStore 签名映射**：当支付宝或微信请求签名的支付认证令牌时，FingerprintPay 会调用标准 Android `KeyStore` 生成受 `KeyGenParameterSpec.Builder(..., PURPOSE_SIGN).setUserAuthenticationRequired(true)` 保护的非对称密钥对。
3. **BiometricPrompt 握手**：系统向用户弹出原生指纹验证弹窗。硬件指纹校验通过后，加密密钥即对支付载荷进行签名，并将符合预期的认证令牌返回给支付应用。

---

## 安装与配置步骤

1. 确保设备已安装并正常运行 **Vector** 或 **LSPosed** 框架。
2. 安装 `FingerprintPay.apk` 应用。
3. 打开 **Vector 管理器** → 启用 **FingerprintPay** → 在作用域（Scope）中勾选**系统框架（System Framework）**、**支付宝**与**微信**。
4. 重启手机。
5. 打开 **FingerprintPay** 应用，确认 IFAA 与 Soter 两项服务检测均显示通过。
6. 打开支付应用，进入**设置** → **生物识别 / 指纹支付**，开启指纹验证开关即可。
