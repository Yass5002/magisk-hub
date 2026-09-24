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

export interface ModuleData {
  id: string;
  name: string;
  repo: string;
  category: string;
  description: string;
  compatibility: ('Magisk' | 'KernelSU' | 'APatch')[];
  license: string;
  icon: string | null;
  stars: number;
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
};

let cachedModules: ModuleData[] | null = null;

export function getAllModules(): ModuleData[] {
  if (cachedModules) {
    return cachedModules;
  }

  const modulesDir = path.resolve(process.cwd(), 'modules');
  if (!fs.existsSync(modulesDir)) {
    return [];
  }

  const files = fs.readdirSync(modulesDir).filter(f => f.endsWith('.json') && f !== 'schema.json');
  const modules: ModuleData[] = [];

  for (const file of files) {
    try {
      const fullPath = path.join(modulesDir, file);
      const raw = fs.readFileSync(fullPath, 'utf-8');
      const data = JSON.parse(raw) as ModuleData;
      modules.push(data);
    } catch (err) {
      console.error(`Failed to parse module ${file}:`, err);
    }
  }

  // Sort: Tier 1 first, then by stars descending
  modules.sort((a, b) => {
    const tierA = a.contentTier || (a.stars >= 200 ? 2 : 3);
    const tierB = b.contentTier || (b.stars >= 200 ? 2 : 3);
    if (tierA !== tierB) {
      return tierA - tierB;
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
