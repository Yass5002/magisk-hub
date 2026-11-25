"""Real headless Chromium E2E checks for Magisk Hub production dist/."""

import functools
import http.server
import os
import socketserver
import threading
import unittest

from playwright.sync_api import sync_playwright

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class TestChromiumE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(QuietHandler, directory=DIST_DIR)
        cls.httpd = ThreadedTCPServer(("127.0.0.1", 0), handler)
        cls.port = cls.httpd.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def _new_page(self, width, height):
        ctx = self.browser.new_context(viewport={"width": width, "height": height})
        page = ctx.new_page()
        # Abort third-party analytics requests so headless runs stay deterministic
        page.route("https://analytics.mehro.me/**", lambda route: route.abort())
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        return ctx, page, errors

    def test_mobile_header_pill_drawer_and_no_horizontal_overflow(self):
        ctx, page, errors = self._new_page(375, 812)
        try:
            for path in ["/", "/zh/", "/categories/root-management/", "/compatibility/kernelsu/", "/modules/alwaysstrong/"]:
                page.goto(f"{self.base_url}{path}", wait_until="domcontentloaded")
                overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
                self.assertFalse(overflow, f"Horizontal overflow detected on mobile {path}")

                pill = page.locator('[data-umami-event="navbar-github-click"][data-umami-event-placement="header-pill"]')
                self.assertTrue(pill.is_visible(), f"Header GitHub pill must be visible on mobile {path}")
                header_h = page.locator("header").bounding_box()["height"]
                self.assertLessEqual(header_h, 72, f"Mobile header wrapped unexpectedly on {path}: height={header_h}")

            # Open mobile hamburger menu and verify it toggles cleanly
            page.goto(f"{self.base_url}/", wait_until="domcontentloaded")
            menu = page.locator("#mobile-menu")
            self.assertFalse(menu.is_visible())
            page.locator("#mobile-menu-btn").click()
            self.assertTrue(menu.is_visible())
            page.locator("#mobile-menu-btn").click()
            self.assertFalse(menu.is_visible())
            self.assertEqual(errors, [])
        finally:
            ctx.close()

    def test_desktop_fuzzy_search_url_sync_category_filter_and_superseded_banner(self):
        ctx, page, errors = self._new_page(1280, 800)
        try:
            page.goto(f"{self.base_url}/", wait_until="networkidle")
            search = page.locator("#searchInput")
            search.fill("playintegriyfix")
            self.assertIn("?q=playintegriyfix", page.url)
            self.assertTrue(page.locator('.module-card-wrapper[data-id="playintegrityfix"]').is_visible())

            page.locator("#resetBtn").evaluate("el => { /* no-op if hidden */ }")
            page.locator("#searchClearBtn").click()
            self.assertNotIn("?q=", page.url)

            # Category filter page interactive search + compat filter
            page.goto(f"{self.base_url}/categories/root-management/", wait_until="networkidle")
            page.locator("#compatSelect").select_option("APatch")
            self.assertIn("compat=APatch", page.url)
            self.assertGreater(page.locator(".module-card-wrapper:visible").count(), 0)

            # Superseded ?from= banner
            page.goto(f"{self.base_url}/modules/disable-flag-secure/?from=simple-flag-secure", wait_until="domcontentloaded")
            banner = page.locator("#supersededNoticeBanner")
            self.assertTrue(banner.is_visible())
            self.assertIn("Simple Flag Secure", page.locator("#supersededNoticeTitle").inner_text())

            # Archived module page
            page.goto(f"{self.base_url}/archived/perfgame/", wait_until="domcontentloaded")
            self.assertGreater(page.locator("a[href*='/modules/']").count(), 0)
            self.assertEqual(errors, [])
        finally:
            ctx.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
