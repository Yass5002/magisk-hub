---
id: "adguardhomeforroot"
title: "AdGuardHome for Root：本机独立 DNS 服务与广告屏蔽引擎"
sidebarTitle: "AdGuardHome for Root"
description: "在 Android 设备本地原生运行独立 AdGuard Home 服务，并通过系统级 iptables 重定向 DNS 流量，零 VPN 额外开销。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "adguardhome for root magisk 模块"
  - "安卓本地 adguard home iptables"
  - "adguardhome 安卓 root webui 3000"
  - "twoone3 adguard home root 下载"
  - "安卓 root 全局 dns 去广告"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "设备架构：arm64-v8a 或 armeabi-v7a"
  - "必须在系统网络设置中关闭 Android「私人 DNS」（设为关闭），防止 DoT 流量绕过 iptables 重定向"
conflicts:
  - "官方明确说明：与其他代理软件无已知冲突（可明确与 NekoBox、FlClash、Box for Magisk 及 akashaProxy 共存）"
  - "若开启系统内置 Android 私人 DNS（DoT），流量将绕过本地 DNS 服务"
configPaths:
  - "/data/adb/agh/settings.conf"
  - "/data/adb/agh/AdGuardHome.yaml"
  - "/data/adb/agh/bin/agh.pid"
  - "/data/adb/modules/AdGuardHome/"
features:
  - "原生本地 DNS 过滤：在设备本机直接运行官方 AdGuard Home，不占用 Android VPN 通道"
  - "内置 AWAvenue 广告过滤规则：预置轻量省电且低误杀率的移动端优化规则集"
  - "完整 Web 管理控制台：访问 http://127.0.0.1:3000 即可查看实时查询日志、切换上游 DNS 并管理自定义拦截列表"
  - "防断网启动保护：内置 120 秒监听超时机制，若守护进程启动失败则自动跳过 iptables 重定向，避免设备完全断网"
  - "多代理方案共存：支持与 FlClash、NekoBox 等第三方代理客户端同时运行"
faq:
  - question: "为什么必须关闭 Android 的「私人 DNS」设置？"
    answer: "Android 内置的私人 DNS 功能会通过 853 端口以加密 TLS（DoT）形式将 DNS 请求直连发送至上游服务商，从而完全绕过标准的 53 端口 UDP/TCP iptables 重定向链。将其设为「关闭」后，AdGuard Home 才能在本地顺利接管并过滤全部设备的域名查询。"
  - question: "Web 管理后台的默认登录凭据是什么？"
    answer: "首次访问 http://127.0.0.1:3000 管理面板时，默认的用户名和密码均为 root / root。"
---

## 概述

由 **twoone3** 维护的 **AdGuardHome for Root** 将桌面及服务端级别的 **AdGuard Home** DNS 过滤引擎完整移植到了已 Root 的 Android 设备上。

常规移动端去广告应用通常需要借助 Android `VpnService` 接口创建一个本地虚拟 VPN 隧道来截获 DNS 查询。这种方式不仅会带来额外耗电与网络延迟，还会独占系统唯一的 VPN 槽位，导致用户无法同时开启真正的 VPN 或代理客户端。AdGuardHome for Root 通过在本地运行原生编译的 AdGuard Home 守护进程，并配合 Linux `iptables` 规则重定向系统 DNS，彻底摆脱了上述限制。

---

## 技术架构与工作原理

### 独立 DNS 守护进程与防火墙重定向

AdGuardHome for Root 在 `/data/adb/agh/` 目录下构建了一套完全自洽的本地网络服务架构：

1. **原生二进制守护进程**：将官方编译的 ARM Linux 版 AdGuard Home 作为常驻后台服务运行，并由 `service.sh` 统一托管生命周期。
2. **Iptables 端口重定向**：当 `settings.conf` 中配置了 `enable_iptables=true` 时，模块会注入防火墙规则，将 53 端口（UDP 与 TCP）的所有出站 DNS 请求直接转发至 AdGuard Home 内部的 `5591` 监听端口。
3. **防回环与 GID 放行**：守护进程以专用的 `net_raw` 组 ID 身份运行，使其自身发往上游加密 DNS（如 Cloudflare 或 Quad9）的查询流量能够直接放行出站，避免陷入本地重定向死循环。
4. **防断网超时兜底**：开机阶段，`service.sh` 最多等待 120 秒以确认 DNS 守护进程已成功绑定监听套接字。若超时仍未就绪，脚本将自动跳过 iptables 规则写入，确保手机保持正常联网而不会出现全盘 DNS 失效。

---

## 安装与配置

### 1. 关闭私人 DNS
安装模块前，请确保已停用 Android 原生 DNS-over-TLS 客户端：
- 打开系统 **设置 > 网络和互联网 > 私人 DNS**。
- 选择 **关闭**。

### 2. 刷入模块
1. 从官方发布仓库下载最新版模块压缩包。
2. 在 Magisk、KernelSU 或 APatch 中刷入模块。
3. 重启设备。

### 3. 访问 Web 控制台
设备重启完成后，在任意手机浏览器中打开以下地址：
```text
http://127.0.0.1:3000
```
使用默认管理员账号密码登录：
- **用户名**：`root`
- **密码**：`root`

---

## 配置与日常使用

### 模块配置（`settings.conf`）

可在 `/data/adb/agh/settings.conf` 中按需调整守护进程参数：
- **禁用内置 Iptables 重定向**：若仅希望将 AdGuard Home 作为本地 DNS 服务器而不接管全局设备流量，可设置 `enable_iptables=false`。
- **屏蔽 IPv6 DNS**：设置 `block_ipv6_dns=true`，强制使 IPv6 DNS 查询回落并通过 IPv4 过滤规则解析。
- **绕过指定地址**：将特定 IP 地址添加至 `ignore_dest_list` 或 `ignore_src_list`，即可跳过 AdGuard Home 过滤。

### 过滤规则集
模块默认集成了 **AWAvenue-Ads-Rule**（秋风广告规则），这是一份针对移动端优化的轻量列表，内存占用极低且误杀率少。你也可以直接在 WebUI 的 `http://127.0.0.1:3000/#filters` 页面订阅更多社区拦截规则。

---

## 常见问题与排查

- **设备完全无法联网 / DNS 解析失败**：请确认系统设置中的「私人 DNS」已彻底关闭。若仍无法解析，可检查 `/data/adb/agh/bin/agh.pid` 确认守护进程是否存活，或查看 AdGuard Home 查询日志中的报错信息。
- **与其他 DNS 守护进程端口冲突**：若设备上已有其他模块或本地服务占用了 53 或 3000 端口，请前往 `/data/adb/agh/AdGuardHome.yaml` 修改其中的 `redir_port` 与 Web 绑定端口。
