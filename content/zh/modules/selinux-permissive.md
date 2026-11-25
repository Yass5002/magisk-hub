---
id: "selinux-permissive"
title: "SELinux Permissive：带检测伪装的开发模式切换工具"
sidebarTitle: "SELinux Permissive"
description: "由 Denis Efremov 开发的调试实用工具，开机时将 Android SELinux 切换至 Permissive 宽容模式，同时限制 sysfs 读取权限并向非 Root 应用伪装状态属性。"
category: "development-instrumentation"
tier: 1
searchQueries:
  - "SELinux Permissive Magisk 模块"
  - "evdenis selinux_permissive"
  - "Android Root 切换 SELinux 宽容模式"
  - "隐藏 SELinux Permissive 状态"
  - "三星 CONFIG_ALWAYS_ENFORCE Magisk"
prerequisites:
  - "已刷入 Magisk 并获取 Root 权限的 Android 设备"
  - "编译时未开启 `CONFIG_ALWAYS_ENFORCE=y` 的 Linux 内核"
conflicts:
  - "内置强制 `CONFIG_ALWAYS_ENFORCE=y` 编译选项的三星原厂内核"
configPaths:
  - "/data/adb/modules/selinux_permissive/"
features:
  - "双阶段执行机制：在 `post-fs-data` 早期阶段将 SELinux 切换为 Permissive，并在 `service` 后期阶段确保持久生效"
  - "防检测权限收紧：限制 `/sys/fs/selinux/enforce` 的全局可读权限，使无特权应用无法直接读取当前强制状态"
  - "系统属性伪装：借助 Magisk `resetprop` 将 `ro.boot.selinux` 伪装为 `enforcing`"
  - "干净的回滚卸载：专用卸载脚本会在移除模块时恢复原有的 sysfs 节点权限与启动属性"
faq: []
---

## 概述

由内核工程师 Denis Efremov（`@evdenis`）编写的 **SELinux Permissive** 是一款面向开发者、ROM 移植者及 Root 工具作者的专业级无侵入（Systemless）模块。在 Android 默认的 Enforcing（强制）模式下，Security-Enhanced Linux（SELinux）会拦截并审计所有未在设备 sepolicy 策略中显式声明的系统操作。

尽管强制模式对于正式版设备的安全性至关重要，但在新机型适配（Bring-up）、定制 Vendor HAL 调试或运行复杂插桩工具时却经常造成权限拦截。该模块会在开机时将 SELinux 切换至 Permissive（宽容）模式——允许受审计的系统调用继续执行而非直接失败——同时向普通用户空间应用掩盖这一状态以降低被检测的概率。

> [!WARNING]
> Permissive 宽容模式会主动降低系统的安全隔离边界。除非处于特定的开发调试或故障排查流程中，否则请勿在存有敏感银行凭证的主力日常设备上使用此模块。

## 前置要求与兼容性

- **Root 框架**：Magisk（正式版或 Canary 测试版）。
- **内核支持**：设备内核必须允许在运行时动态切换 SELinux 模式。

### 已知不兼容情况

- **三星原厂内核**：本模块**无法工作**于编译配置中包含 `CONFIG_ALWAYS_ENFORCE=y` 的三星原厂内核。三星 Knox 安全模型会从内核底层锁死状态，即便拥有完整 Root 权限也无法更改 SELinux 模式。此类设备必须先刷入支持宽容模式的第三方定制内核。

## 架构与检测伪装机制

普通的模式切换脚本往往只执行一次 `setenforce 0`。但银行类应用与反作弊引擎通常会检查两个常见特征来识别设备是否处于宽容模式：
1. 直接读取 `/sys/fs/selinux/enforce` 节点文件。
2. 检查 Bootloader 传递的系统属性 `ro.boot.selinux`。

SELinux Permissive 采用了更严谨的双重防护措施：

1. **权限收紧**：在 `post-fs-data.sh` 与 `service.sh` 两个阶段均执行 `chmod 640 /sys/fs/selinux/enforce` 或调整 DAC 所有权，使无特权应用查询该节点时收到 `Permission Denied` 错误，而非读取到 `0`。
2. **属性伪装**：使用 `resetprop` 将 `ro.boot.selinux` 覆写为 `enforcing`，从而绕过常规的只读属性检测逻辑。

## 安装与验证

1. 从代码仓库或 Magisk 模块库下载最新版本发布包。
2. 在 Magisk 中刷入该模块并重启设备。
3. 在 Root Shell（`su`）中验证当前 SELinux 运行状态：
   ```bash
   getenforce
   # Returns: Permissive
   ```
4. 以非 Root 的普通 Shell 用户身份测试访问限制是否生效：
   ```bash
   cat /sys/fs/selinux/enforce
   # Returns: Permission denied
   ```

## 卸载方法

如需移除模块并恢复默认的 Enforcing 强制安全模式：
1. 在 Magisk 中卸载该模块。
2. 模块内置的 `uninstall.sh` 会在设备重启前自动恢复 `/sys/fs/selinux/enforce` 的默认全局可读权限，并还原相关系统属性。
