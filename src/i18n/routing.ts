export type Locale = 'en' | 'zh';

export const SITE_URL = 'https://magisk.yssn.tech';

export function normalizeTrailingSlash(pathname: string): string {
  const clean = (pathname || '/').split('?')[0].split('#')[0];
  if (clean === '/') return '/';
  return clean.endsWith('/') ? clean : `${clean}/`;
}

export function getLocaleFromPath(pathname: string): Locale {
  const normalized = normalizeTrailingSlash(pathname);
  if (normalized === '/zh/' || normalized.startsWith('/zh/')) {
    return 'zh';
  }
  return 'en';
}

export function stripLocalePrefix(pathname: string): string {
  const normalized = normalizeTrailingSlash(pathname);
  if (normalized === '/zh/') return '/';
  if (normalized.startsWith('/zh/')) {
    return normalized.slice(3);
  }
  return normalized;
}

export function localizePath(pathname: string, locale: Locale): string {
  if (/^https?:\/\//i.test(pathname)) {
    return pathname;
  }
  const base = stripLocalePrefix(pathname);
  if (locale === 'zh') {
    return base === '/' ? '/zh/' : `/zh${base}`;
  }
  return base;
}

export function getAbsoluteUrl(pathname: string, locale: Locale): string {
  return `${SITE_URL}${localizePath(pathname, locale)}`;
}

export function getAlternateUrls(pathname: string) {
  const enUrl = getAbsoluteUrl(pathname, 'en');
  const zhUrl = getAbsoluteUrl(pathname, 'zh');
  return {
    en: enUrl,
    zhHans: zhUrl,
    xDefault: enUrl,
  };
}
