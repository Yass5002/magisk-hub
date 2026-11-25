---
id: "xhhttp"
title: "xh：面向 Android Root 终端的高速友好型 HTTP 客户端"
sidebarTitle: "xh HTTP Client"
description: "将 Rust 语言重构的轻量级 HTTPie 替代工具 xh 无侵入部署至 Android 系统，在终端轻松实现直观的 API 调试、JSON 格式化与接口测试。"
category: "system-utilities"
tier: 1
searchQueries:
  - "xh http Magisk 模块下载"
  - "xh 安卓 Root 终端命令行工具"
  - "Termux HTTPie 替代品"
  - "安卓 Root 终端发送 HTTP 请求"
  - "Rust HTTP 客户端 Magisk"
prerequisites:
  - "通过 Magisk 获取 Root 权限"
conflicts: []
configPaths:
  - "/data/adb/modules/xhhttp/"
features:
  - "Rust 原生高性能：基于 Rust 编译，具备毫秒级瞬时冷启动、极低内存占用与高吞吐表现"
  - "直观人性化的请求语法：无需繁琐参数即可轻松构造 GET、POST、PUT、DELETE 请求及自定义请求头与 JSON 数据"
  - "语法高亮与 JSON 自动排版：在终端内自动缩进并高亮着色展示 JSON 响应体及 HTTP 响应头"
  - "会话与 Cookie 持久化：支持在连续的命令行调用间自动保存身份认证 Cookie 与会话状态"
  - "无侵入式系统部署：将 `xh` 可执行文件干净挂载至 `/system/bin`，完全不改动原厂系统分区文件"
---

## 概述

在 Android 终端下调用 REST API、测试 Webhook 回调或排查本地 HTTP 服务时，传统做法往往只能在参数晦涩冗长的 `curl` 与体积庞大的图形化接口测试应用之间二选一。

由 Magisk-Modules-Alt-Repo 维护（打包自 ducaale 开源的 `xh` 项目）的 **xhhttp** 将广受开发者喜爱的 **xh** 命令行 HTTP 客户端直接移植到了已 Root 的 Android 设备上。作为 HTTPie 的 Rust 高性能复刻版，`xh` 为移动端终端带来了极其顺滑直观的交互体验，让发送网络请求、检查 JSON 负载与测试接口变得轻松高效。

## 语法与实战示例

模块安装后会在系统路径中注册 `xh` 可执行命令，可在任意 Root Shell、Termux 终端或 ADB 会话中直接调用。

### 1. 发送简单 GET 请求并格式化输出
```bash
su -c xh httpbin.org/json
```
*(自动对返回的 JSON 字段、HTTP 状态码及响应头进行缩进排版与语法着色。)*

### 2. 发送 JSON 请求体
无需手动转义繁琐的双引号即可直观构造 JSON 对象：
```bash
su -c xh POST httpbin.org/post name="Android Root" status:=true version:=15
```

### 3. 设置自定义请求头与身份认证
```bash
su -c xh GET api.example.com/user "Authorization: Bearer <token>" "Accept: application/json"
```

### 4. Curl 命令转换模式
想了解某条 `xh` 命令对应的原生 `curl` 等价写法？只需加上 `--curl` 参数：
```bash
su -c xh --curl POST httpbin.org/post user=admin
```

## 安装与验证

1. 从 GitHub Releases 下载最新的 `xh-magisk-module.zip` 压缩包。
2. 在 **Magisk** 中刷入该模块。
3. 重启设备。
4. 在终端中执行以下命令验证可执行文件是否就绪：
   ```bash
   su -c xh --version
   ```
