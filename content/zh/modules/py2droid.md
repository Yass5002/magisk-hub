---
id: "py2droid"
title: "Py2Droid：适用于 Android Root 环境的独立原生 Python 3 运行时"
sidebarTitle: "Py2Droid"
description: "以无系统分区修改（Systemless）方式在 Android 上安装自带 pip 支持的完整独立 Python 3 运行时，无需依赖 Termux 或 Linux chroot 环境。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "py2droid Magisk 模块"
  - "Mrakorez py2droid"
  - "Android Root Python 3 模块"
  - "KernelSU APatch 安装 Python pip"
  - "Android 独立全局 Python 环境"
prerequisites:
  - "通过 Magisk、KernelSU 或 APatch 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/py2droid/"
features:
  - "原生 Python 3 解释器：安装预编译的现代 Python 3.14+ 二进制文件，直接链接至 Android Bionic libc"
  - "内置 pip 包管理：可直接在命令行中安装并管理 Python Wheel 与纯 Python 第三方库"
  - "零外部依赖：独立运行，无需安装 Termux、PRoot 或完整的 Linux chroot 容器"
  - "无侵入 PATH 链接：将 `python3` 与 `pip` 以 Systemless 方式软链接至标准可执行路径 `/system/bin`"
  - "跨框架架构兼容：专为 Magisk、KernelSU 与 APatch 无缝协作而设计"
faq: []
---

## 概述

在 Android 设备上运行 Python 自动化脚本、遥测采集工具、网络爬虫或系统管理守护程序，传统上需要安装 Termux 或搭建完整的 Linux PRoot 容器。这些方案虽能胜任，但均运行在独立的应用沙盒之内，不仅需要手动授予文件访问权限，还必须额外维护后台保活机制以防进程被杀。

由 Mrakorez 开发的 **Py2Droid** 是一款无系统分区修改（Systemless）的 Root 模块，能够将原生的 Python 3 运行时直接部署到 Android 系统 Root 环境中。它会在任意 Root Shell、ADB 控制台以及开机自启脚本中全局暴露 `python3` 和 `pip` 命令。

## 核心能力

- **基于 Bionic 链接的原生二进制**：不同于运行在 PRoot 容器内的 glibc 版 Python 发行版，Py2Droid 专门针对 Android 的 Bionic C 运行库编译，具备极快的启动速度与极低的内存占用。
- **开箱即用的 pip 依赖安装**：内置 pip 包管理器，可直接安装各类自动化与开发库（如 `requests`、`beautifulsoup4`、`schedule`、`flask`）：
  ```bash
  su -c pip install requests
  ```
- **直接访问硬件与 Root Shell**：通过 Py2Droid 执行的 Python 脚本天然拥有原生 Root 权限，可直接读写 sysfs 节点、调用 Toybox 命令并与 Android 系统服务直接交互。

## 安装与验证

1. 从 GitHub Releases 下载最新的 `py2droid-v*.zip` 模块包。
2. 通过 **Magisk**、**KernelSU** 或 **APatch** 刷入该模块。
3. 重启设备。
4. 打开任意终端应用（如 Termux）或连接 `adb shell`，获取 Root 权限后验证解释器是否生效：
   ```bash
   su
   python3 --version
   ```
