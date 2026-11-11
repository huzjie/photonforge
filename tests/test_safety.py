# -*- coding: utf-8 -*-
import unittest

from photonforge.safety import filter as sf, watermark


class TestSafetyFilter(unittest.TestCase):
    def test_check_clean(self):
        ok, hits = sf.check_prompt("一只柴犬")
        self.assertTrue(ok)
        self.assertEqual(hits, [])

    def test_check_blocked(self):
        ok, hits = sf.check_prompt("暴力内容")
        self.assertFalse(ok)
        self.assertIn("暴力", hits)

    def test_sanitize(self):
        out = sf.sanitize("暴力内容")
        self.assertNotIn("暴力", out)


class TestWatermark(unittest.TestCase):
    def test_embed_verify(self):
        img = [[[0.5] * 16 for _ in range(16)] for _ in range(3)]
        wm = watermark.embed_bits(img, "huzjie-2026")
        ratio = watermark.verify(wm, "huzjie-2026")
        self.assertGreater(ratio, 0.99)

    def test_verify_wrong(self):
        img = [[[0.5] * 16 for _ in range(16)] for _ in range(3)]
        wm = watermark.embed_bits(img, "aaa")
        ratio = watermark.verify(wm, "bbb")
        self.assertLess(ratio, 0.7)


if __name__ == "__main__":
    unittest.main()
