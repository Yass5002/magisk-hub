---
id: "kpatch-next-module"
title: "KPatch-Next：动态内核热补丁模块"
sidebarTitle: "KPatch-Next"
description: "适用于 KernelSU-Next 的内核热补丁（Live-Patching）模块，支持在无需重启的情况下动态修改运行中的内核函数。"
category: "root-management"
tier: 1
searchQueries:
  - "kpatch next magisk 模块"
  - "安卓内核热补丁 live patching"
  - "kernelsu next kpatch 使用指南"
  - "root 安卓动态内核 hook"
  - "kpatch 模块下载"
prerequisites:
  - "KernelSU-Next 或兼容的内核环境"
  - "Linux 5.10+ 内核（推荐使用 GKI 架构）"
conflicts:
  - "不支持 ftrace / livepatch 的旧版非 GKI 3.18/4.4 内核"
configPaths:
  - "/data/adb/kpatch/"
  - "/data/adb/modules/kpatch-next-module/"
features:
  - "基于 Linux ftrace 与 kprobes 实现内存级动态内核函数修补"
  - "无需重启操作系统即可应用安全补丁、SELinux 策略修改及挂载点 Hook"
  - "配套命令行工具，支持热加载、检查与卸载内核热补丁"
  - "专为现代 KernelSU-Next 生态工程化打造"
faq:
  - question: "Android 上的内核热补丁有什么作用？"
    answer: "内核热补丁允许开发者与高级用户在设备运行期间直接修改内存中的内核函数。常用于测试安全绕过、免重刷 boot.img 修复漏洞，以及按需动态调整内核行为。"
  - question: "错误的 kpatch 补丁会导致设备崩溃吗？"
    answer: "会。由于热补丁直接运行在 Ring 0（内核空间），补丁中的无效内存解引用会直接引发内核恐慌（Kernel Panic）并导致设备立即重启。KernelSU-Next 内置安全模式保护机制，检测到异常重启时会自动解除补丁挂钩。"
---

## 概述

**KPatch-Next** 由 **KernelSU-Next** 开发团队维护，是一款将 Linux 内核热补丁技术引入已 Root Android 手机的进阶模块。

传统方式下，任何对 Linux 内核的改动（例如调整文件系统行为、禁用安全检查或修改硬件驱动）都需要改动内核源码、在电脑端重新编译 `boot.img`，再通过 Fastboot 刷入设备。KPatch-Next 借助 Linux 内核原生的热补丁基础设施（`kpatch` / `ftrace`），可在设备运行期间将编译好的二进制补丁实时应用到目标内核函数中。

---

## 技术架构与工作原理

### 基于 Ftrace 的函数重定向

1. **内核符号解析**：KPatch-Next 读取 `/proc/kallsyms` 以定位目标内核函数的内存地址。
2. **跳板指令注入**：利用内核内置的 `ftrace`（Function Tracer）子系统，KPatch-Next 将目标函数入口指令替换为无条件跳转指令，指向新的替换代码。
3. **安全切换执行**：当 Android 内核中任意线程进入原函数时，执行流会瞬间跳转至已修补代码块，完全绕过原始逻辑。
4. **干净卸载恢复**：运行时可随时动态停用补丁，恢复原始内核指令且不残留任何修改痕迹。

---

## 安装与命令行用法

1. 在 **KernelSU-Next** 或 **APatch** 中刷入 `kpatch-next-module-vX.zip`。
2. 重启设备。
3. 在具备 Root 权限的终端（如 **Termux**）中执行命令：
   ```bash
   # 列出当前已激活的内核补丁：
   su -c "kpatch list"

   # 加载已编译的内核补丁模块：
   su -c "kpatch load /data/adb/kpatch/my_patch.ko"

   # 卸载指定补丁：
   su -c "kpatch unload my_patch"
   ```
