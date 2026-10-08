import type { APIRoute } from 'astro';
import { getAllModules, CATEGORIES, PLATFORMS } from '../lib/modules';

export const GET: APIRoute = async () => {
  const modules = getAllModules().map(m => ({
    id: m.id,
    type: 'module' as const,
    title: m.name,
    subtitle: m.description,
    url: `/modules/${m.id}/`,
    icon: m.icon || `/assets/icons/${m.id}.png`,
    badge: m.category,
    keywords: [m.author || '', m.softwareType, ...m.compatibility].join(' ')
  }));

  const categories = Object.values(CATEGORIES).map(c => ({
    id: c.id,
    type: 'category' as const,
    title: c.name,
    subtitle: c.description,
    url: `/categories/${c.id}/`,
    badge: 'Category',
    keywords: 'category ' + c.name
  }));

  const platforms = Object.values(PLATFORMS).map(p => ({
    id: p.id,
    type: 'platform' as const,
    title: `${p.name} Modules`,
    subtitle: p.description,
    url: `/compatibility/${p.id}/`,
    badge: 'Platform',
    keywords: `platform ${p.name} root`
  }));

  const installs = [
    {
      id: 'install-magisk',
      type: 'install' as const,
      title: 'Install Magisk',
      subtitle: 'Systemless root & Zygisk environment',
      url: '#',
      badge: 'Install',
      icon: '/assets/icons/magisk.png',
      keywords: 'install magisk root'
    },
    {
      id: 'install-kernelsu',
      type: 'install' as const,
      title: 'Install KernelSU',
      subtitle: 'Kernel-assisted root solution',
      url: '#',
      badge: 'Install',
      icon: '/assets/icons/kernelsu.png',
      keywords: 'install kernelsu ksu root'
    },
    {
      id: 'install-apatch',
      type: 'install' as const,
      title: 'Install APatch',
      subtitle: 'KernelPatch based root manager',
      url: '#',
      badge: 'Install',
      icon: '/assets/icons/apatch.png',
      keywords: 'install apatch kp root'
    }
  ];

  const guides = [
    {
      id: 'guides-hub',
      type: 'guide' as const,
      title: 'Guides & Articles',
      subtitle: 'Rooting tutorials, setup workflows, and best practices',
      url: '#',
      badge: 'Guides',
      keywords: 'guides articles tutorials blog'
    }
  ];

  const searchIndex = [...categories, ...platforms, ...installs, ...guides, ...modules];

  return new Response(JSON.stringify(searchIndex), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=86400, stale-while-revalidate=3600'
    }
  });
};
