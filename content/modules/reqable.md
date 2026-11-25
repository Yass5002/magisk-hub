---
id: "reqable"
title: "Reqable: All-in-One Android HTTP/HTTPS MITM Capture & API Debugger"
sidebarTitle: "Reqable"
description: "High-performance Android HTTP/HTTPS/HTTP3 MITM traffic sniffer and API testing client supporting rootless local VPN capture as well as Root/Magisk system CA installation."
category: "networking-proxies"
tier: 1
searchQueries:
  - "reqable apk android download"
  - "reqable magisk system certificate"
  - "android http mitm proxy capture root"
  - "reqable android 14 apex cacerts"
  - "com.reqable.android"
prerequisites:
  - "64-bit ARM (`arm64-v8a`) Android device"
  - "Rootless local VPN mode works out of the box; Root (Magisk, KernelSU, or APatch) required for system-level CA trust and transparent interception"
conflicts:
  - "Simultaneous active Android `VpnService` apps (VPN tunnels, ad-blockers, or other capture tools) when using Rootless VPN mode"
  - "Applications enforcing strict TLS certificate pinning without SSL unpinning hooks"
configPaths:
  - "/data/data/com.reqable.android/"
  - "/system/etc/security/cacerts/"
  - "/apex/com.android.conscrypt/cacerts/"
features:
  - "Dual capture architecture: Rootless `NetbareVpnService` local VPN capture and Root-assisted system CA / transparent proxy workflows"
  - "Native-accelerated networking stack (`libreqable_netbare.so`, `libreqable_cronet.so`, `libtun2proxy.so`) supporting HTTP/1.1, HTTP/2, HTTP/3, WebSocket, and SSE"
  - "Interactive MITM debugging: live breakpoints, request/response rewriting, replay, HAR import/export, and custom scripting"
  - "Integrated API testing client with collections, scoped environment variables, and desktop QR/Wi-Fi pairing + MCP support"
faq:
  - question: "Why should I use Root/Magisk with Reqable instead of Rootless VPN mode?"
    answer: "Since Android 7.0 (Nougat), apps target API 24+ and ignore user-installed CA certificates by default unless their `network_security_config.xml` explicitly opts in. In Rootless mode, Reqable captures packets via `NetbareVpnService`, but HTTPS decryption fails for those apps. With Magisk, KernelSU, or APatch, Reqable's CA certificate can be installed into the system trust store (including Android 14+ `/apex/com.android.conscrypt/cacerts` via a root CA module), enabling HTTPS MITM inspection across standard apps."
  - question: "Is Reqable open source?"
    answer: "No. As stated in the official `Reqable/reqable-app` repository, Reqable is a closed-source proprietary tool; the GitHub repository is used for issue tracking, documentation, and official release APK distribution. Most core capture and API testing features are free in the Community edition."
  - question: "Can Reqable bypass SSL Pinning on its own?"
    answer: "Installing a system CA certificate solves standard OS trust verification, but apps implementing custom certificate pinning (OkHttp `CertificatePinner`, Flutter BoringSSL, or native TLS libraries) will still reject MITM proxies. For pinned targets, pair Reqable with an Xposed/Frida unpinning tool such as TrustMeAlready or Frida scripts."
---

## Overview

**Reqable** (`com.reqable.android`) is a cross-platform API debugging and HTTP(S) traffic analysis suite that unifies **MITM packet capture** (similar to Charles or Fiddler) with an **API testing client** (similar to Postman). On Android, it runs natively on `arm64-v8a` without requiring a desktop computer, while also pairing seamlessly with desktop Reqable instances over Wi-Fi.

---

## Technical Architecture & Capture Modes

Inspecting `reqable-app-android-arm64.apk` shows a Flutter UI backed by a high-throughput native C/C++/Rust-style networking core (`libnetbare-jni.so`, `libreqable_netbare.so`, `libtun2proxy.so`, `libreqable_cronet.so`, `libreqable_http.so`, `libreqable_protobuf.so`, `libreqable_brotli.so`, `libreqable_zstd.so`, and `libobjectbox-jni.so` for fast local persistence).

### 1. Rootless Local VPN Mode (`NetbareVpnService`)

- Uses Android's `android.net.VpnService` (`com.reqable.android.NetbareVpnService`) to create a local loopback tunnel on the device and route app traffic into Reqable's MITM engine without modifying system partitions.
- **Limitation**: Only apps that trust user-installed CA certificates (or unencrypted HTTP traffic) can be decrypted cleanly on Android 7+. Additionally, apps that inspect `ConnectivityManager` for `TRANSPORT_VPN` can detect an active VPN interface.

### 2. Root / Magisk / KernelSU Enhanced Mode

- **System CA Store Injection**: With Root access (or companion system-cert Magisk modules on Android 14+ where Conscrypt certificates live inside `/apex/com.android.conscrypt/cacerts/`), Reqable's root CA is trusted globally by all apps using standard Android `TrustManager` APIs.
- **Transparent Proxy / Desktop Forwarding**: Rooted setups avoid user-CA trust rejections and allow flexible proxy routing or collaborative forwarding to Reqable Desktop without fighting VPN-detection checks.

---

## Installation & Configuration

1. Download `reqable-app-android-arm64.apk` and install it on your `arm64-v8a` Android device.
2. **For Rootless Testing**: Open Reqable, follow the guided certificate installation to install the CA certificate into **User Credentials**, and grant the local VPN permission when prompted.
3. **For Rooted Devices (Android 7–13)**: Export or install Reqable's root CA certificate using Reqable's root certificate prompt or move the `.0` hashed PEM into `/system/etc/security/cacerts/` via a Magisk module.
4. **For Rooted Devices (Android 14–16+ APEX Conscrypt)**: Install the Reqable CA as a user cert first, then use a systemless Conscrypt cert-sync module (e.g., MagiskTrustUserCerts / Movecert-style modules) so `/apex/com.android.conscrypt/cacerts/` mirrors it across Zygote namespaces.
5. Configure target app filters, breakpoints, rewrite rules, or Python-compatible scripts directly inside the **Debugging** tab.

---

## Common Issues & Troubleshooting

- **HTTPS Traffic Shows `TLS Handshake Failed` or `Unknown CA`**: The target app targets Android 7+ and ignores User CAs. Move the Reqable CA into the System store (and verify `/apex/com.android.conscrypt/cacerts/` on Android 14+) or test on a debuggable build.
- **Cannot Capture While Using Another VPN**: Android permits only one active `VpnService` at a time. Disable WireGuard, AdGuard VPN, or Clash before starting Reqable's local VPN capture, or switch to proxy/transparent routing on rooted devices.
- **Specific Apps Have No Internet During Capture**: The app likely enforces SSL Pinning (e.g., OkHttp `CertificatePinner` or Cronet pinning). Exclude the app from Reqable's MITM scope if you do not need to inspect it, or apply an unpinning module in LSPosed/Frida.
