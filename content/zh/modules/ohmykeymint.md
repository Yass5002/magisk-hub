---
id: "ohmykeymint"
title: "OhMyKeymint：基于 Rust 的 Keystore 2.0 与 KeyMint 拦截器"
sidebarTitle: "OhMyKeymint"
description: "采用 Rust 开发的密钥证明重定向模块，挂钩 Android 12+ 的 keystore2 守护进程并将加密证明路由至自定义 KeyMint 配置。"
category: "root-management"
tier: 1
searchQueries:
  - "ohmykeymint magisk 模块"
  - "qwq233 ohmykeymint"
  - "android keystore2 rust hook"
  - "ohmykeymint config toml 配置"
  - "keymint 密钥证明伪装"
prerequisites:
  - "Android 12 及以上系统（依赖 keystore2 架构）"
  - "64 位处理器架构（arm64-v8a）"
  - "Magisk、KernelSU 或 APatch"
conflicts:
  - "无已知的常规模块冲突；但请勿与其他 keystore2 注入器（如 TrickyStore 或 TEESimulator）同时运行"
configPaths:
  - "/data/adb/ohmykeymint/config.toml"
  - "/data/adb/ohmykeymint/"
features:
  - "Rust 驱动的注入引擎：通过 ptrace 或 dlopen 挂钩 keystore2，具备零运行时垃圾回收（GC）开销"
  - "自定义 KeyMint 路由：拦截硬件密钥生成调用并定向至用户定义的 KeyMint 提供程序"
  - "TOML 格式配置：精细化声明目标应用包名、设备标识与密钥证明策略"
  - "零生物识别干扰：未列入目标的应用可透明访问设备真实安全硬件飞地"
  - "无缝生态兼容：适配 Magisk、KernelSU 与 APatch 下的现代 Root 环境"
faq:
  - question: "为什么 OhMyKeymint 要求 Android 12 或更高版本？"
    answer: "OhMyKeymint 专为挂钩 Android Keystore 2.0 系统守护进程（keystore2）及其 AIDL KeyMint HAL 接口而架构。Android 11 及更早版本使用的是旧版 C++ keystore 守护进程与 HIDL Keymaster HAL，不在本引擎支持范围内。"
  - question: "如何在 OhMyKeymint 中配置目标应用？"
    answer: "所有配置均在 /data/adb/ohmykeymint/config.toml 中管理，可在其中定义目标应用包名、伪造的安全补丁日期以及 Keybox 证书链参数。"
---

## 概述

**OhMyKeymint** 由 **qwq233** 开发，是一款采用 Rust 编写、专为现代 Android 版本（Android 12+）打造的高级密钥证明拦截框架。

随着 Google 将旧版 Keymaster HIDL 服务全面迁移至基于 AIDL 的 Keystore 2.0（`keystore2`），应用请求硬件级密钥证明的机制也随之重构。OhMyKeymint 直接挂钩 `keystore2` 进程，允许用户通过程序化生成的 KeyMint 配置文件满足 Play Integrity 校验，同时完整保留常规生物识别认证所需的真实设备硬件密钥能力。

---

## 技术架构与工作原理

### Keystore 2.0 守护进程挂钩

OhMyKeymint 运行在系统 keystore 进程的地址空间内：

1. **Binder 事务拦截**：在 `keystore2` 守护进程内部挂钩 Android 的 `android.system.keystore2` AIDL 接口。
2. **选择性策略评估**：当客户端应用携带证明参数调用 `generateKey` 时，OhMyKeymint 会查询其 TOML 配置，判断发起调用的 UID 是否匹配已声明的目标应用。
3. **KeyMint 模拟**：被拦截的请求会被重定向至软件模拟的 KeyMint 实例，使用配置好的密钥凭证为返回的证书链签名。

---

## 安装与配置

1. 确认设备运行 **Android 12** 或更高版本且为 **64 位**平台。
2. 下载最新的 `OhMyKeymint-*.zip` 发布包。
3. 在 Root 管理器（Magisk、KernelSU 或 APatch）中刷入模块。
4. 重启设备。

---

## 配置与使用

在以下路径中配置目标应用包名与密钥证明参数：
```toml
/data/adb/ohmykeymint/config.toml
```
请参考项目文档中的示例配置，按需填写应用包名与安全补丁级别。

---

## 故障排查与常见问题

- **Keystore 守护进程反复崩溃**：如果 `keystore2` 守护进程不断重启，请检查 `config.toml` 是否存在 TOML 语法错误，并确认当前未同时启用其他 keystore 挂钩模块。
