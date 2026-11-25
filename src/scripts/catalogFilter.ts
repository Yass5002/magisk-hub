export interface CatalogFilterOptions {
  spotlightId?: string;
  featuredBanner?: HTMLElement | null;
  heroSection?: HTMLElement | null;
  heroText?: HTMLElement | null;
  trackUmami?: boolean;
  syncUrl?: boolean;
}

const SEARCH_STOPWORDS = new Set([
  'http', 'https', 'magisk', 'yssn', 'tech', 'modules', 'module', 'download',
  'install', 'kernelsu', 'apatch', 'android', 'latest', 'release', 'github',
  'from', 'with', 'this', 'that', 'your', 'reference', 'file', 'note', 'root',
]);

export function normalizeSearchText(s: string): string {
  return s.toLowerCase().replace(/[-_.\s/\\:()[\]]+/g, '');
}

/** Bounded Levenshtein edit distance returning maxDist + 1 early when exceeded. */
export function boundedLevenshtein(a: string, b: string, maxDist: number): number {
  const la = a.length;
  const lb = b.length;
  if (Math.abs(la - lb) > maxDist) return maxDist + 1;
  if (a === b) return 0;

  let prev = new Array<number>(lb + 1);
  let curr = new Array<number>(lb + 1);
  for (let j = 0; j <= lb; j++) prev[j] = j;

  for (let i = 1; i <= la; i++) {
    curr[0] = i;
    let rowMin = curr[0];
    const ca = a.charCodeAt(i - 1);
    for (let j = 1; j <= lb; j++) {
      const cost = ca === b.charCodeAt(j - 1) ? 0 : 1;
      const val = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
      curr[j] = val;
      if (val < rowMin) rowMin = val;
    }
    if (rowMin > maxDist) return maxDist + 1;
    const tmp = prev;
    prev = curr;
    curr = tmp;
  }
  return prev[lb];
}

function matchSmartFallback(rawQuery: string, wrappers: HTMLElement[]): Set<string> {
  const matchedIds = new Set<string>();
  const urlSlug = rawQuery.match(/\/modules\/([a-z0-9][a-z0-9_-]*)/i)?.[1];
  if (urlSlug) {
    const normUrlSlug = normalizeSearchText(urlSlug);
    for (const el of wrappers) {
      const id = el.getAttribute('data-id') || '';
      const normId = normalizeSearchText(id);
      if (normId === normUrlSlug || (normUrlSlug.length >= 6 && normId.includes(normUrlSlug))) {
        matchedIds.add(id);
      }
    }
    if (matchedIds.size > 0) return matchedIds;
  }

  const normQuery = normalizeSearchText(rawQuery);
  const slugTokens = (rawQuery.match(/[a-z0-9]+[-_][a-z0-9_-]+/g) || [])
    .map((t) => normalizeSearchText(t))
    .filter((t) => t.length >= 4 && !SEARCH_STOPWORDS.has(t));
  const words = [
    ...(rawQuery.match(/[a-z0-9]{3,}/g) || []),
    ...(rawQuery.match(/[\u4e00-\u9fff]{2,}/g) || []),
  ]
    .map((t) => t.toLowerCase())
    .filter((t) => !SEARCH_STOPWORDS.has(t));

  for (const el of wrappers) {
    const id = el.getAttribute('data-id') || '';
    const normId = normalizeSearchText(id);
    const normBlob = el.getAttribute('data-search-norm') || '';

    if (normId.length >= 5 && normQuery.includes(normId)) {
      matchedIds.add(id);
      continue;
    }
    if (slugTokens.some((st) => normBlob.includes(st))) {
      matchedIds.add(id);
      continue;
    }
    if (words.length >= 2 && words.every((w) => normBlob.includes(w))) {
      matchedIds.add(id);
    }
  }
  return matchedIds;
}

function matchFuzzyTypoFallback(rawQuery: string, wrappers: HTMLElement[]): Set<string> {
  const matchedIds = new Set<string>();
  const queryNorm = normalizeSearchText(rawQuery);
  const queryTokens = Array.from(
    new Set([
      ...(queryNorm.length >= 4 && !rawQuery.includes(' ') ? [queryNorm] : []),
      ...(rawQuery.toLowerCase().match(/[a-z0-9]{4,}/g) || []),
    ])
  ).filter((t) => !SEARCH_STOPWORDS.has(t) && t.length >= 4);

  if (queryTokens.length === 0) return matchedIds;

  for (const el of wrappers) {
    const id = el.getAttribute('data-id') || '';
    const fuzzyAttr = el.getAttribute('data-fuzzy-tokens') || '';
    if (!fuzzyAttr) continue;
    const cardTokens = fuzzyAttr.split(' ');
    const hit = queryTokens.some((qt) => {
      const maxDist = qt.length >= 7 ? 2 : 1;
      return cardTokens.some((ct) => boundedLevenshtein(qt, ct, maxDist) <= maxDist);
    });
    if (hit) matchedIds.add(id);
  }
  return matchedIds;
}

export function initCatalogFilter(opts: CatalogFilterOptions = {}) {
  const searchInput = document.getElementById('searchInput') as HTMLInputElement | null;
  const searchClearBtn = document.getElementById('searchClearBtn') as HTMLButtonElement | null;
  const compatSelect = document.getElementById('compatSelect') as HTMLSelectElement | null;
  const categorySelect = document.getElementById('categorySelect') as HTMLSelectElement | null;
  const sortSelect = document.getElementById('sortSelect') as HTMLSelectElement | null;
  const resetBtn = document.getElementById('resetBtn') as HTMLButtonElement | null;
  const moduleGrid = document.getElementById('moduleGrid');
  const cardWrappers = Array.from(document.querySelectorAll('.module-card-wrapper')) as HTMLElement[];
  const noResults = document.getElementById('noResults');
  const moduleCount = document.getElementById('moduleCount');

  if (!moduleGrid || cardWrappers.length === 0) return;

  const pageLocale = document.documentElement.lang?.toLowerCase().startsWith('zh') ? 'zh' : 'en';
  let currentSearch = '';
  let currentCompat = 'all';
  let currentCategory = 'all';
  let currentSort = sortSelect?.value || 'trending';
  let currentTotalVisible = cardWrappers.length;

  // Hydrate initial ?q=, ?compat=, ?cat=, ?sort= from URL query string
  try {
    const params = new URLSearchParams(window.location.search);
    const initialQ = (params.get('q') || '').trim();
    const initialCompat = (params.get('compat') || '').trim();
    const initialCat = (params.get('cat') || '').trim();
    const initialSort = (params.get('sort') || '').trim();

    if (initialQ && searchInput) {
      searchInput.value = initialQ;
      currentSearch = initialQ.toLowerCase();
      searchClearBtn?.classList.remove('hidden');
    }
    if (initialCompat && compatSelect && Array.from(compatSelect.options).some((o) => o.value === initialCompat)) {
      compatSelect.value = initialCompat;
      currentCompat = initialCompat;
    }
    if (initialCat && categorySelect && Array.from(categorySelect.options).some((o) => o.value === initialCat)) {
      categorySelect.value = initialCat;
      currentCategory = initialCat;
    }
    if (initialSort && sortSelect && Array.from(sortSelect.options).some((o) => o.value === initialSort)) {
      sortSelect.value = initialSort;
      currentSort = initialSort;
    }
  } catch {
    // Ignore URL parsing errors
  }

  function syncUrlState() {
    if (opts.syncUrl === false) return;
    try {
      const url = new URL(window.location.href);
      const qVal = searchInput?.value.trim() || '';
      if (qVal) url.searchParams.set('q', qVal);
      else url.searchParams.delete('q');

      if (compatSelect && currentCompat !== 'all') url.searchParams.set('compat', currentCompat);
      else url.searchParams.delete('compat');

      if (categorySelect && currentCategory !== 'all') url.searchParams.set('cat', currentCategory);
      else url.searchParams.delete('cat');

      if (sortSelect && currentSort !== 'trending') url.searchParams.set('sort', currentSort);
      else url.searchParams.delete('sort');

      const nextRelative = `${url.pathname}${url.search}${url.hash}`;
      const currentRelative = `${window.location.pathname}${window.location.search}${window.location.hash}`;
      if (nextRelative !== currentRelative) {
        window.history.replaceState(null, '', nextRelative);
      }
    } catch {
      // Ignore history API restrictions
    }
  }

  function applyFiltersAndSort() {
    let visibleCount = 0;
    const isSearching = currentSearch.length > 0;
    const normSearch = isSearching ? normalizeSearchText(currentSearch) : '';

    const shouldShowSpotlight =
      Boolean(opts.featuredBanner && opts.spotlightId) &&
      !isSearching &&
      (currentCompat === 'all' || currentCompat === 'Magisk') &&
      currentCategory === 'all';

    if (opts.featuredBanner) {
      opts.featuredBanner.style.display = shouldShowSpotlight ? '' : 'none';
    }

    if (opts.heroSection && opts.heroText) {
      if (isSearching) {
        opts.heroSection.classList.remove('py-5', 'sm:py-10');
        opts.heroSection.classList.add('py-3.5', 'sm:py-5');
        opts.heroText.classList.add('hidden');
      } else {
        opts.heroSection.classList.add('py-5', 'sm:py-10');
        opts.heroSection.classList.remove('py-3.5', 'sm:py-5');
        opts.heroText.classList.remove('hidden');
      }
    }

    const matchedIds = new Set<string>();
    if (isSearching) {
      for (const el of cardWrappers) {
        const id = el.getAttribute('data-id') || '';
        const searchBlob = el.getAttribute('data-search') || '';
        const searchNorm = el.getAttribute('data-search-norm') || '';
        if (searchBlob.includes(currentSearch) || (normSearch.length >= 2 && searchNorm.includes(normSearch))) {
          matchedIds.add(id);
        }
      }
      if (matchedIds.size === 0) {
        for (const id of matchSmartFallback(currentSearch, cardWrappers)) {
          matchedIds.add(id);
        }
      }
      if (matchedIds.size === 0) {
        for (const id of matchFuzzyTypoFallback(currentSearch, cardWrappers)) {
          matchedIds.add(id);
        }
      }
    }

    for (const el of cardWrappers) {
      const id = el.getAttribute('data-id') || '';
      const cat = el.getAttribute('data-category') || '';
      const compat = (el.getAttribute('data-compat') || '').split(',');

      if (shouldShowSpotlight && opts.spotlightId && id === opts.spotlightId) {
        el.style.display = 'none';
        continue;
      }

      const matchesSearch = !isSearching || matchedIds.has(id);
      const matchesCategory = !categorySelect || currentCategory === 'all' || cat === currentCategory;
      const matchesCompat = !compatSelect || currentCompat === 'all' || compat.includes(currentCompat);

      if (matchesSearch && matchesCategory && matchesCompat) {
        el.style.display = '';
        visibleCount++;
      } else {
        el.style.display = 'none';
      }
    }

    const sorted = [...cardWrappers].sort((a, b) => {
      if (currentSort === 'trending') {
        const dlA = parseInt(a.getAttribute('data-trending') || '0', 10);
        const dlB = parseInt(b.getAttribute('data-trending') || '0', 10);
        const starsA = parseInt(a.getAttribute('data-stars') || '0', 10);
        const starsB = parseInt(b.getAttribute('data-stars') || '0', 10);
        if (dlB !== dlA) return dlB - dlA;
        return starsB - starsA;
      } else if (currentSort === 'stars') {
        const starsA = parseInt(a.getAttribute('data-stars') || '0', 10);
        const starsB = parseInt(b.getAttribute('data-stars') || '0', 10);
        return starsB - starsA;
      } else if (currentSort === 'name') {
        const nameA = a.getAttribute('data-name') || '';
        const nameB = b.getAttribute('data-name') || '';
        return nameA.localeCompare(nameB);
      } else if (currentSort === 'recent') {
        const dateA = new Date(a.getAttribute('data-date') || 0).getTime();
        const dateB = new Date(b.getAttribute('data-date') || 0).getTime();
        return dateB - dateA;
      }
      return 0;
    });

    for (const el of sorted) {
      moduleGrid.appendChild(el);
    }

    const totalVisible = visibleCount + (shouldShowSpotlight ? 1 : 0);
    currentTotalVisible = totalVisible;

    if (moduleCount) {
      const prefix = moduleCount.getAttribute('data-prefix') || '';
      const suffix = moduleCount.getAttribute('data-suffix') || ' modules';
      moduleCount.textContent = `${prefix}${totalVisible}${suffix}`;
    }

    if (noResults) {
      if (totalVisible === 0) {
        noResults.classList.remove('hidden');
        const reqBtn = document.getElementById('requestModuleBtn') as HTMLAnchorElement | null;
        if (reqBtn) {
          const baseHref = 'https://github.com/Yass5002/magisk-hub/issues/new?template=module-request.yml';
          const rawQ = searchInput?.value.trim() || '';
          reqBtn.href = rawQ
            ? `${baseHref}&title=${encodeURIComponent(`[Module Request]: ${rawQ}`)}`
            : baseHref;
        }
      } else {
        noResults.classList.add('hidden');
      }
    }
  }

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      searchInput?.focus();
    }
  });

  searchInput?.addEventListener('input', (e) => {
    const q = (e.target as HTMLInputElement).value.trim();
    currentSearch = q.toLowerCase();
    if (searchClearBtn) {
      searchClearBtn.classList.toggle('hidden', currentSearch.length === 0);
    }
    applyFiltersAndSort();
    syncUrlState();

    if (opts.trackUmami) {
      clearTimeout((window as any).searchUmamiTimeout);
      (window as any).searchUmamiTimeout = setTimeout(() => {
        if (q.length >= 2 && (window as any).umami) {
          (window as any).umami.track('search-modules', {
            query: q,
            results_count: currentTotalVisible,
            locale: pageLocale,
          });
          if (currentTotalVisible === 0) {
            (window as any).umami.track('search-zero-results', { query: q, locale: pageLocale });
          }
        }
      }, 750);
    }
  });

  searchClearBtn?.addEventListener('click', () => {
    if (searchInput) {
      searchInput.value = '';
      currentSearch = '';
      searchClearBtn.classList.add('hidden');
      searchInput.focus();
      applyFiltersAndSort();
      syncUrlState();
    }
  });

  compatSelect?.addEventListener('change', (e) => {
    currentCompat = (e.target as HTMLSelectElement).value;
    applyFiltersAndSort();
    syncUrlState();
    if (opts.trackUmami && (window as any).umami) {
      (window as any).umami.track('filter-platform', { platform: currentCompat, locale: pageLocale });
    }
  });

  categorySelect?.addEventListener('change', (e) => {
    currentCategory = (e.target as HTMLSelectElement).value;
    applyFiltersAndSort();
    syncUrlState();
    if (opts.trackUmami && (window as any).umami) {
      (window as any).umami.track('filter-category', { category: currentCategory, locale: pageLocale });
    }
  });

  sortSelect?.addEventListener('change', (e) => {
    currentSort = (e.target as HTMLSelectElement).value;
    applyFiltersAndSort();
    syncUrlState();
    if (opts.trackUmami && (window as any).umami) {
      (window as any).umami.track('sort-modules', { sort: currentSort, locale: pageLocale });
    }
  });

  resetBtn?.addEventListener('click', () => {
    if (searchInput) searchInput.value = '';
    currentSearch = '';
    currentCompat = 'all';
    currentCategory = 'all';
    currentSort = 'trending';

    searchClearBtn?.classList.add('hidden');
    if (compatSelect) compatSelect.value = 'all';
    if (categorySelect) categorySelect.value = 'all';
    if (sortSelect) sortSelect.value = 'trending';

    applyFiltersAndSort();
    syncUrlState();
    if (opts.trackUmami && (window as any).umami) {
      (window as any).umami.track('reset-filters', { locale: pageLocale });
    }
  });

  applyFiltersAndSort();
}
