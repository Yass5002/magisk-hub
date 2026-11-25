---
id: "joyctl-android"
title: "JoyCtl Android：小米 / 澎湃 OS Joyose 云控本地编辑工具"
sidebarTitle: "JoyCtl Android"
description: "基于 hexwander/joyctl 移植的 MIT 开源原生 Root 应用（com.hexwander.joyctl），通过 su 直接在手机端读写小米 Joyose 的 teg_config.db 数据库，修改温控阈值、帧率锁与 migt 调度。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "JoyCtl Android 下载"
  - "小米 Joyose 云控修改工具"
  - "澎湃 OS teg_config.db 温控解除"
  - "com.hexwander.joyctl"
  - "persist.sys.sc_allow_conn 冻结云控"
prerequisites:
  - "搭载 MIUI 或澎湃 OS（HyperOS）并包含 `com.xiaomi.joyose` 的小米、Redmi 或 POCO 设备"
  - "已获取 Root 权限（Magisk、KernelSU 或 APatch），且允许第三方应用调用 `su`"
conflicts:
  - "其他同时覆盖 `teg_config.db` 或通过 Hook 劫持 `com.xiaomi.joyose` 云控配置的 Xposed/Root 模块"
configPaths:
  - "/data/data/com.xiaomi.joyose/databases/teg_config.db"
  - "/data/user/0/com.xiaomi.joyose/databases/teg_config.db"
  - "/data/user_de/0/com.xiaomi.joyose/databases/teg_config.db"
  - "/data_mirror/data_ce/null/0/com.xiaomi.joyose/databases/teg_config.db"
features:
  - "通过 `su` 在手机本地直接读写 `com.xiaomi.joyose` 的 `teg_config.db` 数据库，推送前自动生成 `.joyctl.bak` 备份并支持回读校验"
  - "拉取本机配置或导入规则后，自动按本机 Joyose 版本（或机型探测）获取云端未修改基准 `teg_config_baseline.db`，精准识别本地改动是否被 MCC 云控覆盖"
  - "内置 PC 风格规则卡片模板，支持多选游戏放宽温控阈值（自动转换为 Joyose PID 格式，如 `47` → `47:48`）、解除帧率锁（`dynamic_fps`）与调整 `migt` 大核基线"
  - "支持通过 `persist.sys.sc_allow_conn=0/1` 一键冻结或恢复 Joyose MCC 云控同步，并提供异常恢复官方 Joyose 配置的重置工具"
faq:
  - question: "如果提示找不到 `teg_config.db` 该如何处理？"
    answer: "系统刚刷机或刚清除数据时，Joyose 尚未生成本地云控数据库。请先打开一次小米「游戏工具箱」或启动一款游戏触发 Joyose 初始化数据库，再回到 JoyCtl Android 的「设备」页面点击拉取。"
  - question: "如何防止修改 `teg_config.db` 后被小米云控服务端重新覆盖？"
    answer: "在 JoyCtl Android 的「设备」页执行「冻结云控」，应用会将 `persist.sys.sc_allow_conn` 设为 `0` 并停止 Joyose 进程，从而阻止 MCC 云端下发规则覆盖本地修改；你也可以随时通过 `teg_config_baseline.db` 对比功能检查配置是否发生变化。"
---

## 概述

**JoyCtl Android**（包名 `com.hexwander.joyctl`）是基于桌面端开源项目 [hexwander/joyctl](https://github.com/hexwander/joyctl) 开发的 Android 原生客户端。原版桌面工具需要用电脑通过 ADB 连接已 Root 的小米手机来拉取并修改 Joyose 数据库，而 JoyCtl Android 直接在手机本地调用 `su` 权限完成读取、基线比对、规则修改与写回校验全流程。

在小米 MIUI 与澎湃 OS 设备上，`com.xiaomi.joyose` 负责下发游戏动态帧率限制（`dynamic_fps`）、温控降频 PID 策略（`thermal`）以及 `migt` 调度基线，全部存储在 SQLite 数据库 `teg_config.db` 中。

---

## 技术架构与数据流机制

通过分析 `JoyCtl-Android-v1.0.17.apk`（`com.hexwander.joyctl`）的 DEX 代码与官方说明，其核心工作原理如下：

### 1. 多路径 `teg_config.db` 自动探测（`JoyoseDb`）
针对不同 Android 版本及加密/挂载环境，JoyCtl 会按需在以下路径定位 `com.xiaomi.joyose` 数据库：
- `/data/data/com.xiaomi.joyose/databases/teg_config.db`
- `/data/user/0/com.xiaomi.joyose/databases/teg_config.db`
- `/data/user_de/0/com.xiaomi.joyose/databases/teg_config.db`
- `/data_mirror/data_ce/null/0/com.xiaomi.joyose/databases/teg_config.db`
- `/data_mirror/data_de/null/0/com.xiaomi.joyose/databases/teg_config.db`

### 2. 云端基准对照与安全推送
- **云端拉取优先策略**：优先依据本机 Joyose 版本号拉取对应的未修改云端配置作为对照基准（`teg_config_baseline.db`），若拉取不到则根据机型属性（`ro.product.device` / `ro.product.marketname`）探测可用配置，并同步载入 `booster_config` 与 `common_config` 中 `status=1` 的有效规则。
- **备份与回读校验**：推送修改前会在同目录自动备份 `.joyctl.bak`，写入后执行回读校验（`teg_config_device_verify.db`）确保 SQLite 数据未损坏；同时通过 `CompareResult` 判断本地配置是否被 MCC 云控覆盖。

### 3. 规则模板与云控冻结控制
- **温控与帧率规则修改**：支持按「全部游戏」或自定义多选游戏修改已有配置条目，放宽温控时自动将摄氏度数值转换为 Joyose PID 策略格式（例如 `47` → `47:48`），并能同步识别帧率锁（`dynamic_fps`、`dynamic_fps_M`、`dynamic_fps_m`）、`migt` 大核基线及包名变动。
- **冻结 / 恢复与官方重置**：通过控制属性 `persist.sys.sc_allow_conn=0/1` 冻结或恢复 MCC 云控连接；若系统出现异常，「设备」页还提供「恢复官方 Joyose」功能，可清空相关数据、重新启用 `CloudServerReceiver` 与 `JoyoseBroadCastReceiver` 并发送开机广播以重建原厂配置。

---

## 使用步骤与命令行验证

1. 在已 Root 的小米 / Redmi / POCO 手机上安装 `JoyCtl-Android-v1.0.17.apk`。
2. 打开应用并在 **Magisk**、**KernelSU** 或 **APatch** 弹窗中允许第三方应用调用 `su` 权限。
3. 在 **设备** 页点击拉取，读取当前 `teg_config.db` 与云端对照基准。
4. 切换至 **规则** 页选择目标游戏，按需调整温控阈值、帧率锁或 `migt` 基线并点击 **修改**，随后回到 **设备** 页推送生效。
5. 建议在 **设备** 页点击冻结云控以防止后台自动还原。

### 命令行状态检查

```bash
# 检查 Joyose MCC 云控连接开关状态（0 为已冻结，1 为允许）
getprop persist.sys.sc_allow_conn

# 查看 teg_config.db 与 .joyctl.bak 备份文件
su -c "ls -la /data/data/com.xiaomi.joyose/databases/"
```

> **注意**：放宽游戏温控阈值或解除帧率锁会显著增加 SoC 功耗与机身发热量，请结合散热条件谨慎调节，并妥善保留 `.joyctl.bak` 备份。
