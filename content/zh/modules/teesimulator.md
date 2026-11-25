---
id: "teesimulator"
title: "TEESimulator：进程内 KeyMint 软件级密钥证明模拟引擎"
sidebarTitle: "TEESimulator"
description: "通过将 AOSP 官方参考 KeyMint 可信应用直接嵌入 Android keystore 守护进程，完整满足硬件密钥证明校验的软件模拟框架。"
category: "root-management"
tier: 1
searchQueries:
  - "TEESimulator Magisk 模块下载"
  - "JingMatrix TEESimulator 教程"
  - "KeyMint 硬件密钥证明模拟"
  - "TEESimulator keybox.xml 配置"
  - "Strong Integrity 过检测 TEESimulator"
prerequisites:
  - "Android 10 及以上系统"
  - "64 位处理器架构（arm64-v8a 或 x86_64）"
  - "已安装 Magisk、KernelSU 或 APatch"
  - "有效的硬件级 `keybox.xml` 证书链文件"
conflicts:
  - "明确说明：暂无已知与其他模块的冲突；未配置有效 Keybox 时模块将保持静默空操作"
configPaths:
  - "/data/adb/teesim/config.json"
  - "/data/adb/teesim/keybox.xml"
  - "/data/adb/modules/teesim/"
features:
  - "内嵌参考 KeyMint TA：直接在 Android keystore 守护进程内运行 AOSP 原生 `kmr-ta` 可信应用"
  - "细粒度配置档案：支持按应用包名独立映射 Keybox 凭据、安全补丁日期及设备标识"
  - "动态热重载：修改 `config.json` 后配置即时生效，无需重启系统"
  - "不可变信任根冻结：跨重启冻结设备 Root of Trust 参数，确保 KeyMint 密钥加密密钥始终可正常解密"
  - "选择性路由分流：仅拦截目标应用的密钥证明请求，非目标应用与真实硬件密钥直接透传至物理 TEE"
faq:
  - question: "TEESimulator 与 TrickyStore 有什么区别？"
    answer: "TrickyStore 是在证书生成后拦截并篡改密钥证明证书内容，而 TEESimulator 直接将 AOSP 官方参考 KeyMint 可信应用（kmr-ta）嵌入 keystore 守护进程中。密钥与证书链由完整模拟引擎按真实 TEE 流程现场签发生成，从源头上保证数学逻辑与格式结构的高度自洽。"
  - question: "为什么该模块仅支持 64 位设备？"
    answer: "自 Android 10 起，系统的 keystore 与 keystore2 守护进程均以纯 64 位二进制（arm64-v8a 或 x86_64）形式编译。由于 TEESimulator 需要将原生挂钩库直接注入这些守护进程的地址空间，因此必须匹配 64 位系统架构。"
---

## 概述

由 **JingMatrix** 开发的 **TEESimulator**，通过在系统密钥库服务进程内部运行真实的软件态 KeyMint 可信应用（TA），从底层解决 Android 硬件级密钥证明（Key Attestation）校验难题。

与直接拦截成品证书或临时改写 ASN.1 扩展字段的做法不同，TEESimulator 直接内嵌了 AOSP 原生参考 Rust 版 KeyMint 实现（`kmr-ta`）。借助用户提供的 `keybox.xml` 执行完整的模拟硬件密码学运算，其生成的证明证书在构造流程与密码学特征上与真实硬件可信执行环境（TEE）完全一致。

---

## 技术架构与工作原理

### 守护进程注入与 Binder 路由机制

TEESimulator 将核心职责划分为特权控制守护进程与进程内原生拦截库两部分：

1. **启动初始化与状态采集**：开机时，控制守护进程会生成一个临时硬件密钥以探测物理设备真实的信任根参数（包括 Verified Boot 状态、系统版本与安全补丁级别），并将其冻结为不可变硬件档案，避免重启后原有已存储密钥无法解密。
2. **分版本守护进程拦截**：
   - **Android 12+（`keystore2`）**：模块注入 `keystore2` 守护进程，并对 `AIBinder_transact` 实施 PLT 挂钩。当目标应用发起密钥证明请求时，调用会被重定向至内置 `kmr-ta` 引擎的进程内 `IKeyMintDevice` 实例；未列入目标的应用则原样透传给物理 TEE。
   - **Android 10–11（`keystore`）**：模块在旧版 `keystore` 守护进程内部对 `libbinder` 的 `ioctl` 进行挂钩，将调用路由至本地存根并由软件 KeyMint 引擎签发证明。
3. **实时配置推送**：守护进程持续监听本地 UNIX 域套接字。一旦 `/data/adb/teesim/config.json` 发生保存修改，新策略会立即推送到已注入的拦截器中，无需重启设备或杀掉守护进程。

---

## 安装与配置

### 1. 刷入模块
1. 从官方发布页下载最新版 `TEESimulator-v*.zip`。
2. 在 Magisk、KernelSU 或 APatch 中刷入模块并重启设备。

### 2. 放置 Keybox 凭据文件
将有效且未被吊销的硬件 `keybox.xml` 放入以下配置目录：
```bash
/data/adb/teesim/keybox.xml
```

### 3. 指定目标应用
编辑 `/data/adb/teesim/config.json` 并配置目标应用包名：
```json
{
  "version": 1,
  "profiles": {
    "default": {
      "keybox": "keybox.xml",
      "patchLevel": {
        "system": "today",
        "vendor": "YYYY-MM-05",
        "boot": "YYYY-MM-05"
      },
      "osVersion": "",
      "apps": [
        "com.google.android.gms",
        "com.android.vending"
      ]
    }
  }
}
```
保存文件后，运行中的守护进程会自动同步更新生效的目标过滤规则。

---

## 配置说明与实用技巧

在 `/data/adb/teesim/config.json` 中：
- **动态日期语法**：`today` 会自动解析为当前月份，而 `YYYY-MM-05` 会映射为当前自然月的 5 号，以贴合 Android 月度安全公告的标准日期规范。
- **设备身份模拟**：可在配置档案中手动指定 `brand`、`model`、`serial` 与 `imei` 等字段以应对设备 ID 证明校验；若留空则自动继承物理设备的真实硬件标识符。

---

## 故障排查与常见问题

- **异常恢复与清理状态**：若错误的配置或测试档案导致系统密钥生成异常，可在 Root 终端中手动重启 keystore 守护进程：
  ```bash
  # Android 12+
  su -c 'kill $(pidof keystore2)'
  # Android 10-11
  su -c 'kill $(pidof keystore)'
  ```
  系统会自动拉起全新的 keystore 守护进程，在 TEESimulator 控制进程重新注入配置前保持未拦截状态运行。
