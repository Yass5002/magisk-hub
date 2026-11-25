import assert from 'node:assert/strict';
import test from 'node:test';
import {
  getAbsoluteUrl,
  getAlternateUrls,
  getLocaleFromPath,
  localizePath,
  normalizeTrailingSlash,
  stripLocalePrefix,
} from '../src/i18n/routing.ts';
import {
  parseInlineMarkdown,
  renderEntityMarkdown,
  VERIFIED_MODULE_TARGETS,
} from '../src/lib/inlineMarkdown.ts';

test('normalizeTrailingSlash enforces trailing slash', () => {
  assert.equal(normalizeTrailingSlash('/'), '/');
  assert.equal(normalizeTrailingSlash('/zh'), '/zh/');
  assert.equal(normalizeTrailingSlash('/modules/magisk?q=test#top'), '/modules/magisk/');
});

test('getLocaleFromPath detects en and zh accurately', () => {
  assert.equal(getLocaleFromPath('/'), 'en');
  assert.equal(getLocaleFromPath('/modules/acc/'), 'en');
  assert.equal(getLocaleFromPath('/zh'), 'zh');
  assert.equal(getLocaleFromPath('/zh/'), 'zh');
  assert.equal(getLocaleFromPath('/zh/modules/acc/'), 'zh');
  assert.equal(getLocaleFromPath('/zh-something/'), 'en');
});

test('stripLocalePrefix strips /zh prefix cleanly', () => {
  assert.equal(stripLocalePrefix('/zh/'), '/');
  assert.equal(stripLocalePrefix('/zh/modules/shamiko/'), '/modules/shamiko/');
  assert.equal(stripLocalePrefix('/categories/root-management/'), '/categories/root-management/');
});

test('localizePath switches locales preserving trailing slashes and external URLs', () => {
  assert.equal(localizePath('/', 'zh'), '/zh/');
  assert.equal(localizePath('/zh/', 'en'), '/');
  assert.equal(localizePath('/modules/acc', 'zh'), '/zh/modules/acc/');
  assert.equal(localizePath('/zh/modules/acc/', 'en'), '/modules/acc/');
  assert.equal(localizePath('https://github.com/topjohnwu/Magisk', 'zh'), 'https://github.com/topjohnwu/Magisk');
});

test('getAlternateUrls returns symmetric en, zhHans, and xDefault URLs', () => {
  const fromEn = getAlternateUrls('/modules/shamiko/');
  const fromZh = getAlternateUrls('/zh/modules/shamiko/');
  assert.deepEqual(fromEn, fromZh);
  assert.deepEqual(fromEn, {
    en: 'https://magisk.yssn.tech/modules/shamiko/',
    zhHans: 'https://magisk.yssn.tech/zh/modules/shamiko/',
    xDefault: 'https://magisk.yssn.tech/modules/shamiko/',
  });
  assert.equal(getAbsoluteUrl('/', 'zh'), 'https://magisk.yssn.tech/zh/');
  assert.equal(localizePath('/zh/404/', 'en'), '/404.html');
  assert.equal(localizePath('/404.html', 'zh'), '/zh/404/');
});

test('parseInlineMarkdown escapes HTML tags/XSS while formatting inline code and bold spans', () => {
  const rendered = parseInlineMarkdown('Run `<script>alert(1)</script>` for **<package>** & safety');
  assert.doesNotMatch(rendered, /<script>/i);
  assert.match(rendered, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.match(rendered, /<strong[^>]*>&lt;package&gt;<\/strong>/);
  assert.match(rendered, /&amp; safety/);
});

test('renderEntityMarkdown never creates nested links inside <code> spans', () => {
  const html = renderEntityMarkdown('Pairs with Shamiko and `/data/adb/shamiko/whitelist` config', 'trickystore', 'en', false);
  const codeSegments = html.match(/<code\b[^>]*>.*?<\/code>/g) || [];
  assert.equal(codeSegments.length, 1);
  assert.doesNotMatch(codeSegments[0], /<a\b/i, 'must not link inside <code> elements');
  assert.match(html, /<a href="\/modules\/shamiko\/"[^>]*>Shamiko<\/a>/);
  assert.equal('mountify' in VERIFIED_MODULE_TARGETS, false);
  assert.equal('stevenblock' in VERIFIED_MODULE_TARGETS, false);
});
