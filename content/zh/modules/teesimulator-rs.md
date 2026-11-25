---
id: "teesimulator-rs"
title: "TEESimulator-RS：Rust 原生硬件 Keybox 与 Keystore 密钥证明模拟引擎"
sidebarTitle: "TEESimulator-RS"
description: "高性能 Rust 重写版 TEESimulator，将 AOSP 官方参考 KeyMint 可信应用直接嵌入 Android keystore 守护进程。"
category: "root-management"
tier: 1
searchQueries:
  - "TEESimulator-RS Magisk 模块"
  - "TEESimulator Rust 版 Keybox"
  - "Enginex0 TEESimulator-RS 下载"
  - "Rust Keystore 硬件密钥证明"
  - "Strong Integrity 过检测 TEESimulator-RS"
prerequisites:
  - "Android 10 及以上系统"
  - "64 位处理器架构（arm64-v8a 或 x86_64）"
  - "已安装 Magisk、KernelSU 或 APatch"
  - "有效的硬件级 `keybox.xml` 证书链文件"
conflicts:
  - "明确说明：暂无已知与其他模块的冲突；未配置 Keybox 时将回退至仅软件模式"
configPaths:
  - "/data/adb/teesim/config.json"
  - "/data/adb/teesim/keybox.xml"
  - "/data/adb/teesim/target.txt"
  - "/data/adb/teesim/security_patch.txt"
features:
  - "Rust 原生实现：内存安全且高速执行，显著降低 KeyMint 事务中的 Binder 通信延迟"
  - "内嵌 AOSP 参考 KeyMint TA：直接在 Android 的 `keystore2` 或旧版 `keystore` 守护进程内运行 `kmr-ta`"
  - "灵活的目标筛选模式：同时支持 `target.txt` 包名声明与动态安全补丁级别伪装"
  - "配置实时热重载：自动监听配置文件变更并即时刷新守护进程内存状态，无需重启"
  - "零痕迹透传：未列入目标的应用直接与物理硬件 TEE 芯片通信，完全不受干预"
faq:
  - question: "TEESimulator 与 TEESimulator-RS 有何区别？"
    answer: "TEESimulator-RS 是由 Enginex0 基于 Rust 语言开发的优化重写版本。它在配置格式与密码学行为上与原项目保持完全兼容，同时大幅降低了内存开销并提升了挂钩拦截性能。"
  - question: "没有 keybox.xml 文件时，TEESimulator-RS 还能起作用吗？"
    answer: "不能。如果缺少有效的硬件级 keybox.xml，模块无法签发由 Google 认证信任根签署的合法密码学签名，从而导致严格的完整性校验失败。"
---

## 概述

由 **Enginex0** 维护的 **TEESimulator-RS** 是 TEESimulator 架构的 Rust 语言实现版本，专用于应对 Android 硬件级密钥证明（Key Attestation）检测。

现代系统完整性校验会在硬件安全飞地中通过密码学手段验证 Bootloader 状态。TEESimulator-RS 在系统 Keystore 层拦截密钥创建调用，直接在守护进程内部运行 AOSP 参考 KeyMint Rust 引擎（`kmr-ta`），并借助用户提供的 `keybox.xml` 签发密码学特征真实可信的证明证书。

---

## 技术架构与工作原理

### 进程内 KeyMint 路由机制

TEESimulator-RS 向 Android 密钥库服务注入原生 Rust 拦截引擎：

1. **Binder 事务挂钩**：在 Android 12+ 上，模块对 `keystore2` 进程内的 `AIBinder_transact` 实施挂钩。当已声明的目标应用发起密钥生成请求时，相关事务会被路由至负责调度 `kmr-ta` 的进程内 `IKeyMintDevice` 实例。
2. **选择性应用作用域**：非目标应用（如设备生物识别解锁、Widevine DRM 及 FIDO 凭据）完全绕过模拟器，直接与真实硬件 TEE 通信。
3. **安全补丁级别对齐**：模块读取 `/data/adb/teesim/security_patch.txt`，将上报的系统、厂商及 Boot 安全补丁日期对齐至当前 Play Integrity 校验要求。

---

## 安装与配置

1. 在 Magisk、KernelSU 或 APatch 中刷入最新版 `TEESimulator-RS-*.zip`。
2. 重启设备。
3. 将有效且未被吊销的 `keybox.xml` 放入以下路径：
   ```bash
   /data/adb/teesim/keybox.xml
   ```
4. 在以下文件中声明需要拦截的目标应用包名：
   ```bash
   /data/adb/teesim/target.txt
   ```
5. 控制进程会实时监听上述文件变化，保存后无需再次重启即可生效。

---

## 故障排查与常见问题

- **密钥证明返回 Software-Only（仅软件级）**：若检测工具显示仅具备软件级证明，请检查 `/data/adb/teesim/keybox.xml` 是否存在、权限是否可读，且其中包含有效的 RSA/EC 私钥与完整证书链。
- **守护进程异常恢复**：若错误配置导致密钥操作卡死，可通过 Root 终端重启 keystore 守护进程（`kill $(pidof keystore2)`）。
