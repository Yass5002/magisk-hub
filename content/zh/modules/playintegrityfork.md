---
id: "playintegrityfork"
title: "PlayIntegrityFork：Android 13-15 通过 MEETS_DEVICE 完整性认证指南"
sidebarTitle: "PlayIntegrityFork"
description: "PlayIntegrityFix 的高可定制分支，支持自定义 pif.json 构建属性伪装与字段覆写，助力通过 Google Play Integrity 设备级认证。"
category: "root-management"
tier: 1
searchQueries:
  - "playintegrityfork 与 playintegrityfix 区别"
  - "magisk 怎么过 device integrity"
  - "自定义 pif.json 指纹教程"
  - "magisk 修复银行应用 play integrity"
  - "osm0sis playintegrityfork 下载"
prerequisites:
  - "Magisk 26.0+（启用 Zygisk），或搭配 Zygisk Next 的 KernelSU / APatch"
  - "已安装 Google Play 商店与 Google Play 服务（GMS）"
conflicts:
  - "KOWX712/PlayIntegrityFix（不可同时运行）"
  - "MagiskHidePropsConf（已过时且会干扰完整性认证）"
configPaths:
  - "/data/adb/pif.json"
  - "/data/adb/modules/playintegrityfork/"
features:
  - "精准在 Google Play 服务 DroidGuard 与认证进程内伪装设备属性"
  - "支持动态解析 pif.json，无需重刷模块即可更换未被封禁的自定义设备指纹"
  - "自定义字段伪装：支持按需覆写 PRODUCT、DEVICE、MANUFACTURER、BRAND、MODEL、FINGERPRINT、SECURITY_PATCH 与 FIRST_API_LEVEL"
  - "对非 GMS 应用进程零干扰"
faq:
  - question: "为什么 Play Integrity 认证几天后又从通过变成了失败？"
    answer: "当检测系统发现同一套公开设备指纹伴随大量硬件证明不匹配请求时，Google 会定期将其拉入黑名单。要恢复 MEETS_DEVICE_INTEGRITY，需从未经封禁的认证设备中提取或生成一份非公开的干净 pif.json 指纹并放入 /data/adb/pif.json。"
  - question: "PlayIntegrityFork 能通过 MEETS_STRONG_INTEGRITY 吗？"
    answer: "不能。MEETS_STRONG_INTEGRITY 需要由物理硬件安全模块 / 可信执行环境（TEE）签发的加密证明。在 Bootloader 已解锁的设备上，仅靠软件层属性伪装无法单独通过强完整性认证，你必须配合 TrickyStore 等硬件 Keybox 伪装模块使用。"
---

## 概述

**PlayIntegrityFork** 由知名开发者 **osm0sis** 维护，是在原版 PlayIntegrityFix 引擎基础上打造的功能增强型高灵活度分支。当系统检测到 Bootloader 已解锁时，Google Play 服务会发起基于加密硬件的密钥证明（Key Attestation），从而导致 SafetyNet 与 Play Integrity 校验直接失败。

PlayIntegrityFork 会拦截 Google 认证进程（`com.google.android.gms.unstable`）发起的请求，引导认证客户端回退至早期的软件级证明流程，随后将设备身份字段替换为经过验证的官方 OEM 构建属性，从而顺利通过 Google 的 `MEETS_BASIC_INTEGRITY` 与 `MEETS_DEVICE_INTEGRITY` 检测标准。

---

## 技术架构与工作原理

### DroidGuard 的 Zygisk 拦截机制

1. **目标进程定位**：在 Android 中，设备完整性评估由 Google Play 服务的一个专用子进程负责：`com.google.android.gms.unstable`。
2. **原生动态库注入**：当 Zygisk 初始化该进程时，PlayIntegrityFork 会注入原生配套库（`libplayintegrityfork.so`）。
3. **系统属性屏蔽**：模块在 libc 层挂钩 `__system_property_get` 与 `__system_property_read` 调用。当 Google Play 服务查询 `ro.build.fingerprint` 或 `ro.product.model` 等构建属性时，被 Hook 的函数会返回 `/data/adb/pif.json` 中定义的数值。
4. **认证降级回退**：出厂搭载较旧系统版本（通常为 Android 7.0 及更早系统，或未强制执行硬件 Keymaster 认证的设备）的机型不强制要求硬件级 Keystore 证明。通过提交带有匹配 `FIRST_API_LEVEL` 属性的早期有效指纹，PlayIntegrityFork 会促使 Google Play 服务切换至软件证明模式。

---

## 前置准备与安装步骤

### 第一步：准备运行环境
1. 确保你的 Root 方案已启用有效的 Zygisk 实现：
   - **Magisk**：在设置中开启 Zygisk。
   - **KernelSU / APatch**：安装并确认 **Zygisk Next** 或 **ReZygisk** 正常运行。
2. 卸载所有过时的属性伪装模块（例如旧版 PIF 或 MagiskHidePropsConf）。

### 第二步：刷入模块
1. 从发布页下载最新的 `PlayIntegrityFork-vX.zip`。
2. 在 Root 管理器中进入**模块** → **从本地安装** → 选择该压缩包。
3. 重启设备。

### 第三步：清理 GMS 缓存
重启完成后，清理 Google Play 服务缓存与数据以刷新残留的认证令牌：
```bash
su -c "pm clear com.google.android.gms"
su -c "killall com.google.android.gms.unstable"
```

---

## 配置与自定义 pif.json

PlayIntegrityFork 内置了默认回退指纹，但为避免受公开指纹封禁波及，强烈建议配置自定义 `pif.json`。

创建或编辑 `/data/adb/pif.json`：
```json
{
  "PRODUCT": "marlin",
  "DEVICE": "marlin",
  "MANUFACTURER": "Google",
  "BRAND": "google",
  "MODEL": "Pixel XL",
  "FINGERPRINT": "google/marlin/marlin:7.1.2/NJH47F/4146048:user/release-keys",
  "SECURITY_PATCH": "2017-08-05",
  "FIRST_API_LEVEL": "25"
}
```

每次更新 `/data/adb/pif.json` 后，强行重启 `unstable` 进程即可立即应用新属性：
```bash
su -c "killall -9 com.google.android.gms.unstable"
```

---

## 常见问题与故障排查

- **银行应用仍然检测到 Root**：
  通过 Play Integrity 并不代表自动隐藏了 Root 文件痕迹。请确认已将银行应用添加至 Magisk 的**排除列表（DenyList）**或在 **Shamiko / Zygisk Assistant** 中完成配置，并核实应用未检测到 Magisk 管理器包名（请开启「隐藏 Magisk 应用」）。
- **Play 商店仍显示「设备未认证」**：
  通过 `MEETS_DEVICE_INTEGRITY` 后，Play 商店应用的认证状态缓存最长可保留 24 小时。请前往**设置** → **应用** → **Google Play 商店** → **存储** → **清除存储空间**，随后重启设备。
