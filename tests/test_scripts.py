"""Unit tests for sync_releases.py, sync_trending.py, and generate_llms.py."""

import glob
import json
import os
import re
import sys
import tempfile
import unittest
from unittest import mock

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import sync_releases  # noqa: E402
import sync_trending  # noqa: E402


class TestSyncReleasesHelpers(unittest.TestCase):
    def test_preserves_clean_english_description_over_cjk_upstream(self):
        cand = {
            "name": "device_faker",
            "description": "High-performance Rust-based Zygisk module for granular per-application device model spoofing.",
        }
        upstream = {"description": "自定义配置Zygisk机型伪装"}
        self.assertEqual(sync_releases.choose_preserved_description(cand, upstream), cand["description"])

    def test_rejects_boilerplate_and_cjk_descriptions(self):
        self.assertFalse(sync_releases.is_clean_english_text("TrickyStore active root module."))
        self.assertFalse(sync_releases.is_clean_english_text("自定义配置Zygisk机型伪装"))
        self.assertTrue(sync_releases.is_clean_english_text("Customizes status bar and Quick Settings on Pixel devices."))

    def test_preserves_optional_fields_and_curated_seo(self):
        cand = {
            "id": "demo-mod",
            "name": "DemoMod",
            "repo": "owner/demo",
            "author": "CustomMaintainer",
            "sourceType": "github",
            "contentTier": 1,
            "seo": {
                "title": "DemoMod – Download (Magisk/KSU) | Magisk Hub",
                "description": "Download DemoMod for Magisk and KernelSU. Custom curated English description verified locally.",
            },
        }
        info = {
            "nameWithOwner": "owner/demo",
            "stargazerCount": 420,
        }
        entry = sync_releases.build_synced_module_entry(
            c=cand,
            info=info,
            slug="demo-mod",
            category="system-utilities",
            sw_type="flashable-module",
            compat=["Magisk", "KernelSU"],
            spdx="GPL-3.0",
            desc="Clean English module description.",
            icon_path="assets/icons/demo-mod.png",
            chosen_asset={"downloadUrl": "https://example.com/demo.zip", "name": "demo.zip"},
            latest_rel={"tagName": "v1.0.0", "publishedAt": "2026-10-01T00:00:00Z", "url": "https://example.com/rel"},
        )
        self.assertEqual(entry["author"], "CustomMaintainer")
        self.assertEqual(entry["sourceType"], "github")
        self.assertEqual(entry["contentTier"], 1)
        self.assertEqual(entry["seo"]["description"], cand["seo"]["description"])

    def test_mass_prune_circuit_breaker_triggers_on_api_outage(self):
        self.assertTrue(sync_releases.is_mass_prune_aborted(214, 0, 214, 0))
        self.assertTrue(sync_releases.is_mass_prune_aborted(200, 140, 60, 200))
        self.assertFalse(sync_releases.is_mass_prune_aborted(214, 210, 4, 214))

    def test_cat_map_audio_resolves_to_audio_dsp(self):
        self.assertEqual(sync_releases.CAT_MAP["audio"], "audio-dsp-acoustics")


class TestSyncTrending(unittest.TestCase):
    def test_skips_when_api_key_empty_and_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_path = os.path.join(tmp, "trending.json")
            seed = {"magisk": 42}
            with open(out_path, "w", encoding="utf-8") as fp:
                json.dump(seed, fp)

            with mock.patch.object(sync_trending, "UMAMI_API_KEY", ""), mock.patch.object(
                sync_trending, "OUTPUT_FILE", out_path
            ):
                sync_trending.main()

            with open(out_path, "r", encoding="utf-8") as fp:
                self.assertEqual(json.load(fp), seed)

    def test_empty_list_response_does_not_wipe_existing_trending_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_path = os.path.join(tmp, "trending.json")
            seed = {"playintegrityfix": 19}
            with open(out_path, "w", encoding="utf-8") as fp:
                json.dump(seed, fp)

            with mock.patch.object(sync_trending, "OUTPUT_FILE", out_path), mock.patch.object(
                sync_trending, "fetch_trending_downloads", return_value={}
            ):
                sync_trending.main()

            with open(out_path, "r", encoding="utf-8") as fp:
                self.assertEqual(json.load(fp), seed)


class TestLlmsDiscoveryIntegrity(unittest.TestCase):
    def test_llms_txt_module_urls_point_to_active_catalog_slugs(self):
        active_slugs = {
            os.path.basename(f)[:-5]
            for f in glob.glob(os.path.join(REPO_ROOT, "modules", "*.json"))
            if os.path.basename(f) != "schema.json"
        }
        for rel in ("public/llms.txt", "public/zh/llms.txt"):
            with open(os.path.join(REPO_ROOT, rel), "r", encoding="utf-8") as fp:
                text = fp.read()
            referenced = set(re.findall(r"https://magisk\.yssn\.tech/(?:zh/)?modules/([a-z0-9-]+)/", text))
            missing = sorted(referenced - active_slugs)
            self.assertEqual(missing, [], f"{rel} links to non-active modules: {missing}")


if __name__ == "__main__":
    unittest.main()
