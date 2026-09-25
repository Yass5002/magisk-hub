---
id: "dockerd"
title: "Docker Engine Daemon & CLI for Rooted ARM64 Android Devices"
sidebarTitle: "Docker Daemon (dockerd)"
description: "Deploys a native Docker daemon and container management CLI onto Android, backed by an automated init service and Unix socket runtime."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "dockerd magisk module"
  - "run docker on android root"
  - "mgksu dockerd"
  - "docker daemon kernelsu arm64"
  - "docker patched android kernel containers"
prerequisites:
  - "ARM64 (aarch64) device architecture"
  - "Root access via Magisk or KernelSU"
  - "Custom Linux kernel compiled with Docker prerequisites (cgroups v1/v2, namespaces, OverlayFS, Netfilter/iptables)"
conflicts: []
configPaths:
  - "/data/adb/docker/"
  - "/data/adb/docker/bin/"
  - "/data/adb/docker/run/docker.sock"
features:
  - "Automated boot service: spawns the native dockerd daemon during late boot using a dedicated service manager"
  - "Service lifecycle utility: provides dockerd.service helper script to start, stop, restart, or tail live container logs"
  - "Native CLI toolchain: packages static docker client binaries accessible directly inside Termux or ADB shells"
  - "Standard socket integration: listens on a local Unix socket at unix:///data/adb/docker/run/docker.sock"
---

## Overview

Running containerized microservices and developer environments directly on an Android handset turns mobile hardware into an ultra-low-power, portable Linux server. However, Android's stock kernel configuration lacks critical virtualization primitives—such as namespace separation, cgroup memory limits, and OverlayFS mount capabilities—and stock root distributions lack Docker daemon binaries.

Developed by mgksu, **dockerd** packages a complete, native Docker engine (`dockerd`) and command-line client (`docker`) formatted specifically for rooted ARM64 Android environments. Accompanied by a dedicated service control wrapper, the module manages container lifecycle states across device reboots without requiring a full Linux chroot.

## Hardware & Kernel Requirements

Container virtualization directly interfaces with Linux kernel primitives. Before installing this module, ensure your environment meets the following criteria:

- **CPU Architecture**: Strictly `arm64` (64-bit ARM). 32-bit (armv7) and x86_64 devices are unsupported.
- **Docker-Patched Kernel**: Android stock OEM kernels have essential container flags disabled. You must run a custom kernel compiled with:
  - Namespaces (`CONFIG_NAMESPACES`, `CONFIG_IPC_NS`, `CONFIG_PID_NS`, `CONFIG_NET_NS`, `CONFIG_UTS_NS`)
  - Control Groups (`CONFIG_CGROUPS`, `CONFIG_MEMCG`, `CONFIG_CGROUP_SCHED`)
  - File Systems (`CONFIG_OVERLAY_FS`)
  - Networking (`CONFIG_NETFILTER_XT_MATCH_ADDRTYPE`, `CONFIG_NETFILTER_XT_MATCH_CONNTRACK`, `CONFIG_IP_NF_FILTER`, `CONFIG_IP_NF_TARGET_MASQUERADE`)
  - *Tip*: You can evaluate your current kernel compatibility by running the upstream `check-config.sh` diagnostic script inside Termux.

## Environment Setup & PATH Configuration

The module deploys its binaries into `/data/adb/docker/bin` and manages its socket runtime in `/data/adb/docker/run/`. To make `docker` and management commands accessible from any interactive shell (such as Termux):

1. Open your shell profile (e.g., `~/.bashrc` or `~/.zshrc`) in Termux or root shell.
2. Add the following export declarations:
   ```bash
   export PATH=/data/adb/docker/bin:$PATH
   export DOCKER_HOST="unix:///data/adb/docker/run/docker.sock"
   ```
3. Source the updated profile:
   ```bash
   source ~/.bashrc
   ```

## Service Control (`dockerd.service`)

The module provides an init utility, `dockerd.service`, to supervise the background daemon without manually managing PID files:

- **Check Daemon Status & Logs**:
  ```bash
  su -c dockerd.service logs
  ```
- **Restart Docker**:
  ```bash
  su -c dockerd.service restart
  ```
- **Stop Daemon**:
  ```bash
  su -c dockerd.service stop
  ```
- **Start Daemon**:
  ```bash
  su -c dockerd.service start
  ```

## Running Containers

Once the service is active, standard Docker CLI commands operate as expected:

```bash
# Verify daemon connectivity
su -c docker info

# Pull and run a lightweight Alpine container
su -c docker run -it --rm alpine sh

# Host a local Nginx web server
su -c docker run -d -p 8080:80 --name webserver nginx:alpine
```

## Troubleshooting

- **Error: "Cannot connect to the Docker daemon"**: Check whether the daemon is active using `su -c dockerd.service logs`. If the daemon aborted during startup, verify that `DOCKER_HOST` is pointing to `unix:///data/adb/docker/run/docker.sock`.
- **OverlayFS or iptables Errors**: Inspect `dmesg` output. If `dockerd` logs show `overlayfs: filesystem not supported` or missing network tables, your kernel is missing required kernel config flags and must be recompiled.
