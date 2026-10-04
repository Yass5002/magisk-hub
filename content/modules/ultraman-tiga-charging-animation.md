---
id: "ultraman-tiga-charging-animation"
title: "Ultraman Tiga Lockscreen Charging Animation & Audio: Technical Guide"
sidebarTitle: "Tiga Charging FX"
description: "Vendor overlay RRO module replacing lockscreen battery charging graphics and audio effects with Ultraman Tiga Spark Lens transformation visual dynamics."
category: "customization-ui"
tier: 1
searchQueries:
  - "ultraman tiga charging animation magisk"
  - "miui charging animation mod"
  - "vendor overlay charging fx root"
  - "spark lens charging animation android"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "MIUI 12, 13, 14, or HyperOS with stock lockscreen framework"
conflicts:
  - "Other charging animation overlay modules targeting vendor lockscreen resources"
configPaths:
  - "/system/vendor/overlay/充电动画.apk"
  - "/data/adb/modules/ChargeChange/uninstall.sh"
features:
  - "Custom Spark Lens energetic light animation replacing default charging bubble"
  - "Authentic Ultraman transformation sound effect triggered upon power connection"
  - "Pure Runtime Resource Overlay (RRO) design requiring zero binary bytecode modification"
  - "Includes clean uninstallation script for complete stock lockscreen restoration"
faq:
  - question: "Does this mod affect turbo charge or fast charging indicators?"
    answer: "No. The module modifies the presentation drawables and audio triggers in the lockscreen UI overlay; hardware battery charge negotiation and quick-charge protocol handshakes remain completely untouched."
  - question: "Which ROMs are compatible?"
    answer: "The overlay specifically targets Xiaomi MIUI and HyperOS lockscreen resource identifiers. AOSP-based custom ROMs that do not share the Xiaomi SystemUI keyguard assets will ignore the overlay safely."
---

## Overview

**Ultraman Tiga Charging Animation & SFX** (authored by Fu Chen Ran Xi / 酷安@浮尘染溪) transforms the standard device lockscreen battery connection experience into an energetic tribute to Ultraman Tiga's iconic transformation sequence.

Using Android's native **Runtime Resource Overlay (RRO)** framework, this module swaps the stock OEM charging visual assets and connection sound effects cleanly without altering system APK signatures or modifying core system libraries.

---

## Technical Architecture & How It Works

### 1. Runtime Resource Overlay (RRO) Injection

Android's overlay subsystem allows resource replacement at runtime without modifying the base application package. The module injects:

```text
/system/vendor/overlay/
└── 充电动画.apk
```

Inside `充电动画.apk`, the manifest declares target priority and target package specification:

```xml
<overlay
    android:targetPackage="com.android.systemui"
    android:targetName="MiuiKeyguardChargeAnimation"
    android:priority="100"
    android:isStatic="true" />
```

### 2. Asset Replacement & Animation Dynamics

When the battery driver reports `ACTION_POWER_CONNECTED` via `BatteryManager`, SystemUI inflates the keyguard charging view. The overlay overrides the following resources:

- **Vector & Lottie Drawables**: Replaces the concentric battery charge rings with the multi-stage crystalline Spark Lens energy transformation sequence.
- **Audio Effects**: Swaps the stock subtle charging chime with the iconic Ultraman crystal activation audio effect.

### 3. Systemless Reversibility

The module includes an automated `uninstall.sh` script that cleans up temporary overlay caches in `/data/resource-cache/` upon module deletion, preventing residual graphical artifacts.

---

## Installation & Verification

1. Install via Magisk, KernelSU, or APatch.
2. Reboot the smartphone.
3. Lock the screen and connect a charging cable. The Tiga transformation animation will illuminate the display with custom audio.
