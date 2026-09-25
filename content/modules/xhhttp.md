---
id: "xhhttp"
title: "xh: Friendly & Fast HTTP Client for Android Root Terminal"
sidebarTitle: "xh HTTP Client"
description: "Installs xh—the fast, friendly Rust reimplementation of HTTPie—systemlessly on Android for intuitive API requests, JSON formatting, and testing."
category: "system-utilities"
tier: 1
searchQueries:
  - "xh http magisk module"
  - "xh android root"
  - "httpie alternative android terminal"
  - "send http requests termux root"
  - "rust http client android magisk"
prerequisites:
  - "Root access via Magisk"
conflicts: []
configPaths:
  - "/data/adb/modules/xhhttp/"
features:
  - "Rust-powered performance: compiled in Rust for instantaneous binary startup, low memory usage, and high throughput"
  - "Intuitive API syntax: easily construct GET, POST, PUT, and DELETE queries with simplified header and JSON parameter declarations"
  - "Syntax highlighting & JSON formatting: automatically indents and colorizes JSON payloads and HTTP response headers directly in the console"
  - "Session & cookie management: persists authentication cookies and session state across consecutive CLI requests"
  - "Systemless execution: places the xh executable cleanly into /system/bin without modifying core Android partition files"
---

## Overview

Interacting with REST APIs, testing webhooks, or debugging local HTTP services on Android typically requires either the verbose, complex argument syntax of `curl` or bulky graphical API test apps.

Maintained by Magisk-Modules-Alt-Repo (packaging the open-source `xh` project by ducaale), **xhhttp** brings the popular **xh** command-line HTTP client directly to rooted Android devices. Built in Rust to reimplement the beloved user experience of HTTPie, `xh` provides a delightfully intuitive terminal interface for sending web requests, inspecting JSON payloads, and managing REST interactions.

## Syntax & Practical Examples

The executable is named `xh` and operates seamlessly in any root shell, Termux console, or ADB session.

### 1. Simple GET Request with Formatted Output
```bash
su -c xh httpbin.org/json
```
*(Automatically formats and highlights JSON fields, status codes, and response headers).*

### 2. Sending JSON Payloads
Construct JSON objects without escaping tedious quotation marks:
```bash
su -c xh POST httpbin.org/post name="Android Root" status:=true version:=15
```

### 3. Setting Custom Headers & Authentication
```bash
su -c xh GET api.example.com/user "Authorization: Bearer <token>" "Accept: application/json"
```

### 4. Curl Translation Mode
Curious what the corresponding raw curl command looks like? Append `--curl`:
```bash
su -c xh --curl POST httpbin.org/post user=admin
```

## Installation & Verification

1. Download the latest `xh-magisk-module.zip` package from GitHub releases.
2. Flash the module in **Magisk Manager**.
3. Reboot your device.
4. Verify the executable in your terminal:
   ```bash
   su -c xh --version
   ```
