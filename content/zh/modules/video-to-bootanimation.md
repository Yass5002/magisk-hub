---
id: "video-to-bootanimation"
title: "Video To Bootanimation：将 MP4 视频片段一键转换为自定义 Android 开机动画"
sidebarTitle: "Video To Bootanimation"
description: "自动化模块安装器与命令行工具集，可将用户本地 MP4 视频文件转换为高帧率 bootanimation.zip 开机动画，支持分辨率自动识别与启动音频提取。"
category: "system-environment"
tier: 1
searchQueries:
  - "video to bootanimation Magisk 模块"
  - "rhythmcache video to bootanimation 下载"
  - "Android MP4 转开机动画"
  - "bootvideo mp4 面具模块"
  - "Root 自定义开机动画制作"
prerequisites:
  - "运行基于 AOSP 或采用标准 bootanimation.zip 结构厂商 ROM 的 Android 设备"
  - "已通过 Magisk 或 KernelSU 获取 Root 权限"
  - "安装前需将源 MP4 文件放置于 /sdcard/bootvideo.mp4"
conflicts:
  - "三星 One UI 设备（使用三星专有 .qmg 压缩格式，而非 bootanimation.zip）"
configPaths:
  - "/sdcard/bootvideo.mp4"
  - "/sdcard/cfg.txt"
  - "/data/adb/modules/video-to-bootanimation/"
features:
  - "本地视频实时编译：刷入模块时直接在手机端将 MP4 视频逐帧拆解并打包为标准 Android part 分段目录"
  - "媒体参数自动探测：自动识别视频分辨率、纵横比与帧率，无需手动裁剪图片序列"
  - "可选启动音频：支持提取视频内嵌音轨并打包为 audio.wav，适用于支持开机音效的 ROM"
  - "输出路径自适应：自动识别或手动指定输出挂载到 /system/media 或 /system/product/media"
  - "内置命令行工具：安装后可在终端直接调用 vid2boot 与 boot2vid 二进制工具进行双向转换"
faq: []
---

## 概述

传统手动制作 Android 开机动画的过程相当繁琐：需要提取视频帧、手动为数百张 PNG 图片编号、编写精确的 `desc.txt` 时序描述文件，最后再以“零压缩（Store）”模式打包为特定结构的 ZIP 压缩包。只要图片分辨率或时序参数与硬件限制稍有偏差，设备开机时就会直接黑屏。

由 rhythmcache 开发的 **Video To Bootanimation** 将整套制作流程直接自动化集成到了手机端。你只需将普通 MP4 视频放入内部存储并刷入模块，安装脚本就会自动调用内置媒体工具解析视频、生成描述文件、编排分段目录，并以无系统分区修改（Systemless）方式覆盖生效。

## 前置条件与格式限制

- **源文件位置**：刷入模块 ZIP 压缩包**之前**，必须先将视频文件存放于 `/sdcard/bootvideo.mp4`（即 `/storage/emulated/0/bootvideo.mp4`）。
- **ROM 架构要求**：适用于标准 AOSP、LineageOS、Pixel、小米、摩托罗拉及其他在 `/system/media/` 或 `/system/product/media/` 目录下读取 `bootanimation.zip` 的 ROM。
- **三星 One UI 不兼容说明**：三星手机并不读取 `bootanimation.zip`，而是依赖 `bootchecker` 二进制程序渲染专有的 `.qmg` 格式文件。因此本模块无法更改三星原厂固件的开机动画。

## 配置参数说明（`cfg.txt`）

如未提供配置文件，模块会自动探测屏幕尺寸与视频帧率；如需自定义转换参数，可在刷入前提前创建 `/sdcard/cfg.txt`：

```ini
# video2boot configuration file
# Lines starting with # are ignored. Empty values = auto-detect.

# Custom path to source video
video=/sdcard/bootvideo.mp4

# Force custom resolution (leave blank to match source video)
width=1080
height=2400

# Target frame rate (e.g., 30 or 60)
fps=60

# Include audio track from video (on/off)
audio=off

# Target install location: auto, system/media, or system/product/media
output=auto
```

- **音频支持说明**：设置 `audio=on` 会将视频中的音轨提取为 `audio.wav`。请注意，开机音效能否播放取决于 ROM 内核与系统框架配置；目前许多现代 AOSP 编译版本默认禁用了开机声音功能。

## 安装步骤指引

1. 准备好你希望用作开机动画的视频片段，并确保其封装格式为 `.mp4`。
2. 将该文件重命名为 `bootvideo.mp4`，放置到手机内部存储根目录（`/sdcard/bootvideo.mp4`）。
3. *（可选）* 如需强制指定分辨率、帧率或开启开机音效，请先创建 `/sdcard/cfg.txt`。
4. 打开 Magisk 或 KernelSU 管理器，刷入 **Video To Bootanimation** ZIP 模块包。
5. 观察刷入控制台输出，等待模块自动完成视频解析、抽帧与 `bootanimation.zip` 打包。
6. 重启设备，即可体验全新的自定义视频开机动画。

## 终端命令行工具

本模块还会在系统环境安装独立的命令行二进制工具，可通过 Root 终端直接调用：

- **`vid2boot`**：无需重新刷入模块，随时将任意视频文件实时转换为开机动画包：
  ```bash
  su -c vid2boot /path/to/custom_video.mp4
  ```
- **`boot2vid`**：支持逆向还原，将现有的 `bootanimation.zip` 开机动画包重新转换回 MP4 视频文件。
