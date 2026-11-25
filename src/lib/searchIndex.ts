import { getCollection } from 'astro:content';
import { CATEGORIES, getAllModules, type ModuleData } from './modules';
import { localizeCategory } from '../i18n/taxonomy';

export const normalizeSearchToken = (text: string): string =>
  text.toLowerCase().replace(/[-_.\s/\\:()[\]]+/g, '');

export interface SearchMetadataContext {
  zhModulesMap: Map<string, ModuleData>;
  searchQueriesById: Map<string, string[]>;
}

export async function loadSearchMetadataContext(): Promise<SearchMetadataContext> {
  const zhModulesMap = new Map(getAllModules('zh').map((m) => [m.id, m]));
  let enDocs: Awaited<ReturnType<typeof getCollection<'modules'>>> = [];
  let zhDocs: Awaited<ReturnType<typeof getCollection<'modulesZh'>>> = [];
  try {
    enDocs = await getCollection('modules');
  } catch {
    enDocs = [];
  }
  try {
    zhDocs = await getCollection('modulesZh');
  } catch {
    zhDocs = [];
  }

  const searchQueriesById = new Map<string, string[]>();
  for (const entry of [...enDocs, ...zhDocs]) {
    const prev = searchQueriesById.get(entry.data.id) || [];
    const next = [entry.data.title, ...(entry.data.searchQueries || [])].filter(Boolean);
    searchQueriesById.set(entry.data.id, [...prev, ...next]);
  }
  return { zhModulesMap, searchQueriesById };
}

export function buildModuleFilterAttributes(
  module: ModuleData,
  ctx: SearchMetadataContext
) {
  const zhModule = ctx.zhModulesMap.get(module.id);
  const enCatInfo = CATEGORIES[module.category];
  const zhCatInfo = enCatInfo ? localizeCategory(enCatInfo, 'zh') : undefined;

  const searchIndex = [
    module.id,
    module.name,
    module.enName || '',
    zhModule?.name || '',
    module.description,
    module.enDescription || '',
    zhModule?.description || '',
    module.repo || module.author || '',
    module.latestRelease?.assetName || '',
    module.latestRelease?.tag || '',
    module.category,
    enCatInfo?.name || '',
    zhCatInfo?.name || '',
    ...module.compatibility,
    ...(module.searchAliases || []),
    ...(zhModule?.searchAliases || []),
    ...(ctx.searchQueriesById.get(module.id) || []),
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();

  const searchNorm = normalizeSearchToken(searchIndex);

  const fuzzySources = [
    module.id,
    module.name,
    module.enName || '',
    module.repo?.split('/')[1] || '',
    ...(module.searchAliases || []),
  ]
    .join(' ')
    .toLowerCase();

  const fuzzyTokens = Array.from(
    new Set(
      [
        ...(fuzzySources.match(/[a-z0-9]{4,}/g) || []),
        normalizeSearchToken(module.id),
        normalizeSearchToken(module.enName || module.name),
      ].filter((t) => t.length >= 4)
    )
  ).join(' ');

  return {
    nameLower: module.name.toLowerCase(),
    searchIndex,
    searchNorm,
    fuzzyTokens,
  };
}
