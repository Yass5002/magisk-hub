---
id: "revanced-extended"
title: "ReVanced Extended：YouTube 与 YouTube Music 无系统分区增强模块"
sidebarTitle: "ReVanced Extended"
description: "自动化部署并以无系统分区修改方式挂载 ReVanced Extended（Morphe）版 YouTube 与 YouTube Music 的 Root 模块。"
category: "customization-ui"
tier: 1
searchQueries:
  - "ReVanced Extended Magisk 模块"
  - "Morphe YouTube Root 模块下载"
  - "ReVanced Extended YouTube Music 模块"
  - "无侵入挂载 ReVanced 模块"
  - "NoName-exe revanced-extended"
prerequisites:
  - "Magisk、KernelSU 或 APatch"
  - "已安装与模块发行版本匹配的官方原版 YouTube（com.google.android.youtube）或 YouTube Music 基础 APK"
  - "建议配合 zygisk-detach 使用，防止 Google Play 商店自动更新覆盖已挂载版本"
conflicts:
  - "目前暂无与其他 Root 模块的已知冲突（但若未分离商店更新，Google Play 后台自动更新会覆盖挂载后的应用）"
configPaths:
  - "/data/adb/modules/yt-morphe/"
  - "/data/adb/modules/ytm-morphe/"
  - "/data/adb/modules/yt-morphe/disabled_by_action"
  - "/data/adb/post-fs-data.d/"
features:
  - "无系统分区 APK 挂载：零修改系统分区文件即可替换原版 YouTube 二进制程序"
  - "全方位广告拦截：彻底去除片头片中视频广告、横幅广告、搜索广告及音频流广告"
  - "后台与画中画播放：无需订阅会员即可解锁息屏后台听歌与画中画悬浮窗播放"
  - "Root 模式免装 MicroG：直接对接系统原生 Google Play 服务，无需依赖 Vanced MicroG"
  - "自动 Odex 预编译：安装时自动预编译 dex/odex 文件，消除首次启动卡顿"
faq:
  - question: "使用 ReVanced Extended Root 模块时还需要安装 MicroG 吗？"
    answer: "不需要。由于 Root 模块直接将修补后的 APK 挂载覆盖到原版系统应用包名（com.google.android.youtube）上，应用会直接调用设备原生的 Google Play 服务账号体系，因此完全不需要 MicroG。"
  - question: "为什么用了一段时间后，应用会变回未去广告的原版？"
    answer: "Google Play 商店会在后台自动检测应用更新并覆盖基础 APK。为避免此情况，建议刷入 zygisk-detach 模块，将 YouTube 与 YouTube Music 从 Play 商店更新队列中分离隐藏。"
---

## 概述

由 **NoName-exe** 维护的 **ReVanced Extended**（Morphe）模块，为已获取 Root 权限的 Android 设备提供了一套简洁高效的全自动无系统分区方案，用于集成去广告增强版 YouTube 与 YouTube Music。

与非 Root 独立修改版需要更改包名并依赖独立 microG 服务同步账号不同，本模块直接将修补后的程序动态覆盖挂载至原版应用之上。这完整保留了原生 Google Play 服务授权、Cast 投屏协议兼容性以及系统级 Intent 跳转体验。

---

## 技术架构与工作原理

### 动态挂载与服务生命周期

该模块通过在用户空间初始化早期编排文件替换来发挥作用：

1. **架构与版本校验**：刷入过程中，`customize.sh` 会检测宿主设备 ABI（`arm64-v8a` 或 `armeabi-v7a`），判断目标包（`com.google.android.youtube` 或 `com.google.android.apps.youtube.music`）属于系统应用还是用户应用，并在必要时卸载冲突的系统更新。
2. **开机晚期挂载（`service.sh`）**：模块会等待 `sys.boot_completed` 变为 `1` 且 `/sdcard/Android` 目录可访问。随后通过包管理器查询基础 APK 路径（`get_basepath`），并执行 tmpfs 绑定挂载（Bind Mount），将预编译优化好的 ReVanced Extended APK 无缝覆盖到原版安装目录。
3. **字节码预编译优化**：安装脚本会针对新挂载的模块触发 ART 编译（`cmd package compile -m speed`），确保启动速度媲美甚至超越未修补的原厂包，消除首次运行时的 JIT 编译卡顿。

---

## 安装与配置

### 1. 准备原版基础应用
- 确保设备中已安装与模块发行版本标签相对应的原版 YouTube 或 YouTube Music。
- 如果你的设备出厂预装了 YouTube 作为系统应用，请前往 **设置 > 应用 > YouTube > 卸载更新**，先清除 Play 商店推送过的更新包。

### 2. 刷入模块
1. 从官方 GitHub Releases 仓库下载对应的发布包（`youtube-morphe-module-*.zip` 或 `youtube-music-morphe-module-*.zip`）。
2. 在 Magisk、KernelSU 或 APatch 中刷入该模块。
3. 重启设备。

### 3. 从 Play 商店分离更新
为防止 Google Play 商店自动下载官方更新覆盖已挂载的增强版：
- 刷入 **zygisk-detach** 模块，并在配置中勾选分离 `com.google.android.youtube` 与 `com.google.android.apps.youtube.music`。

---

## 功能配置与使用

ReVanced Extended 的各项功能均可在 YouTube 应用内部直接调整：
- 进入 **设置 > ReVanced Extended**（或 **Morphe 设置**）。
- **广告拦截（Ad Blocker）**：按需开关视频内嵌广告、浮层广告及信息流广告过滤规则。
- **SponsorBlock**：启用众包片段跳过功能，自动跳过片头、赞助商口播及非音乐片段。
- **Return YouTube Dislike**：在所有视频播放页恢复显示社区点踩数量。
- **视频播放（Video Playback）**：分别为 Wi-Fi 与移动网络设定默认首选清晰度。

---

## 常见问题与排查

- **应用无法打开 / 启动即闪退**：请核对设备中安装的原版 YouTube 版本号是否与模块发布页标注的配套版本完全一致。版本不匹配会导致 Binder 接口调用失败。
- **临时禁用模块**：如需在不卸载的情况下临时停用挂载，请手动创建 `/data/adb/modules/yt-morphe/disabled_by_action` 空文件并重启设备。
