---
id: "re-malwack"
title: "Re-Malwack：进阶遥测、广告与恶意软件拦截套件"
sidebarTitle: "Re-Malwack"
description: "全面的隐私保护与 Systemless 广告拦截套件，提供多档位过滤方案、WebUI 可视化管理及 hosts 规则自动同步。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "Re-Malwack Magisk 模块"
  - "ZG089 Re-Malwack 下载"
  - "Android Systemless 恶意域名拦截"
  - "Re-Malwack WebUI 去广告教程"
  - "Android 进阶 hosts 过滤"
prerequisites:
  - "Magisk、KernelSU 或 APatch（亦可通过本地 VPN 配置在未 Root 环境下使用）"
  - "用于切换规则档位的 Root 终端模拟器或 WebUI 访问能力"
conflicts:
  - "明确说明：暂无与其他模块的已知冲突文档记录；但其他编辑 `/system/etc/hosts` 的模块可能会覆盖当前生效的规则集"
configPaths:
  - "/data/adb/modules/Re-Malwack/"
  - "/data/adb/modules/Re-Malwack/config.json"
features:
  - "多档位过滤模式：支持在 Lite、Full、Ultimate 与 Gaming 防护等级之间按需切换"
  - "集成现代 WebUI：无需输入终端命令即可开关规则列表、查看拦截统计并触发更新"
  - "专项追踪与恶意软件防护：拦截移动端遥测探针、追踪信标及已知钓鱼域名"
  - "自动更新机制：定期检查远程黑名单仓库，持续维持最新防护状态"
  - "本地白名单管理：直接在 WebUI 中轻松豁免被误杀的正常域名"
faq:
  - question: "Re-Malwack 与普通的静态 hosts 文件有何区别？"
    answer: "Re-Malwack 是一套完整的管理套件，包含多种防护档位、交互式 WebUI、自动更新脚本以及自定义白名单管理，而非仅仅是一个单一的静态文本文件。"
  - question: "日常使用应该选择哪个过滤档位？"
    answer: "日常使用推荐选择 `Lite` 或 `Full` 档位，它们能在不影响正常购物返利链接或常规分析服务的前提下，提供稳健的广告与追踪器拦截；`Ultimate` 档位则提供更为严格的拦截策略，适合对隐私有极致要求的用户。"
---

## 概述

由 **ZG089** 开发的 **Re-Malwack** 是一款面向 Android 设备的进阶隐私保护与内容过滤框架。

不同于规则过期后必须手动重新刷包的传统静态 hosts 模块，Re-Malwack 将多源威胁情报、交互式 WebUI 与模块化运行档位融为一体，可在所有已安装应用中有效阻断移动广告、后台诊断遥测、监控软件（Stalkerware）域名以及恶意软件分发节点。

---

## 技术架构与工作原理

### 分层防护与域名重定向

Re-Malwack 通过多种协同机制实现全方位的过滤管理：

1. **Systemless Hosts 挂载**：在已 Root 的系统上，模块会将当前编译好的拦截列表挂载至 `/system/etc/hosts`，以零 CPU 开销将命中的主机名重定向至 `0.0.0.0`。
2. **动态档位编译**：模块通过 `/data/adb/modules/Re-Malwack/config.json` 管理规则配置。切换过滤档位时会自动重新组合当前 hosts 结构并刷新 Android 的 DNS 解析缓存。
3. **WebUI 管理引擎**：提供响应式本地网页管理界面，广泛兼容 KernelSU、APatch 及主流 Magisk WebUI 宿主工具。

---

## 安装与配置

1. 下载最新的 `Re-Malwack-*.zip` 发布包。
2. 在你的 Root 管理器（Magisk、KernelSU 或 APatch）中刷入该模块。
3. 重启设备。
4. 从 Root 管理器中启动 WebUI，或打开 Root 终端执行 `remalwack` 命令以选择初始过滤档位。

---

## 日常配置与使用

在 WebUI 或终端管理界面中，你可以进行以下操作：
- **档位选择**：在 Lite、Full 或 Ultimate 防护等级之间切换。
- **自定义白名单**：将银行应用或企业办公应用所需的域名添加至本地白名单，防止误拦截。
- **更新频率设置**：配置后台自动更新策略，确保拦截列表始终与上游安全规则源保持同步。

---

## 故障排查与常见问题

- **部分应用无法正常加载**：若遇到特定应用联网异常，可临时切换至 **Lite** 档位，或通过 WebUI 将该应用的主 API 域名加入本地白名单。
