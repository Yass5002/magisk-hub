import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { JSDOM } from 'jsdom';

const DIST_DIR = path.resolve(process.cwd(), 'dist');

function inlineAstroChunk(filePath) {
  let code = fs.readFileSync(filePath, 'utf-8');
  const dir = path.dirname(filePath);
  code = code.replace(
    /import\s*\{([^}]+)\}\s*from\s*["'](\.\/[^"']+)["']\s*;?/g,
    (_, specs, rel) => {
      const target = path.resolve(dir, rel);
      const depCode = inlineAstroChunk(target).replace(
        /export\s*\{([^}]+)\}\s*;?/g,
        (__, exSpecs) => {
          const pairs = exSpecs.split(',').map((s) => {
            const parts = s.trim().split(/\s+as\s+/);
            return parts.length === 2 ? `${parts[1].trim()}: ${parts[0].trim()}` : parts[0].trim();
          });
          return `return { ${pairs.join(', ')} };`;
        }
      );
      const bindings = specs.split(',').map((s) => {
        const parts = s.trim().split(/\s+as\s+/);
        return parts.length === 2 ? `${parts[0].trim()}: ${parts[1].trim()}` : parts[0].trim();
      });
      return `const { ${bindings.join(', ')} } = (() => {\n${depCode}\n})();`;
    }
  );
  return code;
}

function evalModuleScript(dom, scriptEl) {
  if (!scriptEl.src && scriptEl.textContent) {
    dom.window.eval(scriptEl.textContent);
    return;
  }
  if (scriptEl.src) {
    const urlPath = new URL(scriptEl.src, 'https://magisk.yssn.tech').pathname;
    if (urlPath.startsWith('/_astro/')) {
      const assetPath = path.join(DIST_DIR, urlPath.replace(/^\/+/, ''));
      dom.window.eval(inlineAstroChunk(assetPath));
    }
  }
}

function loadDistDom(relPath, options = {}) {
  const html = fs.readFileSync(path.join(DIST_DIR, relPath), 'utf-8');
  const dom = new JSDOM(html, {
    url: options.url || `https://magisk.yssn.tech/${relPath === 'index.html' ? '' : relPath.replace(/index\.html$/, '')}`,
    runScripts: 'dangerously',
    beforeParse(window) {
      if (options.navigatorLang) {
        Object.defineProperty(window.navigator, 'language', { value: options.navigatorLang, configurable: true });
        Object.defineProperty(window.navigator, 'languages', { value: [options.navigatorLang], configurable: true });
      }
      Object.defineProperty(window.navigator, 'clipboard', {
        value: { writeText: async () => {} },
        configurable: true,
      });
    },
  });

  // JSDOM ignores <script type="module">; evaluate inline and built /_astro/ module scripts explicitly
  for (const s of dom.window.document.querySelectorAll('script[type="module"]')) {
    evalModuleScript(dom, s);
  }
  return dom;
}

test('Chinese home search filters by Chinese aliases and English module names', () => {
  const dom = loadDistDom('zh/index.html', { url: 'https://magisk.yssn.tech/zh/' });
  const doc = dom.window.document;
  const searchInput = doc.getElementById('searchInput');
  const countEl = doc.getElementById('moduleCount');

  assert.ok(searchInput, 'searchInput exists');
  assert.match(countEl.textContent.trim(), /^共 \d+ 个模块$/);

  // Search Chinese alias "旁路供电" -> should narrow results and include acc
  searchInput.value = '旁路供电';
  searchInput.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  const visibleCards = Array.from(doc.querySelectorAll('.module-card-wrapper'))
    .filter(el => el.style.display !== 'none')
    .map(el => el.getAttribute('data-id'));
  assert.ok(visibleCards.includes('acc'), `Expected 'acc' in results for '旁路供电', got ${visibleCards}`);
  assert.ok(visibleCards.length < 30, `Expected filtered results (< 30), got ${visibleCards.length}`);

  // Search English name "Shamiko" on /zh/ -> should match shamiko
  searchInput.value = 'Shamiko';
  searchInput.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  const shamikoCards = Array.from(doc.querySelectorAll('.module-card-wrapper'))
    .filter(el => el.style.display !== 'none')
    .map(el => el.getAttribute('data-id'));
  assert.ok(shamikoCards.includes('shamiko'), `Expected 'shamiko' in results, got ${shamikoCards}`);
  assert.ok(shamikoCards.length < 10, `Expected narrow Shamiko results, got ${shamikoCards.length}`);
});

test('Home page hydrates ?q= query parameter for SearchAction', () => {
  const dom = loadDistDom('zh/index.html', { url: 'https://magisk.yssn.tech/zh/?q=KernelSU' });
  const doc = dom.window.document;
  const searchInput = doc.getElementById('searchInput');
  assert.equal(searchInput.value, 'KernelSU');
  const visibleCards = Array.from(doc.querySelectorAll('.module-card-wrapper'))
    .filter(el => el.style.display !== 'none');
  assert.ok(visibleCards.length > 0 && visibleCards.length < 255, `Expected filtered cards, got ${visibleCards.length}`);
});

test('English home shows non-blocking Chinese suggestion banner for zh-CN browsers', () => {
  const domZh = loadDistDom('index.html', { navigatorLang: 'zh-CN' });
  const bannerZh = domZh.window.document.getElementById('zhLocaleBanner');
  assert.ok(bannerZh && !bannerZh.classList.contains('hidden'), 'Banner should show for zh-CN browser');

  const domEn = loadDistDom('index.html', { navigatorLang: 'en-US' });
  const bannerEn = domEn.window.document.getElementById('zhLocaleBanner');
  assert.ok(bannerEn && bannerEn.classList.contains('hidden'), 'Banner should stay hidden for en-US browser');
});

test('Chinese module detail copy button uses localized labels', async () => {
  const dom = loadDistDom('zh/modules/magisk/index.html', { url: 'https://magisk.yssn.tech/zh/modules/magisk/' });
  const doc = dom.window.document;
  const copyBtn = doc.querySelector('.copy-path-btn');
  assert.ok(copyBtn, 'copy-path-btn exists');
  const textSpan = copyBtn.querySelector('.copy-text');
  assert.equal(textSpan.textContent.trim(), '复制');
  copyBtn.click();
  await new Promise((resolve) => setTimeout(resolve, 0));
  assert.equal(textSpan.textContent.trim(), '已复制');
});

test('Home search handles punctuation differences, asset names, URLs, prompts, and cross-locale queries', () => {
  const dom = loadDistDom('index.html', { url: 'https://magisk.yssn.tech/' });
  const doc = dom.window.document;
  const searchInput = doc.getElementById('searchInput');
  const noResults = doc.getElementById('noResults');

  const queryVisible = (q) => {
    searchInput.value = q;
    searchInput.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
    return Array.from(doc.querySelectorAll('.module-card-wrapper'))
      .filter(el => el.style.display !== 'none')
      .map(el => el.getAttribute('data-id'));
  };

  assert.ok(queryVisible('zygisk assistant').includes('zygisk-assistant'), 'space vs hyphen query');
  assert.ok(queryVisible('harman-kardon').includes('harman-kardon-sound-enhancer'), 'hyphen vs space query');
  assert.ok(queryVisible('bindhosts.zip').includes('bindhosts'), 'assetName search');
  assert.ok(queryVisible('https://magisk.yssn.tech/modules/ohmykeymint/').includes('ohmykeymint'), 'pasted URL search');
  assert.ok(queryVisible('Please install playintegrityfix on KernelSU').includes('playintegrityfix'), 'pasted prompt extraction');
  assert.ok(queryVisible('旁路供电').includes('acc'), 'cross-locale Chinese query on EN home');

  const zero = queryVisible('zzzznonexistentmodule999');
  assert.equal(zero.length, 0, 'genuine miss returns zero results');
  assert.ok(noResults && !noResults.classList.contains('hidden'), 'noResults shown on zero results');
});

test('Localization analytics track zh-banner-shown and attach locale properties', () => {
  const html = fs.readFileSync(path.join(DIST_DIR, 'index.html'), 'utf-8');
  const trackedEvents = [];
  const dom = new JSDOM(html, {
    url: 'https://magisk.yssn.tech/',
    runScripts: 'dangerously',
    beforeParse(window) {
      Object.defineProperty(window.navigator, 'language', { value: 'zh-CN', configurable: true });
      Object.defineProperty(window.navigator, 'languages', { value: ['zh-CN', 'en-US'], configurable: true });
      window.umami = {
        track(name, props) {
          trackedEvents.push({ name, props });
        },
      };
    },
  });
  for (const s of dom.window.document.querySelectorAll('script[type="module"]')) {
    evalModuleScript(dom, s);
  }

  const doc = dom.window.document;
  assert.ok(trackedEvents.some(e => e.name === 'zh-banner-shown' && e.props?.browser_lang === 'zh-CN'));
  assert.equal(doc.getElementById('zhBannerSwitchLink')?.getAttribute('data-umami-event'), 'zh-banner-switch');
  assert.equal(doc.getElementById('zhBannerDismissBtn')?.getAttribute('data-umami-event'), 'zh-banner-dismiss');
  assert.equal(doc.querySelector('[data-umami-event="click-module-card"]')?.getAttribute('data-umami-event-locale'), 'en');

  doc.getElementById('compatSelect').value = 'KernelSU';
  doc.getElementById('compatSelect').dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  assert.ok(trackedEvents.some(e => e.name === 'filter-platform' && e.props?.locale === 'en'));

  const zhDetail = loadDistDom('zh/modules/magisk/index.html', { url: 'https://magisk.yssn.tech/zh/modules/magisk/' });
  assert.equal(zhDetail.window.document.querySelector('[data-umami-event="download-module"]')?.getAttribute('data-umami-event-locale'), 'zh');
  assert.equal(zhDetail.window.document.querySelector('[data-umami-event="navbar-language-switch"]')?.getAttribute('data-umami-event-from'), 'zh');

  // Visible mobile/desktop GitHub star pill & prefilled zero-results issue request CTA
  const headerPill = doc.querySelector('[data-umami-event="navbar-github-click"][data-umami-event-placement="header-pill"]');
  assert.ok(headerPill, 'header GitHub pill renders on homepage');
  assert.ok(!headerPill.classList.contains('hidden'), 'header GitHub pill is visible on mobile viewports too');
  assert.match(headerPill.querySelector('.nav-github-stars')?.textContent?.trim() || '', /^\d+(?:\.\d+)?k?$/);

  const searchInput = doc.getElementById('searchInput');
  searchInput.value = 'RareCustomModule';
  searchInput.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  const reqBtn = doc.getElementById('requestModuleBtn');
  assert.ok(reqBtn && reqBtn.href.includes('template=module-request.yml') && reqBtn.href.includes('RareCustomModule'));
});

test('Fuzzy typo search, URL state sync, category/platform filters, and archived/superseded UX work', () => {
  const dom = loadDistDom('index.html', { url: 'https://magisk.yssn.tech/' });
  const doc = dom.window.document;
  const searchInput = doc.getElementById('searchInput');
  const sortSelect = doc.getElementById('sortSelect');
  const compatSelect = doc.getElementById('compatSelect');
  const resetBtn = doc.getElementById('resetBtn');

  const visibleIds = () =>
    Array.from(doc.querySelectorAll('.module-card-wrapper'))
      .filter(el => el.style.display !== 'none')
      .map(el => el.getAttribute('data-id'));

  // Fuzzy Levenshtein typo tolerance (1-2 edits)
  searchInput.value = 'playintegriyfix';
  searchInput.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  assert.ok(visibleIds().includes('playintegrityfix'), '1-char missing typo matches playintegrityfix');

  searchInput.value = 'zygiskassitant';
  searchInput.dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  assert.ok(visibleIds().includes('zygisk-assistant'), 'typo matches zygisk-assistant');

  // URL state sync
  compatSelect.value = 'KernelSU';
  compatSelect.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  sortSelect.value = 'stars';
  sortSelect.dispatchEvent(new dom.window.Event('change', { bubbles: true }));
  assert.equal(dom.window.location.search, '?q=zygiskassitant&compat=KernelSU&sort=stars');

  resetBtn.click();
  assert.equal(dom.window.location.search, '');

  // Category & Compatibility interactive filters
  const catDom = loadDistDom('categories/root-management/index.html', {
    url: 'https://magisk.yssn.tech/categories/root-management/',
  });
  const catSearch = catDom.window.document.getElementById('searchInput');
  assert.ok(catSearch, 'category detail has search input');
  catSearch.value = 'alwaysstrong';
  catSearch.dispatchEvent(new catDom.window.Event('input', { bubbles: true }));
  const catVisible = Array.from(catDom.window.document.querySelectorAll('.module-card-wrapper'))
    .filter(el => el.style.display !== 'none')
    .map(el => el.getAttribute('data-id'));
  assert.ok(catVisible.includes('alwaysstrong'));

  const platDom = loadDistDom('compatibility/kernelsu/index.html', {
    url: 'https://magisk.yssn.tech/compatibility/kernelsu/',
  });
  assert.ok(platDom.window.document.getElementById('categorySelect'), 'platform detail has category filter');

  // Superseded ?from= notice banner & archived module page
  const supDom = loadDistDom('modules/disable-flag-secure/index.html', {
    url: 'https://magisk.yssn.tech/modules/disable-flag-secure/?from=simple-flag-secure',
  });
  const supBanner = supDom.window.document.getElementById('supersededNoticeBanner');
  assert.ok(supBanner && !supBanner.classList.contains('hidden'), 'superseded banner reveals when ?from= matches');
  assert.match(supDom.window.document.getElementById('supersededNoticeTitle')?.textContent || '', /Simple Flag Secure/);

  const archDom = loadDistDom('archived/perfgame/index.html', {
    url: 'https://magisk.yssn.tech/archived/perfgame/',
  });
  assert.match(archDom.window.document.body.textContent || '', /Recommended Active Alternatives/);
});

test('AppManager and Canta guides preserve <package> inline placeholders and 404 switchers work cleanly', () => {
  const appDom = loadDistDom('modules/app-manager/index.html', {
    url: 'https://magisk.yssn.tech/modules/app-manager/',
  });
  assert.match(
    appDom.window.document.body.textContent || '',
    /<package>/,
    'parseInlineMarkdown should HTML-escape <package> instead of stripping it as an HTML tag'
  );

  const notFoundZh = loadDistDom('zh/404/index.html', {
    url: 'https://magisk.yssn.tech/zh/404/',
  });
  const navSwitchToEn = notFoundZh.window.document.querySelector('[data-umami-event="navbar-language-switch"]');
  assert.equal(navSwitchToEn?.getAttribute('href'), '/404.html');

  // Prototype-key safety on ?from=toString must leave supersededNoticeBanner hidden
  const protoDom = loadDistDom('modules/disable-flag-secure/index.html', {
    url: 'https://magisk.yssn.tech/modules/disable-flag-secure/?from=toString',
  });
  const protoBanner = protoDom.window.document.getElementById('supersededNoticeBanner');
  assert.ok(protoBanner?.classList.contains('hidden'), '?from=toString must not trigger Object.prototype lookup');
});
