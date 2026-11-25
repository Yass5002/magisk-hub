import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { JSDOM } from 'jsdom';

const DIST_DIR = path.resolve(process.cwd(), 'dist');

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
  const moduleScripts = Array.from(dom.window.document.querySelectorAll('script[type="module"]'));
  for (const s of moduleScripts) {
    if (!s.src && s.textContent) {
      dom.window.eval(s.textContent);
    } else if (s.src) {
      const urlPath = new URL(s.src, 'https://magisk.yssn.tech').pathname;
      if (urlPath.startsWith('/_astro/')) {
        const assetPath = path.join(DIST_DIR, urlPath.replace(/^\/+/, ''));
        dom.window.eval(fs.readFileSync(assetPath, 'utf-8'));
      }
    }
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

test('Chinese module detail copy button uses localized labels', () => {
  const dom = loadDistDom('zh/modules/magisk/index.html', { url: 'https://magisk.yssn.tech/zh/modules/magisk/' });
  const doc = dom.window.document;
  const copyBtn = doc.querySelector('.copy-path-btn');
  assert.ok(copyBtn, 'copy-path-btn exists');
  const textSpan = copyBtn.querySelector('.copy-text');
  assert.equal(textSpan.textContent.trim(), '复制');
  copyBtn.click();
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
    if (!s.src && s.textContent) {
      dom.window.eval(s.textContent);
    } else if (s.src) {
      const urlPath = new URL(s.src, 'https://magisk.yssn.tech').pathname;
      if (urlPath.startsWith('/_astro/')) {
        dom.window.eval(fs.readFileSync(path.join(DIST_DIR, urlPath.replace(/^\/+/, '')), 'utf-8'));
      }
    }
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
});
