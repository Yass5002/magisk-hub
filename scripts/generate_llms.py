#!/usr/bin/env python3
"""
Generate English (public/llms.txt, public/llms-full.txt) and
Simplified Chinese (public/zh/llms.txt, public/zh/llms-full.txt)
from modules/*.json and locales/zh/modules/*.json.
"""

import glob
import json
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODULES_DIR = os.path.join(REPO_ROOT, 'modules')
ZH_LOCALES_DIR = os.path.join(REPO_ROOT, 'locales', 'zh', 'modules')
PUBLIC_DIR = os.path.join(REPO_ROOT, 'public')

ZH_CATEGORIES = {
    'root-management': ('Root 管理与隐藏', '核心 su 守护进程、Zygisk 注入引擎、Root 环境隐藏与 Play Integrity 认证绕过工具。'),
    'performance-kernel': ('性能与内核调校', 'CPU/GPU 调度器优化、温控策略调整与游戏帧率性能增强模块。'),
    'system-environment': ('系统环境与框架增强', 'Systemless 系统框架微调、OEM 专属功能解锁与系统级特性修改。'),
    'customization-ui': ('界面定制与美化', '状态栏、手势导航、桌面启动器及系统外观视觉定制模块。'),
    'development-instrumentation': ('开发调试与逆向插桩', '动态 Hook 框架、Frida 注入服务端、系统抓包调试与逆向分析工具。'),
    'system-utilities': ('系统实用工具', '通话录音、自动清理、后台管理、磁盘挂载与终端效率增强工具。'),
    'networking-proxies': ('网络与透明代理', 'Systemless 广告拦截、TPROXY 透明代理网关与隐私 DNS 重定向模块。'),
    'security-certificates': ('安全与证书管理', '系统级 CA 根证书信任注入、设备标识符伪装与隐私安全防护模块。'),
    'xposed-runtime-hooks': ('Xposed 与运行时 Hook', 'ART 运行时方法挂钩、签名校验绕过与应用逻辑增强模块。'),
    'audio-dsp-acoustics': ('音频 DSP 与声学增强', '系统全局均衡器、音频驱动调音、Mixer 通路修改与杜比全景声移植。'),
    'system-typography-fonts': ('系统字体与排版', '无侵入式系统字体替换、CJK 中日韩字符集补全与 Emoji 表情包替换模块。'),
    'battery-power-charging': ('电池与充电控制', '高级充电阈值开关、旁路供电（Idle Mode）、PPS 快充协议解锁与功耗监控。'),
    'boot-animations-ui': ('开机动画与启动画面', '自定义开机动画、Pixel 原生开机特效与充电/启动界面美化模块。'),
}


def load_zh_overrides():
    overrides = {}
    for f in glob.glob(os.path.join(ZH_LOCALES_DIR, '*.json')):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                d = json.load(fp)
            if d.get('id'):
                overrides[d['id']] = d
        except Exception as e:
            print(f"Error loading zh override {f}: {e}")
    return overrides


def generate():
    files = sorted(glob.glob(os.path.join(MODULES_DIR, '*.json')))
    modules = []
    for f in files:
        if os.path.basename(f) == 'schema.json':
            continue
        with open(f, 'r', encoding='utf-8') as fp:
            try:
                modules.append(json.load(fp))
            except Exception as e:
                print(f"Error loading {f}: {e}")

    modules.sort(key=lambda m: (-m.get('stars', 0), m.get('name', '')))
    total_count = len(modules)
    zh_overrides = load_zh_overrides()

    # 1. Generate public/llms-full.txt (English)
    lines_full = [
        '# Magisk Hub - Full Module Catalog (llms-full.txt)',
        '',
        f'> Complete directory of {total_count} community-maintained root modules and extensions for Magisk, KernelSU, APatch, and LSPosed.',
        '',
        'Website: https://magisk.yssn.tech/',
        'Chinese Version: https://magisk.yssn.tech/zh/',
        'Repository: https://github.com/Yass5002/magisk-hub',
        '',
        '## Complete Module Index',
        ''
    ]

    for m in modules:
        mid = m.get('id', '')
        name = m.get('name', '')
        desc = m.get('description', '')
        compat = ', '.join(m.get('compatibility', []))
        stars = m.get('stars', 0)
        tag = m.get('latestRelease', {}).get('tag', '')
        download = m.get('latestRelease', {}).get('downloadUrl', '')
        repo = m.get('repo') or ''
        source_type = m.get('sourceType', 'github' if repo else 'community')
        category = m.get('category', '')
        software_type = m.get('softwareType', 'flashable-module')

        lines_full.append(f"### {name} (`{mid}`)")
        lines_full.append(f"- Description: {desc}")
        lines_full.append(f"- Module URL: https://magisk.yssn.tech/modules/{mid}/")
        lines_full.append(f"- Chinese Module URL: https://magisk.yssn.tech/zh/modules/{mid}/")
        lines_full.append(f"- Category: https://magisk.yssn.tech/categories/{category}/")
        lines_full.append(f"- Software Type: {software_type}")
        lines_full.append(f"- Source Channel: {source_type}")
        lines_full.append(f"- Supported Platforms: {compat}")
        stars_label = 'GitHub Stars' if source_type == 'github' and repo else 'Community Metric'
        lines_full.append(f"- {stars_label}: {stars:,}")
        lines_full.append(f"- Latest Release: {tag}")
        if download:
            lines_full.append(f"- Download Asset: {download}")
        if repo:
            lines_full.append(f"- Upstream Source: https://github.com/{repo}")
        lines_full.append('')

    os.makedirs(PUBLIC_DIR, exist_ok=True)
    with open(os.path.join(PUBLIC_DIR, 'llms-full.txt'), 'w', encoding='utf-8') as out:
        out.write('\n'.join(lines_full))
    print(f"Generated public/llms-full.txt with {total_count} modules")

    # 2. Generate public/llms.txt (English)
    lines_summary = [
        '# Magisk Hub',
        '',
        f'> Magisk Hub is an open directory and technical knowledge hub cataloging {total_count} community-maintained root modules and extensions for Android devices utilizing Magisk, KernelSU, APatch, LSPosed, and Shizuku.',
        '',
        '## Overview & Architecture',
        'Magisk Hub indexes verified open-source and community root packages, technical architecture breakdowns, and official release assets. Every module listed is verified against JSON Schema Draft-07 specifications and physical archive payload inspection.',
        '',
        '- Website: https://magisk.yssn.tech/',
        '- Simplified Chinese Mirror: https://magisk.yssn.tech/zh/',
        '- Chinese LLM Index: https://magisk.yssn.tech/zh/llms.txt',
        '- Source Code: https://github.com/Yass5002/magisk-hub',
        '- Full LLM Module Feed: https://magisk.yssn.tech/llms-full.txt',
        '- Schema Definition: https://github.com/Yass5002/magisk-hub/blob/master/modules/schema.json',
        '- Security & Verification Policy: https://magisk.yssn.tech/security/',
        '',
        '## Root Platform Compatibility',
        'Android privilege environments supported across this directory:',
        '- [Magisk Modules](https://magisk.yssn.tech/compatibility/magisk/): Standard systemless root providing boot image patching, systemless /system mounting, and Zygisk.',
        '- [KernelSU Modules](https://magisk.yssn.tech/compatibility/kernelsu/): Kernel-space root management operating via custom su privilege delegation in GKI kernels.',
        '- [APatch Modules](https://magisk.yssn.tech/compatibility/apatch/): KernelPatch-based root solution modifying the Android kernel in-place without requiring full custom boot image rebuilds.',
        '- [LSPosed Modules](https://magisk.yssn.tech/compatibility/lsposed/): ART runtime hooking framework executing method interceptions in memory.',
        '- [Shizuku Privileged Apps](https://magisk.yssn.tech/compatibility/shizuku/): Unrooted system API access via ADB/root-backed Binder IPC delegation.',
        '- [Rootless Tools](https://magisk.yssn.tech/compatibility/rootless/): Non-root utilities running via Shizuku, wireless debugging (ADB), or Device Owner privileges.',
        '',
        '## Ecosystem Categories',
        'Browse modules by functional domain:',
        '- [Root Management](https://magisk.yssn.tech/categories/root-management/): Core su daemons, Zygisk engines, root cloaking, and attestation bypass tools.',
        '- [Performance & Kernel](https://magisk.yssn.tech/categories/performance-kernel/): CPU/GPU governor tuners, thermal throttle controls, and game performance modules.',
        '- [System Environment](https://magisk.yssn.tech/categories/system-environment/): Framework tweaks, OEM feature restoration, and OS-level modifications.',
        '- [Customization & UI](https://magisk.yssn.tech/categories/customization-ui/): Status bar, gesture, navigation, launcher, and appearance customizations.',
        '- [Development & Instrumentation](https://magisk.yssn.tech/categories/development-instrumentation/): Dynamic hooking frameworks, Frida servers, debugging, and reverse engineering tools.',
        '- [System Utilities](https://magisk.yssn.tech/categories/system-utilities/): Audio DSP engines, call recorders, automated cleanup, and terminal power tools.',
        '- [Networking & Proxies](https://magisk.yssn.tech/categories/networking-proxies/): Systemless adblockers, transparent TPROXY gateways, and privacy DNS redirectors.',
        '- [Security & Certificates](https://magisk.yssn.tech/categories/security-certificates/): CA certificate trust injectors, device identifier spoofing, and privacy guards.',
        '- [Xposed & Runtime Hooks](https://magisk.yssn.tech/categories/xposed-runtime-hooks/): Dynamic method hooks, signature verification bypasses, and app customization.',
        '- [Audio DSP & Acoustics](https://magisk.yssn.tech/categories/audio-dsp-acoustics/): System equalizers, sound drivers, mixer path modifiers, and Dolby Atmos ports.',
        '- [System Typography & Fonts](https://magisk.yssn.tech/categories/system-typography-fonts/): Systemless font replacements, CJK font extensions, and emoji packages.',
        '- [Battery & Power Management](https://magisk.yssn.tech/categories/battery-power-charging/): Advanced charging switches, battery idle mode controls, and PPS unlockers.',
        '- [Boot Animations & Splash](https://magisk.yssn.tech/categories/boot-animations-ui/): Custom boot sequences, Google Pixel boot animations, and boot splash screens.',
        '',
        '## Featured Flagship Guides (Tier 1)',
        'In-depth technical guides with architecture breakdowns, configuration paths, and troubleshooting FAQs:',
        '',
        '- [Magisk](https://magisk.yssn.tech/modules/magisk/): Core systemless root suite providing boot image patching and Zygisk process injection.',
        '- [PlayIntegrityFix](https://magisk.yssn.tech/modules/playintegrityfix/): Fix Play Integrity API verdicts by spoofing valid device fingerprints. Config: `/data/adb/pif.json`.',
        '- [Shamiko](https://magisk.yssn.tech/modules/shamiko/): Closed-source Zygisk module for advanced root hiding and sensitive app cloaking. Config: `/data/adb/shamiko/whitelist`.',
        '- [TrickyStore](https://magisk.yssn.tech/modules/trickystore/): Keystore interception tool supporting software-backed keybox spoofing for hardware-backed attestation bypasses. Config: `/data/adb/tricky_store/target.txt`.',
        '- [ReZygisk](https://magisk.yssn.tech/modules/rezygisk/): Open-source C implementation of the Zygisk API compatible across Magisk, KernelSU, and APatch.',
        '- [OverlayFS MetaModule](https://magisk.yssn.tech/modules/meta-overlayfs-kernelsu/): High-performance OverlayFS filesystem metamodule for KernelSU replacing Magic Mount.',
        '- [FreePPS](https://magisk.yssn.tech/modules/freepps-xiaomi-fast-charge/): Unlocks open-standard USB-PD Programmable Power Supply (PPS) protocol fast charging on Xiaomi devices.',
        '- [bindhosts](https://magisk.yssn.tech/modules/bindhosts/): Cross-platform systemless hosts blocker utilizing mount-bind across Magisk, KernelSU, and APatch.',
        '- [ViPER4Android FX Redesign](https://magisk.yssn.tech/modules/viperfx-re/): Renowned systemless audio DSP equalizer, convolver, and bass management suite.',
        '- [LocusMimic](https://magisk.yssn.tech/modules/locusmimic/): Advanced GPS location and multi-point route simulator operating systemlessly via LSPosed.',
        '- [LSPDoze](https://magisk.yssn.tech/modules/lspdoze/): Instant Deep Doze transitions upon screen-off, background wakelock suppression, and fullscreen AOD.',
        '',
        '## Installation Instructions',
        '1. Download the release archive (`.zip` or `.apk`) from the verified download link on any module page.',
        '2. Open your device root manager application (Magisk, KernelSU Manager, APatch Manager, or LSPosed).',
        '3. For flashable modules: Navigate to **Modules > Install from storage**, select the `.zip`, and reboot.',
        '4. For LSPosed modules: Install the `.apk`, open **LSPosed Manager**, enable the module, configure scope, and restart the target application.',
        ''
    ]

    with open(os.path.join(PUBLIC_DIR, 'llms.txt'), 'w', encoding='utf-8') as out:
        out.write('\n'.join(lines_summary))
    print(f"Generated public/llms.txt with {total_count} modules summary")

    # 3. Generate public/zh/llms-full.txt (Simplified Chinese)
    zh_public_dir = os.path.join(PUBLIC_DIR, 'zh')
    os.makedirs(zh_public_dir, exist_ok=True)
    zh_full = [
        '# Magisk Hub - 中文完整模块索引 (llms-full.txt)',
        '',
        f'> 收录 {total_count} 个适用于 Magisk、KernelSU、APatch 与 LSPosed 的活跃 Android Root 模块、Xposed 插件及特权应用中文索引与技术文档。',
        '',
        '中文主页: https://magisk.yssn.tech/zh/',
        '英文原版: https://magisk.yssn.tech/',
        '开源仓库: https://github.com/Yass5002/magisk-hub',
        '',
        '## 完整模块目录',
        ''
    ]

    for m in modules:
        mid = m.get('id', '')
        zh = zh_overrides.get(mid, {})
        name = zh.get('displayName') or m.get('name', '')
        desc = zh.get('description') or m.get('description', '')
        compat = ', '.join(m.get('compatibility', []))
        stars = m.get('stars', 0)
        tag = m.get('latestRelease', {}).get('tag', '')
        download = m.get('latestRelease', {}).get('downloadUrl', '')
        repo = m.get('repo') or ''
        source_type = m.get('sourceType', 'github' if repo else 'community')
        category = m.get('category', '')
        software_type = m.get('softwareType', 'flashable-module')

        zh_full.append(f"### {name} (`{mid}`)")
        zh_full.append(f"- 模块简介: {desc}")
        zh_full.append(f"- 中文详情页: https://magisk.yssn.tech/zh/modules/{mid}/")
        zh_full.append(f"- 所属分类: https://magisk.yssn.tech/zh/categories/{category}/")
        zh_full.append(f"- 软件包类型: {software_type}")
        zh_full.append(f"- 收录渠道: {source_type}")
        zh_full.append(f"- 兼容平台: {compat}")
        zh_metric_label = 'GitHub Star' if source_type == 'github' and repo else '社区热度指标'
        zh_full.append(f"- {zh_metric_label}: {stars:,}")
        zh_full.append(f"- 最新版本: {tag}")
        if download:
            zh_full.append(f"- 官方下载地址: {download}")
        if repo:
            zh_full.append(f"- 上游仓库: https://github.com/{repo}")
        zh_full.append('')

    with open(os.path.join(zh_public_dir, 'llms-full.txt'), 'w', encoding='utf-8') as out:
        out.write('\n'.join(zh_full))
    print(f"Generated public/zh/llms-full.txt with {total_count} modules")

    # 4. Generate public/zh/llms.txt (Simplified Chinese)
    zh_summary = [
        '# Magisk Hub（简体中文版）',
        '',
        f'> Magisk Hub 是面向 Magisk、KernelSU、APatch 与 LSPosed 生态的开源 Root 模块中文目录与技术文档中心，累计收录 {total_count} 个活跃模块。',
        '',
        '## 项目概览与验证机制',
        '所有收录模块均通过 JSON Schema Draft-07 数据规范校验与真实发布包载荷核查，提供官方直链下载、中文技术原理解析、配置文件路径与救砖排查指南。',
        '',
        '- 中文首页: https://magisk.yssn.tech/zh/',
        '- 英文首页: https://magisk.yssn.tech/',
        '- 完整中文模块索引: https://magisk.yssn.tech/zh/llms-full.txt',
        '- 开源仓库: https://github.com/Yass5002/magisk-hub',
        '- 安全与审核政策: https://magisk.yssn.tech/zh/security/',
        '',
        '## 兼容平台目录',
        '- [Magisk 模块](https://magisk.yssn.tech/zh/compatibility/magisk/): 经典无系统分区修改（Systemless）Root 方案，支持 Boot 镜像修补与 Zygisk。',
        '- [KernelSU 模块](https://magisk.yssn.tech/zh/compatibility/kernelsu/): 基于 GKI 内核空间的 Root 授权管理方案。',
        '- [APatch 模块](https://magisk.yssn.tech/zh/compatibility/apatch/): 基于 KernelPatch 的内核就地修补 Root 方案。',
        '- [LSPosed 模块](https://magisk.yssn.tech/zh/compatibility/lsposed/): 现代 Android ART 运行时方法 Hook 框架。',
        '- [Shizuku 特权应用](https://magisk.yssn.tech/zh/compatibility/shizuku/): 通过 Binder 令牌调用系统特权 API 的免 Root 应用。',
        '- [免 Root 工具](https://magisk.yssn.tech/zh/compatibility/rootless/): 基于无线调试 ADB 或 Device Owner 的免 Root 实用工具。',
        '',
        '## 模块功能分类',
    ]

    for cat_id, (cat_name, cat_desc) in ZH_CATEGORIES.items():
        zh_summary.append(f"- [{cat_name}](https://magisk.yssn.tech/zh/categories/{cat_id}/): {cat_desc}")

    zh_summary.extend([
        '',
        '## 热门核心模块中文指南',
        '- [Magisk（面具）](https://magisk.yssn.tech/zh/modules/magisk/): 通用无系统分区修改（Systemless）Root 方案与镜像修补教程。',
        '- [PlayIntegrityFix (PIF)](https://magisk.yssn.tech/zh/modules/playintegrityfix/): 通过 Zygisk 注入与设备指纹伪装修复 Play Integrity 认证。',
        '- [Shamiko](https://magisk.yssn.tech/zh/modules/shamiko/): LSPosed 团队开发的高隐蔽性 Zygisk Root 隐藏模块。',
        '- [TrickyStore](https://magisk.yssn.tech/zh/modules/trickystore/): 基于 Keystore HAL 拦截与 Keybox 注入通过强完整性认证。',
        '- [ACC 高级充电控制](https://magisk.yssn.tech/zh/modules/acc/): 充电上限保护、限流控温与旁路供电（Idle Mode）守护进程。',
        ''
    ])

    with open(os.path.join(zh_public_dir, 'llms.txt'), 'w', encoding='utf-8') as out:
        out.write('\n'.join(zh_summary))
    print(f"Generated public/zh/llms.txt with {total_count} modules summary")


if __name__ == '__main__':
    generate()
