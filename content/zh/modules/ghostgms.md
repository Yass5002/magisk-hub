---
id: "ghostgms"
title: "GhostGMS：无侵入式 Google Play 服务省电与隐私遥测优化"
sidebarTitle: "GhostGMS"
description: "由 Kaushik 开发的安全可逆 Google Play 服务优化模块，面向 Android 10 至 16 系统降低后台耗电、唤醒锁与遥测上报。"
category: "performance-kernel"
tier: 1
searchQueries:
  - "GhostGMS Magisk 模块"
  - "Kaushik GhostGMS 下载"
  - "Root 解决 Google Play 服务耗电"
  - "GMS 后台优化 Magisk 模块"
  - "GhostGMS Core 和 Legacy 区别"
prerequisites:
  - "Android 10 至 Android 16 系统"
  - "Magisk v20+ 或 KernelSU"
  - "目标设备已安装原厂 Google Play 服务"
conflicts: []
configPaths:
  - "/data/adb/modules/ghostgms/"
  - "/data/local/tmp/ghostgms_uninstall.log"
features:
  - "均衡的 GMS 服务抑制：精准限制过度的唤醒锁与后台轮询，同时确保 Firebase Cloud Messaging（FCM）消息推送正常到达"
  - "隐私遥测屏蔽：禁用非必要的谷歌遥测统计、使用情况追踪与广告衡量后台守护进程"
  - "非破坏性架构：绝不删除系统安装包，全部优化均通过系统属性与服务控制以无系统分区修改方式应用"
  - "完整卸载回滚：记录安装前的原始状态，卸载时自动恢复原厂配置与服务并生成审计日志"
  - "双版本可选：提供主打稳健兼容的 GhostGMS Core 与包含激进深度调校的 GhostGMS Legacy"
faq: []
---

## 概述

由 Kaushik（`@kaushikieeee`）开发的 **GhostGMS** 是一款专注于让 Google Play 服务（GMS）更轻量、更省电、更安静的无侵入式优化模块。在原厂 Android 设备上，Google Play 服务常常是待机耗电的主要来源——频繁在熄屏期间唤醒设备以同步标志位、上传分析数据、轮询位置信息以及运行后台诊断。

粗暴的精简删包脚本往往会无差别禁用 GMS 组件，导致推送失灵、应用闪退乃至 Google 账号登录异常；而 GhostGMS 采取了精细调校的稳妥方案，在抑制冗余后台遥测与待机唤醒锁的同时，完整保留关键的消息推送通道与身份认证框架。

## 前置要求与兼容性

- **Android 版本**：Android 10 至 Android 16。
- **Root 环境**：Magisk v20.0 及以上，或 KernelSU。
- **前置服务**：适用于运行 Google Play 服务的设备。使用纯 microG 或彻底去谷歌化的 ROM 无需安装本模块。

本模块暂无已知冲突。不过，同时叠加多个同类 GMS 冻结模块（例如与 Frosty 并用）属于冗余操作；你只需根据个人偏好在“开箱即用的自动预设（GhostGMS）”与“按类别精细开关（Frosty）”之间择一使用即可。

## 模块版本说明

GhostGMS 提供两个针对不同需求的版本：

1. **GhostGMS Core（推荐）**：面向主力机日常使用的核心版本，侧重安全默认策略、最大化应用兼容性、零推送延迟与极高稳定性。
2. **GhostGMS Legacy**：包含早期更激进深度系统微调的替代版本，适合愿意排查边缘应用兼容性的进阶玩家与跑分测试用户。

## 核心能力与架构

- **唤醒锁与定时唤醒节流**：限制激进的 GMS 定时唤醒（Alarm）频率，防止 CPU 在熄屏待机期间被反复拉起而无法进入深度休眠。
- **遥测组件禁用**：静默关闭谷歌 Clearcut、Phenotype 以及定期上传设备遥测数据的广告指标服务。
- **完整状态回滚引擎**：GhostGMS 会记录所有已应用的系统设置与属性。当你在 Root 管理器中卸载模块时，卸载脚本会自动将所有配置、属性和服务状态还原至安装前原样，并在 `/data/local/tmp/ghostgms_uninstall.log` 输出完整审计日志。

## 安装与验证

1. 从项目仓库下载最新的 `GhostGMS-Core-*.zip` 发布包。
2. 通过 Magisk Manager 或 KernelSU 刷入压缩包。
3. 重启设备。
4. 模块运行文件位于以下目录：
   ```bash
   /data/adb/modules/ghostgms/
   ```

### 验证省电效果

如需确认 GMS 是否正常进入待机休眠：
- 拔掉充电线，保持屏幕关闭待机数小时。
- 前往 **系统设置 > 电池** 查看电量消耗详情。Google Play 服务的后台活跃占比应处于极低水平（通常小于 1%–2%）。
- 验证 WhatsApp、Telegram、Gmail 等依赖推送的应用仍能实时收到消息提醒。

## 故障排查

- **个别应用通知延迟**：如果特定应用出现消息推送延迟，请检查 **系统设置 > 应用 > 电池用量** 中是否已将该应用设为“不受限制”。GhostGMS 会完整保留 GMS 推送链路，但部分厂商激进的后台杀进程机制仍可能休眠客户端应用本身。
- **核查卸载回滚状态**：卸载 GhostGMS 并重启设备后，可查看 `/data/local/tmp/ghostgms_uninstall.log` 以确认原始系统属性已全部恢复。
