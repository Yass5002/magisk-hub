---
id: "blurclosed"
title: "Blur Closed：系统级界面与 SurfaceFlinger 高斯模糊禁用模块"
sidebarTitle: "Blur Closed"
description: "基于 GPL-3.0 协议的无系统分区修改（Systemless）模块，在 post-fs-data.sh 阶段通过条件式 resetprop 与 WindowManager 命令禁用 Android 原生及主流 OEM ROM 的实时背景模糊特效。"
category: "customization-ui"
tier: 1
searchQueries:
  - "Blur Closed 模块下载"
  - "Magisk 关闭系统高斯模糊"
  - "禁用安卓实时毛玻璃特效"
  - "ro.surface_flinger.force_disable_blur"
  - "cmd window disable-blur 1"
prerequisites:
  - "Magisk v20.4+、KernelSU 或 APatch"
  - "推荐 Android 11 及以上版本（安装脚本在 `API < 30` 设备上会提示兼容性警告）"
conflicts:
  - "其他强制开启 SurfaceFlinger 或桌面模糊特效的界面美化模块（如将 `enable_blurs_on_windows` 设为 `1` 的模块）"
configPaths:
  - "/data/adb/modules/blurclosed/post-fs-data.sh"
  - "/data/adb/modules/blurclosed/uninstall.sh"
features:
  - "在 `post-fs-data.sh` 中通过 `check_and_resetprop` 先检测属性是否存在再执行 `resetprop -n`，避免向无关固件盲目注入多余系统属性"
  - "全面禁用 AOSP 与 SurfaceFlinger 模糊开关，包括 `disableBlurs=1`、`disableBackgroundBlur=1`、`enable_blurs_on_windows=0`、`ro.surface_flinger.force_disable_blur=1` 与 `persist.sys.sf.disable_blurs=1`"
  - "兼容 MIUI/澎湃 OS（`ro.miui.has_blur`、`persist.sysui.miui_blur_enabled`）、ColorOS/一加/OPPO、三星 OneUI 与魅族 Flyme 等定制系统模糊属性"
  - "在安装与开机阶段调用 `cmd window disable-blur 1`（`API >= 29`），并在卸载脚本 `uninstall.sh` 中自动还原为 `0`"
faq:
  - question: "为什么 Blur Closed 在调用 `resetprop -n` 前要先判断当前属性值？"
    answer: "模块在 `post-fs-data.sh` 中编写了 `check_and_resetprop()` 函数，会先执行 `resetprop \"$prop_name\"` 读取当前值，若为空或已等于目标值则直接跳过。这种设计可以确保仅改写当前 ROM 真实存在的属性，避免向系统属性区写入无效的跨厂商键名。"
  - question: "卸载 Blur Closed 后系统背景模糊能否正常恢复？"
    answer: "可以。所有属性修改均在开机阶段通过 `resetprop` 无侵入式应用，且 `uninstall.sh` 会自动执行 `cmd window disable-blur 0`（旧版系统执行 `cmd wm disable-blur 0`）。在 Root 管理器中卸载模块并重启即可恢复默认模糊效果。"
---

## 概述

**Blur Closed**（模块 ID：`blurclosed`）由 **Astoritin** 开发，是一款轻量且开源（GPL-3.0）的界面优化模块，旨在关闭 Android WindowManager、SurfaceFlinger 以及各大 OEM 定制系统中的实时高斯模糊特效。在中低端 GPU 或高刷新率屏幕上，通知栏、控制中心及弹窗背后的多层实时模糊渲染容易引发掉帧与额外 GPU 功耗。

该模块通过在 Zygote 启动前的 `post-fs-data` 阶段覆盖系统模糊属性并禁用窗口模糊开关，无需修改任何系统 APK 即可减轻合成器（Compositor）负载。

---

## 技术架构与属性清单

检查 `BlurClosed-1.1.1.zip` 内容可知，模块在 `customize.sh` 中采用逐文件 SHA-256 校验安装，核心逻辑全部位于 `post-fs-data.sh` 与 `uninstall.sh`：

### 1. 条件式属性覆盖（`check_and_resetprop`）
`post-fs-data.sh` 通过辅助函数避免无效注入：
```sh
check_and_resetprop() {
    local prop_name=$1
    local prop_expect_value=$2
    local prop_current_value=$(resetprop "$prop_name")
    [ -z "$prop_current_value" ] && return 1
    [ "$prop_current_value" = "$prop_expect_value" ] && return 0
    resetprop -n "$prop_name" "$prop_expect_value"
}
```
仅当固件原本定义了对应属性且当前值与目标值不一致时，才会调用 `resetprop -n` 改写。

### 2. 覆盖的模糊控制属性分类
- **AOSP / SurfaceFlinger / WindowManager**：
  - `disableBlurs=1`、`disableBackgroundBlur=1`、`enable_blurs_on_windows=0`
  - `ro.surface_flinger.force_disable_blur=1`、`ro.surface_flinger.supports_background_blur=0`、`persist.sys.sf.disable_blurs=1`
  - `ro.sf.blurs_are_costly=1`、`ro.sf.blurs_are_expensive=1`、`ro.launcher.blur.appLaunch=0`
  - `windowBlurBehindEnabled=false`、`windowBlurBehindRadius=0`
- **通用系统与动态模糊属性**：
  - `persist.sys.background_blur_supported=0`、`persist.sys.background_blur_status_default=0`、`persist.sys.background_blur_version=0`、`persist.sys.add_blurnoise_supported=0`、`persist.sys.enable_third_blur=0`、`persist.sys.dynamic_blur_enabled=0`、`persist.perf.wm_static_blur=false`、`persist.sys.static_blur_mode=true`、`persist.vendor.sf.blur.type=none`、`persist.sys.disable_blur_view=true`、`persist.sys.disable_glass_blur=true`、`sys.use_frost_effect=0`
- **OEM 定制系统专属属性**：
  - **MIUI / 澎湃 OS**：`persist.sysui.miui_blur_enabled=0`、`ro.miui.has_blur=0`、`ro.miui.has_real_blur=0`、`ro.miui.backdrop_sampling_enabled=0`、`persist.miui.ui.optimize_blur=0`
  - **ColorOS / 一加 / OPPO**：`persist.sys.oneplus.blur.enabled=0`、`persist.sys.oplus.ui.blur=0`、`persist.sys.oppo.blur.enable=0`
  - **三星 OneUI**：`persist.sys.samsung.blur.disable=1`
  - **魅族 Flyme**：`persist.meizu.gpu_blur=0`

### 3. WindowManager 运行时指令
`customize.sh` 与 `post-fs-data.sh` 均会执行以下指令关闭窗口级模糊：
```sh
[ "$API" -ge "29" ] && cmd window disable-blur 1 || cmd wm disable-blur 1
```
模块卸载时，`uninstall.sh` 会将该参数还原为 `0`。

---

## 安装与验证

1. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入 `BlurClosed-1.1.1.zip`。
2. 重启设备，确保 `post-fs-data.sh` 在系统界面启动前生效。
3. 可通过 ADB Shell 检查模糊属性与窗口服务状态：

```bash
# 查看 AOSP / SurfaceFlinger 模糊属性
getprop ro.surface_flinger.force_disable_blur
getprop persist.sys.sf.disable_blurs
getprop enable_blurs_on_windows

# 检查 WindowManager 模糊开关状态
dumpsys window | grep -i blur
```
