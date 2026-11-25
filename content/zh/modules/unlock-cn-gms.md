---
id: "unlock-cn-gms"
title: "Unlock CN GMS：去除国行 ROM 系统分区 Google 服务 XML 限制"
sidebarTitle: "Unlock CN GMS"
description: "由 fei-ke 开发的无系统修改模块，自动扫描并移除国行系统多个分区中的 cn.google.services 与 services_updater 特性限制，恢复谷歌位置记录与地图时间轴。"
category: "system-environment"
tier: 1
searchQueries:
  - "Unlock CN GMS 下载"
  - "国行手机开启 Google 位置记录"
  - "谷歌地图时间轴 cn.google.services 解锁"
  - "fei-ke unlock-cn-gms 模块"
  - "小米 OPPO 国行 GMS 完整解锁"
prerequisites:
  - "在内置 GMS 框架的国行 ROM 设备上已安装 Magisk、KernelSU 或 APatch"
  - "当前系统至少包含一个声明 `cn.google.services` 的 XML 权限或 sysconfig 配置文件"
conflicts:
  - "其他同时替换相同 `/etc/permissions/` 或 `/etc/sysconfig/` XML 文件的模块"
  - "国际版 / 欧版（EEA）或原生 AOSP ROM（因无限制文件，刷入时会自动中止）"
configPaths:
  - "/data/adb/modules/com.fei_ke.unlockcngms/"
  - "/system/etc/permissions/services.cn.google.xml"
  - "/product/etc/permissions/cn.google.services.xml"
  - "/odm/etc/permissions/com.gnss.bds_preference.xml"
  - "/my_bigball/etc/permissions/oplus_google_cn_gms_features.xml"
  - "/my_product/etc/permissions/oplus_google_cn_gms_features.xml"
features:
  - "自动扫描 `/system`、`/vendor`、`/product`、`/odm`、`/my_bigball`、`/my_product` 与 `/my_heytap` 下 11 个以上常见权限配置文件路径"
  - "直接基于本机现有 XML 动态剔除 `<feature name=\"cn.google.services\" />` 与 `<feature name=\"com.google.android.feature.services_updater\" />`"
  - "针对独立挂载的 OEM 分区（`/odm`、`/my_bigball`、`/my_product`、`/my_heytap`）自动生成 `post-fs-data.sh` `mount -o ro,bind` 挂载脚本"
  - "无侵入式恢复 Google Location History（位置记录）、Google Maps Timeline（时间轴）及网页版 Play 商店设备列表显示"
faq:
  - question: "为什么在 OPPO、一加或小米部分机型上，安装脚本还会额外生成 `post-fs-data.sh`？"
    answer: "标准的 Magisk/KernelSU 模块挂载主要面向 `/system`、`/vendor` 与 `/product` 等常规路径，而 OPlus（ColorOS / realme UI）与部分小米机型会将 GMS 限制文件存放在独立挂载的分区（如 `/my_bigball`、`/my_product`、`/my_heytap` 与 `/odm`）。`customize.sh` 检测到此类分区后，会自动向 `post-fs-data.sh` 写入 `mount -o ro,bind` 命令，确保开机早期完成只读绑定覆盖。"
  - question: "刷入时报错 `No suitable permission file found!` 是什么原因？"
    answer: "这说明扫描列表中的 XML 配置文件在你的当前固件中均不存在，常见于本身就未加入 `cn.google.services` 限制的国际版/类原生 ROM，或厂商使用了未收录的自定义路径。模块此时会安全中止刷入，不会生成无效空文件。"
  - question: "刷入 Unlock CN GMS 后仍然无法开启位置记录怎么办？"
    answer: "该模块负责在系统特性层面解除 `cn.google.services` 封锁，但 Google Play 服务有时还会额外校验手机卡 MCC/MNC 运营商地区代码。如遇此情况，可根据作者说明配合 Xposed 模块 `LocationReportEnabler`（`GhostFlying/LocationReportEnabler`）一同使用。"
---

## 概述

众多国行版本智能手机（小米 HyperOS/MIUI、OPPO/一加 ColorOS、真我 realme UI、vivo OriginOS 等）虽然系统底层预置了 Google 移动服务（GMS），但往往通过系统权限 XML 文件声明了 `cn.google.services` 特性标签，从而在系统层面阉割了部分 Google 服务能力——最典型的表现包括无法启用 **Google Location History（位置记录）**、**Google 地图时间轴（Timeline）** 不可用，以及网页端 Google Play 无法正常识别显示当前设备。

由 **fei-ke** 开发的 **Unlock CN GMS**（模块 ID `com.fei_ke.unlockcngms`）通过动态修补设备本地的权限 XML 文件并配合无系统修改挂载，彻底移除上述限制。

---

## 技术原理与模块内部实现

与直接内置固定 XML 替换文件的方案不同，`unlock-cn-gms-v3.9.zip` 不包含写死的系统文件，而是在刷入时由 `customize.sh` 实时扫描当前设备固件并生成精确补丁，避免误删机型专属的硬件权限配置。

### 覆盖扫描路径

`customize.sh` 会依次检测以下系统及 OEM 分区路径：

- `/system/etc/permissions/services.cn.google.xml`
- `/system/etc/permissions/com.oppo.features.cn_google.xml`
- `/vendor/etc/permissions/services.cn.google.xml`
- `/vendor/etc/permissions/cn.google.services.xml`
- `/product/etc/permissions/services.cn.google.xml`
- `/product/etc/permissions/cn.google.services.xml`
- `/product/etc/sysconfig/cn_feature.xml`
- `/odm/etc/permissions/com.gnss.bds_preference.xml` *（例如小米 8e5 等多分区机型）*
- `/my_bigball/etc/permissions/oplus_google_cn_gms_features.xml`
- `/my_product/etc/permissions/oplus_google_cn_gms_features.xml`
- `/my_heytap/etc/permissions/my_heytap_cn_gms_features.xml` *（若存在 `/my_heytap/etc/permissions/my_heytap_cn_features.xml` 亦会一并处理）*

### XML 剔除与双模式挂载策略

对于每一个命中的源文件，`customize.sh` 会将其复制至模块目录，并通过 `sed` 精准删除以下两行声明：

```xml
<feature name="cn.google.services" />
<feature name="com.google.android.feature.services_updater" />
```

1. **常规 `/system`、`/vendor`、`/product` 分区**：放置于 `$MODPATH/system/...`（或对应 `/system` 路径下），交由 Magisk Magic Mount 或 KernelSU / APatch OverlayFS 无侵入挂载。
2. **独立 OEM 分区（`/odm`、`/my_bigball`、`/my_product`、`/my_heytap`）**：自动在 `$MODPATH/post-fs-data.sh` 中生成 `mount -o ro,bind ${0%/*}/<文件> <目标路径>` 指令，确保多分区共存的设备也能全部生效。

---

## 安装与配置指南

1. 在手机系统中开启内置的 Google 基础服务 / GMS 开关。
2. 在 **Magisk**、**KernelSU** 或 **APatch** 中刷入 `unlock-cn-gms-v3.9.zip`。
3. 观察刷入日志，确认所有命中的路径均输出 `modify <路径>`。
4. 重启设备使权限配置及 `post-fs-data.sh` 挂载生效。
5. 若此前已缓存限制状态，建议强行停止并清理 **Google Play 服务**（`com.google.android.gms`）与 **Google 地图**（`com.google.android.apps.maps`）缓存后再检查位置记录设置。

---

## 常见问题与排查

- **多分区同时存在限制文件（如小米 8e5、OPPO/一加机型）**：部分固件在 `/odm` 与 `/product`，或 `/my_bigball` 与 `/my_product` 下同时存在限制 XML。模块会自动全部处理，请勿手动删除生成的 `post-fs-data.sh`。
- **系统 OTA 升级后失效**：由于修补文件是在刷入模块时从当时系统复制生成的，系统大版本 OTA 更新后建议重新刷入一次本模块，以同步新固件中的其余权限条目。
- **移除特性后位置记录仍为灰色**：重启后可通过 `pm list features | grep cn.google.services` 确认模块已彻底生效；若仍受运营商地区检测限制，请搭配 LSPosed 模块 **LocationReportEnabler** 协同处理。
