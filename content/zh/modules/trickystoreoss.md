---
id: "trickystoreoss"
title: "TrickyStoreOSS：开源 Keystore 密钥证明与 Keybox 伪装模块"
sidebarTitle: "TrickyStoreOSS"
description: "基于 GPLv3 协议完全开源重写的 TrickyStore 实现，提供 Keystore HAL 拦截与自定义 Keybox 注入能力。"
category: "root-management"
tier: 1
searchQueries:
  - "TrickyStoreOSS Magisk 模块"
  - "开源版 TrickyStore 下载"
  - "beakthoven TrickyStoreOSS"
  - "Android 开源 Keybox 密钥证明"
  - "TrickyStoreOSS target.txt 配置"
prerequisites:
  - "Android 10 及以上系统"
  - "已安装 Magisk、KernelSU 或 APatch（并具备 Zygisk 支持）"
  - "有效且未被吊销的 OEM `keybox.xml` 证书文件（基础功能可选，强完整性 Strong Integrity 必需）"
conflicts:
  - "明确说明：暂无已知与其他模块的冲突；刷入前必须先卸载闭源版 TrickyStore"
configPaths:
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/tricky_store/security_patch.txt"
  - "/data/adb/modules/tricky_store/"
features:
  - "100% 自由开源（FOSS）：彻底剔除闭源二进制文件与专有遥测组件"
  - "Keystore 2.0 / Keymaster HAL 挂钩：直接在系统守护进程层拦截密钥证明校验"
  - "实时热重载：修改 `target.txt` 与 `keybox.xml` 后即时生效，无需重启设备"
  - "精细化应用分流：仅对指定包名伪造证书链，同时完整保留系统生物识别解锁功能"
  - "自定义安全补丁日期：支持通过 `security_patch.txt` 覆盖上报的安全补丁级别"
faq:
  - question: "为什么会出现 TrickyStoreOSS 这个项目？"
    answer: "TrickyStoreOSS 由 beakthoven 基于 GPLv3 协议以完全透明、净室重写的方式打造，旨在替代闭源的原版 TrickyStore 模块，在保持功能完全对等的同时消除闭源二进制顾虑。"
  - question: "可以同时运行原版 TrickyStore 和 TrickyStoreOSS 吗？"
    answer: "不可以。两个模块挂钩的是同一批 Keystore HAL 服务入口，且共用 `/data/adb/tricky_store/` 目录结构。安装 TrickyStoreOSS 前必须先卸载闭源版 TrickyStore。"
---

## 概述

由 **beakthoven** 开发的 **TrickyStoreOSS** 是面向已 Root Android 设备的开源 Keystore HAL 拦截实现，采用 GPLv3 协议发布。

当银行应用或 Google Play Integrity 校验硬件级安全状态时，Android 会调用 Keystore HAL 生成用于验证 Boot 状态的密钥证明证书链。TrickyStoreOSS 在系统守护进程内部拦截此类请求，利用用户提供的合法 `keybox.xml` 伪造完整的证明证书链，从而通过 `MEETS_STRONG_INTEGRITY` 检测。

---

## 技术架构与工作原理

### 原生 Keystore 服务挂钩

TrickyStoreOSS 工作在系统服务边界层：

1. **Binder 事务拦截**：在 Android 12+ 上向 `keystore2` 服务守护进程注入挂钩（Android 10–11 上则针对旧版 `keystore`）。
2. **Keybox 替换签发**：当 `target.txt` 中指定的应用发起硬件密钥生成请求时，TrickyStoreOSS 会提取 `keybox.xml` 中的私钥与 Google 签发的证明证书，合成对应的 X.509 证书链。
3. **信任根状态伪装**：在将响应返回给调用方之前，向 ASN.1 证明扩展结构中注入已验证启动标志（`Verified` 与已锁定 Bootloader 状态）。
4. **配置即时同步**：自动监听 `/data/adb/tricky_store/` 下的文件写入事件并刷新内存缓冲区，全程无需重启手机。

---

## 安装与配置

1. 卸载此前安装过的任何闭源版 TrickyStore 模块。
2. 下载并在 Magisk、KernelSU 或 APatch 中刷入最新版 `TrickyStoreOSS-*.zip`。
3. 重启设备。
4. 将未吊销的硬件 Keybox 放置于：
   ```bash
   /data/adb/tricky_store/keybox.xml
   ```
5. 在以下文件中填写需要伪装证明的目标应用包名：
   ```bash
   /data/adb/tricky_store/target.txt
   ```

---

## 配置说明与日常使用

在 `/data/adb/tricky_store/` 目录中：
- **目标应用声明（`target.txt`）**：逐行填入需要返回伪造密钥证明的包名（如 `com.google.android.gms` 及各类银行应用）。
- **安全补丁级别（`security_patch.txt`）**：可选填 `YYYY-MM-DD` 格式日期，用于覆盖密钥证明扩展信息中上报的安全补丁日期。

---

## 故障排查与常见问题

- **密钥证明证书已吊销**：一旦 Google 将当前 Keybox 序列号列入吊销黑名单，认证便会立即失效。此时只需将 `/data/adb/tricky_store/keybox.xml` 替换为有效未吊销的 Keybox 文件即可。
- **生物识别认证失效**：请确保不要把系统生物识别框架相关包名（如 `com.android.settings`、`android`）写入 `target.txt`。
