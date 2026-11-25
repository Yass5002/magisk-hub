---
id: "tcp-optimiser-module"
title: "TCP Optimiser Module：动态网络拥塞控制与队列调度管理"
sidebarTitle: "TCP Optimiser"
description: "由 fatalcoder524 开发的网络优化模块，可根据当前活跃的 Wi-Fi 与蜂窝移动网络接口动态切换 TCP 拥塞算法（BBR、Cubic）及队列调度规则。"
category: "networking-proxies"
tier: 1
searchQueries:
  - "TCP Optimiser Module Magisk"
  - "fatalcoder524 TCP_Optimiser_Module 下载"
  - "Android Wi-Fi BBR 蜂窝 Cubic 自动切换"
  - "Android TCP 拥塞控制算法 WebUI"
  - "initcwnd initrwnd Magisk 优化模块"
prerequisites:
  - "运行 Magisk、KernelSU 或 APatch 的已 Root Android 设备"
  - "设备内核已编译支持目标 TCP 拥塞算法（例如在内核配置中启用了 BBR）"
conflicts: []
configPaths:
  - "/data/adb/modules/tcp_optimiser/"
  - "/data/adb/modules/tcp_optimiser/service.log"
features:
  - "感知接口的拥塞算法切换：在 Wi-Fi（`wlan0`）与移动数据（`rmnet_data0`）之间切换时自动应用最优算法"
  - "Wi-Fi 用 BBR、移动网络用 Cubic：在稳定的 Wi-Fi 环境下借助 BBR 榨取最大无限制吞吐量，同时在蜂窝链路上避免 BBR 因丢包带来的惩罚"
  - "可定制队列调度器（qdisc）：支持按接口配置 `fq`、`fq_codel` 或 `pfifo_fast` 数据包调度器"
  - "TCP 窗口最大化：可选配置将初始拥塞窗口（`initcwnd`）与初始接收窗口（`initrwnd`）调至最大值"
  - "双控制方式：支持通过简洁的文件系统命名约定或交互式模块 WebUI 调整参数"
faq: []
---

## 概述

由 fatalcoder524 开发的 **TCP Optimiser Module** 通过依据设备当前活跃的网络接口动态切换 TCP 拥塞控制算法与队列调度规则（qdisc），从而全面优化 Android 网络传输表现。

现代移动端内核大多已集成 Google 的 BBR（Bottleneck Bandwidth and RTT）算法。虽然在稳定的 Wi-Fi 连接下，BBR 相比传统 Cubic 往往能带来可观的吞吐量提升（上传速率常可高出 50–60 Mbps），但在无线信号波动频繁且存在瞬时丢包的蜂窝移动网络中，BBR 反而容易引发意料之外的延迟惩罚。TCP Optimiser 通过实时监听网络接口切换，自动对 Wi-Fi 应用 BBR、对移动数据应用 Cubic，兼顾两种网络场景下的最佳性能。

## 前置要求与兼容性

- **Root 方案**：兼容 Magisk、KernelSU 与 APatch。
- **内核要求**：设备内核必须已将目标 TCP 拥塞算法编译进内核（如 `CONFIG_TCP_CONG_BBR`、`CONFIG_TCP_CONG_CUBIC` 等）。若指定算法未在内核中编译启用，模块将平滑回退至系统默认算法。

目前暂无已知的模块冲突记录。

## 配置与调优

TCP Optimiser 可通过专用 WebUI 进行配置，也可直接修改以下目录中的文件描述符进行控制：
```bash
/data/adb/modules/tcp_optimiser/
```

### 通过文件描述符调优

模块会在其目录中生成两个接口模板文件：
- `wlan_{algo}_{qdisc}`：控制 Wi-Fi 接口策略。
- `rmnet_data_{algo}_{qdisc}`：控制蜂窝移动数据接口策略。

修改当前生效配置的方法如下：
1. **更改拥塞算法**：重命名文件名中的 `{algo}` 字段（例如将 `wlan_cubic_fq` 改为 `wlan_bbr_fq`）。可选值包括 `bbr`、`cubic`、`westwood`、`reno`，以及 `/proc/sys/net/ipv4/tcp_available_congestion_control` 中列出的任意内核已支持算法。
2. **更改队列调度器（qdisc）**：将 `{qdisc}` 字段重命名为你偏好的数据包调度器（例如 `fq`、`fq_codel`、`pfifo_fast`）。
3. **最大化初始窗口**：在模块目录内新建一个名为 `initcwnd_initrwnd` 的空文件，即可将初始拥塞窗口与初始接收窗口设为最大值。
4. **立即生效**：在模块目录内新建一个名为 `force_apply` 的空文件，无需重启即可立即应用修改后的配置。
5. **重置现有连接（谨慎使用）**：如果希望在网络接口切换时强制断开现有 TCP 套接字连接，可新建名为 `kill_connections` 的空文件（默认关闭，以免中断后台下载任务）。

### 通过 WebUI 调优

如果你偏好图形化操作界面：
- 通过 KernelSU 或 APatch 管理器打开 WebUI（Magisk 用户可使用 KSUWebUIStandalone）。
- 在界面中使用滑块和下拉菜单分别调整蜂窝网络与 Wi-Fi 的配置策略。

## 故障排查与验证

- **验证当前生效的算法**：检查系统当前网络正在使用的拥塞控制算法：
  ```bash
  su -c sysctl net.ipv4.tcp_congestion_control
  ```
- **查看模块执行日志**：
  ```bash
  cat /data/adb/modules/tcp_optimiser/service.log
  ```
- **指定的算法未生效**：若目标算法未能成功启用，请检查 `/proc/sys/net/ipv4/tcp_available_congestion_control` 的输出，确认你当前的设备内核是否确实编译了该算法模块。
