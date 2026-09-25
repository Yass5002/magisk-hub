---
id: "magisk-wifiadb"
title: "Magisk WiFi ADB: Persistent Wireless Debugging Automation"
sidebarTitle: "Magisk WiFi ADB"
description: "Systemless Magisk utility that automates wireless TCP/IP ADB debugging on boot, providing custom listening ports and background daemon health monitoring."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "magisk wifi adb"
  - "persistent wireless debugging magisk"
  - "mrh929 magisk-wifiadb"
  - "adb connect wifi boot root"
  - "service.adb.tcp.port magisk"
prerequisites:
  - "Rooted Android device with Magisk"
  - "Active Wi-Fi or local area network connection"
conflicts: []
configPaths:
  - "/data/adb/modules/magisk-wifiadb/config"
  - "/data/local/tmp/wifiadb.log"
features:
  - "Persistent boot activation: automatically starts the Android ADB daemon in TCP mode on every system startup"
  - "Configurable listening port: allows setting custom port numbers (1–65535) via a root configuration file to avoid standard port conflicts"
  - "Magisk toggle control: easily pause or activate wireless debugging via the module switch in Magisk Manager"
  - "Live diagnostic logging: writes connection states, network interfaces, and error traces to `/data/local/tmp/wifiadb.log`"
---

## Overview

Magisk-WiFiADB, developed by mrh929, provides developers and power users with permanent, boot-persistent wireless ADB debugging on stock and custom Android ROMs. 

Under standard Android behavior, wireless debugging either toggles off automatically upon reboot, rotates pairing ports randomly (on modern Android versions), or requires tethering the phone via USB cable to run `adb tcpip 5555` after every restart. Magisk-WiFiADB eliminates these friction points by managing the ADB daemon at the system property level, keeping TCP debugging consistently listening on your preferred port across reboots.

## Prerequisites & Compatibility

- **Root Solution**: Magisk (supports all modern versions).
- **Network**: An active Wi-Fi or LAN connection reachable by the host development computer.
- **Android Versions**: Compatible with stock and custom Android ROMs running Magisk.

There are no documented module conflicts.

## How It Operates Under the Hood

The module operates by programmatically managing system properties and the `adbd` service during the late boot phase:
```bash
setprop service.adb.tcp.port <custom_port>
stop adbd
start adbd
```
By restarting `adbd` with `service.adb.tcp.port` bound, the Android ADB daemon listens on all local IP addresses for incoming connections from your workstation.

## Configuration & Usage

### Basic Connection

1. Flash the `magisk-wifiadb.zip` package via Magisk Manager and reboot your device.
2. Ensure your phone and PC are connected to the same Wi-Fi network.
3. Locate your phone's local IP address (in **Settings > About Phone > Status** or your router's client table).
4. From your development PC terminal, connect using the designated port:
   ```bash
   adb connect 192.168.1.150:1234
   ```
5. Confirm the connection and proceed with development commands (`adb logcat`, `adb shell`, `adb install`).
6. To disconnect:
   ```bash
   adb disconnect
   ```

### Custom Port & Logging Configuration

To change the default listening port or enable status logging, create a configuration file at `/data/adb/modules/magisk-wifiadb/config`:

```bash
su
cd /data/adb/modules/magisk-wifiadb/
cat << 'EOF' > config
ADB_PORT=5555
ENABLE_LOG=1
STATUS_CHK_FREQUENCY=10
EOF
```

#### Configuration Options

| Parameter | Accepted Values | Description |
| :--- | :--- | :--- |
| `ADB_PORT` | `1`–`65535` | The TCP port number where ADB daemon listens. |
| `ENABLE_LOG` | `1` (ON) / `0` (OFF) | Enables detailed logging to `/data/local/tmp/wifiadb.log`. |
| `STATUS_CHK_FREQUENCY` | Integer (`> 0`) | Time interval (seconds) between daemon health checks. |

## Troubleshooting & Verification

- **Connection Refused**: Verify that the module is toggled ON in the Magisk Manager module list and that your device has fully finished booting. If you accidentally reboot while the module toggle is OFF, the service will not initialize.
- **Inspecting Module Logs**: If unable to connect, read the runtime log directly from the device:
  ```bash
  cat /data/local/tmp/wifiadb.log
  ```
- **Public Wi-Fi Security Warning**: Avoid leaving WiFi ADB enabled with predictable ports on public or untrusted Wi-Fi networks, as any device on the local network could attempt to connect to your ADB interface.
