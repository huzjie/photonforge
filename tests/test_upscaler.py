# -*- coding: utf-8 -*-
import unittest

from photonforge.upscaler import bilinear, lanczos


class TestUpscaler(unittest.TestCase):
    def test_bilinear(self):
        img = [[[0.5] * 4 for _ in range(4)] for _ in range(3)]
        up = bilinear.upscale(img, 2)
        self.assertEqual(len(up[0]), 8)

    def test_lanczos(self):
        img = [[[0.5] * 4 for _ in range(4)] for _ in range(3)]
        up = lanczos.upscale(img, 2)
        self.assertEqual(len(up[0]), 8)


if __name__ == "__main__":
    unittest.main()
