import type { Locale } from './routing';
import type { CategoryInfo, PlatformCompatibility, PlatformInfo, SoftwareType } from '../lib/modules';

const CATEGORIES_ZH: Record<string, { name: string; description: string }> = {
  'root-management': {
    name: 'Root 管理与隐藏',
    description: '核心 su 守护进程、Zygisk 注入引擎、Root 环境隐藏与 Play Integrity 认证绕过工具。',
  },
  'performance-kernel': {
    name: '性能与内核调校',
    description: 'CPU/GPU 调度器优化、温控策略调整与游戏帧率性能增强模块。',
  },
  'system-environment': {
    name: '系统环境与框架增强',
    description: 'Systemless 系统框架微调、OEM 专属功能解锁与系统级特性修改。',
  },
  'customization-ui': {
    name: '界面定制与美化',
    description: '状态栏、手势导航、桌面启动器及系统外观视觉定制模块。',
  },
  'development-instrumentation': {
    name: '开发调试与逆向插桩',
    description: '动态 Hook 框架、Frida 注入服务端、系统抓包调试与逆向分析工具。',
  },
  'system-utilities': {
    name: '系统实用工具',
    description: '通话录音、自动清理、后台管理、磁盘挂载与终端效率增强工具。',
  },
  'networking-proxies': {
    name: '网络与透明代理',
    description: 'Systemless 广告拦截、TPROXY 透明代理网关与隐私 DNS 重定向模块。',
  },
  'security-certificates': {
    name: '安全与证书管理',
    description: '系统级 CA 根证书信任注入、设备标识符伪装与隐私安全防护模块。',
  },
  'xposed-runtime-hooks': {
    name: 'Xposed 与运行时 Hook',
    description: 'ART 运行时方法挂钩、签名校验绕过与应用逻辑增强模块。',
  },
  'audio-dsp-acoustics': {
    name: '音频 DSP 与声学增强',
    description: '系统全局均衡器、音频驱动调音、Mixer 通路修改与杜比全景声移植。',
  },
  'system-typography-fonts': {
    name: '系统字体与排版',
    description: '无侵入式系统字体替换、CJK 中日韩字符集补全与 Emoji 表情包替换模块。',
  },
  'battery-power-charging': {
    name: '电池与充电控制',
    description: '高级充电阈值开关、旁路供电（Idle Mode）、PPS 快充协议解锁与功耗监控。',
  },
  'boot-animations-ui': {
    name: '开机动画与启动画面',
    description: '自定义开机动画、Pixel 原生开机特效与充电/启动界面美化模块。',
  },
};

const PLATFORMS_ZH: Record<PlatformCompatibility, { label: string; title: string; description: string; details: string }> = {
  Magisk: {
    label: 'Magisk 模块',
    title: 'Magisk 模块合集',
    description: '兼容 Android Magisk 无系统分区修改（Systemless）方案的活跃模块。',
    details: 'Magisk 通过修补 Boot 镜像实现无侵入式 Root 权限管理、Magic Mount 挂载与 Zygisk 运行时注入。',
  },
  KernelSU: {
    label: 'KernelSU 模块',
    title: 'KernelSU 模块合集',
    description: '支持 KernelSU 内核级 Root 方案的活跃功能模块。',
    details: 'KernelSU 直接运行于 Linux 内核空间，在 GKI 内核中提供基于内核的 su 权限授权与 OverlayFS/MetaModule 挂载能力。',
  },
  APatch: {
    label: 'APatch 模块',
    title: 'APatch 模块合集',
    description: '适配 APatch（KernelPatch）内核修补 Root 方案的模块目录。',
    details: 'APatch 基于 KernelPatch 直接对 Android 内核进行就地修补，兼顾内核态隐藏与标准模块生态兼容。',
  },
  LSPosed: {
    label: 'LSPosed 模块',
    title: 'LSPosed / Xposed 模块合集',
    description: '基于 LSPosed 框架运行的 Android ART 运行时方法 Hook 模块。',
    details: 'LSPosed 在现代 Android 系统上提供精细到单应用作用域（Scope）的 ART 运行时 Hook 能力。',
  },
  Shizuku: {
    label: 'Shizuku 特权应用',
    title: 'Shizuku 特权应用合集',
    description: '借助 Shizuku 系统服务 Binder 令牌运行的免 Root 高权限应用。',
    details: 'Shizuku 通过 ADB 或 Root 启动守护进程，向第三方应用安全共享系统特权 API 而无需完整 Root 权限。',
  },
  Rootless: {
    label: '免 Root 工具',
    title: '免 Root 与设备管理员工具',
    description: '无需解锁 Bootloader，通过无线 ADB 或 Device Owner 运行的系统增强工具。',
    details: '免 Root 工具利用无线调试 ADB、Shizuku 或设备策略管理器（DPM）实现系统精简与权限管理。',
  },
};

const SOFTWARE_TYPE_ZH: Record<SoftwareType, { label: string; installVerb: string; badgeText: string }> = {
  'flashable-module': { label: '可刷入模块', installVerb: '在 Root 管理器中刷入', badgeText: 'module' },
  'xposed-module': { label: 'Xposed 模块', installVerb: '安装 APK 并在 LSPosed 中启用', badgeText: 'xposed' },
  'standalone-app': { label: '特权应用', installVerb: '安装 APK 并授予权限', badgeText: '应用' },
  'kernel-module': { label: '内核模块', installVerb: '加载内核模块', badgeText: '内核' },
};

export function localizeCategory(cat: CategoryInfo, locale: Locale): CategoryInfo {
  if (locale === 'en') return cat;
  const zh = CATEGORIES_ZH[cat.id];
  if (!zh) return cat;
  return {
    ...cat,
    name: zh.name,
    description: zh.description,
  };
}

export function localizePlatform(platform: PlatformInfo, locale: Locale): PlatformInfo {
  if (locale === 'en') return platform;
  const zh = PLATFORMS_ZH[platform.name];
  if (!zh) return platform;
  return {
    ...platform,
    label: zh.label,
    title: zh.title,
    description: zh.description,
    details: zh.details,
  };
}

export function getSoftwareTypeBadgeText(type: SoftwareType, locale: Locale): string {
  if (locale === 'zh') {
    return SOFTWARE_TYPE_ZH[type]?.badgeText || type;
  }
  return type === 'xposed-module' ? 'xposed' : type === 'standalone-app' ? 'app' : 'kernel';
}
