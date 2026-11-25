---
id: "key-attestation"
title: "Key Attestation：硬件 Keystore 与 KeyMint 密钥证明诊断工具"
sidebarTitle: "Key Attestation"
description: "由知名系统安全研究者 vvb2060 开发的权威离线安全诊断工具，用于生成、解析并验证 Android 硬件 Keystore、StrongBox 及 KeyMint 证书链。"
category: "security-certificates"
softwareType: "standalone-app"
tier: 1
searchQueries:
  - "Key Attestation 下载 vvb2060"
  - "Android 硬件密钥证明检测工具"
  - "KeyMint StrongBox 证书链验证"
  - "检测 Bootloader verifiedBootState 状态"
  - "Tricky Store 搭配 Key Attestation 测试"
prerequisites:
  - "Android 7.0（Nougat / API 24）及以上系统（支持 Keymaster 2.0+）"
  - "完全支持免 Root 运行（无需 Root 权限）"
conflicts:
  - "无（仅作为纯离线分析工具运行）"
configPaths:
  - "vvb2060.org.web.application.keyattestation"
features:
  - "零网络权限设计：完全不包含 `INTERNET` 权限，确保隐私安全与无篡改的纯离线检测分析"
  - "KeyMint 与 StrongBox 验证：检测可信执行环境（TEE）及独立安全芯片（SE）的安全等级"
  - "ASN.1 密钥证明解析器：解码 Verified Boot 状态、系统补丁级别、解锁状态以及信任根公钥哈希"
  - "支持证书链导出：可导出原始 PEM/DER 证书链文件，便于在独立工作站上进行外部交叉校验"
faq:
  - question: "为什么 Key Attestation 刻意不申请任何网络权限？"
    answer: "安全校验必须具备确定性与最小化信任边界。通过完全移除 `android.permission.INTERNET` 权限，应用从根本上杜绝了私钥及证明载荷被外传的可能。此外，应用将证书吊销列表直接内嵌在 APK 中，从而避免了网络请求过程中遭遇中间人（MITM）攻击的风险。"
  - question: "检测报告中的「Software」、「TrustedEnvironment」和「StrongBox」分别代表什么？"
    answer: "`Software` 表示密钥存储在常规 Android 系统内存中，容易因 Root 权限被攻破而泄露；`TrustedEnvironment`（TEE）表示私钥物理隔离在安全处理器飞地（如 ARM TrustZone）中；`StrongBox` 则代表独立的专用硬件安全芯片（例如 Google Titan M2、Apple Secure Enclave 或 Samsung Knox Vault），具备防篡改封装与独立供电线路。"
  - question: "如何将 Key Attestation 与 Tricky Store 或 TEESimulator 配合使用？"
    answer: "玩机用户与开发者通常将 Key Attestation 作为最终的基准验证工具。当你在 Tricky Store 中将 Key Attestation 加入目标列表后，打开该应用即可发起一次密钥证明请求，并直观查看伪装后的硬件证书是否成功下发、以及是否呈现出模拟的「Verified」Bootloader 锁定状态。"
---

## 概述

**Key Attestation** 由著名 Android 系统研究者 vvb2060 开发，是业内公认用于检测 Android 硬件密钥库（Keystore）子系统完整性与密码学能力的权威开源工具。

自 Android 7.0（Nougat）起，Google 引入了**密钥与身份证明（Key and ID Attestation）**机制，使金融支付、移动银行和 MDM 设备管理等安全敏感服务能够通过密码学手段确认：加密密钥确实在硬件安全飞地内部物理生成且不可导出，同时设备的 Bootloader 处于安全锁定状态。

Key Attestation 会在设备硬件密钥库（`KeyStore2` / `KeyMint`）中生成一对非对称密钥，展示完整的 X.509 证书链，并将每一项授权扩展字段精细解析至具体的 ASN.1 位标志。

---

## 技术原理与 ASN.1 证明记录

当 Key Attestation 请求 KeyStore 生成受证明保护的密钥对时，硬件安全模块会使用出厂预置的私钥签发叶证书（Leaf Certificate）。该叶证书包含一条自定义的 X.509 扩展字段（OID `1.3.6.1.4.1.11129.2.1.17`）：

- **Key Attestation 应用**：携带随机生成的证明质询值（Attestation Challenge）发起密钥生成请求。
- **KeyMint / 硬件 TEE 安全飞地**：
  - 在隔离硬件（可信执行环境 TEE 或 StrongBox）内部生成 EC/RSA 密钥对。
  - 使用 Google 或 OEM 出厂批量证明私钥对 X.509 证明证书链进行签名。
  - 将不可篡改的硬件状态参数嵌入 ASN.1 证书扩展字段中。
- **解析输出的安全证明信息**：
  - **安全等级（Security Level）**：`TrustedEnvironment` 或专用 `StrongBox` 硬件。
  - **已验证启动状态（Verified Boot State）**：`Verified`、`SelfSigned` 或 `Failed`。
  - **系统版本与安全补丁级别（OS Version & Security Patch Level）**：目标系统编译日期与安全补丁日期。
  - **已验证启动密钥（Verified Boot Key）**：用于校验系统启动镜像的根签名公钥 SHA-256 摘要。

### 核心授权标签说明

Key Attestation 会精准解析并展示硬件所出具的各项安全属性：
- **`attestationSecurityLevel`**：确认本次证明是由纯软件模拟执行，还是由真实硬件环境完成。
- **`verifiedBootState`**：
  - `Verified` (0)：设备以官方 OEM 锁定 Bootloader 启动，且完整通过已验证启动链校验。
  - `SelfSigned` (1)：Bootloader 已锁定，但使用的是用户自定义的信任根密钥。
  - `Unverified` (2)：Bootloader 处于完全解锁状态（会导致 Play Integrity 认证失败）。
  - `Failed` (3)：启动完整性校验失败。
- **`verifiedBootKey`**：烧录在硬件熔丝（eFuse）中、用于校验当前启动镜像的公钥 SHA-256 指纹。

---

## 独立离线交叉验证

由于处于激活状态的 Root 环境（配合 Zygote 注入 Hook）理论上存在篡改本地界面渲染结果的可能，Key Attestation 支持完整的离线导出校验：
1. 点击 Key Attestation 界面中的 **分享 / 保存（Share / Save）** 图标，将证书链保存为文件。
2. 将导出的证书文件传输至未 Root 的安全工作站或另一台未解锁设备。
3. 在第二台设备上打开 Key Attestation 并选择 **加载证书链（Load Certificate Chain）**，或直接使用 OpenSSL 工具进行校验：
   ```bash
   openssl x509 -in cert.pem -text -noout
   ```
4. 这种方式可确保你查看的硬件密钥证明结果完全真实可靠，不受任何运行时界面 Hook 干扰。
