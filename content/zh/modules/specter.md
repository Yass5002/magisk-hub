---
id: "specter"
title: "Specter：现代密钥证明与防检测自动化管理套件"
sidebarTitle: "Specter"
description: "简洁精干、无冗余代码的管理控制面板与自动化套件，专用于协调 TEESimulator、TrickyStore 与 Play Integrity Fix 模块。"
category: "root-management"
tier: 1
searchQueries:
  - "Specter Magisk 模块下载"
  - "dpejoh Specter 使用教程"
  - "Specter Keybox 认证管理"
  - "Yurikey 重写替代 Specter"
  - "Specter WebUI 过检测配置"
prerequisites:
  - "已安装 Magisk、KernelSU 或 APatch"
  - "已安装 TrickyStore、TEESimulator 或 TEESimulator-RS（若未检测到，Specter 可自动安装 TEESimulator-RS）"
  - "已安装 Play Integrity Fix 或 Play Integrity Fork 模块"
conflicts:
  - "明确说明：暂无已知与其他模块的冲突；定位为替代旧版 Yurikey 的纯净重写版本"
configPaths:
  - "/data/adb/tricky_store/target.txt"
  - "/data/adb/tricky_store/keybox.xml"
  - "/data/adb/modules/specter/"
features:
  - "彻底净室重写：剔除历史遗留冗余逻辑，从底层重构所有管理例程"
  - "多源 Keybox 目录：支持在线浏览、备份、恢复与检测证书包，具备自动吊销状态排查能力"
  - "自动发现目标应用：结合 `inotify` 文件系统监控与进程轮询，实时识别新安装的敏感应用"
  - "交互式 WebUI 面板：通过网页控制台随时查看模块运行状态、调整证明参数并自定义目标列表"
  - "首次启动全自动部署：初次开机自动执行配置备份、目标生成、安全补丁对齐与 Keybox 部署"
faq:
  - question: "Specter 和 Yurikey 之间是什么关系？"
    answer: "Specter 由 dpejoh 在原 Yurikey 项目基础上进行全面重写打造。它摒弃了早期大量堆砌 Shell 脚本的架构，换用了更清爽的现代代码结构、更完善的 WebUI 界面以及基于 inotify 的自动化应用目标捕获机制。"
  - question: "安装 Specter 之前必须先装好 TEESimulator 吗？"
    answer: "不需要。在安装配置过程中，如果 Specter 未检测到现有的 Keystore 拦截模块（TrickyStore、TEESimulator 或 TEESimulator-RS），它会自动为你安装 TEESimulator-RS。"
---

## 概述

由 **dpejoh** 开发的 **Specter** 是面向已 Root Android 设备的新一代密钥证明管理与防检测自动化套件。

作为早期 Yurikey 工具的彻底重写版本，Specter 聚焦运行速度、稳定性与简洁的交互体验。它作为上层编排引擎，自动接管底层 Keystore 模拟后端（如 TEESimulator、TEESimulator-RS 与 TrickyStore）的日常维护工作，无需繁琐的终端命令即可完成目标列表同步、Keybox 轮换及安全补丁日期对齐。

---

## 技术架构与工作原理

### Inotify 目标监控与多后端协同

Specter 作为编排管理层工作在底层 Keystore 挂钩模块之上：

1. **后端解耦兼容**：原生适配 TrickyStore、TEESimulator、TEESimulator-RS 以及 OhMyKeymint。
2. **Inotify 实时监听目标**：实时捕获新应用的安装事件。一旦检测到新安装的银行或支付类应用，Specter 会解析其清单信息并自动将包名写入 `/data/adb/tricky_store/target.txt`。
3. **开机自动维护**：在系统早期启动阶段自动执行，将安全补丁级别与当前 Play Integrity Fix 所用设备指纹对齐，并清理残留的 Google Play 服务进程。

---

## 安装与配置

1. 安装 **Play Integrity Fix** 或 **Play Integrity Fork**。
2. *（可选）* 安装 **TrickyStore** 或 **TEESimulator**（若未检测到现有后端，Specter 将自动安装 TEESimulator-RS）。
3. 在 Magisk、KernelSU 或 APatch 中刷入最新版 `Specter-v*.zip`。
4. 重启设备。
5. 首次开机时，Specter 会自动完成现有配置备份、目标应用写入及 Keybox 部署流程。
6. 在 Root 管理器中打开模块对应的 WebUI 界面即可检查或调整各项设置。

---

## 配置与使用

- **WebUI 控制面板**：通过 KernelSU / APatch 内置 WebUI 打开 Specter 控制台，可管理自定义 Keybox、查看 Google 证书吊销状态并检查当前生效的目标应用。
- **手动核对目标声明**：所有受控包名也可直接查看以下文件：
  ```bash
  /data/adb/tricky_store/target.txt
  ```

---

## 故障排查与常见问题

- **Google 证书吊销**：若当前证书链被标记为已吊销（Revoked），请在 Specter 的 WebUI 目录中切换至其他有效 Keybox，并触发一次进程清理即可恢复。
