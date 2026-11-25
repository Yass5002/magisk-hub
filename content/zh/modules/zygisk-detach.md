---
id: "zygisk-detach"
title: "Zygisk-Detach：将指定应用与 Google Play 商店更新彻底解绑"
sidebarTitle: "Zygisk-Detach"
description: "结合 Zygisk 注入与命令行工具的应用解绑模块，将已安装的特定应用从 Google Play 商店剥离，彻底阻止不必要的自动更新。"
category: "system-environment"
tier: 1
searchQueries:
  - "zygisk detach Magisk 模块"
  - "阻止 Google Play 商店自动更新应用"
  - "YouTube ReVanced 从 Play 商店解绑"
  - "j-hc zygisk-detach 使用教程"
  - "detach.txt 配置方法"
prerequisites:
  - "Magisk（需开启 Zygisk）、KernelSU 或 APatch"
  - "设备已安装 Google Play 商店"
conflicts:
  - "直接修改本地 XML 数据库的传统商店解绑脚本（极易导致数据库损坏）"
configPaths:
  - "/data/adb/zygisk-detach/detach.txt"
  - "/data/adb/modules/zygisk-detach/"
features:
  - "动态拦截目标应用与 Google Play 商店（`com.android.vending`）之间的 Binder IPC 通信"
  - "彻底阻止 Play 商店对修改版、补丁版或锁定的旧版应用推送更新提示"
  - "配套命令行工具：使用 `detach -a <pkg>` 或 `detach -r <pkg>` 随时动态增删解绑列表"
  - "经受住 Play 商店清缓存及 Google Play 服务后台数据库重建的考验"
faq:
  - question: "为什么解绑的应用过了几天又在 Play 商店里出现了？"
    answer: "Google Play 商店会定期执行后台同步任务并重建本地应用缓存。Zygisk-Detach 采用动态查询拦截机制；如果应用重新出现在更新列表中，执行 `su -c 'detach -k'` 强行终止 Play 商店进程即可促使其重新读取解绑列表。"
  - question: "非 Play 商店渠道安装的应用也可以使用 Zygisk-Detach 吗？"
    answer: "可以。默认情况下，Play 商店会扫描设备上所有已安装应用，只要包名与商店内条目匹配（例如侧载 APK 或 ReVanced 补丁版应用）就会推送更新。将其包名加入 detach.txt 后，即可彻底屏蔽 Play 商店的干预。"
---

## 概述

由 **j-hc** 开发的 **Zygisk-Detach** 是 Android 设备上冻结指定应用商店更新的终极工具。

使用修改版应用（例如 **YouTube ReVanced**、**Spotify 修改版**或保留了精简特性的旧版本应用）时，用户经常会遇到一个令人头疼的问题：Google Play 商店会在后台自动更新这些应用，直接覆盖已有补丁并导致功能失效。

早期解决方案往往尝试直接修改 SQLite 数据库（`/data/data/com.android.vending/databases/library.db`），但 Play 商店很快就会在后台同步中覆盖这些改动。Zygisk-Detach 则直接工作在运行时 IPC 通信层，对 Play 商店进程动态隐匿已解绑的应用包名。

---

## 技术架构与工作原理

### 动态 Binder IPC 拦截

1. **进程注入**：借助 Zygisk 机制，模块将原生伴生动态库注入到 `com.android.vending`（Google Play 商店）进程中。
2. **Binder 挂钩（Hook）**：当 Play 商店服务向 Android 包管理器查询已安装应用或汇总本地应用库清单时，Zygisk-Detach 会拦截底层的 IPC 调用。
3. **过滤列表应用**：挂钩逻辑会读取 `/data/adb/zygisk-detach/detach.txt`，凡是在该配置文件中声明的应用包名，都会从返回给 Google 更新检查后台任务的列表中直接剔除。
4. **持久隐匿效果**：由于过滤发生在进程运行时的内存中，Google Play 商店永远无法感知这些已解绑应用的存在，从而永久消除“更新”提示与自动更新行为。

---

## 安装与部署

1. 打开 **Magisk**、**KernelSU** 或 **APatch** 管理器。
2. 刷入最新版的 `zygisk-detach-vX.zip` 模块包。
3. 重启设备使模块生效。

---

## 配置与命令行用法

本模块内置了可在 **Termux** 或 **ADB Shell** 中直接运行的交互式终端命令（`detach`）：

```bash
# Add an application to the detach list:
su -c "detach -a com.google.android.youtube"

# Remove an application from the detach list:
su -c "detach -d com.google.android.youtube"

# List all currently detached applications:
su -c "detach -l"

# Force-kill Play Store to apply changes immediately:
su -c "detach -k"
```

你也可以直接手动编辑配置文件：
`/data/adb/zygisk-detach/detach.txt`（每行填写一个应用包名即可）。
