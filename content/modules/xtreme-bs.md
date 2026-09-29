---
id: "xtreme-bs"
title: "Xtreme Battery Saver: Event-Driven Root Power Controls"
sidebarTitle: "Xtreme Battery Saver"
description: "Configure event-driven CPU, app, Wi-Fi, Doze, and process power controls on rooted Android devices."
category: "performance-kernel"
tier: 1
searchQueries:
  - "xtreme battery saver magisk"
  - "DethByte64 XtremeBS"
  - "android root battery optimization event driven"
  - "XBSctl magisk"
  - "XtremeBS WebUI"
prerequisites:
  - "Rooted Android device with Magisk or KernelSU"
  - "A device and ROM suitable for testing system power-management changes"
  - "ADB or recovery access for recovery from an unsafe configuration"
  - "A backup of the XtremeBS configuration before changing aggressive options"
conflicts:
  - "Other battery or performance modules that modify the same CPU, app, Doze, Wi-Fi, or process settings"
  - "Aggressive settings such as disable_cores, low_ram, doze, or app suspension when essential apps are not allowlisted"
configPaths:
  - "/data/local/tmp/XtremeBS/XtremeBS.conf"
  - "/data/local/tmp/XtremeBS/XtremeBS.status"
  - "/sdcard/XtremeBS.log"
  - "/data/adb/modules/XtremeBS/"
features:
  - "Event-driven v2 configuration for boot, charging, screen_off, low_power, manual, and custom events"
  - "CPU core and governor controls with configurable app and process handling"
  - "Doze, Wi-Fi, low-RAM, and Google Mobile Services controls"
  - "XBSctl command-line control with reload, pause, resume, and safe-mode commands"
  - "Optional localhost WebUI on port 8081 in the upstream v1.0.6+ documentation"
faq:
  - question: "Is XtremeBS plug-and-play?"
    answer: "No. The upstream README describes it as an advanced configurable module. Start with the default configuration, enable one change at a time, and test before enabling aggressive options."
  - question: "What should I do if the device becomes unstable?"
    answer: "Use the upstream safe-mode path, such as `adb shell XBSctl safe`, when ADB remains available. The README also documents setting `safemode=1` in the configuration from recovery. Disable risky options and restore the previous configuration."
  - question: "Which settings are especially risky?"
    answer: "The upstream documentation warns about disable_cores, low_ram, Doze, app suspension, process reprioritization, and Wi-Fi disabling. It specifically advises avoiding disable_cores and handle_cores on Samsung devices and low_ram on OnePlus devices."
  - question: "How do configuration changes take effect?"
    answer: "After editing the configuration, run `XBSctl reload` or reboot. In v2, verify the event name and block syntax; in v1, use the legacy key/value format."
  - question: "Does XtremeBS guarantee a specific battery-life increase?"
    answer: "No. The upstream page mentions a possible increase but also says results depend on the device and configuration. Magisk Hub makes no battery-life guarantee."
---

## Overview

**Xtreme Battery Saver (XtremeBS)** is a root module for configurable power-management behavior. Its documented controls include CPU cores, app handling, process priority, Doze, Wi-Fi, low-RAM mode, and Google Mobile Services. It supports both Magisk and KernelSU according to the upstream README.

This is an aggressive tuning tool, not a universal battery fix. The upstream project warns that poor settings can cause lag, missed notifications or alarms, SystemUI crashes, and device instability. Compatibility varies by device and ROM; the project says it was tested primarily on a Pixel 5 running ProtonAOSP.

## Installation

1. Download the current `XtremeBS.zip` release.
2. Flash it through Magisk or KernelSU.
3. Reboot.
4. Review the generated configuration before enabling non-default behavior.

The module starts its daemon in late-start service mode after Android boot completes. The release includes the `XBSctl` command-line utility and an optional WebUI launcher script.

## Configuration

The configuration file is:

```text
/data/local/tmp/XtremeBS/XtremeBS.conf
```

The upstream project documents two formats:

- **v1:** legacy `key=value` settings controlled by a single trigger.
- **v2:** recommended event blocks such as `boot`, `charging`, `screen_off`, `low_power`, `manual`, or a custom event.

A minimal v2 example from the upstream documentation is:

```text
version=2
delay=3
log_file=/sdcard/XtremeBS.log
log_level=3

screen_off={
  handle_apps=nice
}
```

Reload after editing:

```sh
su -c XBSctl reload
```

Custom events can be started manually:

```sh
su -c "XBSctl start my_event"
```

The upstream documentation says multiple event blocks can stack, so overlapping changes should be planned carefully.

## Controls and safety

The most consequential controls include:

- `disable_cores`: disables selected or automatically selected CPU cores.
- `handle_apps`: can kill, lower priority, or suspend apps.
- `handle_proc`: changes process priority and can delay background work.
- `doze`: forces light or deep Doze and may affect alarms.
- `kill_wifi`: disables Wi-Fi.
- `low_ram`: enables Android low-RAM behavior.
- `handle_gms`: can affect Google services; killing GMS can break Google apps and Play Integrity.

Use an allowlist when suspending apps. Include essential apps such as the keyboard and terminal before testing. Start with one change, observe the device, and keep a recovery route available.

## WebUI and logs

The upstream README documents a WebUI for v1.0.6+ launched through the module action script at:

```text
http://127.0.0.1:8081
```

The documented status and log locations are:

```text
/data/local/tmp/XtremeBS/XtremeBS.status
/sdcard/XtremeBS.log
```

Increase `log_level` when diagnosing behavior, then restore a quieter level after troubleshooting.

## Recovery and troubleshooting

If the device is still responsive through ADB:

```sh
adb shell XBSctl safe
```

This is documented as stopping XtremeBS and unsuspending apps. If ADB is unavailable, the upstream README documents booting recovery and setting `safemode=1` in `/data/local/tmp/XtremeBS/XtremeBS.conf`, then rebooting.

Device-specific cautions from upstream:

- Avoid `disable_cores` and `handle_cores` on Samsung devices.
- Avoid `low_ram` on OnePlus devices.
- Disable or coordinate overlapping features in other battery/performance modules.

## Sources

- [Upstream README](https://github.com/DethByte64/Xtreme-Battery-Saver)
- [Upstream releases](https://github.com/DethByte64/Xtreme-Battery-Saver/releases)
- [Upstream source](https://github.com/DethByte64/Xtreme-Battery-Saver)
