---
id: "sqlite3-magisk-module"
title: "SQLite3 多架构二进制：面向已 Root Android 与模拟器的静态数据库命令行工具"
sidebarTitle: "SQLite3 CLI"
description: "将经过剥离符号且静态链接的 sqlite3 二进制文件部署到 `/system/xbin/`，支持在 ARM、ARM64、x86 与 x86_64 环境下直接通过命令行检查数据库。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "sqlite3 Magisk 模块"
  - "rojenzaman sqlite3"
  - "Android Root sqlite3 命令行"
  - "Waydroid 雷电模拟器 sqlite3 静态包"
  - "Termux Root 查看 Android sqlite 数据库"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
  - "兼容的 CPU 架构：`arm64-v8a`、`armeabi-v7a`、`x86` 或 `x86_64`"
  - "终端模拟器（Termux）或 ADB Shell 环境"
conflicts: []
configPaths:
  - "/data/adb/modules/sqlite3/"
  - "/system/xbin/sqlite3"
features:
  - "全架构交叉编译：内置适用于 32 位 / 64 位 ARM 及 x86 架构的预编译静态链接二进制文件"
  - "零依赖占用：编译时不依赖共享 C 运行库，确保在各种 Android libc/bionic 版本上稳定运行"
  - "广泛环境验证：已在多款物理手机平板及模拟容器（Waydroid、LDPlayer 9）上通过实测验证"
  - "无缝 Shell 集成：将二进制文件挂载覆盖至 `/system/xbin/`，刷入重启后即可在全局终端直接调用"
faq: []
---

## 概述

绝大多数 Android 系统服务、核心数据提供器以及第三方应用程序都将结构化的持久化状态保存在 SQLite 数据库中（位于 `/data/data/<package>/databases/` 下的 `.db` 文件）。无论是通话记录、短信存档，还是 Wi-Fi 凭据与应用偏好设置，查看或修复这些数据库记录都是系统管理员、安全审计人员和自动化脚本作者的基础操作。

然而，Google 早在多年前就从正式版 Android 系统镜像中移除了独立的 `sqlite3` 命令行可执行文件。开发者在尝试通过 ADB 或 Termux 执行数据库查询时，往往会遇到 `sqlite3: inaccessible or not found` 报错。

由 Rojen Zaman 打造的 **SQLite3 for Android** 是一款轻量级无系统分区修改（Systemless）模块，旨在为 **arm64-v8a**、**armeabi-v7a**、**x86** 与 **x86_64** 架构设备重新补全经过优化的静态链接 `sqlite3` 命令行工具。

## 多架构兼容性

不同于直接从开发测试版模拟器镜像中提取的基础二进制文件，本模块采用了由 Jacopo Tediosi 维护的静态编译脚本构建。由于可执行文件经过完整的符号剥离（Stripped）且与标准 C 运行库静态链接，因此在较老版本或非标准定制的 Android 系统上也不会出现动态链接器符号报错。

### 已验证硬件与虚拟环境：
- **arm64-v8a**：物理智能手机与平板电脑（已在 Lenovo Tab M10 Plus Gen 3、小米 6、Samsung Galaxy S6 Edge 上测试通过）。
- **armeabi-v7a**：早期 32 位 ARM 架构移动设备。
- **x86 / x86_64**：Android 模拟平台、虚拟机及容器环境（已在 Linux 下的 **Waydroid** 与 PC 端的 **LDPlayer 9** 上测试通过）。

## 安装与验证

1. 从 GitHub Releases 页面下载 `SQLite-for-magisk.multi-arch.zip` 压缩包。
2. 使用 **Magisk**、**KernelSU** 或 **APatch** 刷入该模块。
   - 安装脚本会自动识别你的 CPU 架构，并将对应的二进制文件软链接至 `/system/xbin/sqlite3`。
3. 重启设备。
4. 打开 Termux 或连接 `adb shell`，获取 Root 权限并验证程序是否正常运行：
   ```bash
   su -c sqlite3 --version
   ```
   命令执行后应返回所编译的 SQLite 版本号。

## 常用数据库管理命令

安装完成后，即可直接从命令行查询或修改 Android 数据库：

### 查询系统设置
```bash
# Query global Android system settings table
su -c sqlite3 /data/system/users/0/settings_global.db "SELECT name, value FROM global WHERE name LIKE '%adb%';"
```

### 检查应用数据库
```bash
# Open an interactive SQLite session with an app database
su -c sqlite3 /data/data/com.example.app/databases/app_data.db

# Inside the SQLite prompt:
.tables
.schema user_profiles
SELECT * FROM user_profiles LIMIT 5;
.quit
```

### 执行自动化脚本维护
```bash
# Execute WAL checkpointing and database vacuuming
su -c sqlite3 /data/data/com.example.app/databases/cache.db "PRAGMA wal_checkpoint(TRUNCATE); VACUUM;"
```

## 故障排查

- **打开数据库提示“Permission denied”**：位于 `/data/data/` 下的数据库受 SELinux 与 UNIX 文件权限严格保护，请务必在 Root Shell（`su`）权限下执行 `sqlite3`。
- **二进制架构不匹配**：若在非常规模拟器上运行并遇到 `cannot execute binary file: Exec format error` 报错，请通过 `uname -m` 检查内核架构，确认安装脚本选用了正确的二进制版本。
