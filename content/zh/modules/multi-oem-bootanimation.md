---
id: "multi-oem-bootanimation"
title: "Multi-OEM Dynamic Boot Animation：支持防卡米保护的自定义开机动画引擎"
sidebarTitle: "多品牌随机开机动画"
description: "面向小米 MIUI/HyperOS、OPPO ColorOS、Realme UI 等系统的无侵入式开机动画定制引擎，内置每次开机随机切换动画及 60 秒自动防卡死看门狗。"
category: "boot-animations-ui"
tier: 1
searchQueries:
  - "开机动画 Magisk 模块"
  - "MIUI 自定义开机动画"
  - "ColorOS 开机动画替换"
  - "开机动画看门狗防变砖"
prerequisites:
  - "Magisk 20.4+、KernelSU 或 APatch"
  - "运行 MIUI/HyperOS、ColorOS、Realme UI 或 AOSP 的设备"
conflicts:
  - "其他目标路径为 /system/media/bootanimation.zip 的开机动画替换模块"
configPaths:
  - "/data/adb/modules/bootanimation/random_animation.sh"
  - "/data/adb/modules/bootanimation/service.sh"
  - "/data/adb/modules/bootanimation/bootanimation.zip"
features:
  - "在不修改物理 system 或 product 分区的前提下替换厂商开机动画"
  - "兼容 MIUI、ColorOS 与 Realme UI 所使用的复杂多阶段开机动画结构"
  - "内置动态随机脚本（random_animation.sh），每次开机自动切换不同动画序列"
  - "集成 60 秒 init 看门狗，遇到损坏的动画压缩包时自动规避 Bootloop"
  - "支持自主卸载机制（umount.sh），开机异常时无需人工干预即可自动剥离挂载"
faq:
  - question: "如果放入的自定义 bootanimation.zip 损坏或格式无效会怎样？"
    answer: "内置的 service 看门狗会持续监测 init.svc.bootanim 属性。若动画守护进程连续运行超过 60 秒（这是系统无法顺利过渡到 SurfaceFlinger/SystemUI 的典型标志），脚本会自动写入 disable 禁用标记，触发 umount.sh 卸载异常动画并安全重启设备。"
  - question: "如何添加多个开机动画供随机引擎轮换？"
    answer: "将其他开机动画 ZIP 文件直接放入模块目录（/data/adb/modules/bootanimation/）即可。每次关机或重启周期中，random_animation.sh 脚本都会随机抽取一个文件，为下一次开机做好准备。"
---

## 概述

**Multi-OEM Dynamic Boot Animation**（由 Stinky Panda 开发）为多款主流定制系统提供了一套稳定可靠的无侵入式开机动画框架，覆盖小米（MIUI/HyperOS）、OPPO（ColorOS）、真我（Realme UI）以及通用 AOSP 固件。

长期以来，刷入自定义开机动画一直是玩机用户遭遇 Bootloop 的常见诱因之一。帧尺寸不匹配、错误的图像压缩方式（使用了常规 Deflate 压缩而非仅存储模式）或 `desc.txt` 末尾缺少换行符，都会导致 Android 原生 `bootanimation` 程序崩溃或陷入无限循环。

Multi-OEM Dynamic Boot Animation 通过为动画加载过程包裹一层自主健康检查看门狗，从机制上消除了这类风险——看门狗会实时监测启动耗时，一旦发现异常立即卸载覆盖层。

---

## 技术架构与工作原理

该模块由三个协同工作的组件构成：

### 1. 多阶段动画覆盖挂载

Android 会按优先级从以下位置加载开机动画：
1. `/product/media/bootanimation.zip`
2. `/system/media/bootanimation.zip`

模块会在上述路径建立无侵入式（Systemless）挂载，注入包含完整阶段目录（`part0`、`part1` 等）且符合硬件解码器要求的无压缩格式（`zip -0`）动画包。

### 2. 启动看门狗（service.sh）

模块的 `late_start service` 守护脚本会监测核心 Android init 系统属性：

```bash
sleep 60
if [[ "`getprop init.svc.bootanim`" = "running" ]]; then
    # Boot animation is still looping after 60 seconds -> potential hang
    echo > $MODDIR/disable
    sh $MODDIR/umount.sh
    echo "Device startup failure detected. Module disabled automatically." > $MODDIR/boot_failure.log
    exit
else
    # Startup successful -> execute random animation selection for next boot
    sh $MODDIR/random_animation.sh
fi
```

若动画守护进程在 60 秒后仍处于运行状态，模块即判定系统启动挂起，随即调用 `umount.sh` 从内存中卸载覆盖层并写入恢复日志。

### 3. 动态随机轮换器（random_animation.sh）

当手机顺利进入正常桌面状态后，`random_animation.sh` 会扫描模块目录中的备选动画压缩包，利用 `$RANDOM` 随机挑选一个并部署为主 `bootanimation.zip`，供下次设备重启时使用。

---

## 添加自定义开机动画

如需导入个人收集的动画包：
1. 确保动画压缩包采用 0% 压缩率打包（在 7-Zip 中选择“仅存储（Store）”模式，或执行 `zip -0 -r bootanimation.zip desc.txt part*`）。
2. 确认 `desc.txt` 文件末尾保留了一个空行。
3. 使用不重复的文件名（如 `cyberpunk.zip`）将压缩包复制到 `/data/adb/modules/bootanimation/` 目录中。
