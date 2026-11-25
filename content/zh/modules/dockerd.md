---
id: "dockerd"
title: "Docker Engine 守护进程与 CLI：面向已 Root ARM64 Android 设备的容器方案"
sidebarTitle: "Docker 守护进程 (dockerd)"
description: "在 Android 系统上部署原生 Docker 守护进程与容器管理命令行工具，并配备自动化启动服务及 Unix Socket 运行时。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "dockerd Magisk 模块"
  - "Android Root 原生运行 Docker"
  - "mgksu dockerd"
  - "KernelSU ARM64 Docker 守护进程"
  - "Docker 定制内核 Android 容器"
prerequisites:
  - "ARM64 (aarch64) 架构设备"
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "已开启 Docker 所需特性编译的定制 Linux 内核（cgroups v1/v2、namespaces、OverlayFS、Netfilter/iptables）"
conflicts: []
configPaths:
  - "/data/adb/docker/"
  - "/data/adb/docker/bin/"
  - "/data/adb/docker/run/docker.sock"
features:
  - "开机自启服务：通过专用服务管理器在系统启动后期自动拉起原生 `dockerd` 守护进程"
  - "生命周期控制工具：提供 `dockerd.service` 辅助脚本，支持启动、停止、重启与实时查看容器日志"
  - "原生 CLI 工具链：内置静态编译的 `docker` 客户端程序，可直接在 Termux 或 ADB Shell 中调用"
  - "标准 Socket 集成：监听本地 Unix Socket 路径 `unix:///data/adb/docker/run/docker.sock`"
faq: []
---

## 概述

直接在 Android 手机上运行容器化微服务和开发环境，能够将移动硬件转变为一台超低功耗的便携式 Linux 服务器。然而，Android 原厂内核配置通常缺少关键的虚拟化底层能力（例如命名空间隔离、cgroup 内存限制及 OverlayFS 挂载支持），同时系统默认环境也未包含 Docker 守护程序。

由 mgksu 开发的 **dockerd** 专为已 Root 的 ARM64 Android 环境打包了完整的原生 Docker 引擎（`dockerd`）和命令行客户端（`docker`）。配合专用的服务控制脚本，该模块无需完整的 Linux chroot 环境即可在设备重启间可靠管理容器生命周期。

## 硬件与内核要求

容器虚拟化需要直接调用 Linux 内核原语。安装本模块前，请务必确认你的设备环境满足以下条件：

- **CPU 架构**：严格限制为 `arm64`（64 位 ARM）。不支持 32 位（armv7）与 x86_64 设备。
- **支持 Docker 的定制内核**：Android 厂商原厂内核默认禁用了容器所需的关键编译选项。你必须刷入包含以下配置的定制内核：
  - 命名空间（`CONFIG_NAMESPACES`、`CONFIG_IPC_NS`、`CONFIG_PID_NS`、`CONFIG_NET_NS`、`CONFIG_UTS_NS`）
  - 控制组（`CONFIG_CGROUPS`、`CONFIG_MEMCG`、`CONFIG_CGROUP_SCHED`）
  - 文件系统（`CONFIG_OVERLAY_FS`）
  - 网络转发与防火墙（`CONFIG_NETFILTER_XT_MATCH_ADDRTYPE`、`CONFIG_NETFILTER_XT_MATCH_CONNTRACK`、`CONFIG_IP_NF_FILTER`、`CONFIG_IP_NF_TARGET_MASQUERADE`）
  - *提示*：你可以在 Termux 中运行上游提供的 `check-config.sh` 诊断脚本，以检测当前内核的兼容性。

## 环境配置与 PATH 设置

模块会将可执行文件部署至 `/data/adb/docker/bin`，并在 `/data/adb/docker/run/` 下管理运行时 Socket。若想在任意交互式 Shell（如 Termux）中直接调用 `docker` 及管理命令：

1. 在 Termux 或 Root Shell 中打开你的 Shell 配置文件（例如 `~/.bashrc` 或 `~/.zshrc`）。
2. 添加以下环境变量导出声明：
   ```bash
   export PATH=/data/adb/docker/bin:$PATH
   export DOCKER_HOST="unix:///data/adb/docker/run/docker.sock"
   ```
3. 重新加载配置文件使其生效：
   ```bash
   source ~/.bashrc
   ```

## 服务控制（`dockerd.service`）

模块内置了初始化管理工具 `dockerd.service`，用于托管后台守护进程而无需手动管理 PID 文件：

- **查看守护进程状态与日志**：
  ```bash
  su -c dockerd.service logs
  ```
- **重启 Docker 服务**：
  ```bash
  su -c dockerd.service restart
  ```
- **停止守护进程**：
  ```bash
  su -c dockerd.service stop
  ```
- **启动守护进程**：
  ```bash
  su -c dockerd.service start
  ```

## 运行容器

服务启动后，即可按标准方式执行各类 Docker CLI 命令：

```bash
# Verify daemon connectivity
su -c docker info

# Pull and run a lightweight Alpine container
su -c docker run -it --rm alpine sh

# Host a local Nginx web server
su -c docker run -d -p 8080:80 --name webserver nginx:alpine
```

## 故障排查

- **报错“Cannot connect to the Docker daemon”**：使用 `su -c dockerd.service logs` 检查守护进程是否处于运行状态。若启动阶段异常退出，请核对 `DOCKER_HOST` 是否正确指向 `unix:///data/adb/docker/run/docker.sock`。
- **OverlayFS 或 iptables 报错**：请检查 `dmesg` 内核日志。如果 `dockerd` 输出 `overlayfs: filesystem not supported` 或缺失网络表项，说明当前内核缺少必要的编译选项，需要重新编译内核启用对应功能。
