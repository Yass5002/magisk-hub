---
id: "freezeit-background-optimizer"
title: "FreezeIt 后台应用优化器：内核级墓碑进程冻结"
sidebarTitle: "FreezeIt 墓碑冻结"
description: "基于 Linux 内核 cgroups 与进程 Freezer 子系统的智能后台冻结守护进程，彻底消除待机后台耗电与进程唤醒锁（Wakelock）。"
category: "battery-power-charging"
tier: 1
searchQueries:
  - "FreezeIt 墓碑 Magisk 模块"
  - "Android Root 后台冻结墓碑"
  - "Linux cgroups freezer 安卓墓碑"
  - "Root 彻底解决后台应用耗电"
prerequisites:
  - "支持 cgroups 与 freezer 子系统的内核（Android 8 及以上）"
  - "Magisk 20.4+、KernelSU 或 APatch"
conflicts:
  - "与会发送冲突性 `SIGSTOP` 信号的其他激进后台查杀工具存在冲突"
configPaths:
  - "/data/adb/modules/freezeit/freezeit.conf"
  - "/data/adb/modules/freezeit/whitelist.txt"
  - "/sys/fs/cgroup/freezer/"
features:
  - "利用 Linux cgroup freezer 子系统暂停后台进程，无需强行杀掉进程"
  - "完整保留应用内存运行状态，切回前台时实现零卡顿秒级恢复"
  - "强力遏制后台唤醒锁（Wakelock）、定时唤醒闹钟与静默耗电行为"
  - "内置智能白名单机制，自动保护即时通讯应用、下载管理器与 Root 守护进程"
faq:
  - question: "冻结（墓碑）后台与直接杀掉后台进程有什么区别？"
    answer: "杀掉应用会清空其内存，下次打开时不得不触发高 CPU 占用的冷启动。而冻结是通过内核 cgroups 将进程置于 `FROZEN` 状态并保留在内存中：待机时消耗 0% CPU 与电量，点击切回时可立即无缝恢复运行。"
  - question: "开启冻结后会漏接聊天软件的即时推送消息吗？"
    answer: "主流即时通讯服务（如 WhatsApp、Telegram、微信）默认已加入白名单。你也可以将任何需要保持常驻的应用包名添加到 `/data/adb/modules/freezeit/whitelist.txt` 中予以豁免。"
---

## 概述

**FreezeIt 后台应用优化器**（作者：JARK006）是一款高性能无系统分区修改（Systemless）电池优化守护进程，专为解决现代 Android 设备的待机后台耗电问题而打造。

现代移动应用往往会在后台拉起大量服务、消息推送监听、统计分析守护进程及轮询任务，导致 CPU 长期处于唤醒状态（Wakelock）。虽然原生 Android Doze 机制能起到一定抑制作用，但许多应用会通过注册高优先级 JobScheduler 绕过限制。FreezeIt 直接在内核层面出手，将非必要后台进程移入 Linux `freezer` 控制组（cgroup）彻底冻结。

---

## 技术架构与工作原理

FreezeIt 依托 Linux 内核控制组（`cgroups`）中的 Freezer 冻结子系统（`CONFIG_CGROUP_FREEZER`）工作：

### 1. 进程状态管理

当应用从前台切换至后台时：

```text
Foreground Activity -> App Minimized -> Grace Period (e.g. 30s) -> Kernel Freeze
```

守护进程会将目标应用的进程 ID（PID）写入 cgroup freezer 控制节点：

```bash
echo $PID > /sys/fs/cgroup/freezer/freezeit/cgroup.procs
echo "FROZEN" > /sys/fs/cgroup/freezer/freezeit/freezer.state
```

处于 `FROZEN` 状态时：
- Linux 内核调度器会直接跳过该任务所属的所有线程。
- 进程不执行任何 CPU 指令，耗电归零。
- 进程数据依然驻留在 RAM 内存中，用户切回时不会发生重载与磁盘 I/O 冷启动开销。

### 2. 唤醒与前台切回握手

当用户重新切换回该应用，或系统下发高优先级系统广播时：

```bash
echo "THAWED" > /sys/fs/cgroup/freezer/freezeit/freezer.state
```

进程内的所有线程会立即从此前暂停的 CPU 指令指针位置恢复执行，全程零延迟。

---

## 配置与白名单管理

你可以通过编辑模块本地配置文件自定义运行策略：

```bash
# Whitelist path
/data/adb/modules/freezeit/whitelist.txt
```

在白名单文件中按行填入需要保持后台常驻的应用包名即可：

```text
com.whatsapp
org.telegram.messenger
com.google.android.gms
```
