---
id: "touch-optimization-turbo"
title: "Touch Optimization Turbo: Low-Latency SurfaceFlinger and Touch Pipeline"
sidebarTitle: "Touch Optimization"
description: "Display rendering and input subsystem tuning module that minimizes Android SurfaceFlinger compositor latency and optimizes touch sampling rates on high-refresh-rate displays."
category: "performance-kernel"
tier: 1
searchQueries:
  - "touch optimization magisk"
  - "surfaceflinger low latency tweak"
  - "android reduce touch delay"
  - "disable backpressure surfaceflinger"
prerequisites:
  - "Magisk 20.4+, KernelSU, or APatch"
  - "Android 9.0 (Pie) through Android 14"
conflicts:
  - "Other modules overriding SurfaceFlinger buffer counts or VSync phase offsets"
configPaths:
  - "/data/adb/modules/boot/system.prop"
features:
  - "Caps compositor buffer queue to double-buffering (max_frame_buffer_acquired_buffers=2) to eliminate up to 16ms of rendering lag"
  - "Enables latch_unsignaled to latch incoming frames without waiting for fence synchronization"
  - "Disables backpressure propagation across high-refresh-rate panels (90Hz/120Hz/144Hz) to avoid dropped frames"
  - "Activates Qualcomm QTI input optimizations with reduced movetouchslop thresholds"
  - "Increases window manager dispatch capacity to 500 events per second"
faq:
  - question: "Does this module alter touch sampling hardware rates?"
    answer: "No. Physical touch sampling rates (such as 240Hz, 360Hz, or 480Hz) are hardware-controlled by the digitizer controller and touch firmware. Touch Optimization Turbo alters how the Linux kernel and Android SurfaceFlinger compositor handle touch events once delivered to user space, reducing software pipeline buffering."
  - question: "Is this module compatible with MediaTek or Tensor chipsets?"
    answer: "The SurfaceFlinger, WindowManager, and View touch slop properties function identically across all Android devices regardless of chipset. The persist.vendor.qti.inputopts properties specifically target Qualcomm Snapdragon hardware and are benignly ignored on other platforms."
---

## Overview

**Touch Optimization Turbo** (authored by Xiaojian) is a systemless performance module focused on reducing input-to-display latency across the Android rendering pipeline.

In stock Android configurations, the graphics subsystem frequently relies on triple-buffering (`debug.egl.buffcount=4`, triple buffer SurfaceFlinger queues) to guard against UI micro-stutters during heavy GPU workloads. While triple-buffering prevents frame tearing, holding queued buffers can add 16ms to 33ms of end-to-end touch latency, making user interactions feel slightly detached or floaty compared to tighter touch subsystems.

Touch Optimization Turbo reconfigures the SurfaceFlinger composition pipeline, VSync alignment offsets, and Qualcomm input event filters to prioritize immediate frame delivery and precision finger tracking.

---

## Technical Architecture & How It Works

The module functions via systemless property injection defined in `system.prop`:

### 1. SurfaceFlinger Pipeline & Buffer Cap

- **Double-Buffering Enforcement**:
  ```properties
  ro.surface_flinger.max_frame_buffer_acquired_buffers=2
  debug.gr.numframebuffers=2
  ```
  By restricting the maximum acquired buffers in the frame buffer queue to two, SurfaceFlinger renders frames in an immediate pipeline rather than buffering an extra frame ahead of time, directly trimming display lag.

- **Backpressure Disablement**:
  ```properties
  debug.sf.disable_backpressure=1
  ```
  Prevents backpressure propagation from throttling the display driver during transient composition spikes, maintaining stable frame pacing on 90Hz, 120Hz, and 144Hz displays.

- **Unsignaled Frame Latching**:
  ```properties
  debug.sf.latch_unsignaled=1
  ```
  Instructs SurfaceFlinger to latch buffer contents immediately when available rather than awaiting explicit fence signaling, decreasing the render-to-screen interval.

### 2. Touch Subsystem & Qualcomm Input Options

- **Touch Movement Slop**:
  ```properties
  view.touch_slop=15
  persist.vendor.qti.inputopts.enable=true
  persist.vendor.qti.inputopts.movetouchslop=0.001
  ```
  Lowers the minimum movement threshold (`touch_slop`) required before the Android framework recognizes a continuous swipe or drag gesture, providing immediate tactile response in fast-paced gaming and rapid scrolling.

- **Event Dispatch Throughput**:
  ```properties
  windowsmgr.max_events_per_sec=500
  ```
  Expands the WindowManager's event dispatch queue limit up to 500 events per second, accommodating high-frequency touch reports from modern capacitive screens without queue bottlenecks.

---

## Verification & Monitoring

To verify that the module properties are actively loaded in the Android runtime, execute the following command in a terminal:

```bash
getprop | grep -E "surface_flinger|touch_slop|qti.inputopts"
```

The output should confirm `max_frame_buffer_acquired_buffers=2` and `debug.sf.disable_backpressure=1`.
