---
id: "trickystore"
title: "TrickyStore：硬件 Keystore 密钥证明与 Keybox 伪装模块"
sidebarTitle: "TrickyStore"
description: "深入 Android Keystore HAL 层的拦截模块，允许已解锁 Bootloader 的设备通过注入有效 Keybox 满足 MEETS_STRONG_INTEGRITY 认证。"
category: "root-management"
tier: 1
searchQueries:
  - "TrickyStore 模块下载"
  - "如何通过 MEETS_STRONG_INTEGRITY"
  - "TrickyStore keybox.xml 配置教程"
  - "Android 14 密钥认证绕过"
  - "TrickyStore target.txt 怎么写"
prerequisites:
  - "支持 Zygisk 的 Magisk、KernelSU 或 APatch"
  - "有效且未被谷歌吊销的 AOSP 或 OEM `keybox.xml` 证书链文件"
conflicts:
  - "其他同样劫持 Keymaster / Keystore HAL 的同类模块"
configPaths:
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/tricky_store/security_patch.txt"
  - "/data/adb/modules/trickystore/"
features:
  - "直接挂钩 Android Keystore 2.0 与 Keymaster HAL 守护进程"
  - "向硬件密钥证明请求注入自定义 EC/RSA 私钥与证书链"
  - "支持通过目标清单精确控制仅对特定应用返回伪装证书链"
  - "可在已解锁 Bootloader 的 Root 设备上实现 MEETS_STRONG_INTEGRITY"
faq:
  - question: "从哪里获取有效的 keybox.xml？"
    answer: "Keybox 是包含由 Google 签发的密钥证明证书链及对应 ECDSA/RSA 私钥的 OEM 加密凭据，无法在本地凭空生成，通常来源于工厂测试固件、OEM 工程机提取或社区流出的有效备份。"
  - question: "没有 keybox.xml 时 TrickyStore 还能用吗？"
    answer: "如果没有有效的 `keybox.xml`，TrickyStore 将无法伪造 Google 认证服务器要求的高强度签名（即无法通过 `MEETS_STRONG_INTEGRITY`）。若你仅拥有普通设备指纹，建议配合 PlayIntegrityFork 获取 `MEETS_DEVICE_INTEGRITY`。"
---

## 概述

由 **5ec1cff** 开发的 **TrickyStore** 是一款工作在 Android Keystore HAL（硬件抽象层）边界的底层模块。

自 Android 8.0 起（并在新版本中日益严格），Google Play Integrity 引入了 **基于硬件的密钥证明（Hardware-Backed Key Attestation）**。当银行或高安全级别应用发起强校验时，Android Keystore 会委托设备物理可信执行环境（TEE）或 StrongBox 芯片生成非对称密钥对，并签发包含启动信任根状态（`bootloader: UNLOCKED`）的认证证书链。

TrickyStore 在 Keystore 守护进程内部拦截此类证明请求，使用未吊销的合法 OEM Keybox 签名构造认证证书链替换真实硬件返回值，从而使服务器认定设备处于 Bootloader 已上锁且经过验证启动的状态。

---

## 技术架构与工作原理

### Keystore 2.0 / Keymaster HAL 拦截机制

1. **系统服务挂钩**：在 Android 12+ 上，密钥管理由 `android.system.keystore2` Binder 服务负责。TrickyStore 向 `keystore2` 守护进程注入原生 Hook。
2. **认证请求拦截**：当目标进程（如 Google Play 服务或企业安全客户端）调用带证明挑战值的 `generateKey` 时，TrickyStore 会在请求抵达硬件 Keystore HAL 前完成拦截。
3. **Keybox 证书链替换**：模块读取 `/data/adb/tricky_store/keybox.xml` 中的私钥与证书链，在软件层签发合法的 X.509 证书链。
4. **信任根状态伪造**：生成的证书包含 ASN.1 证明扩展字段，其中 `verifiedBootState` 被标记为 `Verified` 且 `deviceLocked` 为 `true`。
5. **按包名精准过滤**：依托 `/data/adb/tricky_store/target.txt`，TrickyStore 仅对清单内的应用返回伪装证明，确保生物识别解锁与 DRM 密钥（Widevine L1）继续正常调用物理硬件 Keystore。

---

## 安装与配置指南

### 第一步：刷入 TrickyStore
1. 在你的 Root 管理器（Magisk、KernelSU 或 APatch）中刷入 `TrickyStore-vX.zip`。
2. 重启设备。

### 第二步：放置 `keybox.xml`
将有效的 Keybox 文件保存至 `/data/adb/tricky_store/keybox.xml`：
```xml
<?xml version="1.0"?>
<AndroidAttestation>
    <NumberOfKeyboxes>1</NumberOfKeyboxes>
    <Keybox DeviceID="...">
        <Key algorithm="ecdsa">
            <PrivateKey format="pem">
-----BEGIN EC PRIVATE KEY-----
...
-----END EC PRIVATE KEY-----
            </PrivateKey>
            <Certificate format="pem">
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
            </Certificate>
        </Key>
    </Keybox>
</AndroidAttestation>
```

### 第三步：配置 `target.txt`
在 `/data/adb/tricky_store/target.txt` 中列出需要伪装密钥证明的应用包名：
```text
com.google.android.gms
com.google.android.gms.unstable
com.android.vending
```
*（如有其他需要直接校验证书链的银行或企业应用，请追加其包名。）*

### 第四步：自定义安全补丁日期（可选，v1.2.1+）
如需覆盖认证中上报的系统、Vendor 或 Boot 安全补丁日期，可创建 `/data/adb/tricky_store/security_patch.txt`：
```text
# 格式：os/vendor/boot 安全补丁日期（如 YYYYMM 或 YYYYMMDD）
# 填入 '!' 表示跳过修改对应字段
```
修改后实时生效，无需重启设备。

---

## 常见问题与排查

- **Keybox 被吊销（Revoked）**：当 Google 发现某份泄漏的 Keybox 后，会将其证书序列号加入 Android CRL 吊销列表。此时认证会立即返回 `REVOKED` 或跌落至 `NO_INTEGRITY`，需要更换新的未吊销 `keybox.xml`。
- **指纹解锁或 FIDO 功能异常**：如果遇到应用内生物识别失效，请检查 `/data/adb/tricky_store/target.txt`，确保**没有**误将系统生物识别框架包名（如 `com.android.settings`、`android`）写入其中。
