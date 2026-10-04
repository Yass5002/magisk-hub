---
id: "fas-rs"
title: "FAS-RS: Frame-Aware Scheduling Daemon in Rust for Android"
sidebarTitle: "FAS-RS"
description: "Userland performance daemon by shadow3aaa written in Rust that dynamically throttles and boosts CPU/GPU frequencies based on actual frame rendering latency."
category: "performance-kernel"
tier: 1
searchQueries:
  - "fas-rs magisk module"
  - "frame aware scheduling android"
  - "shadow3aaa fas-rs download"
  - "fas-rs games.toml configuration"
  - "android frame rate stabilizer root"
prerequisites:
  - "Android 9.0 (Pie) or newer"
  - "Root access via KernelSU, APatch, or Magisk"
  - "Multi-core SoC with frequency scaling drivers (Qualcomm Snapdragon, MediaTek Dimensity, Google Tensor)"
conflicts:
  - "Static governor locking modules (e.g. Uperf, Scene performance modes overriding cpufreq scaling)"
  - "Aggressive OEM game boosters overriding SurfaceFlinger buffer queues"
configPaths:
  - "/sdcard/Android/fas-rs/games.toml"
  - "/data/adb/modules/fas-rs/"
features:
  - "SurfaceFlinger frame-time monitoring: samples rendering latency directly from Android's compositor"
  - "Dynamic headroom governor: scales hardware power to maintain 60/90/120 FPS targets while minimizing wattage"
  - "Per-game TOML configuration: define custom target refresh rates and power profiles per application package"
  - "Zero kernel patching required: operates completely in userland with broad SoC compatibility"
faq:
  - question: "How does FAS-RS differ from traditional governors like schedutil or performance?"
    answer: "Standard Linux governors scale frequencies based on CPU load percentages, which is blind to actual rendering smoothness. An unoptimized game might hit 100% CPU on an inefficient thread while rendering frames smoothly at 60 FPS, wasting power. FAS-RS measures the exact time taken to render each visual frame: if frames are delivered comfortably within the display refresh budget (e.g. 16.6ms for 60Hz), it gently downclocks hardware to reduce heat."
  - question: "Can I use FAS-RS alongside Scene or Uperf?"
    answer: "No. You should disable performance governor scripts in Scene or uninstall Uperf before running FAS-RS. If another module locks CPU frequencies to maximum or enforces aggressive static governors, it directly interferes with FAS-RS's dynamic frame-time calculations."
  - question: "How do I configure target FPS for a specific game?"
    answer: "Open `/sdcard/Android/fas-rs/games.toml` in any text editor. Under the `[game]` table, add your package name with target frame rate: `\"com.miHoYo.GenshinImpact\" = 60`. Save the file; FAS-RS will reload rules automatically without restarting."
---

## Overview

Traditional mobile CPU governors (such as `schedutil`, `interactive`, and `ondemand`) determine processor clock speeds strictly by measuring execution runqueue load and task waiting times. While effective for general computing, this paradigm is fundamentally flawed for mobile gaming and graphic workloads:

1. **Wattage Waste**: A game thread executing busy-wait loops may push a CPU core to 100% utilization, prompting standard governors to lock maximum clock frequencies—generating extreme heat and thermal throttling—even when the display is already saturated at a solid 60 FPS.
2. **Thermal Throttling**: Unnecessary clock boosts trigger device thermal limits, causing sudden frequency cliffs and frame drops.
3. **Stutter Spikes**: Conversely, if a complex scene arrives, standard governors often react too late to deliver the burst required for frame deadlines.

**FAS-RS** (Frame Aware Scheduling in Rust), developed by shadow3aaa, inverts this approach. Instead of guessing performance needs from kernel load heuristics, FAS-RS positions its controller from the user's perspective: it directly monitors Android's graphics compositor (**SurfaceFlinger**) to observe whether frames are meeting their physical delivery deadlines.

---

## Technical Architecture & Working Mechanics

FAS-RS runs as a standalone daemon written in Rust running with root privileges:

```
┌────────────────────────────────────────────────────────┐
│                   Android Display                      │
│            (e.g., 120Hz Target = 8.33ms)               │
└───────────────────────────▲────────────────────────────┘
                            │ Displays frame
┌───────────────────────────┴────────────────────────────┐
│                    SurfaceFlinger                      │
│  - Measures Frame Presentation & VSYNC Timestamps      │
└───────────────────────────┬────────────────────────────┘
                            │ Real-time frame latency metrics
┌───────────────────────────▼────────────────────────────┐
│                     fas-rs Daemon                      │
│  - Calculates Frame Delivery Margin:                   │
│    * If frame render < 6.0ms: Downclock (save heat)    │
│    * If frame render > 8.0ms: Instant boost headroom   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│             Kernel cpufreq & devfreq Nodes             │
│  /sys/devices/system/cpu/cpufreq/policy*/              │
└────────────────────────────────────────────────────────┘
```

1. **Metric Acquisition**: FAS-RS hooks into SurfaceFlinger's buffer queue and timestamp statistics, calculating the exact microsecond duration taken by the GPU and CPU to render each frame.
2. **Margin Calculation**: If the frame is completed significantly ahead of the VSYNC deadline (headroom is positive), FAS-RS lowers CPU and GPU clock states.
3. **Zero Jitter Response**: If frame presentation approaches the deadline threshold, FAS-RS instantly scales clock speeds to prevent dropped frames.

---

## Installation & Setup

### Prerequisites
- KernelSU, APatch, or Magisk.
- Android 9 or newer.

### Installation Steps
1. Download `fas-rs.zip` from the official GitHub release.
2. Flash the module in your root manager (Magisk, KernelSU, or APatch).
3. Reboot your device.
4. The daemon will initialize automatically on boot and create default configuration files in `/sdcard/Android/fas-rs/`.

---

## Configuration: `games.toml`

FAS-RS reads its per-game configuration from `/sdcard/Android/fas-rs/games.toml`:

```toml
# Default configuration
[config]
mode = "balance" # Options: "powersave", "balance", "performance", "fast"

# Target frame rates per package
[game]
"com.miHoYo.GenshinImpact" = 60
"com.activision.callofduty.shooter" = 120
"com.pubg.imobile" = 90
```

- When you launch a listed application, FAS-RS automatically engages.
- When you exit the application, FAS-RS automatically releases frequency clamps back to stock operating system defaults.

---

## Troubleshooting & Verification

### Verifying Daemon Status
Open any terminal emulator with root:
```bash
su
# Check running process:
ps -ef | grep fas-rs

# Inspect live log output:
cat /sdcard/Android/fas-rs/fas_log.txt
```

### Module Conflicts
If you experience micro-stutters or unpredictable frame drops:
- Ensure no other performance modules (Uperf, Scene Performance Service, Thermal Modifiers) are actively forcing governor policies.
- Disable aggressive battery saver apps that throttle background thread execution.

### Emergency Uninstallation
```bash
rm -rf /data/adb/modules/fas-rs
rm -rf /sdcard/Android/fas-rs
reboot
```
