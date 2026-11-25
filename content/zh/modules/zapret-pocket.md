---
id: "zapret-pocket"
title: "zapret Pocket：独立运行的 DPI 深度包检测绕过引擎"
sidebarTitle: "zapret Pocket"
description: "由 sevcator 移植自 bolvan zapret 的 Root Android 工具，无需外部 VPN 隧道即可实现数据包乱序、SNI 分片与伪造 TLS ClientHello。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "zapret pocket Magisk 模块"
  - "sevcator zapret-pocket 下载"
  - "Android Root 绕过 DPI 限速"
  - "nfqws Android Magisk 配置"
  - "zapret 安卓版策略切换"
prerequisites:
  - "已获取 Root 权限的 Android 设备（Magisk、KernelSU 或 APatch）"
  - "内核支持 `iptables` 或 `nftables` 数据包过滤与队列转发（`nfqueue`）"
conflicts: []
configPaths:
  - "/data/adb/modules/zapret/"
  - "/data/adb/modules/zapret/zapret/"
features:
  - "多策略 DPI 规避：支持 TCP 分段拆分、SNI 分片、伪造 TLS ClientHello、错误校验和及跳数 TTL 干扰"
  - "零外部服务器依赖：直接在设备本地改写数据包流，无需将流量转发至第三方代理节点或 VPN 服务器"
  - "丰富预设规则库：内置针对不同地区运营商与特定平台（YouTube、Discord 语音、在线游戏）调优的配置脚本"
  - "透明运行机制：在 Netfilter 层拦截处理网络流量，完整保留 Android 系统 VPN 卡槽供其他应用使用"
faq: []
---

## 概述

由 sevcator 移植并维护的 zapret Pocket 将知名的 `zapret` 深度包检测（DPI）绕过工具带到了已 Root 的 Android 设备上。在部分网络环境中，互联网服务提供商（ISP）或监管网关会利用中间盒对特定协议（如 YouTube 4K 视频流、Discord 语音网关与社交平台）进行限速或阻断，这些 DPI 引擎通过解析初始 TLS ClientHello 与 SNI（服务器名称指示）字段来丢弃或延迟数据包。

zapret Pocket 无需远程 VPN 或代理服务器即可绕过此类中间盒。该模块完全在设备本地通过 `nfqws`（Netfilter Queue Web Surrogate）与内核包过滤机制运行，对发出的数据包实施乱序重排——包括发送乱序分段、构造目标服务器会直接丢弃但足以干扰中间盒判断的错误校验和包，以及拆分 TLS 握手包以防止检测设备识别目标域名。

## 前置要求与兼容性

- **Root 环境**：兼容 Magisk、KernelSU 与 APatch。
- **内核要求**：需要 Linux 内核支持 Netfilter 数据包队列（`CONFIG_NETFILTER_NETLINK_QUEUE` / `iptables` `NFQUEUE`）。绝大多数现代 Android 原厂及第三方内核均原生支持这些标准网络特性。

目前无已知的模块冲突。但需注意，若同时运行开启全局终止开关（Killswitch）的系统级 VPN 应用，流量会先进入该 VPN 隧道，导致 zapret 无法在物理网卡出口处处理原始数据包。

## 数据包乱序机制

zapret Pocket 通过 `nfqws` 配合预设的乱序脚本工作：

- **伪造 TLS ClientHello**：在真实 TLS 握手之前发送构造的虚假 TLS ClientHello 数据包。中间盒会锁定在虚假域名上，而目标服务器会忽略无效包并正常建立真实连接。
- **SNI 分片（`splitsniext`）**：在 Server Name Indication 字段边界处将 TLS ClientHello 拆分为多个 TCP 分段，使依赖完整主机名匹配的中间盒无法重组识别。
- **TTL / 跳数限制技巧（`ttlpadencap`）**：精确设置数据包的生存时间（TTL）参数，使伪造包刚好能够抵达并迷惑检测设备，而在到达真实目标服务器前即过期丢弃。
- **QUIC / HTTP3 握手扰动**：改写 UDP QUIC 初始报文头部，帮助 YouTube 及现代浏览器通过 HTTP/3 恢复正常连接。

## 配置与使用

1. 从项目仓库下载最新的 `zapret` 模块压缩包。
2. 通过 Magisk、KernelSU 或 APatch 刷入模块。
3. 重启设备。
4. 模块开机后会自动选用一套通用的默认绕过策略。
5. 如需测试或切换其他策略，可查看以下目录中的预设脚本：
   ```bash
   /data/adb/modules/zapret/zapret/
   ```
   内置预设包含针对特定场景优化的脚本，例如 `discordfake.sh`、`discord_voice_badseq.sh`、`general_alt*.sh` 以及部分区域运营商模板。
6. 运行状态文件与二进制程序存放于：
   ```bash
   /data/adb/modules/zapret/
   ```

## 故障排查与验证

- **DPI 依然阻断连接**：不同宽带运营商与移动蜂窝网络的 DPI 设备配置差异较大。如果默认预设未能成功解锁服务，请在模块目录中尝试切换其他策略脚本（例如测试 `fake-i.sh`、`splitsniext.sh` 或 `faketlsalt_*.sh`）。
- **DNS 污染阻断**：zapret 仅针对 TCP 与 UDP 数据流进行乱序处理，无法绕过 DNS 投毒或劫持。请务必搭配加密 DNS（如 DNS-over-HTTPS 或 DNS-over-TLS）使用，以防止域名解析阶段被重定向。
