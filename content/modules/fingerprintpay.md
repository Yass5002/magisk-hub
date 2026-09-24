---
id: "fingerprintpay"
title: "FingerprintPay: Enable Biometric Payment on Custom ROMs"
sidebarTitle: "FingerprintPay"
description: "Bridges standard Android BiometricPrompt APIs to proprietary payment services (Alipay, WeChat Pay, QQ) on rooted and custom AOSP ROMs."
category: "customization-ui"
tier: 1
searchQueries:
  - "fingerprintpay magisk module"
  - "alipay fingerprint payment custom rom"
  - "wechat biometric pay rooted android"
  - "eritpchy fingerprintpay guide"
  - "ifaas service bridge android"
prerequisites:
  - "Android 8.0 through Android 15"
  - "Root access via Magisk, KernelSU, or APatch"
  - "LSPosed or Vector framework active"
conflicts:
  - "Devices already running stock Chinese OEM ROMs (MIUI/ColorOS) with factory IFAA/Soter blobs"
configPaths:
  - "/data/adb/modules/fingerprintpay/"
  - "/data/user/0/org.sugar.fingerprintpay/"
features:
  - "Emulates proprietary OEM IFAA (Internet Finance Authentication Alliance) and Soter security daemons"
  - "Translates Alipay and WeChat Pay proprietary biometric handshakes to standard Android KeyStore and BiometricPrompt"
  - "Restores instant fingerprint and face authentication in financial payment apps on AOSP, LineageOS, and Pixel Experience"
  - "Includes dedicated companion app for diagnostic key generation and validation"
faq:
  - question: "Why do payment apps like Alipay refuse fingerprint setup on custom ROMs?"
    answer: "Payment providers in certain regions mandate hardware-signed vendor security tokens (IFAA / Tencent Soter) embedded in stock OEM vendor partitions. When flashing AOSP or LineageOS, these proprietary services are missing. FingerprintPay emulates the IFAA interface, routing authentication requests to the native Android Biometric API."
  - question: "Is this secure?"
    answer: "FingerprintPay relies entirely on Android's secure BiometricPrompt and KeyStore hardware cryptography. It does not bypass fingerprint authentication; it merely bridges the proprietary vendor protocol to the standard Android OS security framework."
---

## Overview

Developed by **eritpchy**, **FingerprintPay** is a critical customization module for users of custom ROMs (such as LineageOS, PixelOS, crDroid, or Paranoid Android) who utilize Asian financial payment platforms like **Alipay**, **WeChat Pay**, and **QQ Wallet**.

Stock firmware from OEMs like Xiaomi, OnePlus, Oppo, and Vivo includes proprietary hardware authentication daemons (IFAA and Tencent Soter) that sign biometric payment transactions. When flashing an AOSP-based custom ROM, these proprietary vendor services are absent, causing payment apps to permanently disable fingerprint authentication. FingerprintPay provides a software translation bridge, enabling standard Android biometrics inside these payment gateways.

---

## Technical Architecture & How It Works

### IFAA & Soter Protocol Emulation

1. **Service Emulation**: The module injects mock system services into Android's system server, declaring availability of `org.ifaa.android.manager.IFAAManager` and `com.tencent.soter.core.model.SoterCore`.
2. **KeyStore Signature Mapping**: When Alipay or WeChat requests a signed payment attestation token, FingerprintPay invokes Android's standard `KeyStore` to generate an asymmetric key pair protected by `KeyGenParameterSpec.Builder(..., PURPOSE_SIGN).setUserAuthenticationRequired(true)`.
3. **BiometricPrompt Handshake**: The user is presented with the standard system fingerprint dialog. Upon successful hardware verification, the cryptographic key signs the payment payload and returns the expected token to the payment app.

---

## Installation & Setup

1. Ensure **Vector** or **LSPosed** is installed and running.
2. Install the `FingerprintPay.apk` application.
3. Open **Vector Manager** $\rightarrow$ enable **FingerprintPay** $\rightarrow$ set scope to include **System Framework**, **Alipay**, and **WeChat**.
4. Reboot your phone.
5. Open the **FingerprintPay** app and verify that both IFAA and Soter service tests pass.
6. Open your payment app, navigate to **Settings** $\rightarrow$ **Biometrics / Fingerprint Payment**, and toggle on fingerprint verification.
