---
id: "wadbd"
title: "Wireless ADB Controller (wadbd)：持久化无线调试、密钥管理与 WebUI 控制中心"
sidebarTitle: "Wireless ADB Controller (wadbd)"
description: "通过命令行或 WebUI 全面控制 Android 无线 ADB 守护进程，支持开机持久化监听、自定义网络端口以及 ADB 加密公钥批量导入导出。"
category: "system-utilities"
tier: 1
searchQueries:
  - "Wireless ADB Controller Magisk 模块"
  - "rhythmcache wadbd 下载"
  - "Android Root 持久化无线 ADB 调试"
  - "wadbd 开机自动开启 5555 端口"
  - "Root 导入 adbkey.pub 免弹窗授权"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "Android 设备已连接至局域网 Wi-Fi 或热点"
  - "终端模拟器（如 Termux）或支持 WebUI 的 Root 管理器"
conflicts: []
configPaths:
  - "/data/adb/modules/wadbd/"
features:
  - "即时开关与开机持久化控制：一键启停当前会话的无线 ADB，或配置系统重启后自动在后台拉起调试服务"
  - "自定义网络端口绑定：支持指定任意监听端口（默认为 5555），有效避免局域网端口冲突"
  - "预授权密钥管理：直接向设备导入 `adbkey.pub` 公钥，无需屏幕弹窗确认即可让开发主机静默认证连接"
  - "凭证安全维护工具：单条命令即可完成所有已授权 ADB 加密密钥的备份、恢复与彻底清空"
  - "WebUI 可视化面板：原生适配 KernelSU、APatch 与 MMRL 的触控仪表盘"
---

## 概述

虽然 Android 系统的“开发者选项”原生提供了无线调试功能，但系统默认实现会在每次断开连接后重置端口，并在设备重启后自动关闭服务。对于移动应用开发者、测试工程师及自动化测试集群而言，每天反复手动开关设置与重新配对极度低效。

由 rhythmcache 开发的 **Wireless ADB Controller（wadbd）** 为 Android 原生 `adbd` 服务提供了持久化、可编程的控制方案。借助统一的命令行工具（`wadbd`）与直观的 WebUI 界面，用户可将无线 ADB 固定至默认或自定义端口，通过预置公钥免弹窗静默授权开发机，并实现跨重启的自动化调试就绪状态。

## 命令行用法

打开 Termux 或 ADB Root Shell，使用超级用户权限调用 `wadbd`（`su -c wadbd <subcommand>`）：

### 守护进程控制
```bash
# 在默认端口（5555）启动无线 ADB
su -c wadbd on

# 在自定义端口启动无线 ADB
su -c wadbd on 5556

# 停止无线 ADB 守护进程
su -c wadbd off

# 查看当前运行状态、局域网 IP 地址与监听端口
su -c wadbd status
```

### 开机自启配置
```bash
# 配置设备开机时自动在 5555 端口启用无线 ADB
su -c wadbd enable-on-boot

# 配置开机自启并指定监听端口
su -c wadbd enable-on-boot 5556

# 取消开机自动启动无线 ADB
su -c wadbd disable-on-boot
```

### ADB 密钥与认证管理
标准无线调试在首次连接时需要在手机屏幕上点击“一律允许使用这台计算机进行调试”。`wadbd` 支持直接写入公钥完成静默授权：

```bash
# 从存储导入开发机生成的公钥（adbkey.pub）
su -c wadbd --import-key /sdcard/Download/adbkey.pub

# 将当前所有已授权 ADB 密钥备份至本地存储
su -c wadbd --backup /sdcard/Download/adb_keys_backup

# 从历史备份文件恢复 ADB 授权密钥
su -c wadbd --restore /sdcard/Download/adb_keys_backup

# 吊销并清除设备端存储的所有已授权密钥
su -c wadbd --clear-keys
```

## 图形界面（WebUI）

在运行 **KernelSU**、**APatch** 或 **MMRL** 的设备上，`wadbd` 提供了专为触控优化的 WebUI 控制中心：
- 单击开关即可快速启停无线 ADB 服务。
- 实时查看设备当前局域网 IP 地址与占用端口信息。
- 无需记忆终端指令即可一键管理开机自启状态。

## 安装与配置

1. 在 Magisk、KernelSU 或 APatch 中刷入 `wadbd` 的 `.zip` 模块包。
2. 重启设备。
3. 打开 Termux 并通过 `su` 获取 Root 权限后执行 `wadbd on`，或直接在 Root 管理器内打开模块的 WebUI 面板。
4. 在开发电脑终端中直接发起连接：
   ```bash
   adb connect <device-ip>:5555
   ```

## 安全最佳实践

> [!IMPORTANT]
> 开启无线 ADB 会在局域网内开放一个网络监听端口。当设备接入咖啡厅、机场等不可信的公共 Wi-Fi 网络时，请务必执行 `su -c wadbd off` 关闭无线调试或切换为非标准端口，以防遭到局域网恶意扫描与未授权访问。
