---
id: "dirtysepolicy-bypass"
title: "DirtySepolicy Bypass：拦截 App-Zygote SELinux 探测与策略篡改检测"
sidebarTitle: "DirtySepolicy Bypass"
description: "拦截 App-Zygote 对 SELinux 虚拟文件系统的查询，全面绕过 DirtySepolicy 在 `/sys/fs/selinux/` 与策略加载序列号上的检测手段。"
category: "root-management"
tier: 1
searchQueries:
  - "DirtySepolicy Bypass Magisk 模块"
  - "flipphoneguy DirtySepolicy Bypass"
  - "绕过 DirtySepolicy v2.2 Zygisk 检测"
  - "App-Zygote SELinux 探测拦截"
  - "伪造 sys fs selinux access 检测"
prerequisites:
  - "通过 Magisk 或 KernelSU 获取 Root 权限"
  - "Root 管理器中已启用 Zygisk 运行时"
  - "Android 10 至 Android 15+ 系统"
conflicts: []
configPaths:
  - "/data/adb/modules/dirtysepolicy-bypass/"
features:
  - "全面应对 DirtySepolicy：完整击败 LSPosed/DirtySepolicy 至 v2.2 版本所采用的四类核心探测技术"
  - "虚拟化 SELinux 文件系统：直接拦截针对 `/sys/fs/selinux/access` 与上下文节点的底层 `open`/`read`/`write` 调用"
  - "策略序列号伪装：屏蔽 `/sys/fs/selinux/status` 中策略加载计数器的变动，隐藏运行时 sepolicy 注入痕迹"
  - "App-Zygote 沙盒隔离：阻止隔离服务进程枚举框架注入的自定义安全上下文类型"
faq: []
---

## 概述

现代反 Root 检测套件（例如 LSPosed/DirtySepolicy、Momo 以及各类高强度金融风控 SDK）早已不再局限于扫描 `su` 二进制文件或检索 `which` 路径。如今它们会主动拉起非特权的 **App-Zygote** 子进程，直接探测内核的 SELinux 虚拟文件系统（`/sys/fs/selinux/`）。

由于 Magisk、KernelSU 与 APatch 等 Root 框架在运行超级用户守护进程时，往往需要向实时内核 sepolicy 注入自定义域规则，App-Zygote 便可通过探测非原厂上下文是否存在，或校验策略重载序列号（`seqno`）是否递增来判断环境异常。只要发现蛛丝马迹，应用就会将设备判定为已遭篡改。

由 flipphoneguy 开发的 **DirtySepolicy Bypass** 是一款专门在原生 libc 系统调用边界运作的 Zygisk 模块，旨在彻底屏蔽上述 SELinux 探测技术。

## 成功拦截的探测向量

DirtySepolicy Bypass 逐一化解了 DirtySepolicy v2.2 及其衍生检测器所实现的全部四大核心探测向量：

### 1. `contextExists()` 上下文探测
检测器会尝试向 `/sys/fs/selinux/context` 写入特定安全上下文或读取 `/proc/self/attr/current`，借此试探当前活跃策略字典中是否包含 Root 注入类型（如 `magisk`、`kernelsu` 或 `su`）。本模块会直接拦截这些写入操作并返回 `EINVAL`（无效参数），以完美模拟原厂系统的标准响应。

### 2. 内核直连 `checkSELinuxAccess()` 校验
高阶检测器会直接从 `/sys/fs/selinux/class/` 解析类别与权限标识符，并跳过用户态 `libselinux.so` 直接向 `/sys/fs/selinux/access` 提交二进制权限查询。DirtySepolicy Bypass 通过挂钩底层的 `openat`、`read` 与 `write` 系统调用拦截此类低级探测，并严格返回原厂策略的校验结果。

### 3. 策略重载与序列号监控（`readStatus()`）
每当 Magisk 或 KernelSU 在启动阶段注入规则时，内核就会递增 `/sys/fs/selinux/status` 中的内部 `policyload` 计数器。检测器通过比对该计数与原厂基准值即可发现异常。本模块会向其呈现虚拟化的静态状态结构，从而掩盖一切运行时的策略修改。

### 4. 间接原厂上下文探测
部分检测器还会试探原厂 Android 上下文之间本不该存在的放行规则（例如仅因 Root 框架修改规则图才会出现的 `rootfs → tmpfs:associate`）。DirtySepolicy Bypass 同样会拦截这类间接查询并返回原厂默认的拒绝结果。

## 安装与设置

1. 确保已在 Magisk 或 KernelSU 中开启 **Zygisk**。
2. 从 GitHub 下载 `DirtySepolicy_Bypass` `.zip` 安装包。
3. 在 Root 管理器中刷入该模块。
4. 重启手机。
5. 运行检测测试应用（如 DirtySepolicy 测试程序或 Momo），此时所有 SELinux 探测项均应顺利通过。
