---
id: "magisk"
title: "Magisk（面具）：通用 Android 无系统分区修改（Systemless）Root 方案"
sidebarTitle: "Magisk（面具）"
description: "开源 Android Root 核心解决方案，提供无侵入式系统修改（Systemless）、Zygisk 注入框架与精细化超级用户权限管理。"
category: "root-management"
tier: 1
searchQueries:
  - "如何使用 Magisk 获取 Android Root"
  - "Magisk 面具官方 APK 下载"
  - "修补 boot.img 安装 Magisk 教程"
  - "什么是 Magisk Zygisk"
  - "Magisk 与 KernelSU、APatch 对比"
prerequisites:
  - "已解锁 Bootloader（BL 锁）"
  - "与设备当前系统版本号完全一致的官方原版 `boot.img` 或 `init_boot.img`"
  - "Android 平台调试工具（fastboot / adb）"
conflicts:
  - "SuperSU（已停止维护且不兼容现代系统）"
  - "切勿混用 KingRoot 等直接改写系统分区的传统 Root 工具"
configPaths:
  - "/data/adb/magisk.db"
  - "/data/adb/modules/"
  - "/data/adb/post-fs-data.d/"
  - "/data/adb/service.d/"
features:
  - "无系统分区修改（Systemless）Root 接口，支持按应用粒度管理超级用户权限"
  - "Magic Mount 系统级叠加挂载机制，无需直接修改只读 `/system` 分区"
  - "内置 Zygisk 运行时框架，可在 Zygote 孵化应用进程时直接注入模块代码"
  - "Resetprop 引擎，支持在运行时安全修改 `ro.*` 只读系统属性"
  - "原生 DenyList（排除列表）机制，用于向指定应用隔离隐藏 Root 环境"
faq:
  - question: "安装 Magisk 会触发三星 Knox 熔断或影响 Google Play Integrity 吗？"
    answer: "解锁 Bootloader 本身就会永久触发三星 Knox 硬件熔断（0x1）。针对 Google Play Integrity，Magisk 提供了无侵入式隔离与 Zygisk 排除列表，但要通过现代的 MEETS_DEVICE 或 MEETS_STRONG 认证检查，仍需搭配 PlayIntegrityFork 或 TrickyStore 等辅助模块。"
  - question: "修补镜像时应该选择 boot.img 还是 init_boot.img？"
    answer: "出厂即搭载 Android 13 及以上版本（GKI 通用内核镜像）的设备通常需要将 Magisk 修补到 `init_boot.img` 中；出厂为 Android 12 及更早版本的设备则修补标准的 `boot.img`。"
---

## 概述

由 John Wu（@topjohnwu）创建的 **Magisk（中文社区常称“面具”）** 是现代 Android 设备最主流的 Root 平台。与早期直接改写 `/system` 块设备的 Root 工具不同，Magisk 采用 **无系统分区修改（Systemless）** 架构：它通过修改内核内存盘（Ramdisk）中的 `init` 入口拦截 Linux 启动流程，将根文件系统切换至叠加层，并在不破坏系统只读分区的状态下挂载自定义二进制文件与模块资源。

Magisk 核心包含以下四个组成部分：
1. **`magiskd`**：后台 Root 守护进程，负责处理超级用户提权请求。
2. **Magisk App**：管理应用界面，用于审批 Root 授权、刷入模块及配置排除列表（DenyList）。
3. **Zygisk**：动态注入框架，挂钩 Android 核心 Zygote 进程，使模块能够在应用进程创建前加载代码。
4. **Magic Mount**：基于 Linux 挂载命名空间与 OverlayFS 的文件替换机制，可在不修改原系统分区的前提下覆盖或新增系统文件。

---

## 技术架构与工作原理

### Systemless 挂载与挂钩流程

Android 设备开机启动时，Magisk 按以下顺序接管并初始化环境：
1. **Bootloader 校验**：Bootloader 验证内核与内存盘签名。当 BL 锁处于已解锁状态时，允许启动经过修补的自定义 Ramdisk。
2. **`init` 劫持**：Magisk 修补 Boot 镜像中的 `init`，在把控制权交还给原生 `/init` 之前优先执行 Magisk 引导逻辑。
3. **早期挂载与 SELinux 策略注入**：在 Android 编译并强制执行 SELinux 策略前，Magisk 会实时修补 `sepolicy` 规则以定义专属的 `magisk` 域，在保证系统原有策略完整的同时赋予 Root 进程无限制权限。
4. **`post-fs-data` 阶段**：Android 挂载 `/data` 分区后，Magisk 执行 `/data/adb/post-fs-data.d/` 中的脚本，并触发各个模块的 `post-fs-data.sh`。
5. **Magic Mount 阶段**：Magisk 将 `/data/adb/modules/<id>/system` 中的模块文件通过回环设备及 `tmpfs`/`overlayfs` 挂载覆盖到对应的 `/system` 路径。
6. **Zygote 进程孵化（Zygisk）**：`zygote` 启动后，Zygisk 挂钩 ART 运行时；每当孵化新应用进程时，Zygisk 会依据配置决定执行排除列表卸载，或加载各模块的伴生动态库。

---

## 前置准备与安装步骤

### 第一步：提取原版纯净 Boot 镜像
下载与手机当前已安装系统版本号完全一致的官方线刷包或卡刷包，从中提取 `boot.img`（出厂 Android 13+ 机型请提取 `init_boot.img`）。

### 第二步：在 Magisk App 中修补镜像
1. 在设备上安装官方 Magisk APK（`Magisk-v30.x.apk` 或最新版本）。
2. 点击顶部 **安装** → **选择并修补一个文件**。
3. 选中刚刚提取的 `boot.img` 或 `init_boot.img`。
4. Magisk 会在手机 `Download` 目录下生成 `magisk_patched_[随机字符].img`。

### 第三步：通过 Fastboot 刷入修补镜像
将生成好的修补镜像传输至电脑，并将手机重启至 Fastboot 模式后执行：
```bash
# 若设备使用 boot.img：
fastboot flash boot magisk_patched.img

# 若设备使用 init_boot.img（Android 13+）：
fastboot flash init_boot magisk_patched.img

# 重启设备
fastboot reboot
```

---

## 配置与日常使用

### 管理 Root 权限
所有应用的超级用户授权记录均保存在 `/data/adb/magisk.db` SQLite 数据库中。既可在 Magisk App 的 **超级用户** 标签页中管理，也可通过命令行核验状态：
```bash
# 验证当前 Root 版本
su -c "magisk -v"

# 查看当前挂载特性状态
su -c "magisk --mount-features"
```

### 启用 Zygisk 与排除列表（DenyList）
1. 打开 **Magisk App** → 点击右上角 **设置** 齿轮图标。
2. 打开 **Zygisk** 开关。
3. **遵守排除列表（Enforce DenyList）**：若你搭配 Shamiko 或 Zygisk Assistant 等第三方隐藏模块使用，请保持**关闭**；仅依赖 Magisk 原生隐藏时再开启。
4. 点击 **配置排除列表**，勾选需要隐藏 Root 的目标应用（如银行软件、政务应用或游戏）。

---

## 常见问题与救砖排查

### 模块引发无法开机（Bootloop）恢复
如果刷入不兼容的模块导致手机卡在开机动画无法进入系统：
- **系统安全模式**：在支持按键组合的机型上，开机动画期间长按“音量下”键进入 Android 安全模式，Magisk 会自动检测到安全模式并禁用全部模块。
- **ADB 恢复模式**：若 Recovery 或早期启动阶段支持 ADB 连接：
  ```bash
  adb wait-for-device
  adb shell "touch /data/adb/modules/.disable_magisk"
  adb reboot
  ```
- **第三方 Recovery（TWRP / OrangeFox）**：进入内置文件管理器，打开 `/data/adb/modules/` 目录，直接删除导致异常的模块文件夹后重启即可。
