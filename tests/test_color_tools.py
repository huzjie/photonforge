# -*- coding: utf-8 -*-
import unittest

from photonforge.tools import color, histogram, format as fmt


class TestColor(unittest.TestCase):
    def test_brightness(self):
        img = [[[0.5] * 4 for _ in range(4)] for _ in range(3)]
        out = color.adjust_brightness(img, 0.2)
        self.assertAlmostEqual(out[0][0][0], 0.7)

    def test_contrast_clamp(self):
        img = [[[0.5] * 4 for _ in range(4)] for _ in range(3)]
        out = color.adjust_contrast(img, 3.0)
        self.assertGreaterEqual(out[0][0][0], 0.0)
        self.assertLessEqual(out[0][0][0], 1.0)


class TestHistogram(unittest.TestCase):
    def test_hist(self):
        img = [[[0.5] * 4 for _ in range(4)] for _ in range(1)]
        h = histogram.histogram(img, 8)
        self.assertEqual(sum(h), 16)

    def test_equalize(self):
        img = [[[0.2] * 4 for _ in range(4)] for _ in range(1)]
        out = histogram.equalize(img, 8)
        self.assertEqual(len(out[0]), 4)


class TestFormat(unittest.TestCase):
    def test_to_rgb(self):
        img = [[[0.5] * 4 for _ in range(4)]]
        rgb = fmt.to_rgb(img)
        self.assertEqual(len(rgb), 3)


if __name__ == "__main__":
    unittest.main()
