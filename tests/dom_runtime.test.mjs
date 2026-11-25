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

  // JSDOM ignores <script type="module">; evaluate inline module scripts explicitly
  const moduleScripts = Array.from(dom.window.document.querySelectorAll('script[type="module"]'));
  for (const s of moduleScripts) {
    if (!s.src && s.textContent) {
      dom.window.eval(s.textContent);
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
