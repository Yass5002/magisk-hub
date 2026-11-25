---
id: "honor-of-kings-120hz-unlocker"
title: "王者荣耀 120Hz 超高帧率解锁：iQOO 8 Pro 机型伪装模块"
sidebarTitle: "王者荣耀 120Hz 解锁"
description: "通过无侵入式伪装 iQOO 8 Pro 设备型号参数，解锁腾讯《王者荣耀》与《传说对决》（Arena of Valor）原生 120 FPS 极高帧率画质。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "王者荣耀 120 帧 Magisk 模块"
  - "Root 解锁传说对决 120Hz"
  - "iQOO 8 Pro 机型伪装 Magisk"
  - "V2141A system.prop 解锁高帧率"
prerequisites:
  - "Magisk 17.0+、KernelSU 或 APatch"
  - "设备屏幕本身支持 120Hz 物理刷新率"
conflicts:
  - "其他全局修改机型标识的伪装模块"
configPaths:
  - "/data/adb/modules/46793794/system.prop"
features:
  - "注入 vivo iQOO 8 Pro 旗舰机型特征标识（型号 V2141A）"
  - "解锁游戏画面设置中的原生“极高”120 FPS 帧率开关"
  - "打破《王者荣耀》与《传说对决》针对未适配机型的 60 FPS 软件锁帧限制"
  - "仅 2.5 KB 极简体积，无任何后台常驻服务，零额外电量消耗"
faq:
  - question: "刷入后能否保证游戏全程稳跑 120 FPS？"
    answer: "本模块的作用是解锁游戏设置菜单中的 120 FPS 软件开关。实际对局中的帧率稳定性取决于你设备自身的 GPU 性能与散热表现。"
---

## 概述

**王者荣耀 120Hz 超高帧率解锁**（由“YouLinw 的 ROM 日常”制作）可为腾讯旗舰 MOBA 手游解锁原生的 120 FPS 高帧率显示选项。

---

## 技术架构与工作原理

该模块通过 `system.prop` 注入官方合作适配机型的设备属性：

```properties
ro.product.manufacturer=vivo
ro.product.brand=vivo
ro.product.model=V2141A
```

游戏引擎在启动初始化阶段会读取 `Build.MODEL` 系统属性；当检测到设备为 iQOO 8 Pro（`V2141A`）时，便会自动开放游戏内的 120 FPS 超高帧率档位。
