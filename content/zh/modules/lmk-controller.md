---
id: "lmk-controller"
title: "LMK Controller：Android 内存压力与 LMK/LMKD 策略调控模块"
sidebarTitle: "LMK Controller"
description: "自动检测 Android 设备的 LMK 或 LMKD 节点路径，并通过 Magisk 或 KernelSU 应用可选的内存压力配置方案。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "LMK Controller Magisk 模块"
  - "ferrdishx LMK Controller 下载"
  - "Android LMKD 内存优化模块"
  - "低内存杀手调控 KernelSU"
  - "Android PSI LMKD 后台保活配置"
prerequisites:
  - "根据上游 README 说明，需 Android 8.0 及以上系统"
  - "Magisk 20.4 及以上版本，或 KernelSU"
  - "支持 WebUI 的兼容模块管理器（用于打开交互式控制面板）"
  - "在修改内存管理参数前准备救砖恢复方式与数据备份"
conflicts:
  - "会修改 LMK、LMKD、ZRAM、swappiness 或 VM 参数的其他模块或厂商脚本"
  - "未暴露上游文档所列检测路径的特殊内核变体"
configPaths:
  - "/data/adb/modules/lmk_controller_feerd/lmk_mode"
  - "/data/adb/lmk_controller/service.log"
  - "/data/adb/service.d/lmk_controller.sh"
features:
  - "自动识别经典 LMK、PSI LMKD 与传统 LMKD 三类检测路径"
  - "内置 Gamer（游戏）、Stable（稳定）与 Normal（默认）三档配置方案"
  - "持久化保存所选方案并在每次开机时自动重新应用"
  - "对支持的系统参数建立快照，卸载模块时自动恢复原始值"
  - "提供适配主流模块管理器的 WebUI 交互式控制台"
faq:
  - question: "该模块支持哪些 Root 方案？"
    answer: "上游 README 明确列出了 Magisk 20.4+ 与 KernelSU。由于上游指出其在 Kitsune Mask 下存在兼容性问题，因此本指南未将 Kitsune 列入支持列表。"
  - question: "模块具体会修改哪些系统参数？"
    answer: "根据检测到的内核路径与所选配置档位，模块可能调整经典 LMK 的 minfree 阈值、ro.lmk.* 属性、swappiness、VM 虚拟内存参数以及 ZRAM 压缩策略。具体数值会依据配置档位与设备物理内存大小动态适配。"
  - question: "如何确认设备实际命中的检测路径？"
    answer: "可查看 `/data/adb/lmk_controller/service.log` 中的开机或服务日志，并与文档记录的检测节点 `/sys/module/lowmemorykiller/parameters/minfree` 及 `/proc/pressure/memory` 进行对照。"
  - question: "如果应用更频繁重载或系统出现不稳定怎么办？"
    answer: "请切换回 Normal 模式或暂时禁用该模块并重启设备。排查并移除相互冲突的内存优化模块，在检查服务日志后再尝试其他档位。"
  - question: "必须使用 WebUI 才能工作吗？"
    answer: "模块可通过开机脚本自动应用已保存的配置，但上游安装说明建议使用 MMRL、KSU WebUI 或其他兼容管理器来进行交互式切换与控制。"
---

## 概述

LMK Controller 用于精细调控 Android 的内存回收压力机制，且并未假设单一配置能适用于所有设备。该版本可自动识别三种底层路径：

- 存在 `/sys/module/lowmemorykiller/parameters/minfree` 时，判定为 **经典 LMK（Classic LMK）**。
- 存在 `/proc/pressure/memory` 时，判定为 **PSI LMKD**。
- 以上两项节点均不存在时，回退至 **传统 LMKD（Legacy LMKD）**。

识别完成后，模块会应用用户选定的 Gamer、Stable 或 Normal 配置方案并记录诊断日志。其 v1.4.1 版本包含完整的路径探测与持久化逻辑、WebUI 控制面板以及针对支持参数的快照/还原机制。

## 安装步骤

1. 记录当前设备的内存表现，并做好异常恢复准备。
2. 从上游 Releases 页面下载 `LMK_Controller-v1.4.1.zip`。
3. 通过 Magisk、KernelSU、MMRL 或兼容模块管理器刷入模块。
4. 重启设备。
5. 打开模块对应的 WebUI 面板，选择目标配置方案并应用。

上游 README 明确要求 Android 8.0+、Magisk 20.4+ 或 KernelSU 环境；如需使用交互式控制界面，还需搭配支持 WebUI 的模块管理器。

## 状态验证

可通过以下命令检查服务日志与当前保存的模式：

```sh
su -c 'cat /data/adb/lmk_controller/service.log'
su -c 'cat /data/adb/modules/lmk_controller_feerd/lmk_mode'
```

上游 README 还提供了以下属性核查命令：

```sh
su -c 'getprop ro.lmk.low'
su -c 'getprop ro.lmk.medium'
su -c 'getprop ro.lmk.critical'
su -c 'getprop ro.lmk.psi_partial_stall_ms'
```

切勿直接套用其他机型的阈值并假定其安全可靠——该模块会根据检测到的内存容量与内核路径按比例缩放部分配置参数。

## 兼容性与恢复方法

LMK 与 LMKD 的实际表现高度依赖厂商定制与内核版本。同时启用其他内存、ZRAM、性能优化或游戏辅助模块可能会覆盖相同参数并增加排查难度。目前上游仍在调查 Kitsune Mask 的兼容性问题，因此暂不建议在该环境下使用。

如遇系统卡顿或异常，请在 WebUI 中切回 Normal 档位，或在 Root 管理器中禁用本模块后重启。若系统无法正常开机，请通过 Root 管理器的安全模式或兼容 Recovery 环境停用模块。上游版本内置了卸载清理逻辑，旨在移除自启服务项并还原快照记录的参数状态，但具体恢复流程仍取决于所用设备与 Root 方案。

## 参考来源

- [上游项目 README](https://github.com/ferrdishx/LMK-Controller)
- [上游发行版页面](https://github.com/ferrdishx/LMK-Controller/releases/tag/v1.4.1)
- [上游源码仓库](https://github.com/ferrdishx/LMK-Controller)
