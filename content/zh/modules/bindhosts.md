---
id: "bindhosts"
title: "Bindhosts：高速无侵入式 Hosts 广告屏蔽引擎"
sidebarTitle: "Bindhosts"
description: "适用于 Android 的高性能无侵入式 hosts 重定向模块，将自定义广告过滤规则绑定挂载至 /system/etc/hosts 且零额外耗电。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "bindhosts magisk 模块下载"
  - "安卓 systemless hosts 去广告"
  - "已 root 安卓怎么去广告"
  - "adaway 替代品 magisk"
  - "bindhosts custom txt 白名单配置"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "可通过 Shell 或终端调用 Root 权限"
conflicts:
  - "旧版 Systemless Hosts 模块（Magisk 设置中自带选项）"
  - "同时安装的其他替换系统 hosts 的模块"
configPaths:
  - "/data/adb/bindhosts/custom.txt"
  - "/data/adb/bindhosts/whitelist.txt"
  - "/data/adb/bindhosts/sources.txt"
features:
  - "原生绑定挂载架构：零额外开销的直接 hosts 重定向，无需常驻后台 VPN 服务"
  - "多路精选上游拦截源（StevenBlack、AdGuard、OISD、GoodbyeAds）"
  - "提供本机 WebUI 与 CLI 命令行界面，支持一键即时更新规则（`su -c bindhosts -r`）"
  - "细粒度黑白名单支持，不会引发无限重启（Bootloop）或网络死锁"
faq:
  - question: "Bindhosts 会像基于 VPN 的去广告应用那样费电吗？"
    answer: "完全不额外耗电。VPN 类去广告软件（如 AdGuard 应用或个人 VPN 工具）需要在用户态运行本地 tun 虚拟网卡来逐包检查流量。而 Bindhosts 通过 /system/etc/hosts 直接工作在操作系统内核解析层面，被屏蔽的域名会毫秒级解析为 0.0.0.0，无需任何后台抓包解析开销。"
  - question: "如果某个应用因域名被拦截而异常，该如何加入白名单？"
    answer: "只需将误杀域名写入 /data/adb/bindhosts/whitelist.txt（每行一个域名），随后在 Termux 中执行 `su -c bindhosts -r` 即可立即重新编译并生效新的 hosts 文件。"
---

## 概述

由 **bindhosts** 开源团队维护的 **Bindhosts**，是已 Root Android 设备上传统 hosts 去广告工具的现代化继任者。

早期的 AdAway 等工具往往依赖复杂的本地 Web 服务或完整分区重挂载，而 Bindhosts 直接采用了 Linux 内核原生的绑定挂载（`mount --bind`）机制。它将数以百万计经过验证的广告、追踪器、遥测及恶意域名汇总编译为单一的 `/system/etc/hosts` 映射表，供 Android Bionic libc DNS 解析器在所有应用中原生调用。

---

## 技术架构与工作原理

### 无侵入式绑定挂载（Bind Mount）

1. **规则编译阶段**：Bindhosts 从高信誉度规则源（如 StevenBlack、OISD、1Hosts）拉取精选域名拦截列表。
2. **去重与清洗**：内置处理引擎自动对条目去重、剔除无效语法、合并来自 `custom.txt` 的用户自定义规则，并排除 `whitelist.txt` 中指定的放行域名。
3. **暂存文件生成**：编译完成的 hosts 文件最终写入 `/data/adb/bindhosts/hosts`。
4. **命名空间重定向**：在开机早期阶段（`post-fs-data.sh` 与 `service.sh`），Bindhosts 执行以下命令：
   ```bash
   mount --bind /data/adb/bindhosts/hosts /system/etc/hosts
   ```
5. **全局生效**：由于 Android DNS 解析器会在每次出站网络请求前读取 `/system/etc/hosts`，所有广告、追踪脚本与遥测请求都会以零 CPU 延迟直接解析失败。

---

## 安装与配置

1. 打开你的 Root 管理器（**Magisk**、**KernelSU** 或 **APatch**）。
2. 下载并刷入最新的 `bindhosts-vX.zip`。
3. 重启设备。
4. 打开终端应用（如 **Termux**）并执行初始化命令：
   ```bash
   su -c bindhosts -r
   ```
5. Bindhosts 将自动下载最新上游规则、完成合并并立即应用新的 hosts 文件，全程无需再次重启。

---

## 配置文件与自定义规则

所有配置文件均存放在 `/data/adb/bindhosts/` 目录：

- **`custom.txt`**：添加你想手动屏蔽的自定义域名：
  ```text
  0.0.0.0 telemetry.example.com
  0.0.0.0 ads.targetapp.com
  ```
- **`whitelist.txt`**：添加被误杀、需要放行的域名：
  ```text
  s.youtube.com
  login.live.com
  ```
- **通过命令行管理**：
  ```bash
  # 快速更新规则
  su -c bindhosts -r

  # 查看当前生效的 hosts 文件大小与规则条数
  su -c bindhosts -s

  # 临时停用广告屏蔽
  su -c bindhosts -d

  # 重新启用广告屏蔽
  su -c bindhosts -e
  ```
