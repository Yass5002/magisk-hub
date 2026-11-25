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
});
