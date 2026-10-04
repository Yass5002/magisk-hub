import fs from 'node:fs';
import path from 'node:path';

export interface ModuleRelease {
  tag: string;
  publishedAt: string;
  url: string;
  downloadUrl: string;
  assetName: string;
}

export interface ModuleSEO {
  title: string;
  description: string;
}

export type SoftwareType = 'flashable-module' | 'xposed-module' | 'standalone-app' | 'kernel-module';
export type PlatformCompatibility = 'Magisk' | 'KernelSU' | 'APatch' | 'LSPosed' | 'Shizuku' | 'Rootless';

export interface ModuleData {
  id: string;
  name: string;
  repo: string | null;
  author?: string;
  sourceType?: 'github' | 'community';
  sourceUrl?: string;
  category: string;
  softwareType: SoftwareType;
  description: string;
  compatibility: PlatformCompatibility[];
  license: string;
  icon: string | null;
  stars: number;
  trendingDownloads?: number;
  contentTier?: 1 | 2 | 3;
  latestRelease: ModuleRelease;
  seo: ModuleSEO;
}

export interface CategoryInfo {
  id: string;
  name: string;
  description: string;
  icon: string;
}

export const CATEGORIES: Record<string, CategoryInfo> = {
  'root-management': {
    id: 'root-management',
    name: 'Root Management',
    description: 'Core su daemons, Zygisk engines, root cloaking, and attestation bypass tools.',
    icon: 'Shield',
  },
  'performance-kernel': {
    id: 'performance-kernel',
    name: 'Performance & Kernel',
    description: 'CPU/GPU governor tuners, thermal throttle controls, and game performance modules.',
    icon: 'Zap',
  },
  'system-environment': {
    id: 'system-environment',
    name: 'System Environment',
    description: 'Systemless framework tweaks, OEM feature restoration, and OS-level modifications.',
    icon: 'Layers',
  },
  'customization-ui': {
    id: 'customization-ui',
    name: 'Customization & UI',
    description: 'Status bar, gesture, navigation, launcher, and appearance customizations.',
    icon: 'Sliders',
  },
  'development-instrumentation': {
    id: 'development-instrumentation',
    name: 'Development & Instrumentation',
    description: 'Dynamic hooking frameworks, Frida servers, debugging, and reverse engineering tools.',
    icon: 'Code',
  },
  'system-utilities': {
    id: 'system-utilities',
    name: 'System Utilities',
    description: 'Audio DSP engines, call recorders, automated cleanup, and terminal power tools.',
    icon: 'Wrench',
  },
  'networking-proxies': {
    id: 'networking-proxies',
    name: 'Networking & Proxies',
    description: 'Systemless adblockers, transparent TPROXY gateways, and privacy DNS redirectors.',
    icon: 'Globe',
  },
  'security-certificates': {
    id: 'security-certificates',
    name: 'Security & Certificates',
    description: 'CA certificate trust injectors, device identifier spoofing, and privacy guards.',
    icon: 'Lock',
  },
  'xposed-runtime-hooks': {
    id: 'xposed-runtime-hooks',
    name: 'Xposed & Runtime Hooks',
    description: 'ART method hooks, signature verification bypasses, and runtime memory modifiers.',
    icon: 'Cpu',
  },
  'audio-dsp-acoustics': {
    id: 'audio-dsp-acoustics',
    name: 'Audio DSP & Acoustics',
    description: 'System-wide equalizers, sound drivers, mixer path modifiers, and Dolby Atmos ports.',
    icon: 'Volume2',
  },
  'system-typography-fonts': {
    id: 'system-typography-fonts',
    name: 'System Typography & Fonts',
    description: 'Systemless font replacements, CJK font extensions, emoji replacements, and glyph engines.',
    icon: 'Type',
  },
  'battery-power-charging': {
    id: 'battery-power-charging',
    name: 'Battery & Power Management',
    description: 'Advanced charging switches, battery idle mode controls, thermal throttles, and power monitors.',
    icon: 'BatteryCharging',
  },
  'boot-animations-ui': {
    id: 'boot-animations-ui',
    name: 'Boot Animations & Splash',
    description: 'Custom boot sequences, Google Pixel boot animations, and boot splash screen replacements.',
    icon: 'PlaySquare',
  },
};

export const SOFTWARE_TYPE_CONFIG: Record<SoftwareType, { label: string; badgeColor: string; installVerb: string }> = {
  'flashable-module': { label: 'Flashable Module', badgeColor: 'bg-emerald-50 text-emerald-700 border-emerald-200', installVerb: 'Flash in Root Manager' },
  'xposed-module': { label: 'Xposed Module', badgeColor: 'bg-purple-50 text-purple-700 border-purple-200', installVerb: 'Install APK & Enable in LSPosed' },
  'standalone-app': { label: 'Privileged App', badgeColor: 'bg-blue-50 text-blue-700 border-blue-200', installVerb: 'Install APK & Authorize' },
  'kernel-module': { label: 'Kernel Object', badgeColor: 'bg-amber-50 text-amber-700 border-amber-200', installVerb: 'Load Kernel Module' },
};

export interface PlatformInfo {
  id: string;
  name: PlatformCompatibility;
  label: string;
  shortName: string;
  title: string;
  description: string;
  details: string;
}

export const PLATFORMS: Record<PlatformCompatibility, PlatformInfo> = {
  Magisk: {
    id: 'magisk',
    name: 'Magisk',
    label: 'Magisk Modules',
    shortName: 'Magisk',
    title: 'Magisk Modules',
    description: 'Active modules compatible with Magisk systemless root on Android.',
    details: 'Magisk provides systemless root, boot image patching, and the Zygisk framework.'
  },
  KernelSU: {
    id: 'kernelsu',
    name: 'KernelSU',
    label: 'KernelSU Modules',
    shortName: 'KernelSU',
    title: 'KernelSU Modules',
    description: 'Root modules supporting KernelSU kernel-assisted root.',
    details: 'KernelSU operates in kernel space with custom su privilege delegation.'
  },
  APatch: {
    id: 'apatch',
    name: 'APatch',
    label: 'APatch Modules',
    shortName: 'APatch',
    title: 'APatch Modules',
    description: 'Root modules verified for APatch (KernelPatch).',
    details: 'APatch modifies the Android kernel in-place using KernelPatch.'
  },
  LSPosed: {
    id: 'lsposed',
    name: 'LSPosed',
    label: 'LSPosed Modules',
    shortName: 'LSPosed',
    title: 'LSPosed & Xposed Modules',
    description: 'Runtime ART method hooking modules for the LSPosed framework.',
    details: 'LSPosed provides ART runtime hooking with per-app scope management on modern Android.'
  },
  Shizuku: {
    id: 'shizuku',
    name: 'Shizuku',
    label: 'Shizuku Apps',
    shortName: 'Shizuku',
    title: 'Shizuku Privileged Apps',
    description: 'Applications leveraging Shizuku privileged system API binder tokens.',
    details: 'Shizuku shares system service binder tokens with third-party applications without giving full root access.'
  },
  Rootless: {
    id: 'rootless',
    name: 'Rootless',
    label: 'Rootless Utilities',
    shortName: 'Rootless',
    title: 'Rootless & Device Owner Utilities',
    description: 'Powerful Android system utilities operational via Wireless ADB or Device Owner without root.',
    details: 'Rootless utilities run via ADB wireless debugging, Shizuku, or Device Policy Manager without unlocking bootloaders.'
  }
};

export function getAllPlatforms(): PlatformInfo[] {
  return Object.values(PLATFORMS);
}


let cachedModules: ModuleData[] | null = null;

export function getAllModules(): ModuleData[] {
  if (cachedModules) {
    return cachedModules;
  }

  const modulesDir = path.resolve(process.cwd(), 'modules');
  if (!fs.existsSync(modulesDir)) {
    return [];
  }

  const trendingFile = path.resolve(process.cwd(), 'src/data/trending.json');
  let trendingMap: Record<string, number> = {};
  if (fs.existsSync(trendingFile)) {
    try {
      trendingMap = JSON.parse(fs.readFileSync(trendingFile, 'utf-8'));
    } catch {
      trendingMap = {};
    }
  }

  const files = fs.readdirSync(modulesDir).filter(f => f.endsWith('.json') && f !== 'schema.json');
  const modules: ModuleData[] = [];

  for (const file of files) {
    try {
      const fullPath = path.join(modulesDir, file);
      const raw = fs.readFileSync(fullPath, 'utf-8');
      const data = JSON.parse(raw) as ModuleData;
      data.trendingDownloads = trendingMap[data.id] || 0;
      modules.push(data);
    } catch (err) {
      console.error(`Failed to parse module ${file}:`, err);
    }
  }

  // 2-Tier Trending Sort:
  // Tier 1: trendingDownloads >= 3, sorted by trendingDownloads DESC, then stars DESC
  // Tier 2: trendingDownloads < 3, sorted by stars DESC
  modules.sort((a, b) => {
    const K = 3;
    const dlA = a.trendingDownloads || 0;
    const dlB = b.trendingDownloads || 0;
    const isT1_A = dlA >= K;
    const isT1_B = dlB >= K;

    if (isT1_A && !isT1_B) return -1;
    if (!isT1_A && isT1_B) return 1;

    if (isT1_A && isT1_B) {
      if (dlB !== dlA) return dlB - dlA;
      return (b.stars || 0) - (a.stars || 0);
    }

    return (b.stars || 0) - (a.stars || 0);
  });

  cachedModules = modules;
  return modules;
}

export function getModuleById(id: string): ModuleData | undefined {
  return getAllModules().find(m => m.id === id);
}

export function getModulesByCategory(category: string): ModuleData[] {
  return getAllModules().filter(m => m.category === category);
}

export function getModulesByCompatibility(platform: string): ModuleData[] {
  return getAllModules().filter(m => m.compatibility.includes(platform as any));
}

export function getStats() {
  const all = getAllModules();
  return {
    total: all.length,
    tier1: all.filter(m => m.contentTier === 1).length,
    tier2: all.filter(m => m.contentTier === 2).length,
    tier3: all.filter(m => m.contentTier === 3).length,
    categories: Object.keys(CATEGORIES).length,
    totalStars: all.reduce((sum, m) => sum + (m.stars || 0), 0),
  };
}

export function formatPlatformsShort(compatibility: PlatformCompatibility[]): string {
  return compatibility.map(p => PLATFORMS[p]?.shortName || p).join('/');
}


export function formatPlatformsSentence(compatibility: PlatformCompatibility[]): string {
  if (!compatibility || compatibility.length === 0) return 'Android';
  if (compatibility.length === 1) return compatibility[0];
  if (compatibility.length === 2) return `${compatibility[0]} and ${compatibility[1]}`;
  return `${compatibility.slice(0, -1).join(', ')}, and ${compatibility[compatibility.length - 1]}`;
}

export function generateModuleSEO(module: ModuleData): { title: string; description: string } {
  // Title template: {ModuleName} – Download ({platforms}) | Magisk Hub
  // Fallback: {ModuleName} – Download | Magisk Hub if > 60 chars
  let title = module.seo?.title;
  if (!title || !title.includes('– Download')) {
    const platShort = formatPlatformsShort(module.compatibility);
    const fullTitle = `${module.name} – Download (${platShort}) | Magisk Hub`;
    const fallbackTitle = `${module.name} – Download | Magisk Hub`;
    title = fullTitle.length <= 60 ? fullTitle : fallbackTitle;
  }

  // Description template: Download {name} for {platforms}. {trimmed desc} (<= 140 chars)
  let description = module.seo?.description;
  if (!description || !description.startsWith(`Download ${module.name} for `) || description.length > 140) {
    const lead = `Download ${module.name} for ${formatPlatformsSentence(module.compatibility)}. `;
    const budget = 140 - lead.length;
    let body = (module.description || '').trim();
    
    // Strip version tag if present
    if (module.latestRelease?.tag) {
      body = body.replace(new RegExp(module.latestRelease.tag.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), '');
    }
    body = body.replace(/\bv?\d+\.\d+(\.\d+)?(-[a-zA-Z0-9.]+)?\b/g, '');
    
    // Strip leading name repetition
    body = body.replace(new RegExp(`^${module.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*[:\\-–]\\s*`, 'i'), '');
    const nameSpaced = module.name.replace(/([a-z])([A-Z])/g, '$1 $2');
    body = body.replace(new RegExp(`^${nameSpaced.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*[:\\-–]\\s*`, 'i'), '');
    body = body.replace(/\s+/g, ' ').replace(/^[:\-–,\s]+/, '').trim();
    
    if (body.length <= budget) {
      // fits in budget
    } else {
      const targetBudget = budget - 3;
      let cut = body.slice(0, targetBudget);
      if (cut.includes(' ')) {
        cut = cut.slice(0, cut.lastIndexOf(' '));
      }
      cut = cut.replace(/[,;:\-–\s]+$/, '');
      body = cut + '...';
    }
    
    description = `${lead}${body}`;
    if (!description.endsWith('.') && !description.endsWith('...')) {
      if (description.length < 140) description += '.';
    }
  }

  return { title, description };
}

