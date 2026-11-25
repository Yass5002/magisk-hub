---
id: "sam"
title: "SAM：集成 SmartDNS、AdGuard Home 与 Mihomo 的透明代理套件"
sidebarTitle: "SAM (DNS & 代理)"
description: "由 5MayRain 打造的三合一整合模块，将 SmartDNS、AdGuard Home 与 Mihomo 融合为统一的 DNS 过滤与透明代理流水线。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "SAM Magisk 模块下载"
  - "5MayRain SAM"
  - "SmartDNS AdGuard Home Mihomo 安卓"
  - "AdGuard 透明代理 Magisk 模块"
  - "SAM DNS 流水线配置指南"
prerequisites:
  - "搭载 Magisk、KernelSU 或 APatch 的已 Root Android 设备"
  - "Web 管理面板所需端口未被其他进程占用"
conflicts:
  - "不可与独立运行的 DNS 转发模块或其他透明代理管理模块同时启用"
configPaths:
  - "/data/adb/modules/SAM/"
  - "/data/adb/modules/SAM/etc/mihomo/base.yaml"
features:
  - "统一三合一网络架构：在单个 Root 模块内无缝串联 SmartDNS、AdGuard Home 与 Mihomo（Clash Meta）"
  - "双流水线拓扑：支持在 `SmartDNS > Mihomo > AdGuardHome` 与 `SmartDNS > AdGuardHome > Mihomo` 两条路由链条间自由切换"
  - "Hosts 实时热重载：自动监测系统 hosts 文件改动，无需重启守护进程即可即时应用新的 DNS 过滤规则"
  - "网络接口与应用排除：支持配置指定 Wi-Fi 网络黑名单，并定义分应用代理路由规则"
  - "Web 管理控制台：提供浏览器管理面板，用于实时监控 AdGuard Home DNS 查询记录并管理 Mihomo 代理节点"
faq: []
---

## 概述

由 5MayRain 开发的 **SAM**（SmartDNS + AdGuardHome + Mihomo）是一款专为 Root Android 平台打造的全功能网络优化、广告拦截与透明代理套件。如果分别独立运行各类 DNS 引擎与代理工具，极易引发端口冲突、DNS 路由死循环以及电量异常消耗；SAM 通过一套完整的 Systemless 流水线将三大组件有机编排在一起，彻底化解了上述难题。

根据实际需求，你可以单独启用其中某个组件、两两组合搭配，或同时运行全套过滤与代理栈。

## 前置要求与兼容性

- **Root 框架**：支持 Magisk、KernelSU 与 APatch。
- **端口可用性**：确保 53（DNS 服务）、3000（AdGuard Home Web 控制台）及 9090（Mihomo 控制面板）端口未被其他进程劫持占用。

### 冲突提示

切勿将 SAM 与其他独立透明代理模块（如 MagicNet 或 Surfing）或独立 DNS 重定向模块（如 AdGuardHomeForRoot）同时启用。多个模块同时争抢绑定 53 端口或修改 iptables 规则将直接导致断网。

## 服务拓扑与优先级流向

SAM 支持两种核心路由链条结构：

1. **`SmartDNS > Mihomo > AdGuardHome`**：
   - 查询请求首先到达 SmartDNS，由其完成智能域名解析与最速 IP 测速优选。
   - 随后流量进入 Mihomo 执行基于规则的代理分流。
   - 最后由 AdGuard Home 执行末端的广告与追踪器过滤。
2. **`SmartDNS > AdGuardHome > Mihomo`**：
   - 流量先经过 AdGuard Home 完成广告过滤后，再交由 Mihomo 进行代理转发。

### 核心组件职责说明
- **SmartDNS**：拥有最低的转发优先级；当其他服务协同运行时，主要承担上游域名解析器的角色。
- **AdGuardHome**：提供系统级本地广告拦截、DNS 查询日志审计与自定义过滤规则管理。
- **Mihomo**：担任透明代理核心，负责将网络套接字流量按策略转发至所配置的代理节点。

## 配置与后台面板

1. 在 Root 管理器中刷入 `SAM-*.zip` 并重启设备。
2. 集成 Web 管理面板的默认登录凭据为：
   - **用户名**：`root`
   - **密码**：`root`
3. 通过浏览器访问 `http://127.0.0.1:3000` 打开 AdGuard Home 管理后台。
4. Mihomo 核心配置文件位于：
   ```bash
   /data/adb/modules/SAM/etc/mihomo/base.yaml
   ```
   > [!IMPORTANT]
   > 请勿随意删除或破坏性修改 `base.yaml`；SAM 依赖该文件内的特定锚点结构来绑定透明代理端口。
5. 所有模块资源与配置文件均持久保存于：
   ```bash
   /data/adb/modules/SAM/
   ```

## 故障排查与验证

- **设备失去网络连接**：
  - 尝试开关一次飞行模式以重置 Android 的网络接口状态。
  - 打开 AdGuard Home 查询日志（`http://localhost:3000`），检查请求是否被误拦截或上游 DNS 服务器是否处于不可达状态。
- **豁免特定 Wi-Fi 网络**：利用 SAM 的 Wi-Fi 黑名单功能，在连接受信任的家庭局域网或企业内网时自动停用代理。
