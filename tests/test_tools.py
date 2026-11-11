# -*- coding: utf-8 -*-
import unittest

from photonforge.tools import image, prompt_templates, meta


class TestImageTools(unittest.TestCase):
    def test_resize(self):
        img = [[[0.5] * 8 for _ in range(8)] for _ in range(3)]
        out = image.resize_nearest(img, 4, 4)
        self.assertEqual(len(out[0]), 4)

    def test_flip(self):
        img = [[[0.0, 1.0]] for _ in range(3)]
        fh = image.flip_h(img)
        self.assertEqual(fh[0][0][0], 1.0)

    def test_grayscale(self):
        img = [[[0.5] * 4 for _ in range(4)] for _ in range(3)]
        g = image.grayscale(img)
        self.assertEqual(len(g), 1)


class TestTemplates(unittest.TestCase):
    def test_build(self):
        s = prompt_templates.build(style="photoreal", subject="一只猫")
        self.assertIn("一只猫", s)
        self.assertIn("写实", s)


class TestMeta(unittest.TestCase):
    def test_stats(self):
        img = [[[0.5] * 4 for _ in range(4)] for _ in range(3)]
        st = meta.stats(img)
        self.assertEqual(st["height"], 4)
        self.assertAlmostEqual(st["mean"], 0.5)


if __name__ == "__main__":
    unittest.main()
